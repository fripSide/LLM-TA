"""LLM client abstraction."""

import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI

from llm_ta.llm.prompts import DEFAULT_PROMPTS, PromptManager


class LLMClient:
    """Client for interacting with LLM APIs."""
    
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        prompts_file: Path | None = None,
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("LLM_MODEL", "gpt-4")
        
        if not self.api_key:
            raise ValueError(
                "LLM API key is required. "
                "Set LLM_API_KEY in .env file or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.prompt_manager = PromptManager(prompts_file) if prompts_file else None
    
    def _get_prompts(self, stage: str) -> tuple[str, str]:
        """Get system and user prompts for a stage."""
        if self.prompt_manager:
            return (
                self.prompt_manager.get_system_prompt(stage),
                self.prompt_manager.get_user_prompt(stage),
            )
        return DEFAULT_PROMPTS[stage]["system"], DEFAULT_PROMPTS[stage]["user"]
    
    def _extract_list(self, result: dict | list, key: str) -> list[dict]:
        """Extract list from result, handling both wrapped and direct responses."""
        if isinstance(result, list):
            return result
        return result.get(key, result.get("data", []))
    
    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        """Send a chat completion request and return the response text."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    
    def _repair_json(self, text: str) -> str:
        """Attempt to repair common JSON issues from LLM responses."""
        import re
        
        # Remove trailing commas before closing brackets
        text = re.sub(r',(\s*[\]}])', r'\1', text)
        
        # Add missing commas between objects in arrays: }{ → },{
        text = re.sub(r'\}(\s*)\{', r'},\1{', text)
        
        # Add missing commas after strings before new keys: "..." "key" → "...", "key"
        text = re.sub(r'(")\s*\n(\s*")', r'\1,\n\2', text)
        
        # Fix unescaped quotes in strings (basic heuristic)
        # This handles: "text with "quote" inside" -> "text with \"quote\" inside"
        # Only do this if the line looks like it has an issue
        lines = text.split('\n')
        fixed_lines = []
        for line in lines:
            # Count unescaped quotes
            quote_count = len(re.findall(r'(?<!\\)"', line))
            if quote_count > 2 and ':' in line:
                # Likely a string value with embedded quotes
                # Try to fix by escaping internal quotes
                match = re.match(r'^(\s*"[^"]+"\s*:\s*)"(.*)"\s*(,?)$', line)
                if match:
                    prefix, value, suffix = match.groups()
                    # Escape internal quotes
                    value = value.replace('"', '\\"')
                    line = f'{prefix}"{value}"{suffix}'
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def chat_json(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 8192,
        retries: int = 3,
    ) -> dict[str, Any] | list:
        """Send a chat request and parse the response as JSON with retries."""
        if messages and messages[-1]["role"] == "user":
            # Ensure JSON instruction is present
            if "JSON" not in messages[-1]["content"]:
                messages[-1]["content"] += "\n\nPlease respond in JSON format only, no other text."
        
        last_error = None
        
        for attempt in range(retries):
            try:
                response = self.chat(messages, temperature=temperature, max_tokens=max_tokens)
                
                # Extract JSON from response text
                text = response.strip()
                
                # Find the first { or [ and the last } or ]
                start_json = -1
                end_json = -1
                
                # Basic bracket matching to find the outermost object/array
                for i, char in enumerate(text):
                    if char in '{[':
                        start_json = i
                        break
                
                for i, char in enumerate(reversed(text)):
                    if char in '}]':
                        end_json = len(text) - i
                        break
                
                if start_json != -1 and end_json != -1:
                    text = text[start_json:end_json]
                
                # Remove markdown formatting if still present
                text = text.replace("```json", "").replace("```", "").strip()
                
                # Try parsing as-is first
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    # Try repairing the JSON
                    repaired = self._repair_json(text)
                    return json.loads(repaired)
                    
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON Parse Error (Attempt {attempt + 1}/{retries}): {e}")
                last_error = e
                # Retry with slightly higher temperature to get different output
                temperature = min(0.7, temperature + 0.1)
        
        # If all retries fail
        print(f"Failed to parse JSON after {retries} attempts.")
        raise last_error
    
    def generate_codes(
        self,
        interview_text: str,
        research_questions: list[str],
        participant_id: str,
    ) -> list[dict]:
        """Generate initial codes from interview text."""
        system_prompt, user_template = self._get_prompts("coding")
        
        user_prompt = user_template.format(
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            interview_text=interview_text,
            participant_id=participant_id,
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self._extract_list(self.chat_json(messages), "codes")
    
    def generate_codes_for_question(
        self,
        question: str,
        answers: list[dict],  # [{participant_id, answer}, ...]
        research_questions: list[str],
    ) -> list[dict]:
        """Generate codes from all participants' answers to a single question.
        
        This reduces context length by processing one question at a time
        instead of all questions for one participant.
        """
        system_prompt, user_template = self._get_prompts("coding_by_question")
        
        # Filter out empty answers
        valid_answers = [a for a in answers if a.get('answer', '').strip()]
        participant_count = len(valid_answers)
        expected_codes = participant_count * 4  # Target 3-5, use 4 as midpoint
        
        # Format answers as a list
        answers_text = "\n\n".join(
            f"**{a['participant_id']}**: {a['answer']}"
            for a in valid_answers
        )
        
        user_prompt = user_template.format(
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            question=question,
            answers=answers_text,
            participant_count=participant_count,
            expected_codes=expected_codes,
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self._extract_list(self.chat_json(messages), "codes")
    
    def generate_themes(
        self,
        codes: list[dict],
        research_questions: list[str],
    ) -> list[dict]:
        """Generate themes from selected codes."""
        system_prompt, user_template = self._get_prompts("theming")
        
        user_prompt = user_template.format(
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            codes=json.dumps(codes, ensure_ascii=False, indent=2),
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self._extract_list(self.chat_json(messages), "themes")
    
    def merge_codes(
        self,
        codes: list[dict],
        research_questions: list[str],
    ) -> list[dict]:
        """Merge codes from multiple questions, removing duplicates and combining similar codes."""
        system_prompt, user_template = self._get_prompts("merge_codes")
        
        user_prompt = user_template.format(
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            codes_json=json.dumps(codes, ensure_ascii=False, indent=2),
            total_codes=len(codes),
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self._extract_list(self.chat_json(messages, max_tokens=16384), "codes")
    
    def generate_sub_themes(
        self,
        codes: list[dict],
        target_rq: str,
        rq_id: str,
        research_questions: list[str],
    ) -> list[dict]:
        """Generate sub-themes for a specific research question."""
        system_prompt, user_template = self._get_prompts("sub_theming")
        
        user_prompt = user_template.format(
            target_rq=target_rq,
            rq_id=rq_id,
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            codes=json.dumps(codes, ensure_ascii=False, indent=2),
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self._extract_list(self.chat_json(messages), "sub_themes")
    
    def generate_major_themes(
        self,
        sub_themes_by_rq: dict[str, list[dict]],
        research_questions: list[str],
    ) -> list[dict]:
        """Synthesize sub-themes into major themes."""
        system_prompt, user_template = self._get_prompts("major_theming")
        
        user_prompt = user_template.format(
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            sub_themes_by_rq=json.dumps(sub_themes_by_rq, ensure_ascii=False, indent=2),
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self._extract_list(self.chat_json(messages), "themes")
    
    def generate_insights(
        self,
        themes: list[dict],
        research_questions: list[str],
    ) -> dict:
        """Generate high-level insights for discussion section."""
        system_prompt, user_template = self._get_prompts("insight")
        
        user_prompt = user_template.format(
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            themes=json.dumps(themes, ensure_ascii=False, indent=2),
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        return self.chat_json(messages)
    
    def generate_discussion(
        self,
        themes: list[dict],
        insights: dict,
        research_questions: list[str],
        background: str = "",
        raw_data_context: str = "",
    ) -> dict:
        """Generate Discussion section draft for academic paper."""
        system_prompt, user_template = self._get_prompts("discussion")
        
        user_prompt = user_template.format(
            background=background or "No background provided.",
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            themes=json.dumps(themes, ensure_ascii=False, indent=2),
            insights=json.dumps(insights, ensure_ascii=False, indent=2),
            raw_data_context=raw_data_context,
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        result = self.chat_json(messages)
        if isinstance(result, list):
            return {"sections": result, "rq_answers": []}
        return result

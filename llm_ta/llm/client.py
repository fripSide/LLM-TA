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
                
                return json.loads(text)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON Parse Error (Attempt {attempt + 1}/{retries}): {e}")
                last_error = e
                # Optionally increase temperature or add instruction about valid JSON?
                # For now just retry
        
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
    ) -> dict:
        """Generate Discussion section draft for academic paper."""
        system_prompt, user_template = self._get_prompts("discussion")
        
        user_prompt = user_template.format(
            background=background or "No background provided.",
            research_questions="\n".join(f"- {rq}" for rq in research_questions),
            themes=json.dumps(themes, ensure_ascii=False, indent=2),
            insights=json.dumps(insights, ensure_ascii=False, indent=2),
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        result = self.chat_json(messages)
        if isinstance(result, list):
            return {"sections": result, "rq_answers": []}
        return result

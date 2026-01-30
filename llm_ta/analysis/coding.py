"""Core logic for the Coding stage of thematic analysis."""

from pathlib import Path
from typing import Any

from llm_ta.llm.client import LLMClient
from llm_ta.models.coding import Code, Codebook, ConsolidatedCode, CodeOccurence
from llm_ta.models.interview import Interview


class CodingEngine:
    """Engine for extracting and consolidating codes."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def extract_codes_for_interview(
        self, 
        interview: Interview, 
        research_questions: list[str]
    ) -> list[Code]:
        """Extract initial codes from a single interview."""
        raw_codes = self.llm.generate_codes(
            interview_text=interview.get_full_text(),
            research_questions=research_questions,
            participant_id=interview.participant_id,
        )
        
        codes = []
        for raw in raw_codes:
            code = Code(
                id=raw.get("id", ""),  # ID will be reassigned by the caller for global index
                text=raw.get("text", ""),
                source_quote=raw.get("source_quote", ""),
                participant_id=raw.get("participant_id", interview.participant_id),
                selected=False,
            )
            codes.append(code)
        return codes

    def consolidate(
        self,
        codes: list[Code],
        research_questions: list[str]
    ) -> list[ConsolidatedCode]:
        """Consolidate a list of codes into canonical concepts using LLM."""
        # Convert codes to a simple JSON format for the prompt
        codes_data = [
            {
                "id": c.id,
                "text": c.text,
                "source_quote": c.source_quote,
                "participant_id": c.participant_id
            }
            for c in codes
        ]
        
        # In a real-world scenario with >100 codes, we would batch this or use embeddings.
        # For now, we pass all to the consolidate prompt.
        import json
        results = self.llm.chat_json([
            {"role": "system", "content": self.llm._get_prompts("consolidate")[0]},
            {"role": "user", "content": self.llm._get_prompts("consolidate")[1].format(
                codes_json=json.dumps(codes_data, ensure_ascii=False, indent=2)
            )}
        ])
        
        # Handle both dict with 'consolidated_codes' key and direct list response
        if isinstance(results, list):
            consolidated_results = results
        else:
            consolidated_results = results.get("consolidated_codes", [])
        
        # Map original codes to their new consolidated homes
        consolidated_codes = []
        raw_lookup = {c.id: c for c in codes}
        
        for res in consolidated_results:
            occurences = []
            # Handle various field name formats from LLM
            original_ids = (
                res.get("original_code_ids") or 
                res.get("merged_code_ids") or 
                res.get("source_ids") or 
                res.get("merged_from") or 
                []
            )
            for orig_id in original_ids:
                if orig_id in raw_lookup:
                    orig = raw_lookup[orig_id]
                    occurences.append(CodeOccurence(
                        participant_id=orig.participant_id,
                        source_quote=orig.source_quote,
                        original_code_id=orig.id
                    ))
            
            # Extract fields with fallbacks for different LLM response formats
            code_id = res.get("id") or res.get("code_id") or res.get("new_id") or f"CC_{len(consolidated_codes)+1:03d}"
            code_name = res.get("name") or res.get("merged_name") or res.get("code_name") or res.get("label") or ""
            code_desc = res.get("description") or res.get("definition") or res.get("desc") or ""
            
            # If name is empty but description exists, generate name from first few words
            if not code_name and code_desc:
                words = code_desc.split()[:5]
                code_name = " ".join(words).rstrip(",.:;")
                if len(words) >= 5:
                    code_name += "..."
            
            c_code = ConsolidatedCode(
                id=code_id,
                name=code_name,
                description=code_desc,
                occurrences=occurences,
                selected=True  # Default to selected for themes
            )
            consolidated_codes.append(c_code)
            
        return consolidated_codes

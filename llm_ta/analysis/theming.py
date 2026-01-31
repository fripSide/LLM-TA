"""Core logic for the Theming stage of thematic analysis."""

import json
from pathlib import Path
from typing import Any

from llm_ta.llm.client import LLMClient
from llm_ta.models.coding import Codebook, ConsolidatedCode, Code
from llm_ta.models.theme import Theme
from llm_ta.utils.io import load_json


class ThemingEngine:
    """Engine for generating themes from codes."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self._interview_lookup: dict[str, list[dict]] = {}
    
    def load_interviews(self, interviews_path: Path) -> int:
        """Load interview data for fetching complete source quotes.
        
        Returns the number of participants loaded.
        """
        if not interviews_path.exists():
            return 0
        
        interviews_data = load_json(interviews_path)
        for interview in interviews_data:
            p_id = interview.get("participant_id", "")
            if p_id:
                self._interview_lookup[p_id] = [
                    {"question": r.get("question", ""), "answer": r.get("answer", "")}
                    for r in interview.get("responses", [])
                ]
        return len(self._interview_lookup)
    
    def prepare_codes_for_llm(
        self,
        codes: list[ConsolidatedCode] | list[Code] | list[Any],
        include_quotes: bool = True,
        max_participants: int = 3,
        max_answer_length: int = 500,
    ) -> list[dict]:
        """Convert codes to dict format for LLM, optionally including source quotes.
        
        If interviews have been loaded, fetches complete quotes from interview data.
        Otherwise falls back to source_quote in code objects.
        """
        codes_data = []
        
        for c in codes:
            # Handle both Code (text) and ConsolidatedCode (name) safely
            # Convert to dict first to avoid Pydantic strict attribute access errors
            if hasattr(c, "model_dump"):
                c_dict = c.model_dump()
            elif hasattr(c, "dict"): # Pydantic v1
                c_dict = c.dict()
            elif isinstance(c, dict):
                c_dict = c
            else:
                c_dict = c.__dict__
                
            name = c_dict.get("name") or c_dict.get("text", "")
            description = c_dict.get("description", "")
            
            code_dict = {
                "id": c.id,
                "name": name,
                "description": description,
            }
            
            if include_quotes:
                source_quotes = self._get_source_quotes(
                    c, max_participants, max_answer_length
                )
                code_dict["source_quotes"] = source_quotes
            
            codes_data.append(code_dict)
        
        return codes_data
    
    def _get_source_quotes(
        self,
        code: Any,
        max_participants: int = 3,
        max_answer_length: int = 500,
    ) -> list[str]:
        """Get source quotes for a code, preferring complete interview answers."""
        # Get participant IDs associated with this code
        participant_ids = []
        if hasattr(code, 'occurrences') and code.occurrences:
            participant_ids = [occ.participant_id for occ in code.occurrences]
        elif hasattr(code, 'participant_id') and code.participant_id:
            # Handle comma-separated participant IDs like "P01, P02"
            participant_ids = [p.strip() for p in code.participant_id.split(",")]
        
        # Fetch complete responses from interviews if available
        source_quotes = []
        if self._interview_lookup:
            for p_id in participant_ids[:max_participants]:
                if p_id in self._interview_lookup:
                    responses = self._interview_lookup[p_id]
                    # Get first meaningful answer
                    for resp in responses[:2]:
                        answer = resp.get("answer", "")
                        if answer and len(answer) > 50:
                            truncated = answer[:max_answer_length] + "..." if len(answer) > max_answer_length else answer
                            source_quotes.append(f"({p_id}): {truncated}")
                            break
        
        # Fall back to code's original source_quote if no interview data
        if not source_quotes:
            if hasattr(code, 'occurrences') and code.occurrences:
                source_quotes = [
                    f"({occ.participant_id}): {occ.source_quote}" 
                    for occ in code.occurrences[:max_participants]
                ]
            elif hasattr(code, 'source_quote') and code.source_quote:
                source_quotes = [code.source_quote]
        
        return source_quotes

    def generate_themes(
        self,
        codes: list[ConsolidatedCode] | list[Any],
        research_questions: list[str],
        strategy: str = "global",  # global, per-rq, hierarchical
        deep_mode: bool = False
    ) -> list[Theme]:
        """Generate themes using the specified strategy."""
        
        # Prepare codes for LLM
        codes_data = []
        for c in codes:
            # Robust access via dict conversion
            if hasattr(c, "model_dump"):
                c_dict = c.model_dump()
            elif hasattr(c, "dict"):
                c_dict = c.dict()
            elif isinstance(c, dict):
                c_dict = c
            else:
                c_dict = c.__dict__

            name = c_dict.get("name") or c_dict.get("text", "")
                
            codes_data.append({
                "id": c.id,
                "text": name,
                "description": getattr(c, "description", ""),
                "quotes_count": len(getattr(c, "occurrences", [1]))
            })

        if strategy == "hierarchical" or deep_mode:
            return self._generate_themes_hierarchical(codes_data, research_questions)
        elif strategy == "per-rq":
            return self._generate_themes_per_rq(codes_data, research_questions)
        else:
            # Default to global single-pass
            return self._generate_themes_single_pass(codes_data, research_questions)

    def _generate_themes_per_rq(
        self,
        codes_data: list[dict],
        research_questions: list[str]
    ) -> list[Theme]:
        """Generate independent themes for each research question."""
        all_themes = []
        
        for i, rq in enumerate(research_questions):
            # In a real scenario, we might want to filter codes relevant to this RQ?
            # For now, we pass all codes but ask the LLM to focus on the specific RQ.
            
            # Use the sub_theming prompt but allow it to generate 'Major' themes for this RQ
            # Or use standard theming prompt with modified instruction
            
            # Let's use standard theming but restrict the context
            rq_themes_raw = self.llm.generate_themes(
                codes=codes_data,
                research_questions=[rq],  # Only pass the current RQ
            )
            
            for raw in rq_themes_raw:
                # Append RQ prefix to IDs to avoid collision if needed, 
                # or just let them accumulate. 
                # Better to ensure unique IDs if LLM restarts from T01
                t_id = raw.get("id", "")
                if not t_id.startswith(f"RQ{i+1}"):
                    t_id = f"RQ{i+1}_{t_id}"
                
                all_themes.append(Theme(
                    id=t_id,
                    name=raw.get("name", ""),
                    description=raw.get("description", ""),
                    code_ids=raw.get("code_ids", []),
                ))
        
        return all_themes

    def _generate_themes_single_pass(
        self, 
        codes_data: list[dict], 
        research_questions: list[str]
    ) -> list[Theme]:
        """Legacy single-pass thematic clustering."""
        raw_themes = self.llm.generate_themes(
            codes=codes_data,
            research_questions=research_questions,
        )
        
        themes = []
        for raw in raw_themes:
            themes.append(Theme(
                id=raw.get("id", ""),
                name=raw.get("name", ""),
                description=raw.get("description", ""),
                code_ids=raw.get("code_ids", []),
            ))
        return themes

    def generate_hierarchical_themes(
        self,
        codes_data: list[dict],
        research_questions: list[str],
        progress_callback: Any = None,
        output_dir: Path | None = None
    ) -> tuple[list[Theme], list[dict]]:
        """Multi-stage hierarchical theme synthesis.
        
        Returns:
            tuple: (List of Major Themes with nested sub-themes, List of all raw sub-theme dicts)
        """
        from llm_ta.models.theme import SubTheme
        from llm_ta.utils.io import save_json
        
        sub_themes_by_rq = {}
        all_sub_themes = []
        
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Stage 1: Generate sub-themes per RQ
        for rq_idx, rq in enumerate(research_questions, 1):
            rq_id = f"RQ{rq_idx}"
            
            cache_file = output_dir / f"themes_sub_{rq_id.lower()}.json" if output_dir else None
            
            # Resume capability: Check if we already have results for this RQ
            if cache_file and cache_file.exists():
                try:
                    if progress_callback:
                        progress_callback(f"找到缓存: {rq_id} (跳过生成)")
                    sub_themes_raw = load_json(cache_file)
                    sub_themes_by_rq[rq_id] = sub_themes_raw
                    all_sub_themes.extend(sub_themes_raw)
                    continue
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"读取缓存失败: {e}，重新生成...")
                        
            if progress_callback:
                progress_callback(f"生成 {rq_id} 的子主题...")
                
            sub_themes_raw = self.llm.generate_sub_themes(
                codes=codes_data,
                target_rq=rq,
                rq_id=rq_id,
                research_questions=research_questions,
            )
            
            sub_themes_by_rq[rq_id] = sub_themes_raw
            all_sub_themes.extend(sub_themes_raw)
            
            # Save incremental cache if output directory is provided
            if cache_file:
                try:
                    save_json(sub_themes_raw, cache_file)
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"警告: 无法保存 {rq_id} 缓存: {e}")
        
        # Stage 2: Synthesize major themes
        if progress_callback:
            progress_callback("合成大主题...")
            
        major_themes_raw = self.llm.generate_major_themes(
            sub_themes_by_rq=sub_themes_by_rq,
            research_questions=research_questions,
        )
        
        # Convert to Theme objects with SubTheme hierarchy
        themes = []
        sub_theme_lookup = {st.get("id", ""): st for st in all_sub_themes}
        
        for mt in major_themes_raw:
            sub_theme_ids = mt.get("sub_theme_ids", [])
            sub_theme_objs = []
            
            for st_id in sub_theme_ids:
                st_data = sub_theme_lookup.get(st_id, {})
                if st_data:
                    sub_theme_objs.append(SubTheme(
                        id=st_id,
                        name=st_data.get("name", ""),
                        description=st_data.get("description", ""),
                        code_ids=st_data.get("code_ids", []),
                        rq_id=st_id.split(".")[0] if "." in st_id else "",
                    ))
            
            themes.append(Theme(
                id=mt.get("id", f"T{len(themes)+1:02d}"),
                name=mt.get("name", ""),
                description=mt.get("description", ""),
                sub_themes=sub_theme_objs,
            ))
            
        return themes, all_sub_themes

    def _generate_themes_hierarchical(
        self, 
        codes_data: list[dict], 
        research_questions: list[str]
    ) -> list[Theme]:
        """Legacy internal wrapper for hierarchical generation."""
        themes, _ = self.generate_hierarchical_themes(codes_data, research_questions)
        return themes

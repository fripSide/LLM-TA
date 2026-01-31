"""Core logic for the Reporting stage of thematic analysis."""

from llm_ta.llm.client import LLMClient


class ReportingEngine:
    """Engine for generating insights and discussion."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_insights_and_discussion(
        self,
        themes: list[dict],
        research_questions: list[str],
        project_background: str = "",
        interviews_data: list[dict] | None = None
    ) -> tuple[dict, dict]:
        """Generate both insights and discussion text."""
        
        # 1. Generate high-level insights
        insights = self.llm.generate_insights(
            themes=themes,
            research_questions=research_questions,
        )
        
        # Prepare raw data context if available
        raw_data_context = ""
        if interviews_data:
            raw_data_context = self._prepare_raw_data_context(interviews_data)
        
        # 2. Generate discussion section
        discussion = self.llm.generate_discussion(
            themes=themes,
            insights=insights,
            research_questions=research_questions,
            background=project_background,
            raw_data_context=raw_data_context,
        )
        
        return insights, discussion

    def _prepare_raw_data_context(self, interviews: list[dict], max_participants: int = 8) -> str:
        """Format a sample of raw interview data for context."""
        context_parts = []
        count = 0
        for interview in interviews:
            if count >= max_participants:
                break
            
            p_id = interview.get("participant_id", "Unknown")
            responses = interview.get("responses", [])
            
            p_text = f"Participant {p_id}:\n"
            has_content = False
            for resp in responses:
                q = resp.get("question", "")
                a = resp.get("answer", "")
                if len(a) > 20: # Filter very short answers
                    p_text += f"  Q: {q}\n  A: {a}\n"
                    has_content = True
            
            if has_content:
                context_parts.append(p_text)
                count += 1
                
        return "\n---\n".join(context_parts)

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
        project_background: str = ""
    ) -> tuple[dict, dict]:
        """Generate both insights and discussion text."""
        
        # 1. Generate high-level insights
        insights = self.llm.generate_insights(
            themes=themes,
            research_questions=research_questions,
        )
        
        # 2. Generate discussion section
        discussion = self.llm.generate_discussion(
            themes=themes,
            insights=insights,
            research_questions=research_questions,
            background=project_background,
        )
        
        return insights, discussion

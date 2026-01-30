"""Interview data models."""

from pydantic import BaseModel, Field


class InterviewResponse(BaseModel):
    """A single question-answer pair from an interview."""
    
    question: str = Field(..., description="访谈问题")
    answer: str = Field(..., description="参与者回答")


class Interview(BaseModel):
    """Interview data from a single participant."""
    
    participant_id: str = Field(..., description="参与者ID，如 P01")
    responses: list[InterviewResponse] = Field(default_factory=list, description="问答列表")
    
    def get_full_text(self) -> str:
        """Get concatenated text of all responses for analysis."""
        parts = []
        for resp in self.responses:
            parts.append(f"Q: {resp.question}\nA: {resp.answer}")
        return "\n\n".join(parts)


class InterviewCollection(BaseModel):
    """Collection of all interviews in a study."""
    
    interviews: list[Interview] = Field(default_factory=list)
    
    def get_all_responses(self) -> list[tuple[str, InterviewResponse]]:
        """Get all responses with participant IDs."""
        results = []
        for interview in self.interviews:
            for resp in interview.responses:
                results.append((interview.participant_id, resp))
        return results

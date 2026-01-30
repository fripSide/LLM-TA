"""Coding models for initial code extraction."""

from pydantic import BaseModel, Field


class Code(BaseModel):
    """A single code extracted from interview data."""
    
    id: str = Field(..., description="编码ID，如 C001")
    text: str = Field(..., description="编码文本/标签")
    source_quote: str = Field(..., description="原文引用")
    participant_id: str = Field(..., description="来源参与者ID")
    selected: bool = Field(default=False, description="是否被用户选中")
    
    def to_markdown_line(self) -> str:
        """Convert to markdown checkbox line."""
        checkbox = "[x]" if self.selected else "[ ]"
        return (
            f"- {checkbox} **{self.id}**: {self.text}\n"
            f"  - 原文: \"{self.source_quote}\"\n"
            f"  <!-- ID: {self.id} | P: {self.participant_id} -->"
        )


class CodeOccurence(BaseModel):
    """A specific instance of a code usage."""
    participant_id: str
    source_quote: str
    original_code_id: str | None = None


class ConsolidatedCode(BaseModel):
    """A merged/canonical code representing a unified concept."""
    id: str
    name: str
    description: str = ""
    occurrences: list[CodeOccurence] = Field(default_factory=list)
    selected: bool = False

    def to_markdown_block(self) -> str:
        """Convert to markdown block for review."""
        checkbox = "[x]" if self.selected else "[ ]"
        lines = [
            f"### {checkbox} {self.id}: {self.name}",
            f"**Definition**: {self.description}",
            "- **Evidence**:"
        ]
        for occ in self.occurrences:
            lines.append(f"  - ({occ.participant_id}): \"{occ.source_quote}\"")
        lines.append(f"<!-- END: {self.id} -->\n")
        return "\n".join(lines)


class Codebook(BaseModel):
    """Collection of all codes in a study."""
    
    codes: list[Code] = Field(default_factory=list)
    consolidated_codes: list[ConsolidatedCode] = Field(default_factory=list)
    
    def get_selected_codes(self) -> list[Code]:
        """Get only the codes that were selected by the user."""
        return [c for c in self.codes if c.selected]
    
    def get_selected_consolidated_codes(self) -> list[ConsolidatedCode]:
        return [c for c in self.consolidated_codes if c.selected]
    
    def get_code_by_id(self, code_id: str) -> Code | None:
        """Find a code by its ID."""
        for code in self.codes:
            if code.id == code_id:
                return code
        return None

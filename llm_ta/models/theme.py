"""Theme models for thematic analysis."""

from pydantic import BaseModel, Field


class Theme(BaseModel):
    """A theme grouping related codes."""
    
    id: str = Field(..., description="主题ID，如 T01")
    name: str = Field(..., description="主题名称")
    description: str = Field(default="", description="主题描述")
    code_ids: list[str] = Field(default_factory=list, description="包含的编码ID列表")
    
    def to_markdown_section(self, codes_text: dict[str, str] | None = None) -> str:
        """Convert to markdown section."""
        lines = [
            f"### {self.name}",
            f"<!-- THEME_ID: {self.id} -->",
            "",
        ]
        if self.description:
            lines.append(self.description)
            lines.append("")
        
        for code_id in self.code_ids:
            code_text = codes_text.get(code_id, code_id) if codes_text else code_id
            lines.append(f"- {code_text}")
            lines.append(f"  <!-- CODE_ID: {code_id} -->")
        
        return "\n".join(lines)


class ThemeCollection(BaseModel):
    """Collection of all themes in a study."""
    
    themes: list[Theme] = Field(default_factory=list)
    
    def get_theme_by_id(self, theme_id: str) -> Theme | None:
        """Find a theme by its ID."""
        for theme in self.themes:
            if theme.id == theme_id:
                return theme
        return None
    
    def get_all_code_ids(self) -> set[str]:
        """Get all code IDs across all themes."""
        ids = set()
        for theme in self.themes:
            ids.update(theme.code_ids)
        return ids

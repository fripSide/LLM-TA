"""Theme models for thematic analysis."""

from pydantic import BaseModel, Field


class SubTheme(BaseModel):
    """A sub-theme within a major theme."""
    
    id: str = Field(..., description="子主题ID，如 T01.1")
    name: str = Field(..., description="子主题名称")
    description: str = Field(default="", description="子主题描述")
    code_ids: list[str] = Field(default_factory=list, description="包含的编码ID列表")
    rq_id: str = Field(default="", description="关联的研究问题ID，如 RQ1")
    
    def to_markdown_section(self, codes_text: dict[str, str] | None = None) -> str:
        """Convert to markdown section."""
        lines = [
            f"#### {self.name}",
            f"<!-- SUBTHEME_ID: {self.id} -->",
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


class Theme(BaseModel):
    """A major theme grouping related codes or sub-themes."""
    
    id: str = Field(..., description="主题ID，如 T01")
    name: str = Field(..., description="主题名称")
    description: str = Field(default="", description="主题描述")
    code_ids: list[str] = Field(default_factory=list, description="包含的编码ID列表（扁平结构）")
    sub_themes: list[SubTheme] = Field(default_factory=list, description="子主题列表（层级结构）")
    
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
        
        # Hierarchical: render sub-themes
        if self.sub_themes:
            for sub_theme in self.sub_themes:
                lines.append(sub_theme.to_markdown_section(codes_text))
                lines.append("")
        else:
            # Flat: render code_ids directly
            for code_id in self.code_ids:
                code_text = codes_text.get(code_id, code_id) if codes_text else code_id
                lines.append(f"- {code_text}")
                lines.append(f"  <!-- CODE_ID: {code_id} -->")
        
        return "\n".join(lines)
    
    def get_all_code_ids(self) -> list[str]:
        """Get all code IDs from this theme (flat or via sub-themes)."""
        if self.sub_themes:
            ids = []
            for sub in self.sub_themes:
                ids.extend(sub.code_ids)
            return ids
        return self.code_ids


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
        """Get all code IDs across all themes (flat or hierarchical)."""
        ids = set()
        for theme in self.themes:
            ids.update(theme.get_all_code_ids())
        return ids

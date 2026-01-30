"""Project configuration model."""

from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field


class Project(BaseModel):
    """Project configuration for a thematic analysis study."""
    
    name: str = Field(..., description="项目名称")
    research_questions: list[str] = Field(default_factory=list, description="研究问题列表")
    interview_questions: list[str] = Field(default_factory=list, description="访谈问题列表")
    background: str = Field(default="", description="研究背景描述")
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Language settings
    output_language: str = Field(default="en", description="输出语言: en/zh")
    
    # Directory structure
    data_dir: str = Field(default="data", description="JSON数据目录")
    
    # JSON data files (in data_dir)
    interviews_file: str = Field(default="interviews.json", description="访谈数据文件")
    codebook_file: str = Field(default="codebook.json", description="编码本文件")
    themes_file: str = Field(default="themes.json", description="主题数据文件")
    insights_file: str = Field(default="insights.json", description="洞见数据文件")
    
    # User-editable Markdown files (in project root)
    prompts_file: str = Field(default="prompts.md", description="提示词配置文件")
    coding_md: str = Field(default="01_coding_draft.md", description="编码草稿文件")
    themes_md: str = Field(default="02_themes_draft.md", description="主题草稿文件")
    report_md: str = Field(default="03_report.md", description="最终报告文件")
    
    def get_data_path(self, filename: str) -> Path:
        """Get full path for a data file."""
        return Path.cwd() / self.data_dir / filename
    
    def get_md_path(self, filename: str) -> Path:
        """Get full path for a markdown file (in project root)."""
        return Path.cwd() / filename
    
    def ensure_dirs(self) -> None:
        """Create project directories if they don't exist."""
        (Path.cwd() / self.data_dir).mkdir(exist_ok=True)
    
    def save(self, path: Path) -> None:
        """Save project configuration to JSON file."""
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")
    
    @classmethod
    def load(cls, path: Path) -> "Project":
        """Load project configuration from JSON file."""
        return cls.model_validate_json(path.read_text(encoding="utf-8"))

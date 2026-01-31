"""Markdown parser and generator."""

import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from llm_ta.models.coding import Code, Codebook
from llm_ta.models.theme import Theme, ThemeCollection


class MarkdownParser:
    """Parser for structured Markdown files."""
    
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader("llm_ta", "templates"),
            autoescape=select_autoescape(default=False),
        )
    
    # ================== Generators ==================
    
    def generate_coding_draft(
        self,
        codes: list[Code],
        output_path: Path,
        project_name: str = "",
    ) -> None:
        """Generate the coding draft markdown file."""
        template = self.env.get_template("01_coding.md.jinja2")
        content = template.render(
            project_name=project_name,
            codes=codes,
        )
        output_path.write_text(content, encoding="utf-8")
    
    def generate_consolidated_coding_draft(
        self,
        consolidated_codes: list[Any], # list[ConsolidatedCode]
        output_path: Path,
        project_name: str = "",
    ) -> None:
        """Generate the consolidated coding draft markdown file."""
        template = self.env.get_template("01_consolidated_coding.md.jinja2")
        content = template.render(
            project_name=project_name,
            codes=consolidated_codes,
        )
        output_path.write_text(content, encoding="utf-8")
    
    def generate_themes_draft(
        self,
        themes: list[Theme],
        codebook: Codebook,
        output_path: Path,
        project_name: str = "",
    ) -> None:
        """Generate the themes draft markdown file."""
        # Build code lookups
        codes_text = {c.id: c.text for c in codebook.codes}
        codes_quote = {c.id: c.source_quote for c in codebook.codes}
        codes_participant = {c.id: c.participant_id for c in codebook.codes}
        
        template = self.env.get_template("02_themes.md.jinja2")
        content = template.render(
            project_name=project_name,
            themes=themes,
            codes_text=codes_text,
            codes_quote=codes_quote,
            codes_participant=codes_participant,
        )
        output_path.write_text(content, encoding="utf-8")
    
    def generate_report(
        self,
        themes: list[dict[str, Any]],
        insights: dict[str, Any],
        output_path: Path,
        project_name: str = "",
        discussion: dict[str, Any] | None = None,
    ) -> None:
        """Generate the final report markdown file.
        
        Args:
            themes: List of theme dicts with codes containing source_quote
        """
        if discussion:
            # Normalize 'subsections' to 'sections'
            if "sections" not in discussion:
                if "subsections" in discussion:
                    discussion["sections"] = discussion["subsections"]
                elif "discussion_section" in discussion:
                    ds = discussion["discussion_section"]
                    if "subsections" in ds:
                        discussion["sections"] = ds["subsections"]
                    elif "sections" in ds:
                        discussion["sections"] = ds["sections"]
            


        template = self.env.get_template("03_report.md.jinja2")
        content = template.render(
            project_name=project_name,
            themes=themes,
            insights=insights,
            discussion=discussion,
        )
        output_path.write_text(content, encoding="utf-8")
    
    # ================== Parsers ==================
    
    def parse_coding_draft(self, path: Path) -> Codebook:
        """Parse user-edited coding draft and extract selected codes."""
        # ... (implementation same as before, but I'll add consolidated parsing)
        return self._parse_codes(path)

    def parse_consolidated_coding_draft(self, path: Path) -> list[Any]: # list[ConsolidatedCode]
        """Parse user-edited consolidated coding draft."""
        content = path.read_text(encoding="utf-8")
        consolidated_codes = []
        
        # Determine format: Header-based (### [x] ID) or List-based (- [x] **ID**)
        # The CLI currently generates List-based format.
        
        # Regex patterns for List-based format
        checkbox_pattern = re.compile(
            r'-\s*\[([ xX])\]\s*\*\*([^*]+)\*\*:\s*(.+?)(?=\n|$)'
        )
        desc_pattern = re.compile(
            r'^\s+-\s*定义:\s*(.+?)(?=\n|$)'
        )
        # Matches: - (P25): "quote"
        occ_pattern = re.compile(
            r'^\s+-\s*\(([^)]+)\):\s*["\"](.+?)["\"]'
        )
        
        from llm_ta.models.coding import ConsolidatedCode, CodeOccurence
        
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            checkbox_match = checkbox_pattern.match(line.strip())
            
            if checkbox_match:
                selected = checkbox_match.group(1).lower() == 'x'
                code_id = checkbox_match.group(2).strip()
                name = checkbox_match.group(3).strip()
                
                description = ""
                occurrences = []
                
                # Scan following lines for nested info until next top-level item or divider
                j = i + 1
                while j < len(lines):
                    sub_line = lines[j]
                    stripped_sub = sub_line.strip()
                    
                    if not stripped_sub:
                        j += 1
                        continue
                        
                    # Stop if we hit a new list item, header, or divider
                    if stripped_sub.startswith('- [') or stripped_sub.startswith('#') or stripped_sub.startswith('---'):
                        break
                        
                    # Check for description
                    desc_match = desc_pattern.match(sub_line) # use valid indent check if needed, but match should suffice
                    if desc_match:
                        description = desc_match.group(1).strip()
                        j += 1
                        continue
                        
                    # Check for occurrences
                    occ_match = occ_pattern.match(sub_line)
                    if occ_match:
                        occurrences.append(CodeOccurence(
                            participant_id=occ_match.group(1).strip(),
                            source_quote=occ_match.group(2).strip()
                        ))
                    
                    j += 1
                
                consolidated_codes.append(ConsolidatedCode(
                    id=code_id,
                    name=name,
                    description=description,
                    occurrences=occurrences,
                    selected=selected
                ))
                
                i = j - 1 # Main loop increment will handle the +1
                
            i += 1
            
        return consolidated_codes

    def _parse_codes(self, path: Path) -> Codebook:
        content = path.read_text(encoding="utf-8")
        codes = []
        
        # Pattern to match checkbox lines with code info
        # - [x] **C001**: 编码文本
        #   - 原文: "引用内容"
        #   <!-- ID: C001 | P: P01 -->
        
        checkbox_pattern = re.compile(
            r'-\s*\[([ xX])\]\s*\*\*([^*]+)\*\*:\s*(.+?)(?=\n|$)'
        )
        metadata_pattern = re.compile(
            r'<!--\s*ID:\s*([^\s|]+)\s*\|\s*P:\s*([^\s>]+)\s*-->'
        )
        quote_pattern = re.compile(
            r'-\s*原文:\s*["\"](.+?)["\"]'
        )
        
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            checkbox_match = checkbox_pattern.match(line.strip())
            
            if checkbox_match:
                selected = checkbox_match.group(1).lower() == 'x'
                code_id = checkbox_match.group(2).strip()
                code_text = checkbox_match.group(3).strip()
                
                # Look for quote and metadata in following lines
                source_quote = ""
                participant_id = ""
                
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j]
                    
                    quote_match = quote_pattern.search(next_line)
                    if quote_match:
                        source_quote = quote_match.group(1)
                    
                    meta_match = metadata_pattern.search(next_line)
                    if meta_match:
                        participant_id = meta_match.group(2)
                        break
                
                codes.append(Code(
                    id=code_id,
                    text=code_text,
                    source_quote=source_quote,
                    participant_id=participant_id,
                    selected=selected,
                ))
            
            i += 1
        
        return Codebook(codes=codes)
    
    def parse_themes_draft(self, path: Path) -> ThemeCollection:
        """Parse user-edited themes draft and extract theme structure."""
        content = path.read_text(encoding="utf-8")
        themes = []
        
        # Pattern for theme headers: ### Theme Name
        theme_pattern = re.compile(r'^###\s+(.+?)$', re.MULTILINE)
        theme_id_pattern = re.compile(r'<!--\s*THEME_ID:\s*(\S+)\s*-->')
        code_id_pattern = re.compile(r'<!--\s*CODE_ID:\s*(\S+)\s*-->')
        
        # Split content by theme headers
        parts = re.split(r'(^###\s+.+?$)', content, flags=re.MULTILINE)
        
        current_theme = None
        
        for part in parts:
            theme_match = theme_pattern.match(part.strip())
            
            if theme_match:
                # Start a new theme
                if current_theme:
                    themes.append(current_theme)
                
                current_theme = Theme(
                    id="",
                    name=theme_match.group(1).strip(),
                    description="",
                    code_ids=[],
                    sub_themes=[],
                )
            elif current_theme:
                # Parse theme content
                id_match = theme_id_pattern.search(part)
                if id_match:
                    current_theme.id = id_match.group(1)
                
                # Check for sub-themes (#### SubTheme)
                sub_parts = re.split(r'(^####\s+.+?$)', part, flags=re.MULTILINE)
                
                # First part is main theme description/codes (before any sub-theme)
                main_part = sub_parts[0]
                
                # Extract code IDs for main theme (if any flat codes)
                for code_match in code_id_pattern.finditer(main_part):
                    current_theme.code_ids.append(code_match.group(1))
                
                # Extract main description
                lines = main_part.strip().split('\n')
                desc_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('<!--') and not line.startswith('-'):
                        desc_lines.append(line)
                    elif line.startswith('-'):
                        break
                if desc_lines:
                    current_theme.description = ' '.join(desc_lines)
                
                # Process sub-themes
                from llm_ta.models.theme import SubTheme
                sub_theme_pattern = re.compile(r'^####\s+(.+?)$', re.MULTILINE)
                sub_id_pattern = re.compile(r'<!--\s*SUBTHEME_ID:\s*(\S+)\s*-->')
                
                for k in range(1, len(sub_parts), 2):
                    sub_header = sub_parts[k]
                    sub_body = sub_parts[k+1] if k+1 < len(sub_parts) else ""
                    
                    sub_match = sub_theme_pattern.match(sub_header.strip())
                    if sub_match:
                        sub_theme = SubTheme(
                            id="",
                            name=sub_match.group(1).strip(),
                            description="",
                            code_ids=[]
                        )
                        
                        # Sub-theme ID
                        sub_id_match = sub_id_pattern.search(sub_body)
                        if sub_id_match:
                            sub_theme.id = sub_id_match.group(1)
                        elif current_theme.id:
                             # Fallback ID generation
                             sub_theme.id = f"{current_theme.id}.{len(current_theme.sub_themes)+1}"
                        
                        # Sub-theme codes
                        for cm in code_id_pattern.finditer(sub_body):
                            sub_theme.code_ids.append(cm.group(1))
                        
                        # Sub-theme description
                        s_lines = sub_body.strip().split('\n')
                        s_desc = []
                        for sl in s_lines:
                            sl = sl.strip()
                            if sl and not sl.startswith('<!--') and not sl.startswith('-'):
                                s_desc.append(sl)
                            elif sl.startswith('-'):
                                break
                        if s_desc:
                            sub_theme.description = ' '.join(s_desc)
                            
                        current_theme.sub_themes.append(sub_theme)
        
        if current_theme:
            themes.append(current_theme)
        
        return ThemeCollection(themes=themes)
    
    # ================== Validators ==================
    
    def validate_coding_draft(self, path: Path) -> list[str]:
        """Validate coding draft format and return list of errors."""
        errors = []
        content = path.read_text(encoding="utf-8")
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for malformed checkboxes
            if re.match(r'-\s*\[[^\]]*$', line):
                errors.append(f"第 {i} 行: 复选框格式不完整，缺少 ]")
            
            # Check for missing ID metadata
            if '**C' in line and '**:' in line:
                # This looks like a code line, check for metadata
                found_meta = False
                for j in range(i, min(i + 3, len(lines))):
                    if '<!-- ID:' in lines[j-1]:
                        found_meta = True
                        break
                # Note: We don't require metadata for user-added codes
        
        return errors
    
    def validate_themes_draft(self, path: Path) -> list[str]:
        """Validate themes draft format and return list of errors."""
        errors = []
        content = path.read_text(encoding="utf-8")
        
        # Check for at least one theme
        if '### ' not in content:
            errors.append("未找到主题标题 (应使用 ### 格式)")
        
        return errors

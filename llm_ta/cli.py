"""Main CLI interface for LLM-assisted Thematic Analysis."""

import json
from pathlib import Path
from typing import Annotated, Optional
import re

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Load .env file from current directory or parent directories
load_dotenv()

from llm_ta.models.project import Project
from llm_ta.models.coding import Code, Codebook
from llm_ta.models.theme import Theme
from llm_ta.parsers.interview import InterviewParser
from llm_ta.parsers.markdown import MarkdownParser
from llm_ta.llm.prompts import PromptManager


app = typer.Typer(
    name="llm-ta",
    help="LLM-assisted Thematic Analysis Tool - 基于LLM的主题分析工具",
    add_completion=False,
)
console = Console()

# Project config file name
PROJECT_FILE = "project.json"


def get_project_path() -> Path:
    """Get the project config file path in current directory."""
    return Path.cwd() / PROJECT_FILE


def load_project() -> Project:
    """Load project configuration from current directory."""
    path = get_project_path()
    if not path.exists():
        console.print("[red]错误: 未找到项目配置文件。请先运行 `llm-ta init` 初始化项目。[/red]")
        raise typer.Exit(1)
    return Project.load(path)


def save_json(data: list | dict, path: Path) -> None:
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: Path) -> list | dict:
    """Load data from JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def parse_project_markdown(path: Path) -> tuple[str, list[str], list[str], str]:
    """Parse project configuration from a Markdown file."""
    content = path.read_text(encoding="utf-8")
    
    name = "My Study"
    background = ""
    name = "My Study"
    background = ""
    research_questions = []
    interview_questions = []
    
    # Parse project name from H1
    h1_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if h1_match:
        name = h1_match.group(1).strip()
    
    # Parse sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    
    for section in sections[1:]:
        lines = section.strip().split('\n')
        section_title = lines[0].strip().lower()
        section_content = '\n'.join(lines[1:]).strip()
        
        if '背景' in section_title or 'background' in section_title:
            background = section_content
        # Only match "Research Questions" or "研究问题", strictly avoiding "Interview Questions"
        elif ('question' in section_title and 'research' in section_title) or \
             ('问题' in section_title and '研究' in section_title):
            current_rq = None
            for line in section_content.split('\n'):
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                
                # Check for top-level list item (no indentation)
                is_toplevel = re.match(r'^[-*]\s+', line)
                # Check for indented list item
                is_indented = re.match(r'^\s+[-*]\s+', line)
                
                if is_toplevel:
                    # Start new RQ
                    rq_text = re.sub(r'^[-*]\s*(RQ\d*:?\s*)?', '', stripped_line).strip()
                    if rq_text:
                        current_rq = rq_text
                        research_questions.append(current_rq)
                elif is_indented and current_rq:
                     # Append to current RQ
                     sub_text = re.sub(r'^[-*]\s*', '', stripped_line).strip()
                     # Update the last added RQ in the list
                     research_questions[-1] += f"\n  - {sub_text}"
        
        # Parse Interview Questions
        elif ('question' in section_title and 'interview' in section_title) or \
             ('问题' in section_title and '访谈' in section_title):
            for line in section_content.split('\n'):
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                
                # Check for numbered list item or bullet
                is_item = re.match(r'^(\d+\.|[-*])\s+', line)
                # Check for indented list item (sub-questions)
                is_indented = re.match(r'^\s+[-*]\s+', line)
                
                if is_item:
                    iq_text = re.sub(r'^(\d+\.|[-*])\s*', '', stripped_line).strip()
                    if iq_text:
                        interview_questions.append(iq_text)
                elif is_indented and interview_questions:
                     # Append to current IQ
                     sub_text = re.sub(r'^[-*]\s*', '', stripped_line).strip()
                     # Update the last added IQ in the list
                     interview_questions[-1] += f"\n  - {sub_text}"
    
    return name, research_questions, interview_questions, background


@app.command()
def init(
    name: Annotated[str, typer.Option("--name", "-n", help="项目名称")] = "",
    rq: Annotated[list[str], typer.Option("--rq", help="研究问题 (可多次指定)")] = [],
    background: Annotated[str, typer.Option("--bg", help="研究背景描述")] = "",
    from_md: Annotated[Path, typer.Option("--from-md", "-f", help="从Markdown文件解析配置")] = None,
    lang: Annotated[str, typer.Option("--lang", "-l", help="输出语言: en/zh")] = "en",
):
    """初始化一个新的主题分析项目。"""
    path = get_project_path()
    
    if path.exists():
        overwrite = typer.confirm("项目配置已存在，是否覆盖？")
        if not overwrite:
            console.print("[yellow]已取消。[/yellow]")
            raise typer.Exit(0)
    
    # Parse from markdown if provided
    if from_md:
        if not from_md.exists():
            console.print(f"[red]错误: 文件不存在: {from_md}[/red]")
            raise typer.Exit(1)
        
        md_name, md_rqs, md_iqs, md_bg = parse_project_markdown(from_md)
        name = name or md_name
        if not rq:
            rq = md_rqs
        background = background or md_bg
        console.print(f"[cyan]从 {from_md} 解析配置...[/cyan]")
    else:
        md_iqs = []
    
    if not name:
        name = "My Study"
    
    project = Project(
        name=name,
        research_questions=rq,
        interview_questions=md_iqs,
        background=background,
        output_language=lang,
    )
    
    # Create directories
    project.ensure_dirs()
    
    # Save default prompts
    prompts_path = Path.cwd() / project.prompts_file
    PromptManager.save_default_prompts(prompts_path)
    
    # Save project config
    project.save(path)
    
    console.print(f"[green]✓ 项目 '{name}' 初始化成功！[/green]")
    console.print(f"  配置文件: {path}")
    console.print(f"  提示词: {project.prompts_file}")
    console.print(f"  数据目录: {project.data_dir}/")
    console.print(f"  输出语言: {lang}")
    
    if project.research_questions:
        console.print("\n[cyan]研究问题:[/cyan]")
        for i, q in enumerate(project.research_questions, 1):
            console.print(f"  {i}. {q}")


@app.command("import")
def import_interviews(
    file: Annotated[Path, typer.Argument(help="访谈数据JSON文件路径")],
):
    """导入访谈数据。"""
    project = load_project()
    project.ensure_dirs()
    
    if not file.exists():
        console.print(f"[red]错误: 文件不存在: {file}[/red]")
        raise typer.Exit(1)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("解析访谈数据...", total=None)
        
        try:
            collection = InterviewParser.parse_file(file)
        except Exception as e:
            console.print(f"[red]错误: 解析失败 - {e}[/red]")
            raise typer.Exit(1)
    
    # Save to data directory
    output_path = project.get_data_path(project.interviews_file)
    InterviewParser.save_collection(collection, output_path)
    
    # Show summary
    table = Table(title="导入成功")
    table.add_column("Participant", style="cyan")
    table.add_column("Responses", style="green")
    
    for interview in collection.interviews:
        table.add_row(interview.participant_id, str(len(interview.responses)))
    
    console.print(table)
    console.print(f"\n数据已保存到: {output_path}")


@app.command()
def coding():
    """生成初始编码 (需要LLM API)。"""
    project = load_project()
    project.ensure_dirs()
    
    interviews_path = project.get_data_path(project.interviews_file)
    
    if not interviews_path.exists():
        console.print("[red]错误: 未找到访谈数据。请先运行 `llm-ta import` 导入数据。[/red]")
        raise typer.Exit(1)
    
    # Check for existing files
    coding_md_path = project.get_md_path(project.coding_md)
    if coding_md_path.exists():
        overwrite = typer.confirm(f"编码文件已存在，是否覆盖？")
        if not overwrite:
            console.print("[yellow]已取消。[/yellow]")
            raise typer.Exit(0)
    
    # Load interview data
    collection = InterviewParser.parse_file(interviews_path)
    
    if not collection.interviews:
        console.print("[red]错误: 访谈数据为空。[/red]")
        raise typer.Exit(1)
    
    # Initialize LLM client with prompts
    try:
        from llm_ta.llm.client import LLMClient
        prompts_path = Path.cwd() / project.prompts_file
        llm = LLMClient(prompts_file=prompts_path)
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    all_codes = []
    code_counter = 1
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("生成编码中...", total=len(collection.interviews))
        
        for interview in collection.interviews:
            progress.update(task, description=f"Processing {interview.participant_id}...")
            
            interview_text = interview.get_full_text()
            raw_codes = llm.generate_codes(
                interview_text=interview_text,
                research_questions=project.research_questions,
                participant_id=interview.participant_id,
            )
            
            for raw in raw_codes:
                code = Code(
                    id=f"C{code_counter:03d}",
                    text=raw.get("text", ""),
                    source_quote=raw.get("source_quote", ""),
                    participant_id=raw.get("participant_id", interview.participant_id),
                    selected=False,
                )
                all_codes.append(code)
                code_counter += 1
            
            progress.advance(task)
    
    # Save codebook JSON to data directory
    codebook = Codebook(codes=all_codes)
    codebook_path = project.get_data_path(project.codebook_file)
    save_json([c.model_dump() for c in codebook.codes], codebook_path)
    
    # Generate markdown to output directory
    parser = MarkdownParser()
    parser.generate_coding_draft(
        codes=all_codes,
        output_path=coding_md_path,
        project_name=project.name,
    )
    
    console.print(f"\n[green]✓ 生成了 {len(all_codes)} 个编码[/green]")
    console.print(f"  JSON数据: {codebook_path}")
    console.print(f"  Markdown: {coding_md_path}")
    console.print("\n[cyan]下一步: 编辑Markdown文件，勾选有意义的编码，然后运行 `llm-ta theming`[/cyan]")


@app.command()
def theming():
    """生成主题分析 (需要LLM API)。"""
    project = load_project()
    project.ensure_dirs()
    
    coding_md_path = project.get_md_path(project.coding_md)
    
    if not coding_md_path.exists():
        console.print("[red]错误: 未找到编码文件。请先运行 `llm-ta coding` 生成编码。[/red]")
        raise typer.Exit(1)
    
    themes_md_path = project.get_md_path(project.themes_md)
    if themes_md_path.exists():
        overwrite = typer.confirm(f"主题文件已存在，是否覆盖？")
        if not overwrite:
            console.print("[yellow]已取消。[/yellow]")
            raise typer.Exit(0)
    
    # Parse user-edited coding file
    parser = MarkdownParser()
    codebook = parser.parse_coding_draft(coding_md_path)
    
    selected_codes = codebook.get_selected_codes()
    
    if not selected_codes:
        console.print("[red]错误: 未选中任何编码。[/red]")
        console.print("[yellow]请编辑 01_coding_draft.md，将 [ ] 改为 [x] 来勾选有意义的编码。[/yellow]")
        console.print("[yellow]例如: - [x] **C001**: 编码内容[/yellow]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]已选中 {len(selected_codes)} 个编码[/cyan]")
    
    # Initialize LLM client
    try:
        from llm_ta.llm.client import LLMClient
        prompts_path = Path.cwd() / project.prompts_file
        llm = LLMClient(prompts_file=prompts_path)
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("生成主题中...", total=None)
        
        codes_data = [
            {"id": c.id, "text": c.text, "source_quote": c.source_quote}
            for c in selected_codes
        ]
        
        raw_themes = llm.generate_themes(
            codes=codes_data,
            research_questions=project.research_questions,
        )
    
    # Convert to Theme objects
    themes = []
    for raw in raw_themes:
        theme = Theme(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            description=raw.get("description", ""),
            code_ids=raw.get("code_ids", []),
        )
        themes.append(theme)
    
    # Save themes JSON to data directory
    themes_json_path = project.get_data_path(project.themes_file)
    save_json([t.model_dump() for t in themes], themes_json_path)
    
    # Generate markdown to output directory
    parser.generate_themes_draft(
        themes=themes,
        codebook=codebook,
        output_path=themes_md_path,
        project_name=project.name,
    )
    
    console.print(f"\n[green]✓ 生成了 {len(themes)} 个主题[/green]")
    console.print(f"  JSON数据: {themes_json_path}")
    console.print(f"  Markdown: {themes_md_path}")
    console.print("\n[cyan]下一步: 编辑Markdown文件调整主题结构，然后运行 `llm-ta report`[/cyan]")


@app.command()
def report():
    """生成最终分析报告 (需要LLM API)。"""
    project = load_project()
    project.ensure_dirs()
    
    themes_md_path = project.get_md_path(project.themes_md)
    
    if not themes_md_path.exists():
        console.print("[red]错误: 未找到主题文件。请先运行 `llm-ta theming` 生成主题。[/red]")
        raise typer.Exit(1)
    
    report_md_path = project.get_md_path(project.report_md)
    if report_md_path.exists():
        overwrite = typer.confirm(f"报告文件已存在，是否覆盖？")
        if not overwrite:
            console.print("[yellow]已取消。[/yellow]")
            raise typer.Exit(0)
    
    # Parse user-edited themes file
    parser = MarkdownParser()
    theme_collection = parser.parse_themes_draft(themes_md_path)
    
    if not theme_collection.themes:
        console.print("[red]错误: 未找到任何主题。[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]发现 {len(theme_collection.themes)} 个主题[/cyan]")
    
    # Initialize LLM client
    try:
        from llm_ta.llm.client import LLMClient
        prompts_path = Path.cwd() / project.prompts_file
        llm = LLMClient(prompts_file=prompts_path)
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("生成洞见...", total=None)
        
        # Load codebook to get source quotes
        codebook_path = project.get_data_path(project.codebook_file)
        codes_lookup = {}
        if codebook_path.exists():
            codebook_data = load_json(codebook_path)
            codes_lookup = {c["id"]: c for c in codebook_data}
        
        # Build themes_data with source quotes
        themes_data = []
        for t in theme_collection.themes:
            codes_with_quotes = []
            for code_id in t.code_ids:
                if code_id in codes_lookup:
                    c = codes_lookup[code_id]
                    codes_with_quotes.append({
                        "id": code_id,
                        "text": c.get("text", ""),
                        "source_quote": c.get("source_quote", ""),
                        "participant_id": c.get("participant_id", ""),
                    })
            themes_data.append({
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "codes": codes_with_quotes,
            })
        
        insights = llm.generate_insights(
            themes=themes_data,
            research_questions=project.research_questions,
        )
        
        progress.update(task, description="生成Discussion...")
        
        discussion = llm.generate_discussion(
            themes=themes_data,
            insights=insights,
            research_questions=project.research_questions,
            background=project.background,
        )
    
    # Save JSON data
    insights_json_path = project.get_data_path(project.insights_file)
    save_json({"insights": insights, "discussion": discussion}, insights_json_path)
    
    # Generate report markdown with discussion
    parser.generate_report(
        themes=themes_data,
        insights=insights,
        discussion=discussion,
        output_path=report_md_path,
        project_name=project.name,
    )
    
    console.print(f"\n[green]✓ 报告生成成功[/green]")
    console.print(f"  JSON数据: {insights_json_path}")
    console.print(f"  Markdown: {report_md_path}")
    console.print("\n[cyan]请根据报告内容完成论文写作。[/cyan]")



@app.command()
def check(
    file: Annotated[Path, typer.Argument(help="要检查的Markdown文件")],
):
    """检查Markdown文件格式。"""
    if not file.exists():
        console.print(f"[red]错误: 文件不存在: {file}[/red]")
        raise typer.Exit(1)
    
    parser = MarkdownParser()
    errors = []
    
    filename = file.name
    if "coding" in filename.lower():
        errors = parser.validate_coding_draft(file)
    elif "theme" in filename.lower():
        errors = parser.validate_themes_draft(file)
    else:
        console.print("[yellow]警告: 无法识别文件类型，请确保文件名包含 'coding' 或 'theme'。[/yellow]")
        raise typer.Exit(1)
    
    if errors:
        console.print("[red]发现以下格式问题:[/red]")
        for error in errors:
            console.print(f"  • {error}")
        raise typer.Exit(1)
    else:
        console.print("[green]✓ 格式检查通过[/green]")


@app.command()
def status():
    """显示当前项目状态。"""
    try:
        project = load_project()
    except typer.Exit:
        console.print("[yellow]未初始化项目。运行 `llm-ta init` 开始。[/yellow]")
        return
    
    console.print(f"\n[bold]项目: {project.name}[/bold]")
    console.print(f"创建时间: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
    console.print(f"输出语言: {project.output_language}")
    
    if project.research_questions:
        console.print("\n[cyan]研究问题:[/cyan]")
        for i, rq in enumerate(project.research_questions, 1):
            console.print(f"  {i}. {rq}")
    
    console.print("\n[cyan]文件结构:[/cyan]")
    console.print(f"  {project.prompts_file} - 提示词配置")
    console.print(f"  data/  - JSON数据文件")
    
    console.print("\n[cyan]工作流状态:[/cyan]")
    
    steps = [
        (project.get_data_path(project.interviews_file), "访谈数据", "data/"),
        (project.get_md_path(project.coding_md), "初始编码", ""),
        (project.get_md_path(project.themes_md), "主题分析", ""),
        (project.get_md_path(project.report_md), "分析报告", ""),
    ]
    
    for path, label, dir_name in steps:
        status_mark = "[green]✓[/green]" if path.exists() else "[dim]○[/dim]"
        console.print(f"  {status_mark} {label} ({dir_name}{path.name})")


if __name__ == "__main__":
    app()

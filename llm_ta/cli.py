"""Main CLI interface for LLM-assisted Thematic Analysis."""

import json
from pathlib import Path
from typing import Annotated, Optional
import re

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

# Load .env file from current directory or parent directories
load_dotenv()

from llm_ta.models.project import Project
from llm_ta.models.coding import Code, Codebook, ConsolidatedCode
from llm_ta.models.theme import Theme
from llm_ta.parsers.interview import InterviewParser
from llm_ta.parsers.markdown import MarkdownParser
from llm_ta.llm.prompts import PromptManager

# Import analysis engines
from llm_ta.analysis.coding import CodingEngine
from llm_ta.analysis.theming import ThemingEngine
from llm_ta.analysis.reporting import ReportingEngine


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


from llm_ta.utils.io import load_json, save_json





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
def coding(
    strategy: Annotated[str, typer.Option(
        "--strategy", "-s",
        help="Coding strategy: 'per-participant' (legacy) or 'per-question' (reduces context length)"
    )] = "per-question",
):
    """生成初始编码 (需要LLM API)。"""
    project = load_project()
    project.ensure_dirs()
    
    interviews_path = project.get_data_path(project.interviews_file)
    if not interviews_path.exists():
        console.print("[red]错误: 未找到访谈数据。请先运行 `llm-ta import` 导入数据。[/red]")
        raise typer.Exit(1)
    
    coding_md_path = project.get_md_path(project.coding_md)
    if coding_md_path.exists() and not typer.confirm(f"编码文件已存在，是否覆盖？"):
        raise typer.Exit(0)
    
    collection = InterviewParser.parse_file(interviews_path)
    
    # Initialize Engine
    try:
        from llm_ta.llm.client import LLMClient
        prompts_path = Path.cwd() / project.prompts_file
        llm = LLMClient(prompts_file=prompts_path)
        engine = CodingEngine(llm)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    all_codes = []
    code_counter = 1
    
    if strategy == "per-question":
        # Group all participants' answers by question
        question_answers: dict[str, list[dict]] = {}
        for interview in collection.interviews:
            for response in interview.responses:
                q = response.question
                if q not in question_answers:
                    question_answers[q] = []
                question_answers[q].append({
                    "participant_id": interview.participant_id,
                    "answer": response.answer
                })
        
        # Create per-question codes directory
        codes_by_q_dir = project.get_data_path("codes_by_question")
        codes_by_q_dir.mkdir(exist_ok=True)
        
        # Track codes by question for incremental saving
        codes_by_question: dict[str, list] = {}
        codebook_path = project.get_data_path(project.codebook_file)
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("按问题生成编码中...", total=len(question_answers))
            for q_idx, (question, answers) in enumerate(question_answers.items(), 1):
                # Truncate question for display
                q_display = question[:50] + "..." if len(question) > 50 else question
                progress.update(task, description=f"Q{q_idx}/{len(question_answers)}: {q_display}")
                
                try:
                    codes = engine.extract_codes_by_question(question, answers, project.research_questions)
                except Exception as e:
                    console.print(f"\n[yellow]⚠ Q{q_idx} 编码失败: {e}[/yellow]")
                    progress.advance(task)
                    continue
                
                question_codes = []
                for code in codes:
                    code.id = f"C{code_counter:03d}"
                    all_codes.append(code)
                    question_codes.append(code.model_dump())
                    code_counter += 1
                
                codes_by_question[f"Q{q_idx}"] = question_codes
                
                # Save this question's codes to a separate file
                q_file = codes_by_q_dir / f"codes_q{q_idx:02d}.json"
                save_json(question_codes, q_file)
                
                # Incremental save: write all codes so far after each question
                save_json([c.model_dump() for c in all_codes], codebook_path)
                
                progress.advance(task)
        
        # Save the question mapping for reference
        question_map = {f"Q{i+1}": q for i, q in enumerate(question_answers.keys())}
        save_json(question_map, codes_by_q_dir / "question_map.json")
    else:
        # Legacy: per-participant strategy
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("生成编码中...", total=len(collection.interviews))
            for interview in collection.interviews:
                progress.update(task, description=f"Processing {interview.participant_id}...")
                
                codes = engine.extract_codes_for_interview(interview, project.research_questions)
                
                for code in codes:
                    code.id = f"C{code_counter:03d}"
                    all_codes.append(code)
                    code_counter += 1
                progress.advance(task)
    
    # Save and Generate Markdown
    codebook = Codebook(codes=all_codes)
    save_json([c.model_dump() for c in codebook.codes], project.get_data_path(project.codebook_file))
    
    parser = MarkdownParser()
    parser.generate_coding_draft(all_codes, coding_md_path, project.name)
    
    console.print(f"\n[green]✓ 生成了 {len(all_codes)} 个编码[/green]")
    console.print(f"  下一步: 运行 `llm-ta consolidate` 对编码进行合并去重")


@app.command()
def consolidate():
    """合并同义编码 (需要LLM API)。按问题分别去重，生成按问题组织的文件。"""
    project = load_project()
    
    # Check for per-question codes directory
    codes_by_question_dir = project.get_data_path("codes_by_question")
    question_map_path = codes_by_question_dir / "question_map.json"
    
    if not codes_by_question_dir.exists() or not question_map_path.exists():
        console.print("[red]错误: 未找到按问题编码的数据。请先运行 `llm-ta coding --strategy per-question`。[/red]")
        raise typer.Exit(1)
    
    consolidated_md_path = project.get_md_path("01_consolidated_coding.md")
    
    # Load question map
    question_map = load_json(question_map_path)
    
    # Initialize LLM
    try:
        from llm_ta.llm.client import LLMClient
        prompts_path = Path.cwd() / project.prompts_file
        llm = LLMClient(prompts_file=prompts_path)
        engine = CodingEngine(llm)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    # Process codes by question
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("按问题合并编码...", total=len(list(codes_by_question_dir.glob("codes_q*.json"))))
        
        def update_progress(msg, advance=False):
            if msg:
                progress.update(task, description=msg)
            if advance:
                progress.advance(task)
                
        all_consolidated_by_question, stats = engine.consolidate_by_question(
            codes_by_question_dir=codes_by_question_dir,
            question_map=question_map,
            research_questions=project.research_questions,
            output_dir=project.get_data_path("consolidated_by_question"),
            progress_callback=update_progress
        )
        
    total_original = stats["total_original"]
    total_consolidated = stats["total_consolidated"]
    
    # Save consolidated results (Global Files)
    consolidated_data = {
        q_key: [c.model_dump() for c in codes]
        for q_key, codes in all_consolidated_by_question.items()
    }
    save_json(consolidated_data, project.get_data_path("codebook_consolidated_by_question.json"))
    
    # Also save flat list for theming compatibility
    flat_codes = []
    for codes in all_consolidated_by_question.values():
        flat_codes.extend(codes)
    save_json([c.model_dump() for c in flat_codes], project.get_data_path("codebook_consolidated.json"))
    
    # Generate Markdown organized by questions
    _generate_consolidated_by_question_md(
        all_consolidated_by_question,
        question_map,
        consolidated_md_path,
        project.name
    )
    
    reduction = ((total_original - total_consolidated) / total_original * 100) if total_original > 0 else 0
    console.print(f"\n[green]✓ 按问题合并完成[/green]")
    console.print(f"  原始编码: {total_original} → 合并后: {total_consolidated} (减少 {reduction:.1f}%)")
    console.print(f"  请在 {consolidated_md_path} 中审查合并结果")
    console.print(f"\n[cyan]下一步: 勾选 [x] 以确认合并后的编码，然后运行 `llm-ta theming`[/cyan]")


def _generate_consolidated_by_question_md(
    codes_by_question: dict[str, list[Code]],
    question_map: dict[str, str],
    output_path: Path,
    project_name: str
):
    """Generate consolidated coding markdown organized by questions."""
    lines = [
        f"# {project_name} - 合并后编码 (按问题组织)",
        "",
        "> 请仔细阅读下列编码，勾选您认为有意义的编码 `[x]`，修改文字，或添加新的编码。",
        "> **注意**: 请勿修改 `<!-- ID: ... -->` 注释中的内容。",
        "",
    ]
    
    for q_key in sorted(codes_by_question.keys(), key=lambda x: int(x[1:])):
        codes = codes_by_question[q_key]
        q_text = question_map.get(q_key, f"问题 {q_key}")
        # Extract just the main question (first line)
        main_question = q_text.split("\n")[0] if "\n" in q_text else q_text
        
        lines.append(f"## {q_key}: {main_question}")
        lines.append("")
        lines.append(f"*共 {len(codes)} 个编码*")
        lines.append("")
        
        for code in codes:
            lines.append(f"- [ ] **{code.id}**: {code.name}")
            if code.description:
                lines.append(f"  - 定义: {code.description}")
            if code.occurrences:
                for occ in code.occurrences[:3]:  # Show up to 3 quotes
                    lines.append(f"  - ({occ.participant_id}): \"{occ.source_quote}\"")
                if len(code.occurrences) > 3:
                    lines.append(f"  - *...还有 {len(code.occurrences) - 3} 条引用*")
            participants = ", ".join(occ.participant_id for occ in code.occurrences) if code.occurrences else ""
            lines.append(f"  <!-- ID: {code.id} | P: {participants} -->")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    lines.append("## 使用说明")
    lines.append("")
    lines.append("1. 使用 `[x]` 勾选有意义的编码")
    lines.append("2. 可以直接修改编码文本来润色或纠正")
    lines.append("3. 可以在列表末尾添加新的编码（保持相同格式）")
    lines.append("4. 完成后运行 `llm-ta theming` 生成主题.")
    
    output_path.write_text("\n".join(lines), encoding="utf-8")


@app.command()
def merge_codes(
    batch_size: Annotated[int, typer.Option(
        "--batch-size", "-b",
        help="每轮合并的文件数量"
    )] = 3,
):
    """层级归并编码 (需要LLM API)。将按问题生成的编码进行层级合并。"""
    project = load_project()
    project.ensure_dirs()
    
    codes_by_q_dir = project.get_data_path("codes_by_question")
    if not codes_by_q_dir.exists():
        console.print("[red]错误: 未找到按问题编码的数据。请先运行 `llm-ta coding --strategy per-question`。[/red]")
        raise typer.Exit(1)
    
    # Find all question code files
    q_files = sorted(codes_by_q_dir.glob("codes_q*.json"))
    if not q_files:
        console.print("[red]错误: 未找到按问题编码的文件。[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]找到 {len(q_files)} 个问题编码文件[/cyan]")
    
    # Initialize LLM
    try:
        from llm_ta.llm.client import LLMClient
        prompts_path = Path.cwd() / project.prompts_file
        llm = LLMClient(prompts_file=prompts_path)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    # Load all codes from files
    current_groups = []
    for f in q_files:
        codes = load_json(f)
        current_groups.append({
            "source": f.stem,
            "codes": codes
        })
    
    round_num = 1
    merge_dir = project.get_data_path("merge_rounds")
    merge_dir.mkdir(exist_ok=True)
    
    while len(current_groups) > 1:
        console.print(f"\n[cyan]Round {round_num}: 合并 {len(current_groups)} 组 (batch_size={batch_size})[/cyan]")
        
        next_groups = []
        batch_idx = 0
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            total_batches = (len(current_groups) + batch_size - 1) // batch_size
            task = progress.add_task(f"Round {round_num} 归并中...", total=total_batches)
            
            for i in range(0, len(current_groups), batch_size):
                batch = current_groups[i:i+batch_size]
                batch_idx += 1
                
                progress.update(task, description=f"Batch {batch_idx}/{total_batches}")
                
                # Merge this batch
                all_codes_in_batch = []
                sources = []
                for g in batch:
                    all_codes_in_batch.extend(g["codes"])
                    sources.append(g["source"])
                
                if len(batch) == 1:
                    # No need to merge single batch
                    merged_codes = all_codes_in_batch
                else:
                    # Call LLM to merge codes
                    try:
                        merged_codes = llm.merge_codes(
                            codes=all_codes_in_batch,
                            research_questions=project.research_questions,
                        )
                    except Exception as e:
                        console.print(f"\n[yellow]⚠ Batch {batch_idx} 合并失败: {e}[/yellow]")
                        merged_codes = all_codes_in_batch  # Fallback: keep all
                
                # Save this batch result
                batch_file = merge_dir / f"round{round_num}_batch{batch_idx:02d}.json"
                save_json(merged_codes, batch_file)
                
                next_groups.append({
                    "source": f"round{round_num}_batch{batch_idx:02d}",
                    "codes": merged_codes
                })
                
                progress.advance(task)
        
        current_groups = next_groups
        round_num += 1
    
    # Final merged codes
    final_codes = current_groups[0]["codes"]
    
    # Reassign IDs
    for i, code in enumerate(final_codes):
        code["id"] = f"C{i+1:03d}"
    
    # Save to codebook
    codebook_path = project.get_data_path(project.codebook_file)
    save_json(final_codes, codebook_path)
    
    # Generate markdown
    from llm_ta.models.coding import Code, Codebook
    codes_objs = [Code(**c) for c in final_codes]
    codebook = Codebook(codes=codes_objs)
    
    parser = MarkdownParser()
    coding_md_path = project.get_md_path(project.coding_md)
    parser.generate_coding_draft(codes_objs, coding_md_path, project.name)
    
    console.print(f"\n[green]✓ 层级归并完成: {len(final_codes)} 个编码[/green]")
    console.print(f"  经过 {round_num - 1} 轮合并")
    console.print(f"  Markdown: {coding_md_path}")
    console.print(f"\n[cyan]下一步: 运行 `llm-ta consolidate` 进行语义去重[/cyan]")


@app.command()
def theming(
    strategy: Annotated[str, typer.Option(
        "--strategy", "-s",
        help="Theming strategy: 'global' (default), 'per-rq', or 'hierarchical'"
    )] = "global",
    deep: bool = typer.Option(False, "--deep", "-d", help="Deprecated: use --strategy hierarchical"),
    raw: bool = typer.Option(False, "--raw", "-r", help="Skip semantic deduplication, use raw codes"),
    hierarchical: bool = typer.Option(False, "--hierarchical", help="Shortcut for --strategy hierarchical"),
):
    """Generate thematic analysis (requires LLM API)."""
    # handle deprecated/shortcut flags
    if deep or hierarchical:
        strategy = "hierarchical"
    project = load_project()
    project.ensure_dirs()
    
    # Check for coding files
    consolidated_md_path = project.get_md_path("01_consolidated_coding.md")
    coding_md_path = project.get_md_path(project.coding_md)
    
    parser = MarkdownParser()
    selected_codes = []
    
    if raw:
        # Force use raw codes, skip consolidation
        if coding_md_path.exists():
            console.print(f"[cyan]使用原始编码文件 (跳过语义去重): {coding_md_path.name}[/cyan]")
            codebook = parser.parse_coding_draft(coding_md_path)
            selected_codes = codebook.get_selected_codes()
        else:
            console.print("[red]错误: 未找到原始编码文件。请先运行 `llm-ta coding`。[/red]")
            raise typer.Exit(1)
    elif consolidated_md_path.exists():
        console.print(f"[cyan]使用合并后的编码文件: {consolidated_md_path.name}[/cyan]")
        consolidated_codes = parser.parse_consolidated_coding_draft(consolidated_md_path)
        selected_codes = [c for c in consolidated_codes if c.selected]
    elif coding_md_path.exists():
        console.print(f"[yellow]提示: 未找到合并后的编码，使用原始编码文件: {coding_md_path.name}[/yellow]")
        codebook = parser.parse_coding_draft(coding_md_path)
        selected_codes = codebook.get_selected_codes()
    else:
        console.print("[red]错误: 未找到编码文件。请先运行 `llm-ta coding` 或 `llm-ta consolidate`。[/red]")
        raise typer.Exit(1)
    
    if not selected_codes:
        console.print("[red]错误: 未选中任何编码。[/red]")
        raise typer.Exit(1)
        
    console.print(f"[cyan]已选中 {len(selected_codes)} 个编码[/cyan]")
    
    # Initialize Engine
    try:
        from llm_ta.llm.client import LLMClient
        llm = LLMClient(prompts_file=Path.cwd() / project.prompts_file)
        engine = ThemingEngine(llm)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(1)
    
    if strategy == "hierarchical":
        # Hierarchical mode: sub-themes per RQ → major themes
        console.print("[cyan]Using Hierarchical Theming (Sub-themes -> Major Themes)...[/cyan]")
        
        # Load full interview data for complete source quotes
        interviews_path = project.get_data_path(project.interviews_file)
        n_loaded = engine.load_interviews(interviews_path)
        if n_loaded > 0:
            console.print(f"[dim]Loaded {n_loaded} participants for quotes[/dim]")
        
        # Prepare codes data once (outside the loop)
        codes_data = engine.prepare_codes_for_llm(selected_codes, include_quotes=True)
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("Generating hierarchical themes...", total=len(project.research_questions) + 1)
            
            # Helper to update progress from engine
            def update_progress(msg):
                progress.update(task, description=msg)
                progress.advance(task)
            
            # Define output directory for incremental cache
            themes_out_dir = project.get_data_path("themes_by_rq")
            
            themes, all_sub_themes = engine.generate_hierarchical_themes(
                codes_data=codes_data,
                research_questions=project.research_questions,
                progress_callback=update_progress,
                output_dir=themes_out_dir
            )
        
        console.print(f"\n[green]✓ Generated {len(themes)} Major Themes and {len(all_sub_themes)} Sub-themes[/green]")
    elif strategy == "per-rq":
        console.print("[cyan]Using Per-RQ Theming (Independent themes for each RQ)...[/cyan]")
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            progress.add_task("Generating themes per RQ...", total=None)
            themes = engine.generate_themes(selected_codes, project.research_questions, strategy="per-rq")
        console.print(f"\n[green]✓ Generated {len(themes)} Themes across {len(project.research_questions)} RQs[/green]")
    else:
        # Standard global theming
        console.print("[cyan]Using Global Direct Theming...[/cyan]")
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            progress.add_task("Generating global themes...", total=None)
            themes = engine.generate_themes(selected_codes, project.research_questions, strategy="global")
        console.print(f"\n[green]✓ Generated {len(themes)} Themes[/green]")
        
    # Save themes
    themes_json_path = project.get_data_path(project.themes_file)
    save_json([t.model_dump() for t in themes], themes_json_path)
    
    themes_md_path = project.get_md_path(project.themes_md)
    # We need a dummy codebook for the existing generate_themes_draft parser which expects raw codes
    # Build lookup data for the markdown draft
    if consolidated_md_path.exists() and not raw:
        # Convert ConsolidatedCode to temporary Code objects for the template
        temp_codes = []
        for c in selected_codes:
            # Flatten consolidated code for the themes draft view (using first quote as example)
            temp_codes.append(Code(
                id=c.id,
                text=c.name,
                source_quote=c.occurrences[0].source_quote if c.occurrences else "",
                participant_id=c.occurrences[0].participant_id if c.occurrences else "",
                selected=True
            ))
        dummy_codebook = Codebook(codes=temp_codes)
    else:
        dummy_codebook = Codebook(codes=selected_codes)
        
    parser.generate_themes_draft(themes, dummy_codebook, themes_md_path, project.name)
    
    console.print(f"  Markdown: {themes_md_path}")
    console.print("\n[cyan]下一步: 编辑Markdown文件调整主题结构，然后运行 `llm-ta report`[/cyan]")


@app.command()
def report():
    """生成最终分析报告 (需要LLM API)。"""
    project = load_project()
    project.ensure_dirs()
    
    themes_md_path = project.get_md_path(project.themes_md)
    if not themes_md_path.exists():
        console.print("[red]错误: 未找到主题文件。请先运行 `llm-ta theming`。[/red]")
        raise typer.Exit(1)
        
    report_md_path = project.get_md_path(project.report_md)
    if report_md_path.exists() and not typer.confirm(f"报告文件已存在，是否覆盖？"):
        raise typer.Exit(0)
    
    # Parse themes
    parser = MarkdownParser()
    theme_collection = parser.parse_themes_draft(themes_md_path)
    
    # Initialize Engine
    try:
        from llm_ta.llm.client import LLMClient
        llm = LLMClient(prompts_file=Path.cwd() / project.prompts_file)
        engine = ReportingEngine(llm)
        
        # Smart Codebook Selection based on Theme IDs
        # Check if first theme has code IDs that look like Consolidated (CC_...) or Raw (C...)
        sample_code_id = ""
        for t in theme_collection.themes:
            ids = t.get_all_code_ids()
            if ids:
                sample_code_id = ids[0]
                break
        
        consolidated_path = project.get_data_path("codebook_consolidated.json")
        codebook_path = project.get_data_path(project.codebook_file)
        
        target_codebook_path = None
        is_consolidated = False
        
        # Heuristic: Consolidated usually have "CC_" or different format, 
        # or we check if the ID exists in the respective files.
        if consolidated_path.exists():
            data = load_json(consolidated_path)
            # Check if sample ID is in this file
            if any(c["id"] == sample_code_id for c in data):
                target_codebook_path = consolidated_path
                is_consolidated = True
        
        if not target_codebook_path and codebook_path.exists():
            target_codebook_path = codebook_path
            is_consolidated = False
            
        # Fallback priority
        if not target_codebook_path:
             if consolidated_path.exists(): target_codebook_path = consolidated_path; is_consolidated = True
             elif codebook_path.exists(): target_codebook_path = codebook_path; is_consolidated = False

        console.print(f"[dim]Using Codebook: {target_codebook_path.name}[/dim]")

        codes_lookup = {}
        if target_codebook_path and target_codebook_path.exists():
            data = load_json(target_codebook_path)
            for c in data:
                c_id = c["id"]
                # Normalize structure
                if is_consolidated:
                     codes_lookup[c_id] = {
                        "text": c["name"],
                        "source_quote": c["occurrences"][0]["source_quote"] if c["occurrences"] else "",
                        "participant_id": c["occurrences"][0]["participant_id"] if c["occurrences"] else ""
                    }
                else:
                    codes_lookup[c_id] = {
                        "text": c["text"],
                        "source_quote": c["source_quote"],
                        "participant_id": c.get("participant_id", "")
                    }
    except Exception as e:
        console.print(f"[red]Error loading codebook: {e}[/red]")
        raise typer.Exit(1)
        
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        progress.add_task("生成报告中...", total=None)
        
        # Build theme context with quotes
        themes_data = []
        for t in theme_collection.themes:
            codes_in_theme = []
            for cid in t.code_ids:
                if cid in codes_lookup:
                    codes_in_theme.append(codes_lookup[cid])
            
            # Process sub-themes if they exist
            sub_themes_data = []
            if hasattr(t, "sub_themes"):
                for st in t.sub_themes:
                    st_codes = []
                    for cid in st.code_ids:
                        if cid in codes_lookup:
                            st_codes.append(codes_lookup[cid])
                    
                    sub_themes_data.append({
                        "id": st.id,
                        "name": st.name,
                        "description": st.description,
                        "codes": st_codes
                    })

            themes_data.append({
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "codes": codes_in_theme,
                "sub_themes": sub_themes_data
            })
            
        # Load interviews for context if available
        interviews_path = project.get_data_path(project.interviews_file)
        interviews_data = []
        if interviews_path.exists():
            interviews_data = load_json(interviews_path)
            
        insights, discussion = engine.generate_insights_and_discussion(
            themes_data, 
            project.research_questions, 
            project.background,
            interviews_data=interviews_data
        )
        
    # Save results
    save_json({"insights": insights, "discussion": discussion}, project.get_data_path(project.insights_file))
    parser.generate_report(themes_data, insights, report_md_path, project.name, discussion)
    
    console.print(f"\n[green]✓ 报告生成成功[/green]")
    console.print(f"  Markdown: {report_md_path}")
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

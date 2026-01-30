"""End-to-end integration tests for the complete LLM-TA workflow.

This test suite verifies the full pipeline:
init → import → coding → consolidate → theming → report

LLM calls are mocked to ensure deterministic testing.
"""

import json
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from llm_ta.cli import app


runner = CliRunner()


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def example_dir():
    """Path to example data directory."""
    return Path(__file__).parent.parent / "example"


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace directory."""
    workspace = tmp_path / "workspace"
    # Clean up if already exists
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir()
    yield workspace
    # Cleanup after test
    os.chdir(Path(__file__).parent.parent)


@pytest.fixture
def mock_llm_responses():
    """Mock responses for LLM calls at each stage."""
    return {
        "coding": [
            {"id": "C001", "text": "Password Reuse", "source_quote": "我用同一个密码", "participant_id": "P01"},
            {"id": "C002", "text": "Memory Limitations", "source_quote": "记不住那么多密码", "participant_id": "P01"},
            {"id": "C003", "text": "Tiered Security", "source_quote": "银行卡密码肯定不一样", "participant_id": "P02"},
        ],
        "consolidate": {
            "consolidated_codes": [
                {
                    "id": "CC_01",
                    "name": "Password Reuse Pattern",
                    "description": "Users reuse passwords across accounts.",
                    "original_code_ids": ["C001", "C002"]
                },
                {
                    "id": "CC_02",
                    "name": "Tiered Security Strategy",
                    "description": "Users apply different security to different accounts.",
                    "original_code_ids": ["C003"]
                }
            ]
        },
        "theming": [
            {
                "id": "T01",
                "name": "Cognitive Load Management",
                "description": "Users develop strategies to manage password complexity.",
                "code_ids": ["CC_01", "CC_02"]
            }
        ],
        "insight": {
            "key_findings": [
                {"finding": "Users adopt tiered security strategies.", "supporting_themes": ["T01"]}
            ],
            "research_question_linkage": [
                {"rq": "How do users manage passwords?", "answer": "Through tiered strategies and reuse."}
            ]
        },
        "discussion": {
            "sections": [
                {
                    "title": "RQ1: Password Management Strategies",
                    "content": "Our findings reveal that users employ tiered security strategies...",
                    "type": "rq_answer"
                }
            ]
        }
    }


# ============================================================================
# Integration Test: Full Workflow
# ============================================================================

class TestFullWorkflowIntegration:
    """Test the complete workflow from init to report."""

    def test_init_command_creates_project(self, temp_workspace, example_dir):
        """llm-ta init should create project.json and prompts.md."""
        os.chdir(temp_workspace)
        
        result = runner.invoke(app, [
            "init",
            "--from-md", str(example_dir / "project.md"),
            "--lang", "en"
        ])
        
        assert result.exit_code == 0, f"Init failed: {result.output}"
        assert (temp_workspace / "project.json").exists()
        assert (temp_workspace / "prompts.md").exists()

    def test_import_command_creates_interviews(self, temp_workspace, example_dir):
        """llm-ta import should create interviews.json in data directory."""
        os.chdir(temp_workspace)
        
        # First init
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        
        # Then import
        result = runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        
        assert result.exit_code == 0, f"Import failed: {result.output}"
        assert (temp_workspace / "data" / "interviews.json").exists()

    @patch("llm_ta.llm.client.LLMClient")
    def test_coding_command_generates_codes(self, mock_llm_class, temp_workspace, example_dir, mock_llm_responses):
        """llm-ta coding should generate codebook.json and markdown draft."""
        os.chdir(temp_workspace)
        
        # Setup mock
        mock_llm = MagicMock()
        mock_llm.generate_codes.return_value = mock_llm_responses["coding"]
        mock_llm_class.return_value = mock_llm
        
        # Init and import
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        
        # Run coding
        result = runner.invoke(app, ["coding"])
        
        assert result.exit_code == 0, f"Coding failed: {result.output}"
        assert (temp_workspace / "data" / "codebook.json").exists()
        assert (temp_workspace / "01_coding_draft.md").exists()

    @patch("llm_ta.llm.client.LLMClient")
    def test_consolidate_command_merges_codes(self, mock_llm_class, temp_workspace, example_dir, mock_llm_responses):
        """llm-ta consolidate should create consolidated codebook."""
        os.chdir(temp_workspace)
        
        # Setup mock
        mock_llm = MagicMock()
        mock_llm.generate_codes.return_value = mock_llm_responses["coding"]
        mock_llm.chat_json.return_value = mock_llm_responses["consolidate"]
        mock_llm._get_prompts.return_value = ("system", "user {codes_json}")
        mock_llm_class.return_value = mock_llm
        
        # Init, import, and coding
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        runner.invoke(app, ["coding"])
        
        # Run consolidate
        result = runner.invoke(app, ["consolidate"])
        
        assert result.exit_code == 0, f"Consolidate failed: {result.output}"
        assert (temp_workspace / "data" / "codebook_consolidated.json").exists()
        assert (temp_workspace / "01_consolidated_coding.md").exists()

    @patch("llm_ta.llm.client.LLMClient")
    def test_theming_command_generates_themes(self, mock_llm_class, temp_workspace, example_dir, mock_llm_responses):
        """llm-ta theming should generate themes.json and markdown draft."""
        os.chdir(temp_workspace)
        
        # Setup mock
        mock_llm = MagicMock()
        mock_llm.generate_codes.return_value = mock_llm_responses["coding"]
        mock_llm.chat_json.return_value = mock_llm_responses["consolidate"]
        mock_llm.generate_themes.return_value = mock_llm_responses["theming"]
        mock_llm._get_prompts.return_value = ("system", "user {codes_json}")
        mock_llm_class.return_value = mock_llm
        
        # Full pipeline up to theming
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        runner.invoke(app, ["coding"])
        runner.invoke(app, ["consolidate"])
        
        # Run theming
        result = runner.invoke(app, ["theming"])
        
        assert result.exit_code == 0, f"Theming failed: {result.output}"
        assert (temp_workspace / "data" / "themes.json").exists()
        assert (temp_workspace / "02_themes_draft.md").exists()

    @patch("llm_ta.llm.client.LLMClient")
    def test_report_command_generates_full_report(self, mock_llm_class, temp_workspace, example_dir, mock_llm_responses):
        """llm-ta report should generate final report with Results and Discussion."""
        os.chdir(temp_workspace)
        
        # Setup mock
        mock_llm = MagicMock()
        mock_llm.generate_codes.return_value = mock_llm_responses["coding"]
        mock_llm.chat_json.return_value = mock_llm_responses["consolidate"]
        mock_llm.generate_themes.return_value = mock_llm_responses["theming"]
        mock_llm.generate_insights.return_value = mock_llm_responses["insight"]
        mock_llm.generate_discussion.return_value = mock_llm_responses["discussion"]
        mock_llm._get_prompts.return_value = ("system", "user {codes_json}")
        mock_llm_class.return_value = mock_llm
        
        # Full pipeline
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        runner.invoke(app, ["coding"])
        runner.invoke(app, ["consolidate"])
        runner.invoke(app, ["theming"])
        
        # Run report
        result = runner.invoke(app, ["report"])
        
        assert result.exit_code == 0, f"Report failed: {result.output}"
        assert (temp_workspace / "03_report.md").exists()
        
        # Verify report content
        report_content = (temp_workspace / "03_report.md").read_text(encoding="utf-8")
        assert "## Interview Results" in report_content
        assert "## Discussion" in report_content


# ============================================================================
# Report Quality Validation
# ============================================================================

# LLM Validation Prompt for Report Quality
REPORT_VALIDATION_PROMPT = '''
You are a Quality Assurance reviewer for academic thematic analysis reports.

## Task
Evaluate the following report and determine if it meets the quality criteria.

## Report Content
{report_content}

## Research Questions
{research_questions}

## Quality Criteria

### 1. Results Section (Interview Results)
- [ ] Contains at least one theme with a clear name and description
- [ ] Each theme includes **Supporting Evidence** with direct participant quotes
- [ ] Quotes are attributed to specific participants (e.g., "— P01", "— P02")
- [ ] Quotes are actual interview content (in Chinese), not fabricated

### 2. Discussion Section
- [ ] Discussion section is NOT empty
- [ ] Discussion addresses each Research Question explicitly
- [ ] Discussion references findings from the Results section
- [ ] Discussion provides interpretation, not just summary

## Output Format
Return a JSON object:
```json
{{
  "valid": true/false,
  "results_has_quotes": true/false,
  "results_quotes_attributed": true/false,
  "discussion_not_empty": true/false,
  "discussion_addresses_rqs": true/false,
  "issues": ["list of specific issues found, if any"]
}}
```
'''


class TestReportQualityValidation:
    """Validate the quality and content of generated reports."""

    def test_results_contains_participant_quotes(self, tmp_path):
        """Results section must contain attributed participant quotes."""
        from llm_ta.parsers.markdown import MarkdownParser
        import re
        
        parser = MarkdownParser()
        themes = [{
            "id": "T01",
            "name": "Test Theme",
            "description": "Theme description.",
            "codes": [
                {"text": "Code1", "source_quote": "我用同一个密码", "participant_id": "P01"},
                {"text": "Code2", "source_quote": "记不住那么多", "participant_id": "P02"},
            ]
        }]
        
        output_path = tmp_path / "03_report.md"
        parser.generate_report(themes, {}, output_path, "Test", {"sections": []})
        
        content = output_path.read_text(encoding="utf-8")
        
        # Check for quoted evidence with participant attribution
        quote_pattern = r'>\s*"[^"]+"\s*—\s*P\d+'
        matches = re.findall(quote_pattern, content)
        
        assert len(matches) >= 2, f"Expected at least 2 attributed quotes, found {len(matches)}"
        assert "P01" in content
        assert "P02" in content

    def test_discussion_addresses_research_questions(self, tmp_path):
        """Discussion section must address research questions explicitly."""
        from llm_ta.parsers.markdown import MarkdownParser
        
        parser = MarkdownParser()
        themes = [{"id": "T01", "name": "Theme", "description": "Desc", "codes": []}]
        
        discussion = {
            "sections": [
                {"title": "RQ1: Password Management", "content": "Users adopt tiered strategies...", "type": "rq_answer"},
                {"title": "RQ2: Security Factors", "content": "Financial concerns drive behavior...", "type": "rq_answer"},
            ]
        }
        
        output_path = tmp_path / "03_report.md"
        parser.generate_report(themes, {}, output_path, "Test", discussion)
        
        content = output_path.read_text(encoding="utf-8")
        
        # Verify RQ sections exist
        assert "### RQ1:" in content
        assert "### RQ2:" in content
        
        # Verify content is not empty
        assert "Users adopt tiered strategies" in content
        assert "Financial concerns" in content

    def test_discussion_is_not_empty(self, tmp_path):
        """Discussion section must have substantive content."""
        from llm_ta.parsers.markdown import MarkdownParser
        import re
        
        parser = MarkdownParser()
        themes = [{"id": "T01", "name": "Theme", "description": "Desc", "codes": []}]
        
        discussion = {
            "sections": [
                {"title": "RQ1: Analysis", "content": "Our findings reveal significant patterns in user behavior regarding password management. Users consistently demonstrate a preference for convenience over security in low-stakes situations.", "type": "rq_answer"},
            ]
        }
        
        output_path = tmp_path / "03_report.md"
        parser.generate_report(themes, {}, output_path, "Test", discussion)
        
        content = output_path.read_text(encoding="utf-8")
        
        # Extract discussion section
        discussion_match = re.search(r'## Discussion\s*(.*?)(?=\n---|\Z)', content, re.DOTALL)
        assert discussion_match, "Discussion section not found"
        
        discussion_content = discussion_match.group(1).strip()
        
        # Check minimum length (not empty)
        assert len(discussion_content) > 100, f"Discussion too short: {len(discussion_content)} chars"
        
        # Check for substantive words (not just headers)
        words = discussion_content.split()
        content_words = [w for w in words if not w.startswith('#') and len(w) > 3]
        assert len(content_words) >= 20, "Discussion lacks substantive content"

    def test_validate_real_workspace_report(self):
        """Validate actual workspace report if it exists."""
        workspace_report = Path(__file__).parent.parent / "workspace" / "03_report.md"
        
        if not workspace_report.exists():
            pytest.skip("Workspace report does not exist")
        
        content = workspace_report.read_text(encoding="utf-8")
        
        # Basic structure checks
        assert "## Interview Results" in content, "Missing Results section"
        assert "## Discussion" in content, "Missing Discussion section"
        
        # Evidence checks
        import re
        quote_pattern = r'>\s*"[^"]+"\s*—\s*P\d+'
        matches = re.findall(quote_pattern, content)
        assert len(matches) > 0, "No attributed quotes found in Results"
        
        # Discussion not empty
        discussion_match = re.search(r'## Discussion\s*(.*?)(?=\n---|\Z)', content, re.DOTALL)
        assert discussion_match, "Discussion section not found"
        discussion_content = discussion_match.group(1).strip()
        assert len(discussion_content) > 200, "Discussion section too short"
        
        # Check for RQ references or research question mentions
        has_rq_reference = (
            "RQ" in content or 
            "研究问题" in content or 
            "research question" in content.lower()
        )
        assert has_rq_reference, "Discussion should reference research questions"


# ============================================================================
# Integration Test: Workflow with Real Files (No LLM)
# ============================================================================

class TestWorkflowWithoutLLM:
    """Test workflow steps that don't require LLM calls."""

    def test_init_creates_valid_project_json(self, temp_workspace, example_dir):
        """Project.json should be valid and contain expected fields."""
        os.chdir(temp_workspace)
        
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        
        project_data = json.loads((temp_workspace / "project.json").read_text())
        
        assert "name" in project_data
        assert "research_questions" in project_data
        assert isinstance(project_data["research_questions"], list)
        assert len(project_data["research_questions"]) > 0

    def test_import_preserves_participant_ids(self, temp_workspace, example_dir):
        """Imported interviews should preserve participant IDs."""
        os.chdir(temp_workspace)
        
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        
        interviews = json.loads((temp_workspace / "data" / "interviews.json").read_text())
        
        assert len(interviews) >= 3  # P01, P02, P03 in example
        for interview in interviews:
            assert "participant_id" in interview
            assert interview["participant_id"].startswith("P")

    def test_status_command_shows_project_info(self, temp_workspace, example_dir):
        """llm-ta status should display project status without errors."""
        os.chdir(temp_workspace)
        
        runner.invoke(app, ["init", "--from-md", str(example_dir / "project.md"), "--lang", "en"])
        runner.invoke(app, ["import", str(example_dir / "interviews.json")])
        
        result = runner.invoke(app, ["status"])
        
        assert result.exit_code == 0
        # Should show project name or status info
        assert "密码" in result.output or "password" in result.output.lower() or "项目" in result.output


# ============================================================================
# Run tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

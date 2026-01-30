"""Real end-to-end integration tests using actual LLM calls.

This test suite runs the complete CLI workflow with real LLM API calls.
It requires valid LLM credentials in .env file.

Run with: pytest tests/test_e2e_real.py -v -s
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from dotenv import load_dotenv
from llm_ta.llm.client import LLMClient

# Load .env variables
load_dotenv()

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


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def example_dir():
    """Path to example data directory."""
    return Path(__file__).parent.parent / "example"


@pytest.fixture
def test_workspace(tmp_path):
    """Create a temporary workspace directory for real LLM tests."""
    workspace = tmp_path / "workspace_real"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir()
    yield workspace
    # Return to project root after test
    os.chdir(Path(__file__).parent.parent)


def run_llm_ta(command: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run llm-ta command using local source code."""
    project_root = Path(__file__).parent.parent
    # We don't use capture_output=True here so that results appear in terminal
    # but we still want to return the result for returncode check.
    result = subprocess.run(
        f"python -m llm_ta.cli {command}",
        shell=True,
        cwd=cwd,
        text=True,
        timeout=180,  # 3 minute timeout for LLM calls
        env={**os.environ, "PYTHONPATH": str(project_root)},
    )
    return result


# ============================================================================
# Real LLM Integration Tests
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestRealLLMWorkflow:
    """Test the complete workflow with real LLM API calls.
    
    These tests require:
    - Valid LLM_API_KEY in environment or .env
    - Internet connectivity
    - Run with: pytest -m integration -v -s
    """

    def test_full_pipeline_real_llm(self, test_workspace, example_dir):
        """Run complete pipeline: init → import → coding → consolidate → theming → report."""
        import sys
        import time
        
        def log(msg: str):
            """Print with flush to ensure immediate output."""
            print(msg, flush=True)
        
        os.chdir(test_workspace)
        start_total = time.time()
        
        # Step 1: Init
        log("⏳ Step 1/6: Initializing project...")
        result = run_llm_ta(f"init --from-md {example_dir / 'project.md'} --lang en", test_workspace)
        assert result.returncode == 0, f"Init failed: {result.stderr}"
        assert (test_workspace / "project.json").exists()
        log("✓ Init completed")
        
        # Step 2: Import
        log("⏳ Step 2/6: Importing interviews...")
        result = run_llm_ta(f"import {example_dir / 'interviews.json'}", test_workspace)
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert (test_workspace / "data" / "interviews.json").exists()
        log("✓ Import completed")
        
        # Step 3: Coding (real LLM call)
        log("⏳ Step 3/6: Coding interviews (LLM call, ~30-60s)...")
        start = time.time()
        result = run_llm_ta("coding", test_workspace)
        elapsed = time.time() - start
        assert result.returncode == 0, f"Coding failed: {result.stderr}"
        assert (test_workspace / "data" / "codebook.json").exists()
        assert (test_workspace / "01_coding_draft.md").exists()
        
        codebook = json.loads((test_workspace / "data" / "codebook.json").read_text())
        assert len(codebook) > 0, "Codebook should have codes"
        log(f"✓ Coding completed: {len(codebook)} codes in {elapsed:.1f}s")
        
        # Step 4: Consolidate (real LLM call)
        log("⏳ Step 4/6: Consolidating codes (LLM call, ~20-40s)...")
        start = time.time()
        result = run_llm_ta("consolidate", test_workspace)
        elapsed = time.time() - start
        assert result.returncode == 0, f"Consolidate failed: {result.stderr}"
        assert (test_workspace / "data" / "codebook_consolidated.json").exists()
        assert (test_workspace / "01_consolidated_coding.md").exists()
        
        consolidated = json.loads((test_workspace / "data" / "codebook_consolidated.json").read_text())
        assert len(consolidated) > 0, "Should have consolidated codes"
        log(f"✓ Consolidate completed: {len(consolidated)} merged codes in {elapsed:.1f}s")
        
        # Select all codes for theming
        md_file = test_workspace / "01_consolidated_coding.md"
        content = md_file.read_text()
        content = content.replace("[ ]", "[x]")
        md_file.write_text(content)
        
        # Step 5: Theming (real LLM call)
        log("⏳ Step 5/6: Generating themes (LLM call, ~20-40s)...")
        start = time.time()
        result = run_llm_ta("theming", test_workspace)
        elapsed = time.time() - start
        assert result.returncode == 0, f"Theming failed: {result.stderr}"
        assert (test_workspace / "data" / "themes.json").exists()
        assert (test_workspace / "02_themes_draft.md").exists()
        
        themes = json.loads((test_workspace / "data" / "themes.json").read_text())
        assert len(themes) > 0, "Should have themes"
        log(f"✓ Theming completed: {len(themes)} themes in {elapsed:.1f}s")
        
        # Select all themes for report
        themes_md = test_workspace / "02_themes_draft.md"
        content = themes_md.read_text()
        content = content.replace("[ ]", "[x]")
        themes_md.write_text(content)
        
        # Step 6: Report (real LLM call)
        log("⏳ Step 6/6: Generating report (LLM call, ~30-60s)...")
        start = time.time()
        result = run_llm_ta("report", test_workspace)
        elapsed = time.time() - start
        assert result.returncode == 0, f"Report failed: {result.stderr}"
        assert (test_workspace / "03_report.md").exists()
        
        report_content = (test_workspace / "03_report.md").read_text()
        log(f"✓ Report completed: {len(report_content)} chars in {elapsed:.1f}s")
        
        # Validate report structure
        assert "## Interview Results" in report_content, "Report missing Results section"
        assert "## Discussion" in report_content, "Report missing Discussion section"
        
        # Validate evidence attribution
        import re
        quote_pattern = r'>\s*"[^"]+"\s*—\s*P\d+'
        evidence_matches = re.findall(quote_pattern, report_content)
        assert len(evidence_matches) > 0, "Report should have attributed quotes"
        
        total_time = time.time() - start_total
        log(f"✓ All validation passed: {len(evidence_matches)} attributed quotes")
        log(f"✓ Total pipeline time: {total_time:.1f}s")
        
        # Step 7: LLM-based Quality Scoring
        log("⏳ Step 7/7: Performing LLM-based quality scoring...")
        llm = LLMClient(prompts_file=test_workspace / "prompts.md")
        project_data = json.loads((test_workspace / "project.json").read_text())
        research_questions = project_data.get("research_questions", [])
        
        validation_results = llm.chat_json([
            {"role": "system", "content": "You are a research quality auditor."},
            {"role": "user", "content": REPORT_VALIDATION_PROMPT.format(
                report_content=report_content,
                research_questions="\n".join(f"- {rq}" for rq in research_questions)
            )}
        ])
        
        log(f"📊 LLM Quality Score Results:")
        log(json.dumps(validation_results, indent=2, ensure_ascii=False))
        
        assert validation_results.get("valid") is True, f"LLM determined report is invalid: {validation_results.get('issues')}"
        assert validation_results.get("results_has_quotes") is True
        assert validation_results.get("results_quotes_attributed") is True
        assert validation_results.get("discussion_not_empty") is True
        log("✅ LLM scoring passed!")


# ============================================================================
# Run tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "-m", "integration"])

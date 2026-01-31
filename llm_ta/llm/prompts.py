"""Prompt templates management."""

import json
import re
from pathlib import Path
from typing import Optional


# Default prompts (English output)
DEFAULT_PROMPTS = {
    "coding": {
        "system": "You are an experienced qualitative research analyst skilled in thematic analysis methodology.",
        "user": """You are performing Open Coding on user study interview data.

## Research Questions
{research_questions}

## Interview Content (Participant: {participant_id})
{interview_text}

## Task
Please carefully read the interview content above and extract initial codes relevant to the research questions.

For each code, provide:
1. id: Code ID (format: C001, C002, ...)
2. text: Code label/text (concise summary in English)
3. source_quote: Supporting quote from the original text
4. participant_id: Participant ID

## Output Format
Please output in JSON format:
```json
{{
  "codes": [
    {{
      "id": "C001",
      "text": "Code label in English",
      "source_quote": "Original quote...",
      "participant_id": "{participant_id}"
    }}
  ]
}}
```

Please extract codes comprehensively. Each interview should typically produce 20-40 codes.
"""
    },
    "coding_by_question": {
        "system": "You are an experienced qualitative research analyst skilled in thematic analysis methodology. You conduct thorough, nuanced coding that captures both explicit meanings and underlying patterns.",
        "user": """You are performing Open Coding on user study interview data, analyzing responses to a single question across multiple participants.

## Research Questions
{research_questions}

## Interview Question
{question}

## Participant Responses
{answers}

## Task
Please carefully analyze the responses above and extract initial codes relevant to the research questions.

**IMPORTANT**: Extract 3-5 codes per participant response. Look for:
- Explicit statements and facts
- Underlying attitudes and beliefs
- Behavioral patterns
- Emotional expressions
- Comparisons and contrasts between participants

For each code, provide:
1. id: Code ID (format: C001, C002, ...)
2. text: Code label/text (concise summary in English)
3. source_quote: Supporting quote from the original text
4. participant_id: The participant ID who provided this quote

## Output Format
Please output in JSON format:
```json
{{
  "codes": [
    {{
      "id": "C001",
      "text": "Code label in English",
      "source_quote": "Original quote...",
      "participant_id": "P01"
    }}
  ]
}}
```

Be thorough and extract ALL meaningful codes. For {participant_count} participants, you should generate approximately {expected_codes} codes (3-5 per response).
"""
    },
    "merge_codes": {
        "system": "You are an experienced qualitative research analyst skilled in merging and de-duplicating codes from thematic analysis.",
        "user": """You are MERGING codes from multiple interview questions into a unified codebook.

## Research Questions
{research_questions}

## Codes to Merge ({total_codes} total)
{codes_json}

## Task
Merge these codes by:
1. **Remove exact duplicates**: Combine codes with identical meanings
2. **Merge similar codes**: Combine semantically similar codes, keeping the best quote from each
3. **Preserve unique codes**: Keep distinct codes verbatim

For each merged code, provide:
1. id: Keep one of the original IDs
2. text: The code text (choose the clearest version)
3. source_quote: The most illustrative quote (can combine multiple quotes with "..." separator)
4. participant_id: If merged from multiple, use format "P01, P02, P03"

## Output Format
```json
{{
  "codes": [
    {{
      "id": "C001",
      "text": "Code description",
      "source_quote": "Representative quote...",
      "participant_id": "P01, P02"
    }}
  ]
}}
```

IMPORTANT:
- Preserve code diversity - do NOT over-merge distinct concepts
- Target: reduce by ~30-50% (remove true duplicates only)
- Keep all quotes that provide unique insights
"""
    },
    "theming": {
        "system": "You are an experienced qualitative research analyst skilled in thematic analysis for clustering codes into themes.",
        "user": """You are clustering initial codes into Themes.

## Research Questions
{research_questions}

## Selected Codes
{codes}

## Task
Please cluster the codes above into several themes. Each theme should:
1. Have a clear, descriptive name (in English)
2. Contain related codes
3. Have clear relevance to the research questions

For each theme, provide:
1. id: Theme ID (format: T01, T02, ...)
2. name: Theme name (in English)
3. description: A detailed narrative (1-2 paragraphs) suitable for the "Results" section of the paper. This narrative should:
   - Synthesize the key findings within this theme
   - Explain the patterns observed in the data
   - Set the context for the participant quotes (which will be automatically appended)
   - Do NOT explicitly list quotes or use placeholders like [Quote 1], as the full quotes will be rendered after this text.
   - Be substantial enough to stand alone as a subsection result.
4. code_ids: List of included code IDs

## Output Format
Please output in JSON format:
```json
{{
  "themes": [
    {{
      "id": "T01",
      "name": "Theme Name",
      "description": "This theme reveals that... Participants consistently reported... This suggests that...",
      "code_ids": ["C001", "C003", "C007"]
    }}
  ]
}}
```

Typically produce 5-8 themes. Ensure each code is assigned to a theme.
"""
    },
    "sub_theming": {
        "system": "You are an experienced qualitative research analyst performing hierarchical thematic analysis. You create focused sub-themes that directly address specific research questions.",
        "user": """You are generating SUB-THEMES for a specific research question.

## Target Research Question
{target_rq}

## All Research Questions (for context)
{research_questions}

## Codes Related to This Research Question
{codes}

## Task
Create 3-5 focused sub-themes that directly address the target research question. Each sub-theme should:
1. Capture a distinct aspect of the research question
2. Group semantically related codes
3. Be specific enough to provide actionable insights

For each sub-theme, provide:
1. id: Sub-theme ID (format: {rq_id}.1, {rq_id}.2, ...)
2. name: Sub-theme name (in English)
3. description: 1-2 sentences explaining this sub-theme
4. code_ids: List of included code IDs

## Output Format
```json
{{
  "sub_themes": [
    {{
      "id": "{rq_id}.1",
      "name": "Sub-theme Name",
      "description": "This sub-theme captures...",
      "code_ids": ["C001", "C003"]
    }}
  ]
}}
```

Generate 4-7 sub-themes. Ensure all codes are assigned to exactly one sub-theme.
"""
    },
    "major_theming": {
        "system": "You are an experienced qualitative research analyst synthesizing sub-themes into major overarching themes for an academic paper.",
        "user": """You are synthesizing SUB-THEMES into MAJOR THEMES.

## Research Questions
{research_questions}

## Sub-Themes Grouped by Research Question
{sub_themes_by_rq}

## Task
Create 4 major themes that synthesize the sub-themes above. Each major theme should:
1. Combine related sub-themes across research questions
2. Tell a coherent story about the findings
3. Provide high-level insights suitable for a Results section

For each major theme, provide:
1. id: Theme ID (format: T01, T02, T03, T04)
2. name: Theme name (in English)
3. description: A detailed narrative (2-3 paragraphs) for the Results section that:
   - Synthesizes findings across the included sub-themes
   - Explains patterns and relationships
   - Sets context for participant quotes (which will be automatically appended)
   - Do NOT explicitly list quotes or use placeholders like [Quote 1], as the full quotes will be rendered after this text.
4. sub_theme_ids: List of sub-theme IDs included in this theme

## Output Format
```json
{{
  "themes": [
    {{
      "id": "T01",
      "name": "Major Theme Name",
      "description": "This theme reveals that... The findings indicate...",
      "sub_theme_ids": ["RQ1.1", "RQ1.2", "RQ2.3"]
    }}
  ]
}}
```

Generate 5-7 major themes. Each sub-theme should be assigned to exactly one major theme.
"""
    },
    "insight": {
        "system": "You are an experienced academic writing expert skilled in extracting high-level insights from qualitative research results.",
        "user": """You are extracting high-level insights for the Discussion section of an academic paper.

## Research Questions
{research_questions}

## Thematic Analysis Results
{themes}

## Task
Based on the thematic analysis results above:
1. Summarize key findings
2. Link findings to research questions
3. Extract high-level insights
4. Propose design implications or recommendations

## Output Format
Please output in JSON format:
```json
{{
  "key_findings": [
    {{
      "finding": "Finding description",
      "supporting_themes": ["T01", "T02"],
      "related_rq": "Related research question"
    }}
  ],
  "insights": [
    {{
      "insight": "Insight description",
      "explanation": "Detailed explanation"
    }}
  ],
  "implications": [
    {{
      "implication": "Design implication/recommendation",
      "rationale": "Rationale"
    }}
  ]
}}
```

Ensure each insight is data-supported. Avoid over-interpretation.
"""
    },
    "discussion": {
        "system": "You are an experienced HCI researcher and academic writing expert. You are skilled at writing Discussion sections for CHI/CSCW papers.",
        "user": """You are writing the Discussion section for an academic paper based on the Results section (Themes).

## Study Background
{background}

## Research Questions
{research_questions}

## Results (Themes & Findings)
{themes}

## Task
Write a comprehensive Discussion section that answers the Research Questions.

Structure the discussion as follows:
1. **Answer Research Questions**: For EACH Research Question, create a dedicated subsection.
   - Title: e.g., "RQ1: [Short Title relating to answer]"
   - Content: Summarize relevant key findings from the Results and provide a direct answer/interpretation for this RQ.
2. **(Optional) Other Insights**: Any other important notes.
   (Note: Do not include separate Limitations or Future Work sections unless critical)

## Output Format
Please output in JSON format:
```json
{{
  "sections": [
    {{
      "title": "RQ1: [Short Title]",
      "content": "Full paragraph text answering RQ1...",
      "type": "rq_answer"
    }},
    {{
      "title": "RQ2: [Short Title]",
      "content": "...",
      "type": "rq_answer"
    }}
  ],
  "rq_answers": [
    {{
      "question": "Research question text",
      "answer": "Summary answer based on findings"
    }}
  ]
}}
```
"""
    },
    "consolidate": {
        "system": """
You are a "Codebook Manager" for a qualitative research study. Your job is to clean and consolidate a list of initial coding tags.
""",
        "user": """
Here is a list of raw codes from multiple interviews:
{codes_json}

**Task**:
1. Identify codes that represent the **exact same concept** (e.g., "Forgot Password" vs "Memory failure regarding credentials").
2. Merge them into a single, canonical code with a clear, academic label (in English).
3. Do NOT merge distinct concepts (e.g., "Forgot Password" is different from "Password Rotation Fatigue").
4. Provide a clear definition for the merged code.

**Output Format**:
Please output in JSON format:
```json
{{
  "consolidated_codes": [
    {{
      "id": "C_NEW_01",
      "name": "Cognitive Offloading",
      "description": "Relying on external tools (notes, managers) to remember passwords.",
      "original_code_ids": ["C005", "C023", "C041"]
    }}
  ]
}}
```
Include ALL raw codes in the mapping. If a code is unique and shouldn't be merged, just map it to itself (or a new ID) with its original name.
Everything must be covered.
"""
    }
}


PROMPTS_MD_TEMPLATE = '''# LLM Prompts Configuration

This file contains the prompts used for each analysis stage.
Edit the prompts below to customize LLM behavior.

Available placeholders:
- `{research_questions}` - List of research questions
- `{interview_text}` - Interview content (for coding)
- `{participant_id}` - Participant ID (for coding)
- `{codes}` - Selected codes JSON (for theming)
- `{themes}` - Themes JSON (for insight)

Note that these placehodlers are automatically replaced with the actual values when running the analysis.
Users do not need to fill in these placeholders.

---

## Coding Stage

### System Prompt

```
You are an experienced qualitative research analyst skilled in thematic analysis methodology.
```

### User Prompt

```
You are performing Open Coding on user study interview data.

## Research Questions
{research_questions}

## Interview Content (Participant: {participant_id})
{interview_text}

## Task
Please carefully read the interview content above and extract initial codes relevant to the research questions.

For each code, provide:
1. id: Code ID (format: C001, C002, ...)
2. text: Code label/text (concise summary in English)
3. source_quote: Supporting quote from the original text
4. participant_id: Participant ID

## Output Format
Please output in JSON format:
```json
{{
  "codes": [
    {{
      "id": "C001",
      "text": "Code label in English",
      "source_quote": "Original quote...",
      "participant_id": "{participant_id}"
    }}
  ]
}}
```

Please extract codes comprehensively. Each interview should typically produce 20-40 codes.
```

---

## Consolidate Stage

### System Prompt

```
You are a "Codebook Manager" for a qualitative research study. Your job is to clean and consolidate a list of initial coding tags.
```

### User Prompt

```
Here is a list of raw codes from multiple interviews:
{codes_json}

**Task**:
1. Identify codes that represent the **exact same concept** (e.g., "Forgot Password" vs "Memory failure regarding credentials").
2. Merge them into a single, canonical code with a clear, academic label (in English).
3. Do NOT merge distinct concepts (e.g., "Forgot Password" is different from "Password Rotation Fatigue").
4. Provide a clear definition for the merged code.
5. **CRITICAL**: You MUST include the "original_code_ids" field listing ALL source code IDs that were merged.

## Output Format (STRICT)
Please output in JSON format. Each merged code MUST include the "original_code_ids" array:
```json
{
  "consolidated_codes": [
    {
      "id": "CC_01",
      "name": "Cognitive Offloading",
      "description": "Relying on external tools (notes, managers) to remember passwords.",
      "original_code_ids": ["C005", "C023", "C041"]
    }
  ]
}
```

**IMPORTANT REQUIREMENTS**:
- Every consolidated code MUST have "id", "name", "description", and "original_code_ids" fields
- "original_code_ids" MUST contain at least one ID from the input codes
- If a code is unique and shouldn't be merged, include it with its own ID in original_code_ids
- ALL input codes must be accounted for in the mapping
```

---

## Theming Stage

### System Prompt

```
You are an experienced qualitative research analyst skilled in thematic analysis for clustering codes into themes.
```

### User Prompt

```
You are clustering initial codes into Themes.

## Research Questions
{research_questions}

## Selected Codes
{codes}

## Task
Please cluster the codes above into several themes. Each theme should:
1. Have a clear, descriptive name (in English)
2. Contain related codes
3. Have clear relevance to the research questions

For each theme, provide:
1. id: Theme ID (format: T01, T02, ...)
2. name: Theme name (in English)
3. description: A detailed narrative (1-2 paragraphs) suitable for the "Results" section of the paper. This narrative should:
   - Synthesize the key findings within this theme
   - Explain the patterns observed in the data
   - Set the context for the participant quotes (which will be automatically appended)
   - Do NOT explicitly list quotes or use placeholders like [Quote 1], as the full quotes will be rendered after this text.
4. code_ids: List of included code IDs

## Output Format
Please output in JSON format:
```json
{{
  "themes": [
    {{
      "id": "T01",
      "name": "Theme Name",
      "description": "This theme reveals that... Participants consistently reported... This suggests that...",
      "code_ids": ["C001", "C003", "C007"]
    }}
  ]
}}
```

Typically produce 3-6 themes. Ensure each code is assigned to a theme.
```

---

## Insight Stage

### System Prompt

```
You are an experienced academic writing expert skilled in extracting high-level insights from qualitative research results.
```

### User Prompt

```
You are extracting high-level insights for the Discussion section of an academic paper.

## Research Questions
{research_questions}

## Thematic Analysis Results (Themes)
{themes}

## Task
Based on the thematic analysis results above:
1. Summarize key findings
2. Link findings to research questions
3. Extract high-level insights
4. Propose design implications or recommendations

## Output Format
Please output in JSON format:
```json
{{
  "key_findings": [
    {{
      "finding": "Finding description",
      "supporting_themes": ["T01", "T02"],
      "related_rq": "Related research question"
    }}
  ],
  "insights": [
    {{
      "insight": "Insight description",
      "explanation": "Detailed explanation"
    }}
  ],
  "implications": [
    {{
      "implication": "Design implication/recommendation",
      "rationale": "Rationale"
    }}
  ]
}}
```

Ensure each insight is data-supported. Avoid over-interpretation.
```

---

## Discussion Stage

### System Prompt

```
You are an experienced HCI researcher and academic writing expert. You are skilled at writing Discussion sections for CHI/CSCW papers.
```

### User Prompt

```
You are writing the Discussion section for an academic paper based on the Results section (Themes).

## Study Background
{background}

## Research Questions
{research_questions}

## Results (Themes & Findings)
{themes}

## Raw Data Sample (Context)
{raw_data_context}

## Task
Write a comprehensive Discussion section that answers the Research Questions.

Structure the discussion as follows:
1. **Answer Research Questions**: For EACH Research Question, create a dedicated subsection.
   - Title: e.g., "RQ1: [Short Title relating to answer]"
   - Content: Summarize relevant key findings from the Results and provide a direct answer/interpretation for this RQ.
2. **(Optional) Other Insights**: Any other important notes.
   (Note: Do not include separate Limitations or Future Work sections unless critical)

## Output Format (STRICT)
**CRITICAL**: Each section MUST have a non-empty "title" field. 

Please output in JSON format:
```json
{
  "sections": [
    {
      "title": "RQ1: How Users Manage Passwords",
      "content": "Full paragraph text answering RQ1...",
      "type": "rq_answer"
    },
    {
      "title": "RQ2: Security Perception Factors",
      "content": "...",
      "type": "rq_answer"
    },
    {
      "title": "Emergent Insight: Collaborative Authentication",
      "content": "Other important finding not directly tied to RQs...",
      "type": "insight"
    }
  ],
  "rq_answers": [
    {
      "question": "Research question text",
      "answer": "Summary answer based on findings"
    }
  ]
}
```

**IMPORTANT REQUIREMENTS**:
- Every section MUST have a non-empty "title" field
- Titles should start with "RQ1:", "RQ2:", etc. for research question answers
- Include at least one section for each Research Question
```
'''

class PromptManager:
    """Manage prompts from markdown file or defaults."""
    
    def __init__(self, prompts_file: Path):
        self.prompts_file = prompts_file
        self._prompts: dict = {}
        self._load_prompts()
    
    def _load_prompts(self) -> None:
        """Load prompts from file if it exists, otherwise use defaults."""
        if not self.prompts_file.exists():
            self._prompts = DEFAULT_PROMPTS.copy()
            return
            
        if self.prompts_file.suffix == '.json':
            self._prompts = json.loads(self.prompts_file.read_text(encoding='utf-8'))
        else:
            self._prompts = self._parse_markdown(self.prompts_file.read_text(encoding='utf-8'))
    
    def get_system_prompt(self, stage: str) -> str:
        """Get system prompt for a stage."""
        stage_prompts = self._prompts.get(stage, DEFAULT_PROMPTS.get(stage, {}))
        return stage_prompts.get("system", "")
    
    def get_user_prompt(self, stage: str) -> str:
        """Get user prompt for a stage."""
        stage_prompts = self._prompts.get(stage, DEFAULT_PROMPTS.get(stage, {}))
        return stage_prompts.get("user", "")

    def _parse_markdown(self, content: str) -> dict:
        """Parse markdown prompts file."""
        prompts = {}
        
        # Split by stage headers (## Coding Stage, ## Consolidate Stage, ## Theming Stage, ## Insight Stage, ## Discussion Stage)
        stage_pattern = re.compile(r'^##\s+(Coding|Consolidate|Theming|Insight|Discussion)\s+Stage', re.MULTILINE | re.IGNORECASE)
        
        parts = stage_pattern.split(content)
        
        # parts will be: [intro, "Coding", content, "Theming", content, ...]
        for i in range(1, len(parts), 2):
            stage_name = parts[i].lower()
            stage_content = parts[i + 1] if i + 1 < len(parts) else ""
            
            system_prompt = self._extract_prompt(stage_content, "System Prompt")
            user_prompt = self._extract_prompt(stage_content, "User Prompt")
            
            prompts[stage_name] = {
                "system": system_prompt,
                "user": user_prompt,
            }
        
        # Fill in missing stages with defaults
        for stage in ["coding", "consolidate", "theming", "insight", "discussion"]:
            if stage not in prompts:
                prompts[stage] = DEFAULT_PROMPTS.get(stage, {})
        
        return prompts
    
    def _extract_prompt(self, content: str, header: str) -> str:
        """Extract prompt content from a section."""
        # Find the header and extract the code block after it
        pattern = re.compile(rf'###\s+{re.escape(header)}\s+```\w*\n(.*?)```', re.DOTALL)
        match = pattern.search(content)
        if match:
            return match.group(1).strip()
        return ""

    @staticmethod
    def save_default_prompts(prompts_file: Path) -> None:
        """Save default prompts as markdown for user customization."""
        prompts_file.write_text(PROMPTS_MD_TEMPLATE, encoding="utf-8")

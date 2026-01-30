# LLM Prompts Configuration

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

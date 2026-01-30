# Design Proposal: Iterative & Scalable Thematic Analysis (v2)

This proposal outlines an architectural shift from a "single-pass" workflow to an **iterative, hierarchical process** designed to handle large datasets, minimize code duplication, and ensure high-quality theme synthesis.

## 1. Coding Phase: The "Consolidated Codebook" Model

Currently, coding is done per participant in isolation. To support parallelization and de-duplication:

### A. Stage 1: Fragmented Coding (Parallel)
- **Input**: Individual interview transcripts.
- **Process**: LLM generates codes for each participant independently.
- **Output**: A raw list of `(Participant, Code, Quote)` triplets.

### B. Stage 2: Code Consolidation (New Command: `llm-ta consolidate`)
- **Process**: LLM takes the raw list (or batches if too large) and:
  1. Identifies semantic duplicates (e.g., "Password reuse" vs "Using same password everywhere").
  2. Merges them into a **Unified Codebook**.
  3. Maps multiple `source_quotes` from different participants to the same `CodeID`.
- **Validation**: User reviews the consolidated codebook in a Markdown file to confirm merges.

### C. Stage 3: Thematic Saturation Check
- Use LLM to check if the codebook has "saturated" (no new concepts appearing) after $X$ participants, potentially saving costs on very large studies.

---

## 2. Theming Phase: The "Hierarchical Synthesis" Model

To avoid context window limits and ensure depth:

### A. Round 1: Local Patterning (Clustering)
- Group 10-20 codes into **Sub-themes** (Properties/Dimensions).
- This is much easier for an LLM to manage than 100 codes at once.

### B. Round 2: Overarching Theme Generation
- Take the descriptions of **Sub-themes** (not the raw codes) and cluster them into **Main Themes**.
- This hierarchical jump ensures that the final themes are built on solid, already-synthesized evidence.

### C. Round 3: Verification & Alignment
- LLM performs a "Reflexive Check": Does Theme T01 really fit Quote Q05?
- Generate a "Theme-Code-Quote" traceability matrix.

---

## 3. Human-In-The-Loop (HITL) Interventions

Proposed CLI workflow change:
1. `llm-ta coding` (Per participant)
2. `llm-ta consolidate` (**NEW**: Merge similar codes, creates `codebook_draft.md`)
3. `llm-ta theming` (Hierarchical clustering)
4. `llm-ta report`

## 4. Scalability Strategy: Embedding-Assisted Grouping
For massive datasets (e.g., 50+ interviews / 1000+ codes):
- Use **Embeddings** (e.g., `text-embedding-3-small`) to cluster similar codes/quotes automatically.
- Pass each "Semantic Cluster" to the LLM for high-quality labeling.
- This bypasses the prompt window limit entirely.

---

## Detailed Specification: `llm-ta consolidate`

### 1. Objective
To semantically merge redundant codes generated across multiple interviews into a unified, concise codebook while preserving all evidence (quotes) and participant traceability.

### 2. Data Flow
1.  **Input**: `workspace/data/codebook.json` (Contains all raw codes from `coding` stage, potentially hundreds).
2.  **Process**:
    *   **Embeddings Cluster (Optional for scale)**: If codes > 50, use embeddings to pre-group them into "Semantic Buckets" (e.g., all codes about "Password Managers").
    *   **LLM Merge**: Send each bucket to LLM with the instruction: *"Merge synonyms where the underlying concept is identical. Keep fine-grained distinctions if the nuance is important."*
    *   **Quote Relinking**: When merging `Code A` and `Code B` into `Code C`, the system transfers all `source_quotes` from A and B to C.
3.  **Output**:
    *   `workspace/data/codebook_consolidated.json`: Machine-readable master codebook.
    *   `workspace/01_coding_consolidated.md`: User-facing Review Document.

### 3. Prompt Strategy
**System Prompt**:
> You are a "Codebook Manager" for a qualitative research study. Your job is to clean and consolidate a list of initial coding tags.

**User Prompt**:
> Here is a list of raw codes from multiple interviews:
> {codes_json}
>
> **Task**:
> 1. Identify codes that represent the **exact same concept** (e.g., "Forgot Password" vs "Memory failure regarding credentials").
> 2. Merge them into a single, canonical code with a clear, academic label.
> 3. Do NOT merge distinct concepts (e.g., "Forgot Password" is different from "Password Rotation Fatigue").
> 4. Return a mapping of `Original_Code_ID` -> `New_Canonical_Code_ID`.

### 4. Codebook Migration Logic (Python)
The CLI will execute the merge based on the LLM's mapping:

```python
# Pseudo-code for application logic
for raw_code in raw_codebook:
    target_id = merge_map.get(raw_code.id)
    if not target_id:
         # Code was kept as-is
         continue
    
    target_code = consolidated_codebook.get(target_id)
    # Append quote and participant info to the unified code
    target_code.occurrences.append({
        "participant": raw_code.participant_id,
        "quote": raw_code.source_quote
    })
```

### 5. Review Interface (`01_coding_consolidated.md`)
The markdown will visually group the specific codes that were merged, allowing the user to "undo" a merge by editing the file:

```markdown
### C_FINAL_01: Cognitive Offloading (Merged 3 codes)
**Description**: Relying on external tools or notes to remember passwords.
- [x] Includes:
  - **C005** (P01): "Wrote it on a sticky note"
  - **C023** (P02): "Saved in Notepad"
  - **C041** (P03): "Physical backup paper"

### C_FINAL_02: ...
```

---

## Detailed Specification: `llm-ta theming` (Multi-round)

### 1. Objective
To generate themes using a bottom-up, hierarchical approach that ensures depth and avoids context window limitations.

### 2. Workflow: Round 1 (Sub-Theme Clustering)
*   **Input**: Consolidated Codes (e.g., 50-100 codes).
*   **Process**: Batch codes (e.g., 20 per batch or via semantic similarity). LLM clusters codes into "Sub-Themes" (mid-level categories).
*   **Prompt**:
    > Group these codes into 3-5 sub-themes. For each sub-theme, provide a title and a brief description.
*   **Output**: A list of Sub-Themes (e.g., "ST01: Password Fatigue", "ST02: Insecure Sharing").

### 3. Workflow: Round 2 (Overarching Themes)
*   **Input**: The list of Sub-Themes generated in Round 1.
*   **Process**: LLM synthesizes these sub-themes into "Main Themes".
*   **Prompt**:
    > Synthesize these sub-themes into 3-4 Overarching Themes for the Results section.
    > Each Main Theme must integrate multiple sub-themes and tell a cohesive story.
    > Return `Main Theme -> List[Sub-Themes] -> List[Codes]` hierarchy.
*   **Output**: Final Theme Structure.

### 4. Workflow: Round 3 (Reflexive Audit)
*   **Objective**: Verify that the quotes attached to the codes actually support the generated Main Theme narrative.
*   **Process**: For each Main Theme, fetch the top 3 quotes from its constituent codes and ask LLM:
    > Does this quote support the theme description?
    > If "No", flag for review or remove code from theme.

### 5. Updated `llm-ta theming` Logic
The CLI will default to this new recursive logic:
1. Load `codebook_consolidated.json`.
2. Check code count:
   - If < 30: Use old single-pass logic (Fast path).
   - If > 30: Trigger Multi-round Hierarchical Logic (Deep path).

---

## 5. Implementation Roadmap
- [ ] **Step 1**: Create `ConsolidatedCode` model (supporting list of quotes).
- [ ] **Step 2**: Implement `llm.consolidate_codes` prompt chain.
- [ ] **Step 3**: Implement CLI command `llm-ta consolidate`.
- [ ] **Step 4**: Update `theming` command to read from `codebook_consolidated.json` if it exists.
- [ ] **Step 5**: Implement multi-round theming logic ("Sub-theme" -> "Main Theme").

# LLM-assisted Thematic Analysis Tool

基于 LLM 的主题分析工具，帮助进行 User Study 定性分析。

## 安装与运行

### 方式 1: 安装 (推荐)

在项目根目录下运行：

```bash
pip install -e .
```

之后可以直接使用 `llm-ta` 命令。

### 方式 2: 直接从源码运行

无需安装即可运行：

```bash
# 确保在项目根目录
export PYTHONPATH=$PYTHONPATH:.
python -m llm_ta.cli [command]
```


## 配置

在项目目录下创建 `.env` 文件：

```bash
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
```

## 快速开始

```bash
# 创建工作目录
mkdir workspace && cd workspace

# 从 example 目录的配置初始化
llm-ta init --from-md ../example/project.md --lang en

# 导入访谈数据
llm-ta import ../example/interviews.json

# 生成编码 (编辑 01_coding_draft.md 勾选编码)
llm-ta coding

# 【新增】合并同义编码 (编辑 01_consolidated_coding.md 审查合并)
llm-ta consolidate

# 生成主题 (编辑 02_themes_draft.md 调整主题)
llm-ta theming

# 生成报告 (含 Interview Results 和 Discussion)
llm-ta report
```

## 项目结构

```
workspace/
├── project.json               # 项目配置
├── prompts.md                 # 提示词配置 (可自定义)
├── .env                       # API 配置
├── data/                      # JSON 数据
│   ├── interviews.json
│   ├── codebook.json
│   ├── codebook_consolidated.json  # 合并后的编码本
│   ├── themes.json
│   └── insights.json
├── 01_coding_draft.md         # 编码草稿 (用户编辑)
├── 01_consolidated_coding.md  # 合并后编码 (用户审查)
├── 02_themes_draft.md         # 主题草稿 (用户编辑)
└── 03_report.md               # 最终报告
```

## 命令参考

| 命令 | 功能 |
|------|------|
| `llm-ta init` | 初始化项目 |
| `llm-ta import <file>` | 导入访谈数据 |
| `llm-ta coding` | 生成初始编码 |
| `llm-ta consolidate` | **【新增】** 合并同义编码，减少冗余 |
| `llm-ta theming` | 生成主题分析 (支持合并后的编码) |
| `llm-ta report` | 生成最终报告 (含 Results 和 Discussion) |
| `llm-ta check <file>` | 检查 Markdown 格式 |
| `llm-ta status` | 显示项目状态 |

## 迭代工作流

本工具支持迭代式的主题分析流程：

```
         ┌─────────────────────────────────────────────────────────────┐
         │                    Iterative TA Workflow                    │
         └─────────────────────────────────────────────────────────────┘
                                      │
    ┌──────────────┬──────────────────┼──────────────────┬─────────────┐
    ▼              ▼                  ▼                  ▼             ▼
┌────────┐   ┌───────────┐   ┌──────────────┐   ┌──────────┐   ┌────────┐
│ coding │ → │consolidate│ → │   theming    │ → │  report  │ → │ output │
└────────┘   └───────────┘   └──────────────┘   └──────────┘   └────────┘
    │              │                  │                               │
    ▼              ▼                  ▼                               ▼
Raw Codes    Merged Codes         Themes              Final Report (MD)
 (JSON)        (JSON/MD)           (JSON)           Results + Discussion
```

### Consolidate 阶段说明

`llm-ta consolidate` 命令会：
1. 读取所有原始编码 (`codebook.json`)
2. 使用 LLM 识别语义相似的编码
3. 合并同义编码，生成统一的编码本
4. 保留所有原始证据链 (quotes + participant_id)
5. 输出 `01_consolidated_coding.md` 供用户审查

## 自定义提示词

编辑 `prompts.md` 可自定义 LLM 提示词：

```markdown
## Coding Stage

### System Prompt
```
Your system prompt here...
```

### User Prompt
```
Your user prompt with {research_questions}, {interview_text}...
```
```

支持的阶段：Coding、Consolidate、Theming、Insight、Discussion

## 访谈数据格式

```json
[
  {
    "participant_id": "P01",
    "responses": [
      {"question": "问题1", "answer": "回答..."}
    ]
  }
]
```

## 测试

运行测试套件：

```bash
pip install pytest
python -m pytest tests/ -v
```

## 架构

核心逻辑位于 `llm_ta/analysis/` 模块，已与 CLI 解耦：

- `coding.py`: 编码生成与合并引擎
- `theming.py`: 主题分析引擎
- `reporting.py`: 报告生成引擎

详见 [DESIGN.md](doc/DESIGN.md)

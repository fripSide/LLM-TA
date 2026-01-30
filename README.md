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

# 生成主题 (编辑 02_themes_draft.md 调整主题)
llm-ta theming

# 生成报告 (含 Interview Results 和 Discussion)
llm-ta report
```

## 项目结构

```
workspace/
├── project.json          # 项目配置
├── prompts.md            # 提示词配置 (可自定义)
├── .env                  # API 配置
├── data/                 # JSON 数据
│   ├── interviews.json
│   ├── codebook.json
│   ├── themes.json
│   └── insights.json
├── 01_coding_draft.md    # 编码草稿 (用户编辑)
├── 02_themes_draft.md    # 主题草稿 (用户编辑)
└── 03_report.md          # 最终报告
```

## 命令参考

| 命令 | 功能 |
|------|------|
| `llm-ta init` | 初始化项目 |
| `llm-ta import <file>` | 导入访谈数据 |
| `llm-ta coding` | 生成初始编码 |
| `llm-ta theming` | 生成主题分析 |
| `llm-ta report` | 生成最终报告 (含 Discussion) |
| `llm-ta check <file>` | 检查 Markdown 格式 |
| `llm-ta status` | 显示项目状态 |

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

支持的阶段：Coding、Theming、Report

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

## 架构

详见 [DESIGN.md](doc/DESIGN.md)

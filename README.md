# LLM-assisted Thematic Analysis Tool

基于 LLM 的主题分析工具，帮助进行 User Study 定性分析。

## 主要特性

- **Raw Code Preservation**: 支持直接基于海量原始编码（Raw Codes）生成主题，保留数据的丰富性。
- **Hierarchical Theming**: 支持生成层级化主题（Major Themes -> Sub-themes）。
- **Enhanced Reporting**: 报告生成阶段自动读取原始访谈数据，提供更有深度的讨论（Discussion）。
- **Flexible Workflow**: 支持精简流程直出结果，也支持中间步骤的人工干预。

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

## 快速开始 (精简流程)

这是推荐的高效分析流程：

```bash
# 1. 创建工作目录并初始化
mkdir workspace && cd workspace
llm-ta init --from-md ../example/project.md --lang en

# 2. 导入访谈数据
llm-ta import ../example/interviews.json

# 3. 生成原始编码 (按问题生成)
# 输出: 01_coding_draft.md (建议快速浏览但不必逐个勾选，默认全选)
llm-ta coding --strategy per-question

# 4. 生成层级主题 (使用原始编码)
# 使用 --raw (使用合并前的600多个主题)，或者使用 --consolidated (使用合并后的100多个主题)
# 使用 --hierarchical 生成子主题结构
# 输出: 02_themes_draft.md (建议编辑调整结构)
llm-ta theming --raw --hierarchical

# 5. 生成报告
# 自动读取原始访谈上下文，生成更有深度的 Findings 和 Discussion
# 输出: 03_report.md
llm-ta report
```

### 完整流程 (含语义合并)

如果你需要生成附录用的 Coding Book，可以增加合并步骤：

```bash
# ... (在 Coding 之后) ...

# 【可选】合并同义编码
# 输出: 01_consolidated_coding.md
llm-ta consolidate

# 基于合并后的编码生成主题 (不加 --raw)
llm-ta theming --hierarchical
```

## 项目结构

```
workspace/
├── project.json               # 项目配置
├── prompts.md                 # 提示词配置 (可自定义)
├── .env                       # API 配置
├── data/                      # JSON 数据
│   ├── interviews.json        # 原始访谈数据
│   ├── codes_by_question/     # 按问题分类的原始编码
│   ├── codebook.json          # 汇总编码
│   ├── themes.json            # 主题结构
│   └── insights.json          # 洞察与讨论数据
├── 01_coding_draft.md         # 编码展示
├── 02_themes_draft.md         # 主题草稿 (用户编辑此文件调整主题)
└── 03_report.md               # 最终报告 (Markdown)
```

## 命令参考

| 命令 | 参数示例 | 功能 |
|------|----------|------|
| `llm-ta init` | `--from-md` | 初始化项目 |
| `llm-ta import` | `<file>` | 导入访谈数据 |
| `llm-ta coding` | `--strategy per-question` | 生成初始编码 |
| `llm-ta consolidate` | | **【可选】** 合并同义编码（用于附录） |
| `llm-ta theming` | `--raw --hierarchical` | **【核心】** 生成层级主题 (Sub-themes -> Major Themes) |
| `llm-ta report` | | **【核心】** 生成最终报告 (结合原始访谈数据) |
| `llm-ta check` | `<file>` | 检查 Markdown 格式 |

## 进阶功能

### Hierarchical Theming (层级主题)

使用 `llm-ta theming --hierarchical`：
1. **Sub-themes**: 先针对每个 Research Question 生成子主题。
2. **Major Themes**: 再将子主题聚类为 High-level Major Themes。
3. **Caching**: 支持断点续传（已生成的 RQ 子主题会自动缓存）。

### Enhanced Reporting (深度报告)

`llm-ta report` 命令会自动加载 `data/interviews.json`，并将相关的原始回答（Raw Answers）作为上下文传递给 LLM。这使得生成的 Discussion 部分能够：
- 引用具体的用户原话。
- 提供比单纯基于主题更丰富的数据支持。
- 针对 Research Question 进行直接回应。

## 访谈数据格式

`interviews.json` 示例：

```json
[
  {
    "participant_id": "P01",
    "responses": [
      {"question": "How do you manage passwords?", "answer": "I use a notebook..."}
    ]
  }
]
```

## 测试

```bash
# 测试全部
pytest tests/test_e2e_repro.py

# 通用测试脚本 (指向你的项目路径)
TEST_PROJECT_PATH=/path/to/your/project pytest tests/test_e2e_repro.py -v -s
```
# 需求分析

## 基于LLM的Thematic Analysis工具
开发一个LLM工具帮助写安全领域的User Study论文。  

开发一个基于LLM来做（Using thematic analysis in psychology，V Braun, V Clarke ） User study，人类主导解读与验证，LLM 仅辅助重复性、规模化工作，具体分工如下：

数据熟悉（纯人类）：研究者沉浸数据、建立语境认知；
开放编码（LLM + 人类）：LLM 生成初始编码与代码本，人类审核修正、合并冗余；
初始主题生成（LLM + 人类）：LLM 聚类编码形成候选主题，人类校验主题边界与理论对齐；
主题审核（LLM + 人类）：LLM 辅助合并冗余编码、提示主题问题，人类优化主题结构、确认共识；
报告生成（纯人类）：研究者整合主题与数据、撰写论文。


软件架构如图 [架构图](doc/llm-assisted-ta.png)，

设计思路见文档：[@DESIGN.md](DESIGN.md) 

使用流程：
- 用户先设置研究背景，关键研究问题（Research Questions）
- 用户提交interview问题，和回答的文档（已经清理好， 问题和答案一一对应好了的json格式）
- LLM生成初步codebook，用户调整code
- LLM生成初步主题 (overarching theme)，用户分析调整主题，完成论文的Inteview Results一章的写作
- LLM继续参考一开始的Research Questions，整理主题提炼high level insight，帮助用户完成Disussion章节的写作
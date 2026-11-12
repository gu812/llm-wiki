---
type: source
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/karpathy-llm-wiki.md
tags:
  - 知识管理
  - LLM
  - wiki
---
LLM Wiki 是一份想法说明文件，主张由 LLM 在原始资料与用户之间增量维护一个持久、互相链接的 markdown wiki，用「资料入库时编译一次」取代「每次提问重新检索」的 RAG。

## 要点

### 文档定位（原文「Note」）

- 原文自称是一份「想法文件」（idea file），设计用途是被复制粘贴给自己的 LLM Agent（原文举例 OpenAI Codex、Claude Code、OpenCode / Pi）。
- 有意写得抽象：只传达高层想法，目录结构、schema 约定、页面格式、工具都留给 agent 与用户协作确定。
- 文中所有工具与做法都是可选、可拆分的模块，「挑有用的、忽略没用的」。

### 问题陈述：RAG 不累积（原文「The core idea」）

- 多数人的用法是 RAG：上传一批文件，提问时检索相关片段，再生成答案。
- 它「能用」，但 LLM 每次都在从头重新发现知识。代价具体到这一类问题上：需要综合五份文档才能回答的细微问题，每次都要重新找、重新拼。
- 原文点名 NotebookLM、ChatGPT 文件上传、以及多数 RAG 系统都属于这一类。

### 主张：持久、可复利的 wiki（原文「The core idea」）

- LLM 不只是为日后检索而索引新资料，而是读取、提取关键信息、整合进现有 wiki：更新实体页、修订主题摘要、注明新数据与旧说法在何处矛盾、加强或挑战正在形成的综合。
- 知识「编译一次然后保持最新」，不在每次查询时重新推导。
- 原文对差异的概括：wiki 是持久、复利的产物——交叉引用已经在那，矛盾已经标出，综合已经反映了你读过的全部内容；每加一份资料、每问一个问题，wiki 都更丰富。
- 人几乎不自己写 wiki。人负责取材、探索、提出好问题；LLM 负责摘要、交叉引用、归档、记账这些苦力活。
- 原文的比喻：Obsidian 是 IDE，LLM 是程序员，wiki 是代码库。作者的实际做法是 LLM agent 开一边、Obsidian 开另一边，实时跟链接、看图谱、读更新后的页面（详见 [[Obsidian]]）。

### 适用场景（原文「The core idea」）

- 个人：目标、健康、心理、自我提升，归档日记、文章、播客笔记，逐步建起关于自己的结构化图景。
- 研究：数周到数月深挖一个题目，读论文、文章、报告，逐步建立带演进论点的 wiki。
- 读一本书：按章归档，建人物、主题、情节线索页；原文以 Tolkien Gateway 这类粉丝 wiki 作类比。
- 商业/团队：Slack 线程、会议记录、项目文档、客户通话喂养的内部 wiki，可留人在环审阅。
- 原文还列了竞品分析、尽职调查、旅行规划、课程笔记、爱好深挖。

### 三层架构（原文「Architecture」）

- raw：策展的来源文档，**不可变**，LLM 只读，是事实来源。
- wiki：LLM 生成的 markdown 目录，含摘要、实体页、概念页、对比、overview、综合；LLM 完全拥有这一层，人只读。
- schema：如 Claude Code 的 CLAUDE.md 或 Codex 的 AGENTS.md，规定结构、约定与工作流。原文称其为「关键配置文件」——它让 LLM 成为有纪律的 wiki 维护者而不是通用聊天机器人，并由人与 LLM 长期共同演进（详见 [[Schema 文件]]）。

### 三个操作（原文「Operations」）

- **[[Ingest]]**：读资料 → 与用户讨论关键要点 → 写摘要页 → 更新 index → 更新相关的实体页与概念页 → 追加 log。原文说一份资料可能触及 10-15 个 wiki 页面。作者偏好一次一份、全程参与；也可以批量收录但监督更少。
- **[[Query]]**：LLM 找相关页面、阅读、带引用地综合回答。答案形式可以是 markdown 页、对比表、Marp 幻灯片、matplotlib 图表、canvas。原文强调的关键洞察是：好答案可以存回 wiki 成为新页面——你要求的对比、一份分析、你发现的连接，不该消失在聊天记录里，这样探索也像收录一样复利。
- **[[Lint]]**：定期体检，找页面间的矛盾、被新资料取代的过时说法、无入链的孤立页、被提到却没有独立页的重要概念、缺失的交叉引用、可用网络搜索补上的数据缺口。原文说 LLM 擅长建议新的待查问题和该找的新资料。

### index 与 log（原文「Indexing and logging」）

- index.md 面向内容：wiki 全部内容的目录，每页一行链接、一句话摘要、可选元数据（日期、来源数），按类别组织。每次收录都更新。回答提问时先读 index 找相关页面，再深入。
- 原文判断：这在中等规模（约 100 份资料、数百页面）下效果好得出奇，从而避免了基于 embedding 的 RAG 基础设施。
- log.md 面向时间：只追加，记录收录、提问、体检各发生了什么、何时发生。每条以一致前缀开头（原文例 `## [2026-04-02] ingest | Article Title`）就能用简单 unix 工具解析：`grep "^## \[" log.md | tail -5` 给出最近 5 条。
- log 的作用：给出 wiki 演进的时间线，并帮 LLM 了解最近做了什么。

详见 [[Index 与 Log]]。

### 可选工具（原文「Optional: CLI tools」「Tips and tricks」）

- 搜索：规模小时 index 文件够用，wiki 变大后需要真正的搜索。原文推荐 qmd——本地 markdown 搜索引擎，BM25 与向量混合检索加 LLM 重排，全部在本机，既有 CLI 也有 MCP server；也可以自己写更简单的脚本。
- Obsidian Web Clipper：浏览器扩展，把网文转成 markdown，快速放进 raw。
- 图片本地化：把 Obsidian 附件目录设为固定目录（如 raw/assets/），再在设置→快捷键搜 "Download" 找到 "Download attachments for current file" 绑快捷键。原文说明动机是 LLM 无法一次读带内联图片的 markdown，变通做法是先读文本、再单独看引用的图片。原文标注这些都可选。
- 图谱视图：原文称这是看 wiki 形状的最佳方式——谁连谁、哪些是枢纽、哪些是孤儿。
- Marp（markdown 幻灯片格式，有 Obsidian 插件）、Dataview（在 frontmatter 上跑查询，可把 tags、dates、source counts 变成动态表格）。
- git：wiki 就是一个 markdown 的 git 仓库，白得版本历史、分支、协作。

### 为什么成立（原文「Why this works」）

- 维护知识库最枯燥的不是阅读或思考，是记账：更新交叉引用、让摘要保持最新、记录新数据与旧说法的矛盾、在几十个页面上保持一致。
- 人放弃 wiki 是因为维护负担增长快于价值；LLM 不厌烦、不会忘记更新交叉引用、一次能改 15 个文件。
- 原文的结论句：维护成本接近零，所以 wiki 一直是维护着的。
- 分工：人策展来源、引导分析、提好问题、思考这一切意味着什么；LLM 负责其余全部。
- 思想渊源：与 Vannevar Bush 1945 年的 Memex 精神相通——私人、主动策展的知识库，文档之间的联想路径与文档本身同样有价值；Bush 没解决「谁来做维护」，LLM 解决了这个部分。

## 与已有内容的关系

- **新增**：本仓库收录的第一份资料。此前 `wiki/sources/`、`wiki/entities/`、`wiki/concepts/`、`wiki/analyses/` 均为空，overview 无内容。
- **印证**：无（没有先前页面可比对）。
- **矛盾**：无。

## 涉及页面

- 新建：[[LLM Wiki]]（本页）、[[Andrej Karpathy]]、[[Obsidian]]、[[RAG]]、[[增量编译式知识库]]、[[Schema 文件]]、[[Ingest]]、[[Query]]、[[Lint]]、[[Index 与 Log]]
- 更新：[[overview]]、[[index]]、[[log]]

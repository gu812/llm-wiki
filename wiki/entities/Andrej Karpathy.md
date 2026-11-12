---
type: entity
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/karpathy-llm-wiki.md
tags:
  - 人物
  - LLM
---
Andrej Karpathy 是《LLM Wiki》这份 Gist 的发布者，即「由 LLM 增量维护持久 wiki」这一模式的提出者。

## 与 wiki 的关系

- 本 wiki 收录的 [[LLM Wiki]] 原文出自他的 GitHub Gist：<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>。
- 作者归属的依据是 Gist 地址里的账号名 `karpathy`，**原文正文本身不含署名**。
- 原文「The core idea」以第一人称描述自己的实操：LLM agent 开在一边，[[Obsidian]] 开在另一边，实时跟链接、看图谱、读更新后的页面。

## 立场要点

- 偏好一次收录一份、全程参与，而不是批量灌入（原文「Operations」）。但他也承认批量收录是可行的，只是监督更少。
- 认为 wiki 的价值在于它是持久、复利的产物，而不是聊天式检索（原文「The core idea」，对照 [[RAG]] 与 [[增量编译式知识库]]）。
- 把 schema 当成需要长期共同演进的关键配置，而不是一次性写死的文档（原文「Architecture」，详见 [[Schema 文件]]）。
- 明确声明原文是「想法文件」：所有工具、格式、约定都是可选模块（原文「Note」）。

## 本 wiki 中的其余提及

- 原文「Why this works」把模式的思想渊源接到 Vannevar Bush 1945 年的 Memex，那个人物目前没有独立页面。

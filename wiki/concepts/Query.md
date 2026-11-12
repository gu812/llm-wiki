---
type: concept
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/karpathy-llm-wiki.md
tags:
  - 知识管理
  - 工作流
---
Query（提问）是对 wiki 发问、由 LLM 定位页面并带引用综合回答的操作；原文的关键主张是好的回答要存回 wiki。

## 原文流程（[[LLM Wiki]]「Operations」）

- LLM 检索相关页面、阅读、带引用地综合回答。
- 答案形式随问题而定：markdown 页、对比表、Marp 幻灯片、matplotlib 图表、canvas。
- 定位方式是先读 [[Index 与 Log]] 里的 index，再深入具体页面。

## 关键主张：回答要存回

- 你要求的对比、一份分析、你发现的连接，都有价值，不该消失在聊天记录里。
- 存回之后，探索和收录一样复利——这是「wiki 会变丰富」的第二个来源，第一个来源是 [[Ingest]]。
- 「好不好」由人判断：原文只说「好的回答」可以存回，没给判据，因此本仓库把判断权交给用户。

## 本仓库的落地

- 存回页放在 `wiki/analyses/`；流程见 [AGENTS.md](../../AGENTS.md) 第 5 节，每次提问都会问用户是否存回。

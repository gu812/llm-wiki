---
type: concept
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/karpathy-llm-wiki.md
tags:
  - 知识管理
  - 导航
---
index.md 是按类别组织的内容目录，log.md 是只追加的时间线；两者分工，使中等规模的 wiki 不需要向量检索。

## index.md：面向内容（[[LLM Wiki]]「Indexing and logging」）

- 是 wiki 全部内容的目录：每页一行链接、一句话摘要，可选元数据（日期、来源数），按类别组织。
- 每次收录都要更新。
- 提问时先读 index 找相关页面，再深入具体页面。
- 原文的规模判断：约 100 份资料、数百页面的中等规模下，这个办法效果「好得出奇」，因此避免了基于 embedding 的 [[RAG]] 基础设施。

## log.md：面向时间

- 只追加，记录发生了什么、何时发生：收录、提问、体检。
- 每条以一致前缀开头，就能用简单 unix 工具解析。原文给的例子是 `## [2026-04-02] ingest | Article Title`，配 `grep "^## \[" log.md | tail -5` 取最近 5 条。
- 作用：给出 wiki 演进的时间线，并帮 LLM 了解最近做了什么。

## 两者的分工

- index 回答「这里有什么」，log 回答「最近发生了什么」。原文强调它们服务于不同目的。
- index 每次写入后要保证覆盖所有页面，否则提问时定位不到；[[Lint]] 会检查这一点。

## 本仓库

- 格式见 [AGENTS.md](../../AGENTS.md) 第 3.6、3.7 节；两者都由 `tools/check_links.py` 参与校验。

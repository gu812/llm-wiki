---
type: concept
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/karpathy-llm-wiki.md
tags:
  - 知识管理
  - 工程约定
---
schema 是规定 wiki 结构、页面约定与操作流程的规则文件（Claude Code 的 CLAUDE.md 或 Codex 的 AGENTS.md），原文称其为让 LLM 成为有纪律维护者的关键配置。

## 原文规定（[[LLM Wiki]]「Architecture」）

- 位置：三层架构的第三层，与 raw、wiki 并列。
- 内容：告诉 LLM wiki 如何组织、约定是什么、收录/回答/维护时按什么工作流走。
- 作用：原文称其为「关键配置文件」——它让 LLM 成为有纪律的 wiki 维护者，而不是通用聊天机器人。
- 演进：由人与 LLM 随使用共同演进；原文在「Operations」一节也说，应把自己摸索出的工作流写进 schema，供后续会话沿用。

## 与三个操作的关系

- [[Ingest]]、[[Query]]、[[Lint]] 的具体步骤都写在这里，而不是散落在对话里。
- 它只约束 wiki 层怎么写，不改变原始资料不可变这条边界。

## 本仓库

- schema 正文在仓库根目录 [AGENTS.md](../../AGENTS.md)，`CLAUDE.md` 是指向它的软链接，正文只保留一份。

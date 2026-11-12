---
type: entity
created: 2026-11-12
updated: 2026-11-12
sources:
  - raw/karpathy-llm-wiki.md
tags:
  - 工具
  - markdown
---
Obsidian 是本地 markdown 笔记工具，在 LLM Wiki 模式里担任浏览界面：原文的比喻是「Obsidian 是 IDE，LLM 是程序员，wiki 是代码库」。

## 原文中的角色（[[LLM Wiki]]「The core idea」「Tips and tricks」）

- 实际用法：LLM agent 开一边、Obsidian 开另一边；LLM 按对话改文件，人实时浏览、跟链接、看图谱、读更新后的页面。
- 图谱视图：原文称这是看 wiki 形状的最佳方式——谁连谁、哪些是枢纽、哪些是孤儿。这直接对应 [[Lint]] 要找的孤立页。
- Web Clipper：浏览器扩展，把网文转成 markdown，快速把资料放进 raw 收集区。
- 附件目录：把「文件与链接」里的附件默认路径设成固定目录（如 `raw/assets/`），再在设置→快捷键搜 "Download" 找到 "Download attachments for current file" 绑快捷键，剪藏后一键把图片下载到本地。原文给的动机是 LLM 无法一次读带内联图片的 markdown，变通做法是先读文本、再单独看引用的图片。原文标注这些都可选。
- 插件：Marp（markdown 幻灯片格式，可直接用 wiki 内容做演示）、Dataview（在 frontmatter 上跑查询，可把 tags、dates、source counts 变成动态表格和列表）。

## 在本 wiki 中的位置

- 它是这套模式里唯一被指定为「人看的界面」的组件；wiki 本身只是 markdown 仓库，git 提供版本历史（原文「Tips and tricks」）。
- 本仓库的附件目录已设为 `raw/assets`，配置在 `.obsidian/app.json` 的 `attachmentFolderPath`；目录职责见 [AGENTS.md](../../AGENTS.md) 第 2 节。

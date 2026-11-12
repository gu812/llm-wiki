# llm-wiki

个人知识库，按 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式实例化。

不是「把文档丢给 AI 每次重新检索」，而是让 agent 在收录资料时把知识**编译进持久页面**：新建摘要页、实体页、概念页，更新交叉引用，标出新旧说法之间的矛盾。知识积累一次，之后保持最新，而不是每次提问都重新推导。

## 怎么工作

三层结构：

| 层 | 目录 | 谁负责 |
|---|---|---|
| 原始资料 | `raw/` | 人放进来，**不可变**，agent 只读 |
| 知识库 | `wiki/` | agent 写和维护，人只读 |
| 规则 | `AGENTS.md`（`CLAUDE.md` 软链过来） | 人和 agent 一起演进 |

三个操作，都写在 `AGENTS.md` 里：

- **Ingest 收录**：读资料 → 和用户讨论要点 → 写摘要页 → 更新相关实体页与概念页 → 更新 index → 追加 log。
- **Query 提问**：先读 `wiki/index.md` 定位，再读相关页面，带引用回答。值得留的回答存回 `wiki/analyses/`。
- **Lint 体检**：查矛盾、过时说法、孤立页、缺页的概念、缺失的交叉引用，出报告后再修。

两个特殊文件：

- `wiki/index.md`：按类别组织的内容目录，提问时先读它。约 100 份资料、数百个页面的规模内不需要向量检索。
- `wiki/log.md`：只追加的时间线，`grep "^## \[" wiki/log.md | tail -5` 看最近 5 条。

## 目录

```text
AGENTS.md          schema：结构、页面格式、三个操作的流程
CLAUDE.md          -> AGENTS.md
raw/               原始资料（本仓库不含，见下）
wiki/
  index.md         内容目录
  log.md           时间线
  overview.md      整个 wiki 当前的综合判断
  sources/         每份资料一篇摘要
  entities/        人、组织、产品、工具
  concepts/        方法、理论、术语
  analyses/        存回的提问结果
tools/
  check_links.py   链接、重名、index 覆盖、sources 路径检查
```

## 关于 raw/

**本仓库不包含原始资料。** `raw/` 里放的是第三方文章的全文，转载未经授权，所以 `.gitignore` 把它排除在外，只在本地保留，说明见 [`raw/README.md`](raw/README.md)。

后果是 `wiki/` 页面里指向 `../../raw/xxx.md` 的链接在这里会 404。摘要和引用是自足的，不影响阅读。

## 用法

```bash
git clone https://github.com/gu812/llm-wiki.git
cd llm-wiki
# 把资料放进 raw/，然后让 agent 读 AGENTS.md 开工
```

在 Obsidian 里打开这个文件夹就是一个可视化界面：点 `[[链接]]` 跳转，反向链接面板看谁提到了这一页，图谱视图看整体形状。

## 检查

```bash
python3 tools/check_links.py
```

检查 `[[链接]]` 能否解析、`.md` 是否重名、`wiki/` 页面是否都在 index 里、frontmatter 的 `sources` 路径是否存在，并列出孤立页。只用标准库，不改任何文件。

## 来源

模式由 Andrej Karpathy 在 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 中提出，那份文档本身也收录在本 wiki 里。具体的目录结构、页面格式和流程是按那份文档的说明确定的，没有做个性化改动。

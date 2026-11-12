#!/usr/bin/env python3
"""LLM Wiki 链接检查脚本。

只用 Python 标准库。从仓库根目录运行，不修改任何文件。

检查项（1-4 有任一失败即以非零状态码退出）：
  1. wiki/ 下所有 [[链接]] 都能解析到仓库内存在的文件。
     去掉 |别名 和 #标题 后按文件名匹配。
  2. 仓库内没有重名的 .md 文件。
  3. wiki/ 下除 index.md、log.md 外的每个页面都在 index.md 里出现。
  4. 每个页面 frontmatter 里的 sources 路径都存在。
  5. 孤立页清单：没有任何其他页面链接到它。只输出，不判失败。

退出码：0 通过；1 有失败项；2 无法运行（目录结构不对）。
"""

import re
import sys
from pathlib import Path

WIKI_DIR = "wiki"
# index.md 是自动生成的目录，log.md 是流水账：两者都链向几乎所有页面，
# 计入孤立页判断会让该项永远为空，所以从入链统计里排除。
NOT_ORPHAN_SOURCES = {"index.md", "log.md"}

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
SOURCES_KEY_RE = re.compile(r"^sources:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+)$")


def strip_code(text):
    """去掉围栏代码块和行内代码，避免把示例里的 [[链接]] 当成真实链接。"""
    text = FENCE_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


def collect_files(root):
    """返回仓库内所有文件的相对路径（跳过 .git）。"""
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] == ".git":
            continue
        files.append(rel)
    return files


def build_name_map(files):
    """文件名（含与不含扩展名）到相对路径的映射。"""
    by_stem = {}
    by_name = {}
    for rel in files:
        by_stem.setdefault(rel.stem.casefold(), []).append(rel)
        by_name.setdefault(rel.name.casefold(), []).append(rel)
    return by_stem, by_name


def resolve_link(target, by_stem, by_name):
    """把 [[目标]] 解析成文件列表。按文件名匹配，不看目录。"""
    name = target.split("/")[-1].strip()
    if not name:
        return []
    hits = by_name.get(name.casefold())
    if hits:
        return hits
    if not name.casefold().endswith(".md"):
        hits = by_name.get((name + ".md").casefold())
        if hits:
            return hits
    return by_stem.get(name.casefold(), [])


def parse_frontmatter(text):
    """返回 frontmatter 的行列表；没有 frontmatter 时返回 None。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index]
    return None


def frontmatter_sources(fm_lines):
    """从 frontmatter 抽出 sources 列表。支持块列表与 [a, b] 行内写法。"""
    sources = []
    in_sources = False
    for line in fm_lines:
        match = SOURCES_KEY_RE.match(line)
        if match and line[: len(line) - len(line.lstrip())] == "":
            in_sources = True
            rest = match.group(1).strip()
            if rest.startswith("["):
                inner = rest.strip().strip("[]").strip()
                if inner:
                    sources.extend(
                        item.strip().strip("\"'") for item in inner.split(",") if item.strip()
                    )
                in_sources = False
            continue
        if in_sources:
            item = LIST_ITEM_RE.match(line)
            if item:
                sources.append(item.group(1).strip().strip("\"'"))
                continue
            if line.strip() and not line[0].isspace():
                in_sources = False
    return sources


def main():
    root = Path.cwd()
    if not (root / WIKI_DIR).is_dir() or not (root / "raw").is_dir():
        print(f"错误：当前目录不像仓库根目录（缺少 {WIKI_DIR}/ 或 raw/）：{root}", file=sys.stderr)
        print("请从仓库根目录运行：python3 tools/check_links.py", file=sys.stderr)
        return 2

    files = collect_files(root)
    by_stem, by_name = build_name_map(files)
    failures = []

    wiki_files = [rel for rel in files if rel.parts[0] == WIKI_DIR and rel.suffix.lower() == ".md"]
    wiki_files.sort()

    texts = {}
    for rel in wiki_files:
        texts[rel] = strip_code((root / rel).read_text(encoding="utf-8"))

    print("== LLM Wiki 链接检查 ==")
    print(f"仓库根目录：{root}")
    print(f"wiki 页面数：{len(wiki_files)}")
    print()

    # --- 1. [[链接]] 可解析性 ---
    link_total = 0
    broken = []
    inbound = {}
    for rel, text in texts.items():
        for raw_target in WIKILINK_RE.findall(text):
            target = raw_target.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:  # [[#小节]] 这类同页锚点
                continue
            link_total += 1
            hits = resolve_link(target, by_stem, by_name)
            if not hits:
                broken.append((rel, raw_target, target))
                continue
            for hit in hits:
                if hit == rel:  # 自链接不算入链，否则只链自己的页面不会被报为孤立页
                    continue
                inbound.setdefault(hit, set()).add(rel)
    if broken:
        failures.append("1")
        print(f"[1] [[链接]] 可解析：失败，{len(broken)} 条断链")
        for rel, raw_target, target in broken:
            print(f"    - {rel}：[[{raw_target}]] → 找不到 {target!r}")
    else:
        print(f"[1] [[链接]] 可解析：通过（共 {link_total} 条）")

    # --- 2. .md 重名 ---
    md_by_stem = {}
    for rel in files:
        if rel.suffix.lower() == ".md":
            md_by_stem.setdefault(rel.stem.casefold(), []).append(rel)
    dups = {stem: paths for stem, paths in md_by_stem.items() if len(paths) > 1}
    if dups:
        failures.append("2")
        print(f"[2] .md 文件重名：失败，{len(dups)} 组")
        for stem, paths in sorted(dups.items()):
            joined = "、".join(str(path) for path in paths)
            print(f"    - {stem}：{joined}")
    else:
        print(f"[2] .md 文件重名：通过（{len(md_by_stem)} 个 .md，无重名）")

    # --- 3. index.md 覆盖 ---
    index_rel = Path(WIKI_DIR) / "index.md"
    if index_rel not in texts:
        failures.append("3")
        print(f"[3] index.md 覆盖：失败，找不到 {index_rel}")
        indexed = set()
    else:
        indexed = set()
        for raw_target in WIKILINK_RE.findall(texts[index_rel]):
            target = raw_target.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            for hit in resolve_link(target, by_stem, by_name):
                indexed.add(hit)
        missing = [
            rel
            for rel in wiki_files
            if rel.name not in NOT_ORPHAN_SOURCES and rel not in indexed
        ]
        if missing:
            failures.append("3")
            print(f"[3] index.md 覆盖：失败，{len(missing)} 个页面未出现在 index.md")
            for rel in missing:
                print(f"    - {rel}")
        else:
            print("[3] index.md 覆盖：通过")

    # --- 4. frontmatter sources 路径 ---
    bad_sources = []
    no_frontmatter = []
    for rel in wiki_files:
        if rel.name in NOT_ORPHAN_SOURCES:
            continue
        fm = parse_frontmatter((root / rel).read_text(encoding="utf-8"))
        if fm is None:
            no_frontmatter.append(rel)
            continue
        for src in frontmatter_sources(fm):
            if not (root / src).is_file():
                bad_sources.append((rel, src))
    if bad_sources or no_frontmatter:
        failures.append("4")
        detail = []
        if bad_sources:
            detail.append(f"{len(bad_sources)} 条 sources 路径不存在")
        if no_frontmatter:
            detail.append(f"{len(no_frontmatter)} 个页面缺 frontmatter")
        print(f"[4] frontmatter sources 路径：失败，{'；'.join(detail)}")
        for rel, src in bad_sources:
            print(f"    - {rel}：sources 里的 {src} 不存在")
        for rel in no_frontmatter:
            print(f"    - {rel}：缺 frontmatter")
    else:
        print("[4] frontmatter sources 路径：通过")

    # --- 5. 孤立页（只输出） ---
    orphans = []
    for rel in wiki_files:
        if rel.name in NOT_ORPHAN_SOURCES:
            continue
        sources_of_inbound = {src for src in inbound.get(rel, set()) if src.name not in NOT_ORPHAN_SOURCES}
        if not sources_of_inbound:
            orphans.append(rel)
    print("[5] 孤立页（仅提示，不算失败）")
    if orphans:
        for rel in orphans:
            print(f"    - {rel}（没有 content 页面的入链）")
    else:
        print("    - 无")

    print()
    if failures:
        print(f"结果：失败（检查项 {'、'.join(failures)} 未通过）")
        return 1
    print("结果：通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

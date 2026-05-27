"""
不直接调 MCP（MCP 在 Claude 启动后才在线）。
脚本输出"待 MCP 核查"清单，供 LLM 在 Claude 内逐条 MCP lookup。
"""
import argparse, re, json
from pathlib import Path

STATUTE_RE = re.compile(r"《([^》]+)》(?:第\s*(\d+)\s*条)?")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./citations-check.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    refs = []
    for m in STATUTE_RE.finditer(text):
        refs.append({"law": m.group(1), "article": int(m.group(2)) if m.group(2) else None, "raw": m.group(0)})
    md = "# 引用核查待办\n\n"
    md += "| # | 引用 | 法规 | 条款 | MCP 验证 |\n|---|---|---|---|---|\n"
    for i, r in enumerate(refs, 1):
        md += f"| {i} | {r['raw']} | {r['law']} | {r['article'] or '—'} | TODO mcp__statutes-rag__lookup |\n"
    md += f"\n共 {len(refs)} 处法规引用。LLM 应在 Claude 内逐条调 statutes-rag MCP 验证。\n"
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

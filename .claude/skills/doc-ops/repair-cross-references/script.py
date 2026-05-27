import argparse, re, json
from pathlib import Path

REF_RE = re.compile(r"(本协议|本合同|本条款)?第\s*(\d+(?:\.\d+)?)\s*条")
DEF_RE = re.compile(r"^第\s*(\d+(?:\.\d+)?)\s*条", flags=re.MULTILINE)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./xref-report.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    defined = set(m.group(1) for m in DEF_RE.finditer(text))
    refs = [m.group(2) for m in REF_RE.finditer(text)]
    missing = [r for r in refs if r not in defined]
    md = "# 交叉引用报告\n\n"
    md += f"- 定义的条款：{sorted(defined)}\n"
    md += f"- 引用的条款：{sorted(set(refs))}\n"
    md += f"- ❌ 引用但未定义：{sorted(set(missing))}\n" if missing else "- ✅ 无悬空引用\n"
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

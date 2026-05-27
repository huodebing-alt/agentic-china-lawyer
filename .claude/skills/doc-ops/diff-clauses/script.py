"""
/diff-clauses v1 v2 --clause="第 3 条"
"""
from __future__ import annotations
import argparse, re, difflib
from pathlib import Path

def find_clause(text: str, marker: str) -> str:
    # 提取从 marker 到下一个 "第 X 条" 之前
    pat = re.escape(marker)
    m = re.search(pat + r"[\s\S]*?(?=第\s*\d+(\.\d+)?\s*条|\Z)", text)
    return m.group(0) if m else ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v1"); ap.add_argument("v2"); ap.add_argument("--clause", required=True)
    ap.add_argument("--out", default="./clause.diff.md")
    args = ap.parse_args()
    t1 = Path(args.v1).read_text(encoding="utf-8", errors="ignore")
    t2 = Path(args.v2).read_text(encoding="utf-8", errors="ignore")
    c1, c2 = find_clause(t1, args.clause), find_clause(t2, args.clause)
    if not c1 or not c2:
        print(f"⚠️ 一方未找到条款 {args.clause}"); 
    diff = "\n".join(difflib.unified_diff(c1.splitlines(), c2.splitlines(),
                                          fromfile="v1", tofile="v2", lineterm=""))
    Path(args.out).write_text(f"# {args.clause} 条款对比\n\n```diff\n{diff}\n```\n", encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

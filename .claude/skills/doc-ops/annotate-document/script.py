"""把 LLM 给出的 annotations.json 应用到原文（旁注/脚注）。"""
import argparse, json, re
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--annotations", help="JSON: [{anchor:'第3条', risk:'🔴', note:'...'}, ...]")
    ap.add_argument("--out", default="./annotated.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    if args.annotations and Path(args.annotations).exists():
        notes = json.loads(Path(args.annotations).read_text(encoding="utf-8"))
        for n in notes:
            anchor, risk, note = n["anchor"], n.get("risk", "⚠️"), n.get("note", "")
            text = text.replace(anchor, f"{anchor} {risk} *【批注：{note}】*", 1)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

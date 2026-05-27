import argparse, json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--translations", help="JSON list of strings, same len as paragraphs")
    ap.add_argument("--out", default="./bilingual.md")
    args = ap.parse_args()
    paras = [p.strip() for p in Path(args.doc).read_text(encoding="utf-8", errors="ignore").split("\n\n") if p.strip()]
    trans = json.loads(Path(args.translations).read_text(encoding="utf-8")) if args.translations and Path(args.translations).exists() else ["（待翻译）"] * len(paras)
    md = "| 原文 | 译文 |\n|---|---|\n"
    for src, dst in zip(paras, trans):
        s = src.replace("|", "\\|").replace("\n", "<br>")
        d = dst.replace("|", "\\|").replace("\n", "<br>")
        md += f"| {s} | {d} |\n"
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

import argparse, re
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./toc.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    toc = []
    for m in re.finditer(r"^(#{1,4})\s+(.+)$", text, flags=re.MULTILINE):
        lvl = len(m.group(1)); title = m.group(2).strip()
        toc.append("  " * (lvl-1) + f"- {title}")
    for m in re.finditer(r"^第\s*([一二三四五六七八九十百千万0-9]+)\s*条\s*(.*)$", text, flags=re.MULTILINE):
        toc.append(f"- 第 {m.group(1)} 条 {m.group(2).strip()}")
    Path(args.out).write_text("# 目录\n\n" + "\n".join(toc), encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

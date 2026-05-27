import argparse, re
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--by", default="chapter")
    ap.add_argument("--out", default="./parts")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    Path(args.out).mkdir(parents=True, exist_ok=True)
    if args.by == "chapter":
        parts = re.split(r"(?=^第\s*[一二三四五六七八九十百千万0-9]+\s*章)", text, flags=re.MULTILINE)
    elif args.by == "page":
        parts = re.split(r"\f|\n{4,}", text)
    else:
        parts = re.split(r"\n#{1,3}\s+", text)
    for i, p in enumerate(parts, 1):
        if not p.strip(): continue
        (Path(args.out) / f"part-{i:03d}.md").write_text(p, encoding="utf-8")
    print(f"✓ {len(parts)} parts at {args.out}")

if __name__ == "__main__":
    main()

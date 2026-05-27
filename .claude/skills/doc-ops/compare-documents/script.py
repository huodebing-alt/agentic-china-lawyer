"""
/compare-documents v1 v2 [--out=...] [--format=docx|md|html]

读取 docx / md / txt，输出 diff。
"""
from __future__ import annotations
import argparse, sys, re
from pathlib import Path

def read_text(p: Path) -> str:
    s = p.suffix.lower()
    if s in (".md", ".txt"):
        return p.read_text(encoding="utf-8")
    if s == ".docx":
        try:
            import docx  # python-docx
            d = docx.Document(str(p))
            return "\n".join(para.text for para in d.paragraphs)
        except Exception as e:
            print(f"[warn] cannot read docx {p}: {e}", file=sys.stderr)
            return p.read_bytes().decode("utf-8", errors="ignore")
    return p.read_bytes().decode("utf-8", errors="ignore")

def line_diff(a: str, b: str) -> str:
    import difflib
    al, bl = a.splitlines(), b.splitlines()
    out = []
    for line in difflib.unified_diff(al, bl, fromfile="v1", tofile="v2", lineterm=""):
        out.append(line)
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v1"); ap.add_argument("v2")
    ap.add_argument("--out", default="./out")
    ap.add_argument("--format", choices=["md","docx","html","all"], default="md")
    args = ap.parse_args()
    a = read_text(Path(args.v1)); b = read_text(Path(args.v2))
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    diff = line_diff(a, b)
    (outdir / "diff.md").write_text("# Diff (v1 → v2)\n\n```diff\n" + diff + "\n```\n", encoding="utf-8")
    if args.format in ("html","all"):
        try:
            import difflib
            h = difflib.HtmlDiff(wrapcolumn=80).make_file(a.splitlines(), b.splitlines(), "v1", "v2")
            (outdir / "diff.html").write_text(h, encoding="utf-8")
        except Exception as e:
            print(f"[warn] html diff failed: {e}", file=sys.stderr)
    print(f"✓ diff written to {outdir}")

if __name__ == "__main__":
    main()

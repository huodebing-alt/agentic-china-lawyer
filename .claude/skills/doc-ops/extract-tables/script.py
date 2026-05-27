"""
/extract-tables doc [--out=tables.md]
"""
from __future__ import annotations
import argparse
from pathlib import Path

def from_docx(path: Path):
    try:
        import docx
        d = docx.Document(str(path))
        return [[[c.text for c in row.cells] for row in t.rows] for t in d.tables]
    except Exception:
        return []

def from_pdf(path: Path):
    try:
        import pdfplumber
        with pdfplumber.open(str(path)) as pdf:
            tables = []
            for page in pdf.pages:
                for t in page.extract_tables() or []:
                    tables.append(t)
            return tables
    except Exception:
        return []

def to_md(tables):
    out = []
    for i, t in enumerate(tables, 1):
        out.append(f"## Table {i}")
        if not t: continue
        header = t[0]
        out.append("| " + " | ".join(map(str, header)) + " |")
        out.append("|" + "|".join(["---"] * len(header)) + "|")
        for row in t[1:]:
            out.append("| " + " | ".join(map(str, row)) + " |")
        out.append("")
    return "\n".join(out) or "（未抽到表格）"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./tables.md")
    args = ap.parse_args()
    p = Path(args.doc); ext = p.suffix.lower()
    tables = from_docx(p) if ext == ".docx" else from_pdf(p) if ext == ".pdf" else []
    Path(args.out).write_text(to_md(tables), encoding="utf-8")
    print(f"✓ {args.out} ({len(tables)} tables)")

if __name__ == "__main__":
    main()

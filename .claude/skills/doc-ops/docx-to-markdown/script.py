import argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx"); ap.add_argument("--out", default="./out.md")
    args = ap.parse_args()
    try:
        import mammoth
        with open(args.docx, "rb") as f:
            result = mammoth.convert_to_markdown(f)
        Path(args.out).write_text(result.value, encoding="utf-8")
    except ImportError:
        # fallback: python-docx，逐段落输出 plain
        import docx
        d = docx.Document(args.docx)
        md = []
        for p in d.paragraphs:
            t = (p.text or "").strip()
            if not t: md.append(""); continue
            style = (p.style.name or "").lower()
            if "heading 1" in style: md.append(f"# {t}")
            elif "heading 2" in style: md.append(f"## {t}")
            elif "heading 3" in style: md.append(f"### {t}")
            else: md.append(t)
        Path(args.out).write_text("\n\n".join(md), encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

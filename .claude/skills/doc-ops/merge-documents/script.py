import argparse, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docs", nargs="+")
    ap.add_argument("--out", default="./merged.docx")
    args = ap.parse_args()
    # docx 合并
    if all(d.lower().endswith(".docx") for d in args.docs):
        try:
            from docxcompose.composer import Composer
            from docx import Document
            base = Document(args.docs[0])
            comp = Composer(base)
            for d in args.docs[1:]:
                comp.append(Document(d))
            comp.save(args.out)
            print(f"✓ {args.out}"); return
        except ImportError:
            print("[warn] pip install docxcompose 以获得最佳合并效果", file=sys.stderr)
    # 通用：合并为 markdown
    texts = []
    for d in args.docs:
        texts.append(f"\n\n<!-- 来自 {d} -->\n\n")
        texts.append(Path(d).read_text(encoding="utf-8", errors="ignore"))
    Path(args.out).with_suffix(".md").write_text("".join(texts), encoding="utf-8")
    print(f"✓ {args.out}.md（通用合并）")

if __name__ == "__main__":
    main()

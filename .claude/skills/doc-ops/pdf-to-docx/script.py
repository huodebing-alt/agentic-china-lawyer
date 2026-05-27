import argparse, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--out", default="./out.docx")
    args = ap.parse_args()
    try:
        from pdf2docx import Converter
        cv = Converter(args.pdf); cv.convert(args.out); cv.close()
        print(f"✓ {args.out}")
    except ImportError:
        print("❌ pip install pdf2docx"); sys.exit(2)
    except Exception as e:
        print(f"❌ {e}"); sys.exit(1)

if __name__ == "__main__":
    main()

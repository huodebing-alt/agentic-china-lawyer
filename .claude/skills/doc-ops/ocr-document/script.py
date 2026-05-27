"""
/ocr-document image-or-pdf [--engine=paddleocr|tesseract]
"""
import argparse, sys
from pathlib import Path

def try_paddle(p: Path) -> str:
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        result = ocr.ocr(str(p), cls=True)
        lines = []
        for page in result:
            for box, (text, conf) in page:
                lines.append(f"{text}" + (" ⚠️" if conf < 0.95 else ""))
        return "\n".join(lines)
    except ImportError:
        return ""
    except Exception as e:
        print(f"[paddleocr error] {e}", file=sys.stderr); return ""

def try_tesseract(p: Path) -> str:
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(str(p)), lang="chi_sim+eng")
    except ImportError:
        return ""
    except Exception as e:
        print(f"[tesseract error] {e}", file=sys.stderr); return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--engine", default="paddleocr")
    ap.add_argument("--out", default="./ocr.txt")
    args = ap.parse_args()
    p = Path(args.doc)
    txt = (try_paddle(p) if args.engine == "paddleocr" else try_tesseract(p)) or try_tesseract(p) or try_paddle(p)
    if not txt:
        print("❌ OCR 失败：请确认已安装 paddleocr 或 pytesseract")
        sys.exit(2)
    Path(args.out).write_text(txt, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

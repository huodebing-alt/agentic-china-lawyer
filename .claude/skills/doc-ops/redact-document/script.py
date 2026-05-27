import argparse, re
from pathlib import Path

def redact(text: str, keep_last: int = 4) -> str:
    text = re.sub(r"\b(\d{6})\d{8}(\d{3}[\dXx])\b", lambda m: m.group(1)+"********"+m.group(2), text)
    text = re.sub(r"\b1[3-9]\d{9}\b", lambda m: m.group(0)[:3]+"****"+m.group(0)[-4:], text)
    text = re.sub(r"\b\d{16,19}\b", "[BANK-CARD-REDACTED]", text)
    text = re.sub(r"\b([\w.+-]+)@([\w.-]+\.\w+)\b", lambda m: "***@" + m.group(2), text)
    text = re.sub(r"\b[京津沪渝冀晋辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云陕甘青宁新蒙藏][A-Z][A-Z0-9]{4,5}[A-Z0-9挂学警港澳]\b",
                  lambda m: m.group(0)[0]+"·***", text)
    return text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./redacted.md")
    ap.add_argument("--keep-last", type=int, default=4)
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    Path(args.out).write_text(redact(text, args.keep_last), encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

"""
段首缩进 / 法条引用格式 / 标点规范化。
"""
import argparse, re
from pathlib import Path

def normalize_punct(text: str) -> str:
    # ASCII 引号 → 中文
    text = re.sub(r'"([^"]+)"', r'\1', text).replace("“", "").replace("”", "")
    # 中文 + 数字/英文之间加空格
    text = re.sub(r"([一-龥])([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])([一-龥])", r"\1 \2", text)
    return text

def normalize_statute_refs(text: str) -> str:
    # "民法典第 X 条" → "《中华人民共和国民法典》第 X 条"
    text = re.sub(r"(?<!《)民法典(?!》)\s*第\s*(\d+)\s*条", r"《中华人民共和国民法典》第 \1 条", text)
    text = re.sub(r"(?<!《)公司法(?!》)\s*第\s*(\d+)\s*条", r"《中华人民共和国公司法》第 \1 条", text)
    text = re.sub(r"(?<!《)劳动合同法(?!》)\s*第\s*(\d+)\s*条", r"《中华人民共和国劳动合同法》第 \1 条", text)
    return text

def indent_paragraphs(text: str) -> str:
    lines = []
    for line in text.split("\n"):
        s = line.lstrip()
        if not s or s.startswith(("#", "*", "-", "|", "```", "第", "（", "一、", "二、", "三、", "四、", "五、")):
            lines.append(line)
        else:
            # 段首两个全角空格
            lines.append("　　" + s)
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./formatted.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    text = normalize_punct(text)
    text = normalize_statute_refs(text)
    text = indent_paragraphs(text)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

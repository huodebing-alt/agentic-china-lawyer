"""启发式抽尾部签字块。LLM 后处理。"""
import argparse, re, json
from pathlib import Path

PARTY_RE = re.compile(r"(甲方|乙方|丙方|出借人|借款人|委托人|受托人|出卖人|买受人|出租人|承租人)[（(]?(签字|盖章|公章)?[)）]?[：:]\s*(.+)")
DATE_RE = re.compile(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./signatures.json")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    # 只看末尾 30% 的文本
    tail = text[int(len(text)*0.7):]
    parties = [{"role": m.group(1), "info": m.group(3).strip()} for m in PARTY_RE.finditer(tail)]
    dates = [f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" for m in DATE_RE.finditer(tail)]
    out = {"_note": "启发式抽取，LLM 应精细化", "parties_in_tail": parties, "dates_in_tail": dates}
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

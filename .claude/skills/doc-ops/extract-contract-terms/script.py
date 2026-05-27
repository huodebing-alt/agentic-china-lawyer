"""
/extract-contract-terms doc [--out=terms.json]

读取合同文本，提取候选关键字段（启发式 + 占位），输出 JSON。
LLM 会基于此 stub 做进一步精细抽取。
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

DATE_RE = re.compile(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")
AMT_RE  = re.compile(r"人民币[\s]*([\d,，]+)\s*元")
PARTY_RE= re.compile(r"(甲方|乙方|丙方)[：:]\s*([^\n]+)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./terms.json")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    parties = [{"role": m.group(1), "name": m.group(2).strip()} for m in PARTY_RE.finditer(text)]
    dates = [f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" for m in DATE_RE.finditer(text)]
    amounts = [m.group(1).replace(",", "").replace("，", "") for m in AMT_RE.finditer(text)]
    out = {
        "_schema": "extract-contract-terms@0.1",
        "_note": "本输出为启发式 stub。LLM 应在此基础上做语义抽取。",
        "parties": parties,
        "dates_found": dates,
        "amounts_cny_found": amounts,
        "governing_law": "未抽取" if "适用" not in text else "可能含 '适用 ... 法律' 子句，请 LLM 精确抽取",
        "dispute_resolution": "未抽取" if ("仲裁" not in text and "管辖" not in text) else "含'仲裁'或'管辖'",
    }
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

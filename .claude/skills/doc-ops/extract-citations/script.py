import argparse, re, json
from pathlib import Path

PATTERNS = {
    "statute":   r"《[^》]+》(?:第\s*\d+\s*条)?",
    "case":      r"\(\s*\d{4}\s*\)\s*[^）)]+号",
    "tax_doc":   r"财税\s*[\[【]\s*\d{4}\s*[\]】]\s*\d+\s*号",
    "judicial":  r"法释\s*[\[【]\s*\d{4}\s*[\]】]\s*\d+\s*号",
    "gov_doc":   r"[国发|商务部|工信部|央行][一-龥\w]*\s*[\[【]\s*\d{4}\s*[\]】]\s*\d+\s*号",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./citations.json")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    out = {kind: sorted(set(re.findall(pat, text))) for kind, pat in PATTERNS.items()}
    out["_total"] = sum(len(v) for v in out.values() if isinstance(v, list))
    out["_note"] = "正则启发式抽取。`/check-citations` 会逐条 statutes-rag MCP 验证。"
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {args.out} ({out['_total']} citations)")

if __name__ == "__main__":
    main()

import argparse, re, collections
from pathlib import Path

PARTY_RE = re.compile(r"(甲方|乙方|丙方)[：:]\s*([^\n（）]+)")
AMT_RE = re.compile(r"(人民币|RMB|￥|¥)?\s*([\d,]{1,12})\s*元")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./consistency.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    parties = collections.defaultdict(set)
    for m in PARTY_RE.finditer(text):
        parties[m.group(1)].add(m.group(2).strip())
    amounts = collections.Counter(m.group(2).replace(",", "") for m in AMT_RE.finditer(text))
    md = "# 一致性核查报告\n\n## 当事人名称\n"
    for role, names in parties.items():
        ok = "✅" if len(names) == 1 else "⚠️ 多种写法"
        md += f"- **{role}** {ok}: {sorted(names)}\n"
    md += "\n## 金额（按出现次数）\n"
    for a, c in amounts.most_common(10):
        md += f"- {a} 元 × {c} 次\n"
    md += "\n⚠️ 仅启发式核查，律师必须亲自复核。"
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

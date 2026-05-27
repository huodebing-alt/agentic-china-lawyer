"""脚本仅准备拆段 + glossary 加载。实际翻译由 LLM 完成。"""
import argparse, json
from pathlib import Path

DEFAULT_GLOSSARY = {
  "民法典": "Civil Code",
  "公司法": "Company Law",
  "劳动合同法": "Labor Contract Law",
  "个人信息保护法": "Personal Information Protection Law",
  "反垄断法": "Anti-Monopoly Law",
  "甲方": "Party A", "乙方": "Party B",
  "违约金": "liquidated damages", "管辖": "jurisdiction",
  "仲裁": "arbitration", "适用法律": "governing law",
  "不可抗力": "force majeure", "知识产权": "intellectual property",
  "保密": "confidentiality", "竞业限制": "non-compete",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--target", default="en")
    ap.add_argument("--glossary"); ap.add_argument("--out", default="./translation-prep.md")
    args = ap.parse_args()
    gloss = json.loads(Path(args.glossary).read_text()) if args.glossary and Path(args.glossary).exists() else DEFAULT_GLOSSARY
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    md = f"# 翻译准备 → {args.target}\n\n## Glossary\n\n"
    for k, v in gloss.items(): md += f"- {k} → {v}\n"
    md += f"\n## 段落（共 {len(paras)}）\n\n"
    for i, p in enumerate(paras, 1):
        md += f"### Paragraph {i}\n\n{p}\n\n[ ] 翻译：\n\n"
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"✓ {args.out}（LLM 应在此基础上完成翻译）")

if __name__ == "__main__":
    main()

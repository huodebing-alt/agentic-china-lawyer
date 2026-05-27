import argparse
from pathlib import Path

CHECKS = {
  "管辖 / 仲裁": ["管辖", "仲裁", "诉讼"],
  "通知与送达": ["通知", "送达", "电子邮件"],
  "转让": ["转让", "受让"],
  "修订": ["修订", "变更", "补充协议"],
  "完整协议": ["完整协议", "在先约定"],
  "可分割性": ["可分割", "条款效力", "无效不影响"],
  "不可抗力": ["不可抗力"],
  "知识产权归属": ["知识产权", "著作权", "专利"],
  "保密": ["保密", "secret", "confidential"],
  "期限与终止": ["期限", "终止", "解除"],
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc"); ap.add_argument("--out", default="./boilerplate.md")
    args = ap.parse_args()
    text = Path(args.doc).read_text(encoding="utf-8", errors="ignore")
    md = "# 标准条款完整性审计\n\n| 条款 | 关键词命中 | 状态 |\n|---|---|---|\n"
    for name, kws in CHECKS.items():
        hit = [k for k in kws if k in text]
        status = "✅" if hit else "❌ 建议补充"
        md += f"| {name} | {', '.join(hit) or '—'} | {status} |\n"
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"✓ {args.out}")

if __name__ == "__main__":
    main()

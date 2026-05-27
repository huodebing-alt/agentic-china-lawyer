import argparse
from pathlib import Path

SKELETONS = {
  "memo": "# 备忘录\n\n## 一、事实摘要\n（基于笔记）\n\n## 二、争点\n\n## 三、初步意见\n\n## 四、待补充信息\n",
  "complaint": "# 民事起诉状 — 要点草案\n\n## 原告 / 被告\n## 诉讼请求\n## 事实与理由\n## 证据清单\n## 管辖依据\n",
  "client-letter": "# 致客户函\n\n尊敬的 XX：\n\n（事实背景）\n（法律分析）\n（建议）\n\n顺颂时祺。\n",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notes"); ap.add_argument("--target", default="memo")
    ap.add_argument("--out", default="./draft.md")
    args = ap.parse_args()
    sk = SKELETONS.get(args.target, SKELETONS["memo"])
    notes = Path(args.notes).read_text(encoding="utf-8", errors="ignore")
    out = sk + f"\n---\n\n## 原始笔记（供 LLM 加工）\n\n```\n{notes}\n```\n"
    Path(args.out).write_text(out, encoding="utf-8")
    print(f"✓ {args.out}（骨架已生成，LLM 应填实质内容）")

if __name__ == "__main__":
    main()

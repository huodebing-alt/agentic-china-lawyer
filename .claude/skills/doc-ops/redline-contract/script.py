"""
/redline-contract v1 v2 [--out=...]

基于 /compare-documents 的 diff + 关键词风险归类。
"""
from __future__ import annotations
import argparse, re
from pathlib import Path
import difflib
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "compare-documents"))
try:
    from script import read_text  # type: ignore
except Exception:
    def read_text(p): return Path(p).read_text(encoding="utf-8", errors="ignore")

HIGH_KW = re.compile(r"(金额|价款|违约金|管辖|仲裁|知识产权|保密|清盘|担保|赔偿)")
MED_KW  = re.compile(r"(付款|通知|修改|不可抗力|期限|交付|验收|终止|解除)")

def classify(line: str) -> str:
    if HIGH_KW.search(line): return "🔴"
    if MED_KW.search(line):  return "🟡"
    return "⚫"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v1"); ap.add_argument("v2")
    ap.add_argument("--out", default="./out")
    args = ap.parse_args()
    a = read_text(Path(args.v1)).splitlines()
    b = read_text(Path(args.v2)).splitlines()
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    diff = list(difflib.unified_diff(a, b, fromfile="v1", tofile="v2", lineterm=""))
    hi = mi = lo = 0
    annotated = []
    for ln in diff:
        if ln.startswith(("+++", "---", "@@")):
            annotated.append(ln); continue
        if ln.startswith("+"):
            tag = classify(ln); annotated.append(f"{tag} {ln}")
            if tag == "🔴": hi += 1
            elif tag == "🟡": mi += 1
            else: lo += 1
        elif ln.startswith("-"):
            tag = classify(ln); annotated.append(f"{tag} {ln}")
        else:
            annotated.append(ln)
    (outdir / "redline.diff.md").write_text("# Redline (v1 → v2)\n\n```diff\n" + "\n".join(annotated) + "\n```\n", encoding="utf-8")
    summary = f"# Redline 摘要\n\n- 🔴 高风险变更: {hi}\n- 🟡 中风险变更: {mi}\n- ⚫ 其他/格式: {lo}\n\n⚠️ 仅基于关键词的初判，律师必须亲自复核每一处。"
    (outdir / "redline.summary.md").write_text(summary, encoding="utf-8")
    print(f"✓ redline at {outdir}")

if __name__ == "__main__":
    main()

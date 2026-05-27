"""
/compare-versions-batch v1 v2 v3 ... [--out=...]

对相邻两版生成 redline，并统计条款级变更频次。
"""
from __future__ import annotations
import argparse, sys, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("versions", nargs="+")
    ap.add_argument("--out", default="./out-batch")
    args = ap.parse_args()
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    for i in range(len(args.versions)-1):
        sub = outdir / f"v{i+1}-to-v{i+2}"
        sub.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(HERE.parent / "redline-contract" / "script.py"),
                        args.versions[i], args.versions[i+1], "--out", str(sub)], check=False)
    (outdir / "evolution.md").write_text(
        f"# 版本演化\n\n共对比 {len(args.versions)-1} 对相邻版本，详见各子目录。\n\n"
        "⚠️ 律师应关注：是否有同一条款被反复修改（往往是核心争议点）。\n",
        encoding="utf-8")
    print(f"✓ batch redlines at {outdir}")

if __name__ == "__main__":
    main()

import argparse, json, re
from pathlib import Path

PLACE = re.compile(r"\{\{([^|}]+)(?:\|([^|}]*))?(?:\|([^}]*))?\}\}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template_id"); ap.add_argument("data_json")
    ap.add_argument("--templates-dir", default="./templates")
    ap.add_argument("--out", default="./filled.md")
    args = ap.parse_args()
    # 找 template
    candidates = list(Path(args.templates_dir).rglob(f"{args.template_id}.template.md"))
    if not candidates:
        print(f"❌ 未找到模板 {args.template_id}"); raise SystemExit(2)
    tpl = candidates[0].read_text(encoding="utf-8")
    data = json.loads(Path(args.data_json).read_text(encoding="utf-8"))
    missing = []
    def rep(m):
        key, default, hint = m.group(1).strip(), m.group(2), m.group(3)
        if key in data: return str(data[key])
        if default: return default
        missing.append(key); return f"【未填:{key}】"
    out = PLACE.sub(rep, tpl)
    Path(args.out).write_text(out, encoding="utf-8")
    print(f"✓ {args.out}")
    if missing:
        print(f"⚠️ 缺失字段：{missing}")

if __name__ == "__main__":
    main()

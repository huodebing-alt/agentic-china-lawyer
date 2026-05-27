#!/usr/bin/env bash
# prepare-statutes.sh
#
# 在用户本机运行（不能在沙盒里跑），从官方源下载中国法规原文
# 并落地到 mcp-servers/statutes-rag/statutes/ 下。
#
# 使用：
#   bash scripts/prepare-statutes.sh           # 全部下载
#   bash scripts/prepare-statutes.sh civil_code # 仅下载民法典
#
# 注意：
# - 官方源 URL 可能调整，本脚本只是模板，遇到 404 请到 flk.npc.gov.cn 手工查找最新 URL
# - 不依赖任何付费数据库
# - 下载后自动转换为本项目要求的 markdown 格式
#
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
STATUTES_DIR="$ROOT_DIR/mcp-servers/statutes-rag/statutes"
INDEX_DIR="$ROOT_DIR/mcp-servers/statutes-rag/index"

mkdir -p "$STATUTES_DIR" "$INDEX_DIR"

# 必备工具
need() { command -v "$1" >/dev/null 2>&1 || { echo "请先安装 $1"; exit 1; }; }
need curl
need python3

# 默认全部下载，传参可指定单个
TARGETS=("civil_code" "company_law" "labor_contract_law" "pipl" "data_security_law" "cybersecurity_law" "antitrust_law" "anti_unfair_competition_law" "trademark_law" "patent_law" "copyright_law" "individual_income_tax_law" "enterprise_income_tax_law" "foreign_investment_law" "civil_procedure_law" "arbitration_law" "criminal_law")
if [ $# -gt 0 ]; then
  TARGETS=("$@")
fi

# 官方源映射（用户首次跑后，遇到 404 请到 https://flk.npc.gov.cn/ 手工补 URL，然后重跑）
# 本表 URL 为示意；law id 在全国人大数据库中可能调整
declare -A SRC
SRC[civil_code]="https://flk.npc.gov.cn/api/?type=export&id=ff8080816f3cbb27016f3cd278fa0007"
SRC[company_law]="https://flk.npc.gov.cn/api/?type=export&id=COMPANY_LAW_ID_PLACEHOLDER"
SRC[labor_contract_law]="https://flk.npc.gov.cn/api/?type=export&id=LCL_PLACEHOLDER"
SRC[pipl]="https://flk.npc.gov.cn/api/?type=export&id=PIPL_PLACEHOLDER"
SRC[data_security_law]="https://flk.npc.gov.cn/api/?type=export&id=DSL_PLACEHOLDER"
SRC[cybersecurity_law]="https://flk.npc.gov.cn/api/?type=export&id=CSL_PLACEHOLDER"
SRC[antitrust_law]="https://flk.npc.gov.cn/api/?type=export&id=AML_PLACEHOLDER"
SRC[anti_unfair_competition_law]="https://flk.npc.gov.cn/api/?type=export&id=AUCL_PLACEHOLDER"
SRC[trademark_law]="https://flk.npc.gov.cn/api/?type=export&id=TM_PLACEHOLDER"
SRC[patent_law]="https://flk.npc.gov.cn/api/?type=export&id=PT_PLACEHOLDER"
SRC[copyright_law]="https://flk.npc.gov.cn/api/?type=export&id=CR_PLACEHOLDER"
SRC[individual_income_tax_law]="https://flk.npc.gov.cn/api/?type=export&id=IIT_PLACEHOLDER"
SRC[enterprise_income_tax_law]="https://flk.npc.gov.cn/api/?type=export&id=EIT_PLACEHOLDER"
SRC[foreign_investment_law]="https://flk.npc.gov.cn/api/?type=export&id=FIL_PLACEHOLDER"
SRC[civil_procedure_law]="https://flk.npc.gov.cn/api/?type=export&id=CPL_PLACEHOLDER"
SRC[arbitration_law]="https://flk.npc.gov.cn/api/?type=export&id=ARB_PLACEHOLDER"
SRC[criminal_law]="https://flk.npc.gov.cn/api/?type=export&id=CRIM_PLACEHOLDER"

# 显示名
declare -A NAME
NAME[civil_code]="中华人民共和国民法典"
NAME[company_law]="中华人民共和国公司法"
NAME[labor_contract_law]="中华人民共和国劳动合同法"
NAME[pipl]="中华人民共和国个人信息保护法"
NAME[data_security_law]="中华人民共和国数据安全法"
NAME[cybersecurity_law]="中华人民共和国网络安全法"
NAME[antitrust_law]="中华人民共和国反垄断法"
NAME[anti_unfair_competition_law]="中华人民共和国反不正当竞争法"
NAME[trademark_law]="中华人民共和国商标法"
NAME[patent_law]="中华人民共和国专利法"
NAME[copyright_law]="中华人民共和国著作权法"
NAME[individual_income_tax_law]="中华人民共和国个人所得税法"
NAME[enterprise_income_tax_law]="中华人民共和国企业所得税法"
NAME[foreign_investment_law]="中华人民共和国外商投资法"
NAME[civil_procedure_law]="中华人民共和国民事诉讼法"
NAME[arbitration_law]="中华人民共和国仲裁法"
NAME[criminal_law]="中华人民共和国刑法"

UA="Mozilla/5.0 (compatible; agentic-china-lawyer/0.1; +https://github.com/huodebing-alt/agentic-china-lawyer)"

echo "============================================"
echo "agentic-china-lawyer · 法规库准备脚本"
echo "目标目录：$STATUTES_DIR"
echo "目标法规：${TARGETS[*]}"
echo "============================================"
echo ""
echo "⚠️ 提示："
echo "  - 本脚本会尝试从全国人大官方数据库下载法规原文"
echo "  - 部分 URL 可能需要根据 flk.npc.gov.cn 当前页面手工更新"
echo "  - 下载失败时会保留原 placeholder 文件"
echo "  - 律师在使用法规库前应自行核对最新版本"
echo ""

for t in "${TARGETS[@]}"; do
  url="${SRC[$t]:-}"
  out="$STATUTES_DIR/$t.md"
  name="${NAME[$t]:-$t}"
  if [ -z "$url" ]; then
    echo "[skip] $t — 未配置下载源"
    continue
  fi
  if echo "$url" | grep -q "PLACEHOLDER"; then
    echo "[todo] $t — 请到 https://flk.npc.gov.cn/ 搜索《${name}》后把 id 填入本脚本"
    continue
  fi

  echo "[get ] $t → $url"
  tmp=$(mktemp)
  if curl -fsSL -A "$UA" --max-time 30 "$url" -o "$tmp" 2>/dev/null; then
    # 简易转换：剥离 HTML / 标签，写入 markdown
    python3 - "$tmp" "$out" "$name" "$url" <<'PY'
import sys, re, html
src, dst, name, url = sys.argv[1:5]
text = open(src, "r", encoding="utf-8", errors="ignore").read()
# 粗暴去 tag
text = re.sub(r"<script[\s\S]*?</script>", "", text)
text = re.sub(r"<style[\s\S]*?</style>", "", text)
text = re.sub(r"<[^>]+>", "\n", text)
text = html.unescape(text)
# 把"第N条"前加换行
text = re.sub(r"(?<!\n)(第\s*[一二三四五六七八九十百千万0-9]+\s*条)", r"\n\1", text)
# 把中文条号转阿拉伯（粗糙映射）
cn_to_ar = {"〇":"0","零":"0","一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","十":"10"}
def cn_num(s):
    if s.isdigit(): return s
    # 极简：十X → 1X，X十 → X0，X十Y → XY
    m = re.fullmatch(r"([一二三四五六七八九])?十([一二三四五六七八九])?", s)
    if m:
        a = cn_to_ar.get(m.group(1) or "一","1")
        b = cn_to_ar.get(m.group(2) or "零","0")
        if a == "1" and b == "0": return "10"
        if b == "0" and a != "1": return a + "0"
        if a == "1": return "1" + b
        return a + b
    if all(c in cn_to_ar for c in s):
        return "".join(cn_to_ar[c] for c in s)
    return s
def repl(m):
    raw = m.group(1)
    num = re.sub(r"\s+", "", raw)
    return f"## 第 {cn_num(num)} 条"
text = re.sub(r"第\s*([一二三四五六七八九十百千万0-9]+)\s*条", repl, text)
# 压多余空行
text = re.sub(r"\n{3,}", "\n\n", text)
header = f"# 《{name}》\n\n> 来源：{url}\n> 下载日期：$(date +%Y-%m-%d) — 请律师核对官方最新版本\n\n"
open(dst, "w", encoding="utf-8").write(header + text.strip() + "\n")
print(f"  -> wrote {dst}")
PY
    rm -f "$tmp"
    echo "  ✓ $t saved"
  else
    echo "  ✗ $t 下载失败（HTTP / 网络错误），保留 placeholder"
    rm -f "$tmp"
  fi
done

echo ""
echo "============================================"
echo "完成。下次启动 Claude Code 时，statutes-rag MCP 将使用更新后的法规库。"
echo "如需手工补充，请将官方原文按以下格式写入 $STATUTES_DIR/<name>.md："
echo ""
echo "  # 《XXX 法》"
echo "  ## 第 1 条"
echo "  （条文原文）"
echo "  ## 第 2 条"
echo "  ..."
echo "============================================"

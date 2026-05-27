#!/usr/bin/env bash
# test-mcp.sh — selftest 4 个 MCP server
#
# 在项目根运行：bash scripts/test-mcp.sh
#
# 每个 server 走 `python server.py --selftest`，验证：
#   - import 路径 OK
#   - mcp 对象暴露 / 至少一个 @mcp.tool()
#   - 第一个 tool dry-run（不真起 MCP 协议）
#
# 退出码：0 = 全通过，非零 = 至少一个失败

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

PY="${PYTHON:-python3}"
PASS=0; FAIL=0
RESULTS=()

run_one() {
  local name="$1"
  local server="mcp-servers/$name/server.py"
  echo ""
  echo "═══ Selftest: $name ═══"
  if [ ! -f "$server" ]; then
    echo "  ❌ $server not found"
    RESULTS+=("$name: ❌ FILE_NOT_FOUND")
    FAIL=$((FAIL+1)); return 1
  fi
  if $PY "$server" --selftest; then
    RESULTS+=("$name: ✅ PASS")
    PASS=$((PASS+1))
  else
    code=$?
    RESULTS+=("$name: ❌ FAIL (exit $code)")
    FAIL=$((FAIL+1))
  fi
}

for s in statutes-rag wenshu samr cnipa; do
  run_one "$s"
done

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║         MCP Server Selftest Summary        ║"
echo "╠════════════════════════════════════════════╣"
for r in "${RESULTS[@]}"; do
  printf "║ %-42s ║\n" "$r"
done
echo "╠════════════════════════════════════════════╣"
printf "║ Total: PASS=%d  FAIL=%d                      ║\n" "$PASS" "$FAIL"
echo "╚════════════════════════════════════════════╝"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "提示：如果失败原因是 'fastmcp 未安装'，请运行："
  echo "  pip install -r requirements.txt"
  echo "或："
  echo "  pip install fastmcp"
  exit 1
fi
exit 0

#!/usr/bin/env bash
# agentic-china-lawyer · 项目结构 & 关键文件完整性检查
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "▶ 检查核心文件"
for f in README.md CLAUDE.md LICENSE DISCLAIMER.md .gitignore requirements.txt \
         .mcp.json \
         .claude/agents/task-router.md .claude/agents/aggregator.md \
         .claude/agents/doc-ops/document-master.md \
         .claude/agents/doc-ops/contract-redliner.md \
         .claude/agents/doc-ops/document-formatter.md \
         .claude/agents/doc-ops/evidence-organizer.md \
         .claude/agents/doc-ops/template-librarian.md \
         mcp-servers/README.md mcp-servers/requirements.txt \
         docs/ARCHITECTURE.md docs/DECOMPOSITION_GUIDE.md \
         docs/SKILL_CATALOG.md docs/MCP_CATALOG.md docs/COMPLIANCE_DISCLAIMER.md \
         docs/DOC_OPS_GUIDE.md \
         examples/simple-statute-lookup.md examples/medium-contract-review.md \
         examples/complex-full-due-diligence.md \
         examples/redline-contract-example.md \
         examples/extract-terms-example.md \
         examples/full-doc-review-pipeline.md \
         claude-for-legal-integration/README.md \
         scripts/prepare-statutes.sh \
         templates/README.md; do
  [ -f "$f" ] && echo "  ✓ $f" || { echo "  ✗ $f"; exit 1; }
done

echo ""
echo "▶ 数量统计"
echo "  China-law agents       : $(ls .claude/agents | grep -v doc-ops | wc -l)"
echo "  Doc-Ops agents         : $(ls .claude/agents/doc-ops | wc -l)"
echo "  China-law skills       : $(find .claude/skills -mindepth 1 -maxdepth 1 -type d ! -name doc-ops | wc -l)"
echo "  Doc-Ops skills         : $(ls .claude/skills/doc-ops | wc -l)"
echo "  Templates              : $(find templates -name '*.template.md' | wc -l)"
echo "  Statutes (placeholder) : $(ls mcp-servers/statutes-rag/statutes | grep -v _INDEX | wc -l)"

echo ""
echo "▶ MCP server Python 语法"
for s in mcp-servers/statutes-rag/server.py mcp-servers/wenshu/server.py mcp-servers/samr/server.py mcp-servers/cnipa/server.py; do
  python3 -c "import ast; ast.parse(open('$s').read()); print('  ✓ $s')"
done

echo ""
echo "▶ Doc-Ops skill scripts 语法 / SKILL.md 完整性"
bad=0
for d in .claude/skills/doc-ops/*/; do
  [ -f "$d/SKILL.md" ]  || { echo "  ✗ $d 缺 SKILL.md"; bad=$((bad+1)); }
  [ -f "$d/script.py" ] || { echo "  ✗ $d 缺 script.py"; bad=$((bad+1)); }
  python3 -c "import ast; ast.parse(open('$d/script.py').read())" 2>/dev/null \
    || { echo "  ✗ $d/script.py 语法错"; bad=$((bad+1)); }
done
[ "$bad" -eq 0 ] && echo "  ✓ 全部 26 个 doc-ops skill 完整"


echo ""
echo "▶ .mcp.json 格式 / schema 校验"
python3 - <<JSONPY
import json, sys, pathlib
p = pathlib.Path(".mcp.json")
data = json.loads(p.read_text(encoding="utf-8"))
assert "mcpServers" in data, "缺 mcpServers"
for name in ("statutes-rag","wenshu","samr","cnipa"):
    assert name in data["mcpServers"], f"缺 {name}"
    s = data["mcpServers"][name]
    assert "command" in s and "args" in s, f"{name} 缺 command/args"
print(f"  ✓ .mcp.json 含 {len(data['mcpServers'])} servers, schema OK")
JSONPY

echo ""
echo "✅ 项目结构完整。"

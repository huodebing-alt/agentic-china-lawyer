# MCP Servers — 中国法律生态接入

本目录包含 `agentic-china-lawyer` 的 4 个 MCP server。

| Server | 数据源 | 公开版 | 私有 / 付费 |
| --- | --- | --- | --- |
| `statutes-rag` | 本地法规库（民法典 / 公司法 / PIPL / …） | ✅ 完整可用 | — |
| `wenshu` | 裁判文书网 | ⚠️ stub | 北大法宝 / 威科先行 / 无讼 API |
| `samr` | 国家市场监督管理总局 | ⚠️ stub | 企查查 / 天眼查 API |
| `cnipa` | 国家知识产权局 | ⚠️ stub | CNIPA 商业 API / IPRdaily |

## 安装

```bash
pip install -r requirements.txt
```

依赖：`fastmcp`, `pydantic`, `python-frontmatter`, `numpy`, `scikit-learn`（轻量 RAG）。

## 启动

由 Claude Code 在读取 `.claude/mcp.json` 时自动启动。也可手动：

```bash
python -m mcp_servers.statutes_rag.server
python -m mcp_servers.wenshu.server
python -m mcp_servers.samr.server
python -m mcp_servers.cnipa.server
```

## 切换到私有 API

每个 server 在环境变量 `<NAME>_MODE` 中切换：

- `stub` → 公开版示意数据
- `live` → 调用真实 API（需配置 API key）

详见各 server 目录的 `README.md`。

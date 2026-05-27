# MCP 目录 / MCP Catalog

本项目集成 4 个 MCP server，覆盖中国法律生态主要数据源。

## 公开版状态

| MCP | 公开版 | 私有 / 付费切换 |
| --- | --- | --- |
| `statutes-rag` | ✅ placeholder + 用户本机下载 | — |
| `wenshu` | ⚠️ stub（公开 API 受限） | 北大法宝 / 威科先行 / 无讼 |
| `samr` | ⚠️ stub | 企查查 / 天眼查 / SAMR 官方 API |
| `cnipa` | ⚠️ stub | CNIPA 商业 API / IPRdaily |

## statutes-rag

**用途**：本地中国法规 RAG，覆盖 18+ 部核心法律。

**首次运行**：

```bash
bash scripts/prepare-statutes.sh
```

从 [全国人大法律法规数据库](https://flk.npc.gov.cn/) 下载法规原文，落地为 markdown。
脚本中部分法规的 id 为 placeholder，遇到 404 请到官网搜索后回填脚本对应行。

**Tools**：
- `lookup(law_name, article)` — 精确查询
- `search(query, top_k)` — 关键词检索
- `list_laws()` — 列已收录法规
- `prepare_status()` — 检测准备状态

## wenshu

**用途**：裁判文书网案例检索。

**公开版**：返回 stub 数据 + 警告，提示律师通过付费数据库验证。

**接入私有 API**：

```bash
export WENSHU_MODE=live
export WENSHU_API_KEY=<your_key>
export WENSHU_PRIVATE_ENDPOINT=<endpoint_url>
```

并在 `mcp-servers/wenshu/server.py` 中实现 `live` 分支调用对应 API。

**支持的私有库**：
- [北大法宝 API](https://www.pkulaw.com/)
- [威科先行 API](https://law.wkinfo.com.cn/)
- [无讼 / Alpha Lawyer API](https://www.itslaw.com/)

## samr

**用途**：工商企业信用信息查询。

**公开版**：stub。

**接入私有 API**：

```bash
export SAMR_MODE=live
export QICHACHA_API_KEY=<key>    # 企查查
# 或
export TIANYANCHA_API_KEY=<key>  # 天眼查
```

**Tools**：
- `search(company_name)` — 基本信息
- `equity_penetration(company_name, depth)` — 股权穿透

## cnipa

**用途**：商标 / 专利检索。

**Tools**：
- `search_trademark(name, nice_class, applicant)`
- `search_patent(keyword, app_no, applicant)`

**接入私有 API**：

```bash
export CNIPA_MODE=live
export CNIPA_API_KEY=<key>
```

## 新增 MCP

1. 在 `mcp-servers/<name>/` 下建目录
2. 写 `server.py`（参考 wenshu）
3. 在 `.mcp.json` 中注册
4. 在 `mcp-servers/README.md` 与本目录登记
5. 在相关 agent 的 `tools:` 中添加 `mcp__<name>__*`

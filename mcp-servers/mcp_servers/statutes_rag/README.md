# statutes-rag — 本地中国法规 RAG

实际代码在 `mcp-servers/mcp_servers/statutes_rag/server.py`。
本目录存放：

- `statutes/` — 法规 markdown 文本
- `index/` — RAG 索引（首次运行自动生成）

## 法规格式约定

每个法规一个 `.md` 文件，结构：

```
# 《中华人民共和国民法典》

## 第 1 条 ……

## 第 2 条 ……
```

`server.py` 通过正则 `## 第 N 条` 拆条。

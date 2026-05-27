---
name: check-citations
description: 法规引用核对。每条 "《XX 法》第 N 条" 通过 statutes-rag MCP 验证存在 + 文本一致。
trigger_phrases: ["核对引用", "check citation"]
---

# /check-citations

## 调用
```
/check-citations <doc> [--out=citations-check.md]
```

## 工作
1. `/extract-citations` 抽出所有引用
2. 对法规类逐条调 `mcp__statutes-rag__lookup`
3. 不一致 / 不存在的标 ❌；公开 stub 时标 ⚠️

## 输出
按 `citation-checker` agent 模板。

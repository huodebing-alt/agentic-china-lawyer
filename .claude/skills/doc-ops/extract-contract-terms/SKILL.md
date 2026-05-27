---
name: extract-contract-terms
description: 关键条款抽取为 JSON：金额 / 期限 / 违约金 / 担保 / 管辖 / 仲裁 / 通知 / 签字方 等。
trigger_phrases: ["抽取条款", "提取关键信息", "extract terms"]
---

# /extract-contract-terms

## 调用
```
/extract-contract-terms <doc> [--out=terms.json]
```

## 字段
```json
{
  "title": "...",
  "parties": [{"name":"...","role":"甲方","entity_type":"公司|自然人","id":"..."}],
  "execution_date": "YYYY-MM-DD",
  "effective_date": "...",
  "term": {"start":"...","end":"...","auto_renewal":false},
  "consideration": {"amount_cny":1000000, "currency":"CNY", "payment_schedule":[...]},
  "key_obligations": ["...","..."],
  "warranties": ["..."],
  "liability_cap": {"amount":"...","exceptions":[...]},
  "penalty_clauses": [{"trigger":"...","amount":"...","cap":"..."}],
  "ip_ownership": "...",
  "confidentiality_term": "...",
  "non_compete": {...},
  "governing_law": "...",
  "dispute_resolution": {"mode":"仲裁|诉讼","forum":"...","seat":"...","language":"..."},
  "notice_address": [...],
  "signatures": [{"party":"...","representative":"...","date":"..."}]
}
```

## 路由
`document-master` → LLM 抽取（带 schema 约束）+ `script.py` 后处理校验

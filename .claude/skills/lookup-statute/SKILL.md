---
name: lookup-statute
description: 中国法规条款检索（本地 RAG）。覆盖民法典、公司法、劳动合同法、PIPL、反垄断法等核心法律。
trigger_phrases:
  - "查法规"
  - "查条款"
  - "民法典"
  - "公司法第"
  - "lookup"
---

# /lookup-statute

## 调用

```
/lookup-statute <法规名> [条款号] [--related]
```

例子：

```
/lookup-statute 民法典 1062
/lookup-statute 公司法 --related   # 查公司法 + 配套司法解释
```

## 路由

`research-specialist-statute`

## 输出

```
# 《XXX 法》第 X 条

## 原文
（statutes-rag MCP 返回的原文）

## 立法变迁
（2018 → 2023 修订对比，如有）

## 相关条款
- 第 Y 条、第 Z 条

## 司法解释
- 法释 [YYYY] X 号，第 X 条

## 学理通说（简）
```

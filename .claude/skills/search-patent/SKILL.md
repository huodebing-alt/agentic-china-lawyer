---
name: search-patent
description: 专利检索（发明 / 实用新型 / 外观）。
trigger_phrases: ["专利查询", "search-patent"]
---

# /search-patent

## 输入
- 关键词 / 申请号 / 公开号 / 申请人 / 发明人

## 路由
`ip-specialist` → `mcp__cnipa__search_patent`

## 输出
- 申请号 / 公开号 / 授权公告号
- 申请日 / 公开日 / 授权日
- 法律状态、年费缴纳
- 权利要求摘录

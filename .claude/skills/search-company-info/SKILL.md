---
name: search-company-info
description: 工商企业信息查询（SAMR / 企查查 / 天眼查接入）。
trigger_phrases: ["工商查询", "企业信息", "统一社会信用代码"]
---

# /search-company-info

## 输入
- 公司全称 或 统一社会信用代码

## 路由
`corporate-specialist` → `mcp__samr__search`

## 输出
- 工商基本信息（名称 / 法定代表人 / 注册资本 / 实缴 / 成立日期 / 经营状态）
- 股东信息 + 股权穿透（≤3 层）
- 经营范围
- 行政处罚 / 经营异常 / 严重违法失信
- 对外投资
- 知识产权
- 司法案件（关联诉讼）
- ⚠️ 公开 stub 注明

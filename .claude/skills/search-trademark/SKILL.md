---
name: search-trademark
description: 商标检索（通过 cnipa MCP）。商标名 / 申请人 / 类别 多维查询。
trigger_phrases: ["商标查询", "商标检索", "search-trademark"]
---

# /search-trademark

## 输入
- 商标名称（中 / 英 / 图形描述）
- 尼斯分类号
- 申请人（可选）

## 路由
`ip-specialist` → 调 `mcp__cnipa__search_trademark`

## 输出
- 申请号 / 注册号
- 申请日 / 注册日 / 续展日
- 商品 / 服务范围
- 法律状态（在审 / 注册 / 无效 / 撤销）
- ⚠️ 公开 stub 注明

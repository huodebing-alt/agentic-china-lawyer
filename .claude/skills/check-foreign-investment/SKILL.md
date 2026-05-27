---
name: check-foreign-investment
description: 外商投资准入查询（负面清单 + 鼓励目录）。
trigger_phrases: ["外商投资", "负面清单", "FDI"]
---

# /check-foreign-investment

## 输入
- 行业 / 业务描述
- 自贸区？海南自由贸易港？
- 投资金额 / 持股比例

## 路由
`foreign-investment-specialist`

## 输出
- 是否在负面清单
- 限制 / 禁止具体条款
- 是否需要前置审批
- 鼓励目录 / 优惠
- 国家安全审查 / 反垄断申报评估

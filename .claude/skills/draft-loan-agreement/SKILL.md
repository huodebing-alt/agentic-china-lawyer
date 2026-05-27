---
name: draft-loan-agreement
description: 起草借款合同（自然人 / 企业 / 民间 / 关联）。
trigger_phrases: ["借款合同", "借条", "贷款合同"]
---

# /draft-loan-agreement

## 反问
1. 出借人 / 借款人
2. 借款金额 / 币种 / 用途
3. 期限 / 还款方式
4. 利率（民间借贷 LPR × 4 上限）
5. 担保（保证 / 抵押 / 质押）
6. 违约责任

## 路由
`contract-specialist`

## 红线
- 民间借贷利率超 LPR × 4 部分不予保护（注意法定上限可能调整）
- 企业之间借款合法但需符合一定条件
- 砍头息 / 复利计入本金 一律纠正

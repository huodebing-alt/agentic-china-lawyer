---
name: draft-employment-contract
description: 起草劳动合同（固定期限 / 无固定期限 / 以完成一定工作任务为期限）。
trigger_phrases: ["劳动合同", "雇佣合同"]
---

# /draft-employment-contract

## 输入
- 公司 / 员工信息
- 岗位 / 工作地点
- 合同类型
- 试用期（按劳动合同法严格上限）
- 工资 / 奖金 / 股权激励
- 工时制度（标准 / 综合 / 不定时 — 需当地审批）
- 保密 / 竞业限制

## 路由
`labor-specialist` → `drafting-stylist`

## 红线
- 试用期：1 年以下合同 ≤1 个月、1-3 年 ≤2 个月、3 年以上或无固定 ≤6 个月
- 试用期工资 ≥ 转正工资 80% 且 ≥ 当地最低工资
- 综合 / 不定时工时必须经劳动行政部门批准

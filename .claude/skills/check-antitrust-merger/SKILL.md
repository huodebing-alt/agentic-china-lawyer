---
name: check-antitrust-merger
description: 经营者集中申报评估。判断是否达到申报门槛、走简易 / 普通程序。
trigger_phrases: ["经营者集中", "反垄断申报", "MOFCOM"]
---

# /check-antitrust-merger

## 输入
- 交易双方上一会计年度营业额（全球 / 中国境内）
- 交易结构（股权 / 资产 / 合营企业）
- 行业
- 市场份额估算

## 路由
`antitrust-specialist`

## 输出
- 申报门槛判断（境内合计 ≥4 亿 + 全球 ≥100 亿 或 中国境内 ≥20 亿 等）
- 简易 vs 普通程序
- 申报时点（控制权变更前）
- 申报材料 checklist
- 时限预估

---
name: check-labor
description: 劳动用工合规审查。劳动合同 / 解除 / 经济补偿金 / 社保 / 加班 / 竞业限制。
trigger_phrases:
  - "劳动合规"
  - "辞退"
  - "经济补偿"
  - "check-labor"
---

# /check-labor

## 输入

- 场景（招 / 用 / 留 / 离 / 派遣）
- 城市
- 当事人月工资
- 工作年限

## 路由

`labor-specialist`

## 输出

合规分析 + 经济补偿金测算 + 法律风险 + 程序建议。

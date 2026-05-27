---
name: calculate-inheritance
description: 继承财产分配测算（法定 / 遗嘱 / 遗赠扶养）。中国大陆目前未开征遗产税；涉外可能涉及。
trigger_phrases: ["继承", "遗产", "calculate-inheritance"]
---

# /calculate-inheritance

## 输入
- 被继承人信息（死亡日期 / 户籍 / 国籍）
- 遗产清单
- 法定继承人范围 / 是否有遗嘱
- 是否涉外

## 路由
`family-specialist` + `tax-specialist`

## 输出
- 法定继承顺序与份额
- 遗嘱效力判断
- 应纳税费（继承本身不征个税，但后续处置可能涉及）
- 房产过户 / 股权过户路径
- 涉外提醒（部分国家征遗产税）

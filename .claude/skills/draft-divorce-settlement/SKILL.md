---
name: draft-divorce-settlement
description: 离婚协议起草（协议离婚）。财产分割 + 子女抚养 + 探视 + 一方补偿。
trigger_phrases: ["离婚协议", "协议离婚"]
---

# /draft-divorce-settlement

## 反问
1. 双方信息
2. 婚龄、子女信息
3. 共同财产清单
4. 共同债务
5. 子女抚养（直接抚养方 / 抚养费 / 探视）
6. 一方补偿（家务补偿 / 经济补偿）
7. 离婚冷静期（30 日）

## 路由
`family-specialist` → `tax-specialist`（涉房产过户 / 股权转让税务）→ `drafting-stylist`

## 输出
标准离婚协议书 + 附财产清单 + 附子女抚养附件。

## 红线
- 必带 30 日冷静期提示
- 不得约定剥夺探视权
- 房产 / 股权过户的税务后果必须提示

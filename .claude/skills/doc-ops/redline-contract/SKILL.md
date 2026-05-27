---
name: redline-contract
description: 合同两版 redline 按风险等级标注（红=高/黄=中/绿=新增/蓝=删除/灰=无实质）。
trigger_phrases: ["redline", "合同对比", "合同 redline"]
---

# /redline-contract

## 调用
```
/redline-contract <v1> <v2> [--out=<dir>]
```

## 路由
`contract-redliner` → `script.py` + LLM 二次判断风险等级

## 输出
- `redline.diff.md` 带风险标色的 markdown
- `redline.summary.md` 高/中/低/利己/不利己 变更摘要
- `redline.docx` 带 track-changes（如生成）

## 风险关键词
- 🔴 金额 / 价款 / 违约金 / 管辖 / 仲裁 / IP / 保密
- 🟡 付款节点 / 通知 / 修改 / 不可抗力 / 期限
- 🟢 新增对己方有利条款

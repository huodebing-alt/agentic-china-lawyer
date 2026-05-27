---
name: review-contract-cn
description: 中文合同全面审查，输出 redline + 风险清单 + 修改建议。重点关注违约责任 / 管辖 / 仲裁 / 不可抗力 / IP / 数据。
trigger_phrases:
  - "审合同"
  - "合同审查"
  - "review-contract"
---

# /review-contract-cn

## 调用

```
/review-contract-cn <合同文件路径或粘贴文本>
```

## 路由

复杂度 Medium：`contract-specialist` + 视合同类型并行（涉及股权→ +corporate；涉及劳动→ +labor；涉及数据→ +data-protection；涉及税务→ +tax）

## 输出

见 `aggregator` 模板中"合同审查意见"。

## checklist

见 `.claude/agents/contract-specialist.md`。

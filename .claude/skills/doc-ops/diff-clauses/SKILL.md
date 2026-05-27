---
name: diff-clauses
description: 精确到单个条款的差异分析。
trigger_phrases: ["条款对比", "diff clause"]
---

# /diff-clauses

## 调用
```
/diff-clauses <v1> <v2> --clause="第 X 条"
```

## 工作
1. 按"第 X 条 / 第 X.Y 条"在两版中定位
2. 输出该条款的逐字 diff + LLM 解读

## 输出
- `clause.diff.md`

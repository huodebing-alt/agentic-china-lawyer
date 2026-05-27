---
name: extract-signatures
description: 抽取合同尾部签字盖章信息（双方姓名 / 公章 / 法定代表人 / 日期）。
trigger_phrases: ["签字信息", "盖章", "signature block"]
---

# /extract-signatures

## 调用
```
/extract-signatures <doc> [--out=signatures.json]
```

## 输出
```json
[
  {"party":"甲方","name":"XX 有限公司","representative":"张三","title":"法定代表人","seal":"已盖章","date":"2025-06-01"},
  ...
]
```

---
name: redact-document
description: 涉密信息脱敏（身份证号 / 手机号 / 银行卡号 / 邮箱 / 车牌 → [REDACTED]）。
trigger_phrases: ["脱敏", "redact"]
---

# /redact-document
```
/redact-document <doc> [--out=redacted.md] [--keep-last=4]
```

## 默认脱敏项
- 身份证：保留前 6 + 后 4
- 手机号：保留前 3 + 后 4
- 银行卡：全脱敏
- 邮箱：保留 @ 后域名
- 车牌：保留省字

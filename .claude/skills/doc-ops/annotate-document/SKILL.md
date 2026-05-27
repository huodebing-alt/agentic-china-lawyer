---
name: annotate-document
description: 律师批注 + 风险标记。在合同段落旁打 🔴 🟡 🟢 风险标，附简短点评。
trigger_phrases: ["批注", "annotate"]
---

# /annotate-document
```
/annotate-document <doc> [--out=annotated.md]
```
路由：LLM 配合 `script.py` 输出注释流；最终交给律师修订。

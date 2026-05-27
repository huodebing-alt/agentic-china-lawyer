---
name: bilingual-side-by-side
description: 中英双语对照排版（左中右英）。
trigger_phrases: ["双语对照", "bilingual"]
---

# /bilingual-side-by-side
```
/bilingual-side-by-side <doc> --target=en|zh [--out=bilingual.md]
```

工作：源文档按段落拆，每段附译文，并排展示（markdown table）。LLM 提供译文，`script.py` 排版。

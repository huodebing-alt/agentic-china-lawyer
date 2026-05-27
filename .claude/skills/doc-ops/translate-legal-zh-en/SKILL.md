---
name: translate-legal-zh-en
description: 中英法律文档互译，保留法律术语精确性。LLM + glossary 双语对照，不机翻。
trigger_phrases: ["翻译", "translate", "中英互译"]
---

# /translate-legal-zh-en
```
/translate-legal-zh-en <doc> --target=en|zh [--out=translated.md] [--glossary=path]
```

工作：
1. 按段落 / 条款拆
2. LLM 逐段译，遇术语调 glossary
3. 输出与 `/bilingual-side-by-side` 兼容的格式

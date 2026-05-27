---
name: generate-from-notes
description: 客户访谈笔记 → 备忘录 / 案件摘要 / 起诉状要点 草稿。
trigger_phrases: ["从笔记生成", "访谈纪要"]
---

# /generate-from-notes
```
/generate-from-notes <notes.md> --target=memo|complaint|client-letter [--out=draft.md]
```
路由：LLM 主导，`script.py` 仅做结构骨架准备。

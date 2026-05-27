---
name: compare-documents
description: 任意两文档对比，输出 .docx track-changes 或 markdown diff。
trigger_phrases: ["对比", "compare", "diff", "看变化"]
---

# /compare-documents

## 调用
```
/compare-documents <path-to-v1> <path-to-v2> [--out=<dir>] [--format=docx|md|html]
```

## 路由
`document-master` → `script.py`

## 输出
- `out.diff.md` markdown diff
- `out.redline.docx` Word track-changes（如可生成）
- `out.diff.html` 浏览器可读 redline

## 依赖
`diff-match-patch` `python-docx` `mammoth`

---
name: extract-tables
description: 从合同 / PDF 中抽取表格，输出 markdown 或 CSV。
trigger_phrases: ["抽取表格", "提取表格", "extract table"]
---

# /extract-tables

## 调用
```
/extract-tables <doc> [--out=tables.md] [--format=md|csv]
```

## 依赖
- `pdfplumber` 抽 PDF 表格
- `python-docx` 抽 docx 表格

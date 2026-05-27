---
name: ocr-document
description: 扫描件 / 拍照件 OCR → 可编辑文本。中文优先（PaddleOCR / Tesseract）。
trigger_phrases: ["OCR", "扫描件", "拍照件"]
---

# /ocr-document

## 调用
```
/ocr-document <image-or-pdf> [--engine=paddleocr|tesseract] [--out=ocr.txt]
```

## 依赖
- 优先：`paddleocr`（中文准确率高）
- 备选：`pytesseract`（需本机装 tesseract + chi_sim 包）

## 输出
- `ocr.txt` 纯文本
- `ocr.md` markdown（带页码分割）
- 置信度 < 95% 的字符标 ⚠️

---
name: extract-citations
description: 找出文档中所有法规 / 案例 / 财税文件引用，输出清单。
trigger_phrases: ["抽取引用", "找法条", "找案例", "extract citations"]
---

# /extract-citations

## 调用
```
/extract-citations <doc> [--out=citations.json]
```

## 抽取模式
- 法规：`《XXX》第 N 条`
- 案例：`(YYYY) X 民终 N 号` / `X 法院 (YYYY) X 字第 N 号`
- 财税文件：`财税[YYYY]X 号`
- 司法解释：`法释[YYYY]X 号`
- 通知：`国发[YYYY]X 号` / `XX 发[YYYY]X 号`

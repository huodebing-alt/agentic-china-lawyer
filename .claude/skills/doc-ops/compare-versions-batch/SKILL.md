---
name: compare-versions-batch
description: 多版本演化对比，输出版本演化时间线。
trigger_phrases: ["多版本对比", "版本演化", "version evolution"]
---

# /compare-versions-batch

## 调用
```
/compare-versions-batch <v1> <v2> <v3> ... [--out=<dir>]
```

## 输出
- 每相邻两版 redline
- `evolution.md` 时间线（哪些条款被反复改 / 哪一版最大改动）
- `heatmap.md` 条款级热力图（哪些条款变更最频繁）

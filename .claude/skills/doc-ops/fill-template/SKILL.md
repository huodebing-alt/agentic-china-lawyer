---
name: fill-template
description: 从模板库 + 字段化 data.json 生成新合同 / 文书。
trigger_phrases: ["填模板", "fill template"]
---

# /fill-template
```
/fill-template <template-id> <data.json> [--out=filled.md]
```
路由：`template-librarian`

## 模板查找
1. `templates/**/<template-id>.template.md`
2. 占位符 `{{字段名|默认|提示}}` 用 data.json 替换
3. 缺字段时报告

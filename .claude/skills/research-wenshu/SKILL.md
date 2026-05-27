---
name: research-wenshu
description: 裁判文书网检索（公开版 stub + 私有数据库兼容）。把任意法律议题转化为关键词组合，调 wenshu MCP，输出案例研究备忘。
trigger_phrases:
  - "查案例"
  - "找判例"
  - "类案"
  - "裁判文书"
  - "wenshu"
---

# /research-wenshu

## 调用

```
/research-wenshu <议题> [--court=最高/高级/中级/基层] [--year=2020-2025] [--limit=10]
```

## 内部 → 路由到

`research-specialist-wenshu`

## 输入提示

```
议题：<法律问题，越具体越好>
争点：<2-3 个核心争点>
时间：<近 X 年>
法院层级：<选填>
```

## 输出格式

见 `.claude/agents/research-specialist-wenshu.md` 的"案例检索备忘"模板。

## 公开版 stub 提醒

裁判文书网公开 API 限制较多，本项目默认使用 stub 数据。**律师请通过付费数据库**（北大法宝 / 威科先行 / 无讼）二次验证再引用。

切换私有 API：在 `.claude/mcp.json` 中将 `WENSHU_MODE=stub` 改为 `live` 并配置 `WENSHU_API_KEY`。

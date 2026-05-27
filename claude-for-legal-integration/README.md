# Optional · 与 Anthropic `claude-for-legal` 集成

> ⚠️ **这是可选集成**。`agentic-china-lawyer` 对 Claude 友好但不依赖。
> 若你不用 Claude Code，完全可以跳过本文档。

## 是什么

[`anthropics/claude-for-legal`](https://github.com/anthropics/claude-for-legal) 是
Anthropic 官方的全球律所版 plugin pack（12 plugin / 80+ agent / 20 MCP），主打英美法
通用律所工作流（redline、判例分析、合同模板等）。

## 何时启用集成

| 场景 | 启用？ | 理由 |
| --- | --- | --- |
| 用 Claude Code 跑 `agentic-china-lawyer` + 经常处理英文 / 跨境合同 | ✅ 推荐 | 复用通用 redline / 判例分析能力 |
| 用 Claude Code 跑 `agentic-china-lawyer` + 只做中国法 | 🟡 可选 | 本项目自带的 specialist 已够用 |
| 用 OpenAI / Gemini / 国产模型 runner | ❌ 不集成 | 该 plugin pack 是 Claude 专属，与其他 runner 不兼容 |
| 用 Cursor / Continue / Aider | ❌ 不集成 | 同上 |

## 安装 `claude-for-legal`（仅 Claude Code 用户）

```bash
# 在 Claude Code 中
/plugin install anthropics/claude-for-legal
```

或者克隆到 plugin 路径（具体路径以 Claude Code 文档为准）：

```bash
git clone https://github.com/anthropics/claude-for-legal.git ~/.claude/plugins/claude-for-legal
```

安装后重启 Claude Code，输入 `/plugins` 应能看到 `claude-for-legal`。

## 协同方式

| 场景 | 本项目 specialist | `claude-for-legal` agent | 协同 |
| --- | --- | --- | --- |
| 中文合同审查 | `contract-specialist` | `redline-reviewer` | 本项目用中文输出，调用 `redline-reviewer` 做 diff |
| 英文合同 | `contract-specialist` | `contract-drafter` | 本项目 wrap，输出双语 |
| 判例分析 | `precedent-comparator` | `case-analyzer` | 本项目对接 wenshu MCP，借用其分析框架 |
| 起草 NDA | `/draft-NDA-cn` | NDA template | 本项目用中文模板覆盖 |
| 客户接案 | `intake-specialist` | matter-intake | 本项目加中国律师执业证 / 利益冲突检查 |
| 法律研究 | `research-specialist-statute` | research-assistant | 本项目本地 RAG，国际部分 fallback 到 `claude-for-legal` |

## 优先级规则（写在 `task-router` 心智里）

```
1. 中国法实质工作 → 本项目 specialist 优先
2. 通用法律工作（如英文起草、国际判例） → claude-for-legal 优先（若已装）
3. 二者冲突 → 本项目（更贴合中国法 + 律师 - 客户语境）
4. 未装 claude-for-legal → 本项目独立完成所有工作（功能不缺失，质量略低于专用 agent）
```

## 不要重复造的轮子（前提是你装了 claude-for-legal）

- 通用 redline / diff
- 通用判例摘要
- 通用合同模板（英文）
- 通用引用格式（Bluebook / OSCOLA）

## 必须本地维护的（无论是否装 claude-for-legal）

- 中国法规 RAG
- 中文文书风格
- 中国法律数据库 MCP
- 中国税务计算
- 涉外（中国大陆出发）的法律适用判断

## 不装 `claude-for-legal` 的影响

本项目仍可独立运行。区别：

- 通用 redline / 英文起草由本项目 contract-specialist 自己做（质量略低于专用 agent）
- 国际判例分析能力较弱
- 中国法实质工作不受影响

## 多 runner 用户的建议

如果你想跑 `agentic-china-lawyer` 在 OpenAI / Gemini / 国产模型上：

- **不要装 `claude-for-legal`**（与其他 runner 不兼容）
- 等待本项目的 `runners/openai/`、`runners/gemini/` 适配层（路线图）
- 在这些 runner 上，通用律所能力由你选用的模型 + 本项目自带 specialist 承担

## License 兼容性

- 本项目：MIT
- `claude-for-legal`：以 Anthropic 官方仓库 LICENSE 为准
- 集成方式：本项目通过 agent 提示词层级调用，不修改 `claude-for-legal` 源码

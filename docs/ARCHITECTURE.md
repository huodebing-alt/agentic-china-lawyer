# 架构 / Architecture

`agentic-china-lawyer` 的运行时是一个**三层 agent 网格**，跑在 Claude Code 之上。

## 总览

```
            ┌────────────┐
            │   用户输入  │
            └─────┬──────┘
                  ▼
        ┌────────────────────┐
        │   task-router      │   ← 总指挥 (Opus, ≤30% ctx)
        │   判断 + 拆解 + 编排 │
        └─────────┬──────────┘
                  │
   ┌──────────────┼───────────────┐
   ▼              ▼               ▼
┌──────────┐  ┌──────────┐  ┌────────────┐
│Specialist│  │Specialist│  │ Specialist │  ← Sonnet, fresh ctx, ≤60%
│   (#1)   │  │   (#2)   │  │    (#N)    │     可并行 N 路
└─────┬────┘  └─────┬────┘  └─────┬──────┘
      │             │             │
      └─────────────┼─────────────┘
                    ▼
          ┌──────────────────┐
          │   aggregator     │  ← 整合 (Opus, ≤50%)
          └────────┬─────────┘
                   ▼
        ┌──────────────────────┐
        │ citation-checker     │  ← 引用核查
        │ consistency-checker  │  ← 一致性核查
        └────────┬─────────────┘
                 ▼
         最终 deliverable + 免责语
```

## 三层职责

| 层 | 谁 | 做什么 | 不做什么 |
| --- | --- | --- | --- |
| Routing | `task-router` | 判断复杂度、拆任务、编排 | 不做法律实质工作 |
| Specialist | 20 个领域专家 | 做该领域的真活 | 不越权、不跨域、不整合 |
| Aggregation | `aggregator` + checkers | 整合、去重、复核 | 不重做 specialist、不修改正文 |

## 复杂度档位与拆解

| 复杂度 | 触发条件（任一） | 拆解 | 示例 |
| --- | --- | --- | --- |
| Simple | 长度 < 80 字 / 单领域 / 单文档 | 0 拆，单 specialist | "民法典 1062 条说什么" |
| Medium | 长度 80-200 字 / 2 领域 / 2-3 文档 | 2-4 并行 specialist + aggregator | "审一份带保密 + 竞业的劳动合同" |
| Complex | 长度 > 200 字 / ≥3 领域 / ≥3 文档 / 预估输出 > 3000 字 | **强制** 5-10 fresh-context 子任务 | "尽调一家公司" / "完整离婚方案含财产+税务+子女" |

详见 [`DECOMPOSITION_GUIDE.md`](DECOMPOSITION_GUIDE.md)。

## Context Budget

| 角色 | 上限占用 | 一旦超过 |
| --- | --- | --- |
| `task-router` | 30% | 把剩余编排下发到 sub-router (Task tool) |
| 每个 specialist | 60% (fresh) | 输出尽快返回，避免膨胀 |
| `aggregator` | 50% | 只看 specialist output，不重读原文 |
| `*-checker` | 20% | 只核对引用 / 一致性 |

## 为什么这样设计

1. **避免单 context 溢出**：律所长任务（尽调 / 完整方案）单 context 极易爆
2. **避免 specialist 互相污染**：fresh ctx 让每个 specialist 只见自己的输入
3. **可审计**：每个 specialist 输出有独立 footprint，便于律师事后追溯
4. **可扩展**：新增一个法律领域，只需写一个 specialist，不改 router 与 aggregator

## MCP 接入

四个 MCP server 在 `mcp-servers/`，配置见 `.mcp.json`：

- `statutes-rag` — 本地法规 RAG（首次运行需 `prepare-statutes.sh`）
- `wenshu` — 裁判文书网（默认 stub）
- `samr` — 工商企业信息（默认 stub）
- `cnipa` — 商标 / 专利（默认 stub）

私有 / 付费数据库接入指南见 [`MCP_CATALOG.md`](MCP_CATALOG.md)。

## 与 `claude-for-legal` 的协同

启动 Claude Code 时本项目优先识别本目录下的 agent / skill，**若 `claude-for-legal` 也在 plugin 路径**，
Specialists 会优先调用 `claude-for-legal` 中的英文起草 / 判例分析 / redlining 等通用能力，
再叠加中国元素（法条 / 案例 / 中文文书风格）。

详见 [`../claude-for-legal-integration/README.md`](../claude-for-legal-integration/README.md)。

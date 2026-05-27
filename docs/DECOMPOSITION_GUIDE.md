# 任务拆解指南 / Task Decomposition Guide

本文档解释 `task-router` 的拆解逻辑与 context budget。

## 核心原则

1. **宁可多拆，不可拥挤**：长任务在单 context 处理 = 必然溢出
2. **每个子任务自包含**：fresh-context specialist 只见输入 / 期望输出
3. **不让 aggregator 重做活**：它只整合，不分析
4. **复核与生成分离**：checker 独立检查，发现问题不直接改正文

## 复杂度评分表

| 维度 | Simple (≤1 分) | Medium (2-4 分) | Complex (≥5 分) |
| --- | --- | --- | --- |
| 用户请求长度 (中文字数) | < 80 | 80-200 | > 200 |
| 法律领域数 | 1 | 2 | ≥ 3 |
| 文档 / 主体 / 时点数 | ≤ 1 | 2-3 | ≥ 3 |
| 输出预估字数 | < 800 | 800-3000 | > 3000 |
| 并行子目标数 | 0 | 1-2 | ≥ 3 |

得分：累加。0-2 = Simple，3-5 = Medium，≥6 = Complex。

**拿不准向高分倾斜**。

## 拆解模式

### Simple → 0 拆

直接 dispatch 1 个 specialist。例：

```
用户：民法典第 1062 条说什么
router → research-specialist-statute（单步）→ 用户
```

### Medium → 2-4 并行 → 1 aggregator

```
用户：审一份带保密 + 竞业 + 股权激励的劳动合同
router → [contract-specialist, labor-specialist, corporate-specialist] (并行)
       → aggregator → checkers → 用户
```

并行用一条消息中的多个 Task tool call 触发。

### Complex → 5-10 fresh-context 子任务 → 1 aggregator

```
用户：帮我尽调"XX 科技有限公司"
router 拆：
  T1 corporate-specialist        → 工商基本信息 + 股权穿透
  T2 ip-specialist               → 商标 / 专利 / 软著
  T3 litigation-prep-specialist  → 诉讼 / 仲裁记录
  T4 tax-specialist              → 税务合规初判
  T5 labor-specialist            → 劳动用工合规
  T6 data-protection-specialist  → PIPL / 数据合规
  T7 compliance-specialist       → 行业准入 / 经营资质
  T8 aggregator                  → 整合为尽调报告
  T9 citation-checker            → 法规 / 案例引用核查
  T10 consistency-checker        → 当事人名 / 金额 / 日期一致性
```

## fresh context 是怎么做到的

通过 Claude Code 的 `Task` tool 启动 subagent。每个 subagent：

- 不继承父 context 的对话历史
- 只接收 router 写好的"子任务描述包"
- 完成后只返回 deliverable
- 完成后 context 被丢弃

这意味着 **router 的 context 用量只增长一次**（写 prompt + 接 result），
而非随子任务累计。

## Context Budget 红线

| 角色 | 上限 | 实操建议 |
| --- | --- | --- |
| `task-router` | 30% | 收到长合同别灌入 ctx，先存 /tmp/contract.txt，仅 pass path |
| 单 specialist | 60% | 输出 ≤ 3000 字；超出请二次拆 |
| `aggregator` | 50% | 只读 specialist output，不重读原文 |
| `*-checker` | 20% | 用正则提取引用即可，不做语义分析 |

## 反面教材

❌ 让 task-router 自己审一份 10 万字合同
✅ task-router 把合同存 `/tmp/`，拆成"章节 1-3 → A specialist"、"章节 4-7 → B"、"章节 8-12 → C"

❌ specialist 在自己 ctx 里同时引 50 条法规、50 个案例
✅ specialist 只输出"引用清单 + 简短分析"，详细原文留给 statutes-rag MCP 在 checker 阶段拉

❌ aggregator 因为风格不通顺重写 specialist 的法律结论
✅ aggregator 标 `⚠️ specialist 间结论冲突`，让律师决定

## 自检清单

在每次复杂任务结束前，router 应自检：

- ✅ 我的 ctx 用量是否 ≤ 30%？
- ✅ 是否每个子任务都在 fresh context 跑？
- ✅ aggregator 输出是否覆盖所有 specialist 的 ⚠️ 标记？
- ✅ 引用核查报告是否附在末尾？
- ✅ 免责语是否带？

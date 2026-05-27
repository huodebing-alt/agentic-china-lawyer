# 示例 2（Medium）— 股东协议审查（含税务条款）

## 场景

律师收到一份天使轮股东协议，需审查并给客户出修改意见。合同含股权 / 反稀释 / 税务约定 / 竞业 / 保密。

## 用户输入

```
帮我审一下这份股东协议。客户是创始人方，对方是天使投资人。
合同 18 页，主要关注：1) 反稀释条款是否对己方公平 2) 创始人 vesting 条件
3) 税务安排 4) 退出机制 5) 竞业是否过严。
（粘贴合同文本 ~ 12000 字）
```

## task-router 判断

| 维度 | 取值 | 分 |
| --- | --- | --- |
| 长度 | ~ 80 字 + 长合同附件 | 1 |
| 领域数 | 3（公司 / 税务 / 劳动 - 竞业） | 2 |
| 文档 / 主体 | 1 份合同 + 2 主体 | 1 |
| 输出预估 | 2500 字 | 1 |
| 并行子目标 | 5（关注点） | 1 |

总分 **6 → 边界**。router 选择 **Medium → 3 并行 specialist**（不到 Complex 强制拆解阈值，但够并行收益）。

## 编排

```
task-router
  ├─ /tmp/sa-draft.txt（合同存盘，不灌 ctx）
  ├─ Task → contract-specialist
  │         "审查《股东协议》第 1-12 条（一般条款 + 反稀释 + 治理）"
  ├─ Task → corporate-specialist
  │         "审查第 8-15 条（vesting + 退出 + 优先权）"
  └─ Task → tax-specialist
            "审查第 13-14 条（税务条款）"
  ↓
aggregator
  → 整合为"合同审查意见"模板
  ↓
citation-checker + consistency-checker
  ↓
task-router → 用户
```

## 期望输出（摘要）

```
# 《股东协议》审查意见

> 任务复杂度：Medium
> 调用 specialist：contract / corporate / tax
> 引用核查：✅ 12 / ⚠️ 2 / ❌ 0

## 一、合同结构与有效性
（contract-specialist 摘要）

## 二、条款逐条意见
### 第 1-3 条 序言与定义
### 第 4-7 条 出资与股权结构
### 第 8-10 条 反稀释（⚠️ 建议修改）
（具体 redline）
### 第 11-12 条 公司治理
### 第 13-14 条 税务（tax-specialist：⚠️ 个税承担约定不利于创始人方）
### 第 15-17 条 退出机制
### 第 18 条 通用条款（管辖 / 仲裁）

## 三、风险清单
🔴 高：反稀释完全棘轮 vs 加权平均
🔴 高：vesting 加速触发条件过于宽松
🟡 中：税务承担条款
🟡 中：竞业期限 3 年（建议 ≤ 2 年）
🟢 低：通知与送达

## 四、修改建议（redline 摘要）

## 五、补充条款建议

---
<免责语>
```

## 耗时与 token

- router：~ 1000 token
- 3 specialist 并行：每个 fresh ctx，约 8000 token，合计 24000
- aggregator：~ 4000 token
- checker：~ 2000 token
- 总：约 30000 token，比单 ctx 节省 ~ 40%

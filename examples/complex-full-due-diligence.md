# 示例 3（Complex）— 完整尽调一家公司

> ⭐ 这是本项目最重要的演示。讲清楚为什么要"多 agent + fresh context 拆解"。

## 场景

律师受投资人委托，对一家拟投资的"上海某科技有限公司"做尽调。投资人会议两天后，律师需要一份完整的尽调报告。

## 用户输入

```
做尽调：「上海某某科技有限公司」（统一社会信用代码 91310000XXXXXXXXXX）。
目的：A 轮战略投资。
关注：股权结构、知识产权、诉讼、税务合规、劳动用工、数据合规、行业准入。
时限：2 天。
```

## task-router 判断

| 维度 | 取值 | 分 |
| --- | --- | --- |
| 长度 | ~ 100 字 | 1 |
| 领域数 | 7（明确列出） | 3 |
| 文档 / 主体 | 1 公司 + N 个子公司 + N 个时点 | 2 |
| 输出预估 | > 8000 字 | 2 |
| 并行子目标 | 7 | 2 |

总分 **10 → Complex（强制拆解）**。

## 编排（拆 10 个子任务，6 个 fresh-context specialist + aggregator + 2 checker）

```
task-router (Opus)
│
├─ T1 [fresh ctx] corporate-specialist
│   "查 SAMR + 股权穿透 3 层 + 历史变更 + 章程概要"
│   输入：公司全称 + 统一社会信用代码
│   输出：基本信息表 + 股权穿透图 + 关键变更时间线
│   字数上限：2000
│
├─ T2 [fresh ctx] ip-specialist
│   "查商标 / 专利 / 软著 / 域名 + 权利稳定性"
│   工具：mcp__cnipa__search_trademark / search_patent
│   字数上限：1500
│
├─ T3 [fresh ctx] litigation-prep-specialist
│   "查涉诉 / 涉仲裁 / 失信被执行 / 限制高消费"
│   工具：mcp__wenshu__search
│   字数上限：1500
│
├─ T4 [fresh ctx] tax-specialist
│   "税务合规初判：纳税信用等级 / 大额欠税 / 注销条件"
│   字数上限：1500
│
├─ T5 [fresh ctx] labor-specialist
│   "劳动用工合规初判：社保公积金 / 劳动仲裁 / 集团派遣"
│   字数上限：1500
│
├─ T6 [fresh ctx] data-protection-specialist
│   "PIPL / DSL / CSL 合规：业务数据类型 / 出境 / SDK / Cookie / 隐私政策"
│   字数上限：1800
│
├─ T7 [fresh ctx] compliance-specialist
│   "行业准入 / 经营资质 / 外商投资负面清单 / 行业许可"
│   字数上限：1500
│
└─ ┄┄┄ T1-T7 并行收集 ┄┄┄
      ▼
   T8 aggregator
   "把 T1-T7 输出整合为标准尽调报告（10 节）"
   字数上限：8000
      ▼
   T9 citation-checker
   "核查所有引用：法规条款号 / 案例文号"
      ▼
   T10 consistency-checker
   "核查：公司名 / 金额 / 日期 / 各 specialist 结论无冲突"
      ▼
task-router → 用户
```

## 为什么必须拆 / 为什么 fresh context

### ❌ 反面做法：在单 context 里跑

- ctx 起步空，但 7 个领域 × 每个 1500-2000 字 = 1.5 万字纯输出，加 router 与 prompt：极易触 200K ctx 上限
- 每个 specialist 在同一 ctx 看见前面 specialist 的输出，会"互相污染"（IP 专家被劳动专家的语气带跑）
- 一旦 ctx 满，后续 specialist 输出质量崩盘

### ✅ 本项目做法：fresh context + 强制并行

- 每个 specialist 在干净 ctx 启动，只见自己的"子任务包"
- router 主 ctx 用量 ≈ 7 次 Task tool 的 dispatch + result，可控
- 7 路并行，墙钟时间约等于最长那一路
- aggregator 在自己的 ctx 里只看 specialist output，不重做活

## 期望输出（尽调报告结构）

```
# 上海某某科技有限公司 · 法律尽职调查报告

> 出具日期：YYYY 年 MM 月 DD 日
> 尽调主体：<律师事务所>
> 任务复杂度：Complex
> 调用 specialist：corporate / ip / litigation-prep / tax / labor / data-protection / compliance
> 信息来源：SAMR / 裁判文书网 / CNIPA / 本地法规 RAG / 客户提供资料
> 引用核查：✅ 24 / ⚠️ 5 / ❌ 0

## 一、基本情况
- 名称、统一社会信用代码、法定代表人、注册资本、成立日期、经营状态
- 注册地址、经营地址、经营范围

## 二、股权结构
- 当前股权穿透（≤ 3 层）
- 历史变更（增资 / 减资 / 股权转让 / 实控人变更）
- 股东关联方
- 重大风险点

## 三、知识产权
- 商标（注册号 / 状态 / 类别）
- 专利（发明 / 实用新型 / 外观）
- 软件著作权
- 域名
- 权利稳定性（异议 / 无效 / 撤销）
- 与对外宣称的技术 / 产品的匹配度

## 四、诉讼与仲裁
- 涉诉案件汇总（原告 / 被告身份分布）
- 重大案件详述
- 仲裁案件
- 失信被执行人 / 限制高消费
- 行政处罚

## 五、税务合规
- 纳税信用等级
- 大额欠税 / 税务行政处罚
- 关联交易税务安排
- 跨境业务税务

## 六、劳动用工合规
- 员工人数与社保 / 公积金缴纳
- 劳动仲裁记录
- 重大劳动诉讼
- 灵活用工 / 派遣 / 外包风险

## 七、数据 / PIPL 合规
- 业务涉及个人信息 / 重要数据类型
- 数据出境路径
- 隐私政策与告知 - 同意机制
- 第三方 SDK / Cookie 合规

## 八、行业准入与经营资质
- 是否在外商投资负面清单
- 行业许可 / 备案（如 ICP / EDI / 网络文化 / 出版 / 增值电信）
- 自贸区 / 海南自由贸易港 安排

## 九、综合风险评估
- 🔴 高风险项（按严重度）
- 🟡 中风险项
- 🟢 低风险项

## 十、建议
1. 投资决策前必须解决项（deal-breaker）
2. SPA / SHA 中需特别约定项
3. 投后整改项
4. 进一步调查项

---

附件 A：引用核查报告
附件 B：一致性核查报告
附件 C：信息源说明（公开 stub / 私有数据库 / 客户提供）

---
本文件由 Claude 辅助生成，仅供执业律师内部参考。
最终对外签字、盖章、提交前，必须由律师亲自复核。
本工具不构成法律意见，亦不替代律师执业判断。
```

## Token 与时间

- router：~ 2000 token
- 6 specialist × 5000 token = 30000，fresh ctx 并行（墙钟约最慢那路）
- aggregator：~ 8000 token
- checker × 2：~ 4000 token
- 总：~ 44000 token，**vs 单 ctx 跑需要 ~ 100000 token 且大概率溢出**

## 给律师看的 30 秒讲解

> 不拆任务的话，单 Claude ctx 跑这份尽调约 60% 会在中途 OOM，剩下 40% 输出质量不稳。
> 本项目通过 task-router 把"尽调"硬拆成 7 个领域子任务，每个在干净 ctx 跑，
> 最后 aggregator 整合 + 二次复核。每一步律师可单独查源、单独追责。

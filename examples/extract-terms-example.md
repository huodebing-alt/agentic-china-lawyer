# 示例 — Doc-Ops · 关键条款抽取为 JSON

## 场景

律师手上有 30 份框架协议，要快速做个 summary 表格交给客户：金额、期限、违约金、管辖、签字方……

## 用户输入

```
帮我把这 30 份合同的关键条款抽出来做成表格。重点：金额、期限、违约金、管辖、签字日期、双方主体。
（附 contracts/*.docx 30 个）
```

## task-router 判断

→ **Complex**（30 个文档 + 多字段 + 预估输出长）

## 编排

```
task-router
  → document-master 编排批处理：
    对每份 docx：
      → /extract-contract-terms contract-N.docx → terms-N.json
    → 30 个 JSON 合并 → /merge-documents 或 自定义脚本
    → 生成 markdown table
  → aggregator
  → checkers
  → 用户
```

## 期望输出（摘要）

```
# 30 份合同关键条款汇总

| # | 合同名 | 甲方 | 乙方 | 金额(¥) | 期限 | 违约金 | 管辖 | 签字日期 |
| - | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 框架协议 A | XX 科技 | XX 信息 | 1,200,000 | 1 年 | 总额 20% | 上海仲裁 | 2024-03-15 |
| 2 | 框架协议 B | XX 科技 | YY 服务 | 800,000 | 2 年 | 总额 10% | 北京法院 | 2024-04-02 |
| 3 | ……              |        |        |           |       |          |          |            |

## 数据质量提醒
- ⚠️ 第 8、12、19 份的违约金条款表述模糊，LLM 抽取置信度低，请人工复核
- ⚠️ 第 5 份未抽到管辖条款，可能是漏写

## 建议进一步操作
- 对 ⚠️ 标记的合同跑 `/check-consistency`
- 对管辖空白的跑 `/audit-boilerplate`

> 本表格由 extract-contract-terms × 30 + document-master 出具，律师交付前请亲自复核。
```

## Token / 时间

- 30 次 skill 调用（每次约 1500 token in fresh ctx）= 45000
- 合并 + aggregator：约 3000
- 但 30 次 fresh-context 并行后，**router 主 ctx 仅累计 ~ 5000 token**
- 单 ctx 跑会 OOM；本项目 fresh-context 拆解后从容完成

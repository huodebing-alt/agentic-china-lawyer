# 示例 — Doc-Ops · 完整文档审查 Pipeline（扫描件 → 律师交付）

## 场景

客户拍了一份合同照片发来，要求律师审查。

## 用户输入

```
（用户上传 contract.jpg）
这份合同对方让我下周签。帮我看看有没有问题。
```

## task-router 判断

→ **Complex**（图片 + 全面审查 + 多 specialist）

## 编排 Pipeline（8 步）

```
1. document-master → /ocr-document contract.jpg
   输出：contract.txt（中文 OCR + 置信度 < 95% 标记）
   ⚠️ 第 12 段、第 23 段置信度低，建议补拍清晰版

2. document-master → /extract-contract-terms contract.txt
   输出：terms.json

3. document-master → /extract-citations contract.txt
   输出：citations.json（5 处法规引用）

4. document-master → /check-citations contract.txt
   → 调 statutes-rag MCP 逐条验证
   输出：citations-check.md（✅ 3 / ⚠️ 2 / ❌ 0）

5. document-master → /audit-boilerplate contract.txt
   输出：boilerplate.md（缺：第三方受益人 / 可分割性）

6. contract-specialist + tax-specialist 并行（基于 terms.json）
   → 法律实质审查
   输出：风险清单（高 / 中 / 低）

7. document-master → /annotate-document contract.txt + 风险清单
   输出：annotated.md（律师评注稿，🔴 🟡 🟢 标色）

8. document-master → /format-legal-document annotated.md
   输出：final-review.md（律所标准格式）

→ aggregator 把 1-8 整合为合同审查意见
→ citation-checker + consistency-checker
→ 用户
```

## 期望输出（摘要）

```
# 《XXX 合同》审查意见

> 输入类型：扫描件 → OCR（置信度 92%，2 段需补拍）
> 关键条款抽取：✅
> 法规引用核查：✅ 3 / ⚠️ 2 / ❌ 0
> 标准条款审计：缺 2 项
> 法律实质审查：3 高风险 / 5 中风险 / 1 低风险

## 一、文档质量提醒
- ⚠️ OCR 置信度 92%，建议补拍第 12、23 段清晰版后重审
- ⚠️ 引用《XX 法》第 999 条 → 该条款在本地库未找到，可能引文错误，请律师核对官方原文

## 二、关键条款抽取结果
（terms.json 表格化）

## 三、法律实质审查
（来自 contract-specialist + tax-specialist）

### 第 8 条 违约金 🔴
- 内容：违约金 = 合同金额 50%
- 风险：远超合理预期，超出实际损失 30% 部分可能被法院调整（《民法典》第 585 条）
- 建议：反提违约金 ≤ 合同金额 20% 或与实际损失挂钩

### 第 15 条 管辖 🔴
……

## 四、标准条款审计
- ❌ 缺第三方受益人条款（如有第三方收款，建议补）
- ❌ 缺可分割性条款（建议补）

## 五、修改建议（带 redline 文本）
（具体替代条款）

## 六、签字前 checklist
- [ ] 补拍 OCR 低置信度段落
- [ ] 与对方确认第 8 条违约金调整
- [ ] 与对方确认管辖
- [ ] 补充缺失的 2 项标准条款
- [ ] 律师亲自终审 + 客户签字

---
本意见由 doc-ops pipeline (8 步) + contract-specialist + tax-specialist 联合出具。
律师签字盖章前请亲自复核。
本工具不构成法律意见。
```

## 这个 example 想说什么

**律师文档工作 = pipeline，不是单 skill**。本项目通过 `document-master` 把 OCR / 抽取 / 核查 / 审计 / 审查 / 注释 / 格式化串成 8 步流水线，每步独立可审计。律师不再"全程手动一遍跑"，但每步律师都看得到中间产物，**最终责任仍在律师**。

## Token / 时间

- pipeline 8 步约 25000 token（多数 fresh ctx）
- 单 Claude ctx 跑约会用 80000+ token，且 OCR 输出污染后续 ctx
- 本项目拆解后 **每步独立，可重跑可调试**

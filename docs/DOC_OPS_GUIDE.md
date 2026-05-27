# Document Operations Guide · 文档工作指南

`agentic-china-lawyer` 内置 **5 个 doc-ops agent + 26 个 doc-ops skill + 律所模板库**，覆盖律师日常 30-50% 的文档处理工作。

## 为什么需要 doc-ops

律师真实工作中花在文档上的时间远超过"实质法律分析"：

- 对比客户给的两版合同（手工 diff 找变化）
- 把扫描件 / 拍照件转成可编辑文本
- 从 100 页合同里抽出关键条款形成 summary
- 中英文标点 / 段首缩进 / 法条引用格式手工统一
- 律师函 / 起诉状 / 委托书填空式起草
- 客户访谈笔记整理成备忘录
- 证据清单编号 + 索引
- 隐私 / 涉密信息脱敏

本项目把这些都做成 **可调度的 skill**，由 `document-master` 统一编排。

## 5 个 doc-ops agent

| Agent | 职责 |
| --- | --- |
| `document-master` | 文档任务总协调员，分发给下面 4 个 |
| `contract-redliner` | 合同对比 / redline 风险标注 |
| `document-formatter` | 中文律所文风规范化 |
| `evidence-organizer` | 证据 / 附件清单管理 |
| `template-librarian` | 模板库 + 字段化填空 |

## 26 个 doc-ops skill

### 对比 / Redline (4)
- `/compare-documents` — 通用两文档 diff
- `/redline-contract` — 合同对比按风险标色
- `/compare-versions-batch` — 多版本演化
- `/diff-clauses` — 单条款级别 diff

### 抽取 / Extraction (4)
- `/extract-contract-terms` — 关键条款 → JSON
- `/extract-tables` — 表格抽取
- `/extract-signatures` — 签字盖章信息
- `/extract-citations` — 找出所有法规 / 案例引用

### OCR / 格式转换 (5)
- `/ocr-document` — 扫描件 OCR（中文优先 PaddleOCR）
- `/pdf-to-docx` — PDF → Word
- `/docx-to-markdown` — Word → markdown（git 友好）
- `/merge-documents` — 多文档合并
- `/split-document` — 大合同拆分

### 编辑 / 审查 (5)
- `/format-legal-document` — 律所文风规范化
- `/check-citations` — 法规引用核对（依赖 statutes-rag MCP）
- `/repair-cross-references` — 内部交叉引用核对
- `/audit-boilerplate` — 标准条款完整性
- `/check-consistency` — 文档内部一致性

### 注释 / 标注 (3)
- `/annotate-document` — 风险旁注
- `/redact-document` — 涉密脱敏（身份证 / 手机号 / 银行卡 / 邮箱 / 车牌）
- `/bilingual-side-by-side` — 中英对照排版

### 模板 / 生成 (4)
- `/fill-template` — 模板 + 字段化数据填充
- `/generate-from-notes` — 客户访谈笔记 → 草稿
- `/generate-table-of-contents` — 自动目录
- `/paginate-document` — 页眉页脚 / 律所页头

### 翻译 (1)
- `/translate-legal-zh-en` — 中英法律互译（含 glossary）

## 典型 Pipeline

### Pipeline 1：扫描合同审查

```
扫描件 PDF
  → /ocr-document          → 可编辑文本
  → /extract-contract-terms → JSON 关键条款
  → /extract-citations      → 引用清单
  → /check-citations        → 引用核查报告（依赖 statutes-rag）
  → /audit-boilerplate      → 标准条款缺失清单
  → 律师亲自评估 + /annotate-document
  → /format-legal-document  → 最终交付
```

### Pipeline 2：合同 redline + 起草修订稿

```
对方发来 v3 合同
  → /redline-contract (v2 vs v3)    → 风险标注 redline
  → /diff-clauses (重点条款)         → 单条精确 diff
  → 律师评估 + /annotate-document   → 谈判 talking points
  → 起草反建议条款（contract-specialist）
  → /fill-template (反建议)         → 草稿
  → /format-legal-document          → 发送给对方
```

### Pipeline 3：从模板批量起草

```
客户提供数据（10 个员工劳动合同）
  → 数据脱敏（/redact-document，留导出 audit log）
  → /fill-template employment-contract data-1.json
  → /fill-template employment-contract data-2.json
  → ...
  → /format-legal-document 批量
  → 律师抽样复核（每 5 份完整看 1 份，其余看摘要）
```

## 依赖安装

```bash
pip install -r requirements.txt
```

`requirements.txt` 包含 `python-docx` / `pdfplumber` / `pdf2docx` / `paddleocr` / `pytesseract` / `mammoth` / `diff-match-patch` 等。

OCR 在中文场景推荐用 PaddleOCR：

```bash
pip install paddleocr paddlepaddle
```

## 与 task-router 协作

`task-router` 检测到文档关键词 → 路由到 `document-master` → 编排 pipeline → 调用具体 skill 的 `script.py`。

详见 [`.claude/agents/doc-ops/document-master.md`](../.claude/agents/doc-ops/document-master.md) 与 [`.claude/agents/task-router.md`](../.claude/agents/task-router.md) 末尾的"文档任务识别"附录。

## 模板库

见 [`../templates/README.md`](../templates/README.md)。首发包含 10 个常用模板（NDA / 服务合同 / 股东协议 / 婚前协议 / 离婚协议 / 劳动合同 / 律师函 / 委托书 / 起诉状 / 隐私政策骨架）。

## 红线（务必遵守）

- **OCR 必带置信度警告**（<95% 标 ⚠️）
- **redline 仅做风险归类**，律师必须自己判定是否接受变更
- **填模板后必走 `/format-legal-document` + 律师亲自看一遍**
- **OCR + 模板填充 + 翻译"看起来快"，但律师责任不减**
- **真实客户数据进入项目前请先 `/redact-document`**

# Agentic China Lawyer

> **Multi-Agent AI legal assistant for solo lawyers practicing Chinese law.**
> **为执业中国法律的独立律师打造的多 Agent AI 助手 — 模型无关、即插即用。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Model-Agnostic](https://img.shields.io/badge/Model-Agnostic-success)](#兼容性-roadmap)
[![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-blue)](#架构-architecture)
[![China Law](https://img.shields.io/badge/Jurisdiction-PRC-red)](#)
[![Agentic AI](https://img.shields.io/badge/Style-Agentic-blueviolet)](#)

---

## 这是什么 / What is this

一个**模型无关 (model-agnostic)** 的多 agent AI 律师助手框架，**面向个人 / 青年 / 独立执业律师**。

* **不绑定任何具体模型**：agent definition、skill definition、MCP 全部基于开放标准（markdown frontmatter + JSON）。今天用 Claude Code 跑得最顺，明天可以替换 runner 跑在 OpenAI / Gemini / 通义千问 / DeepSeek / Kimi 等任意 agent 框架上
* **23 个 China-law specialist agent** + **5 个 doc-ops agent**（合计 28）
* **28 个中国法 skill** + **26 个 doc-ops skill**（合计 54）
* **4 个中国法律数据库 MCP** + 律所**模板库**
* **强制任务拆解 (forced task decomposition)**：长任务在 fresh context 自动拆 5-10 个子任务并行执行，避免单 context 溢出
* **基于 Anthropic 的 `claude-for-legal` 之上（optional）**：若你用 Claude Code 并安装了 `claude-for-legal`，本项目复用其 redline / 判例分析能力 + 叠加中国元素；若你不用 Claude，本项目独立可跑

---

## 60 秒 Quickstart / 60-second Quickstart

```bash
git clone https://github.com/huodebing-alt/agentic-china-lawyer.git
cd agentic-china-lawyer
bash scripts/prepare-statutes.sh   # 首次：从官方源下载法规库（约 1-2 分钟）
claude                              # 当前推荐 runner：Claude Code
```

> ⚠️ 本项目不分发任何法规原文。`prepare-statutes.sh` 从全国人大官方法律法规数据库
> (flk.npc.gov.cn) 等下载并落地为 markdown，由 `statutes-rag` MCP 检索。

打开后直接输入：

```
帮我审查这份股东协议（粘贴文本）
```

或：

```
做尽调：公司全称「XX 科技有限公司」
```

`task-router` agent 会自动判断复杂度、拆解任务、并行调度 specialist、最后由 `aggregator` 整合输出。

---

## 兼容性 / Compatibility · Roadmap

| Runner | 状态 | 说明 |
| --- | --- | --- |
| **Claude Code** | ✅ 当前默认 | 现成跑通，无需配置。读 `.claude/` 目录 + `.claude/mcp.json` |
| **Claude API + 自研 runner** | 🟡 文档支持 | Agent / Skill 是纯 markdown，写 100 行 runner 即可调用 Claude API 跑 |
| **OpenAI Codex / GPT API** | 🟡 路线图 | 提供 `runners/openai/` 适配层（agent 提示词 → Responses API + function calling） |
| **Gemini / Vertex AI** | 🟡 路线图 | 提供 `runners/gemini/` 适配层 |
| **国产模型** | 🟡 路线图 | 通义千问 / DeepSeek / Kimi / 智谱 GLM / 月之暗面 等。重点是中文场景实测 |
| **Cursor / Continue / Aider** | 🟢 评估中 | 这些 IDE-agent 工具的 agent 定义格式略不同，需要轻量适配 |

**为什么 model-agnostic 不只是口号**：

- Agent 定义 = `.md` + YAML frontmatter（无 SDK 锁定）
- Skill 定义 = `.md` + 触发关键词（无 SDK 锁定）
- MCP server = 标准 [Model Context Protocol](https://modelcontextprotocol.io/)（跨模型已支持）
- 多 agent 协调逻辑写在 `task-router` 的提示词里，**不依赖任何模型特有功能**
- 唯一"Claude Code 专属"的只剩 `.claude/` 目录约定 — 后续会同步提供 `agents.yaml`（runner-agnostic 通用清单），见 `docs/RUNNER_AGNOSTIC.md`（路线图）

---

## 为什么需要它 / Why

| 痛点 | 这个项目怎么解 |
| --- | --- |
| 全球律所版重型工具（如 Claude-Code-Law-Firm）太重，配置复杂 | **零配置**，`git clone && <runner>` 即用 |
| 通用 LLM 不懂中国法（条款引用错、判例引用错） | **本地法规 RAG + 裁判文书网 MCP**，引用全部基于公开法律文本 |
| 长任务（尽调 / 完整离婚方案 / 股权架构）经常 context 溢出 | **`task-router` 强制拆解 + fresh-context 子任务**，单任务可处理数万字输入 |
| 单 AI 终端做合规审查容易遗漏交叉领域 | **specialist 矩阵 + citation-checker / consistency-checker** 二次复核 |
| 起草中文法律文书风格不对 | 28 个中文 skill **内置律所文书模板**（律师函 / 民事起诉状 / 婚前协议 / 股权激励等） |
| 担心被锁定在某家 AI 厂商 | **model-agnostic 设计**，runner 可替换 |
| 真实律师 30-50% 时间花在文档处理（OCR / redline / 抽取 / 格式化 / 翻译） | **Doc-Ops 模块**：5 agent + 26 skill + 模板库，pipeline 化 |

---

## 架构 / Architecture

```
┌────────────────────────────────────────────────────────┐
│  用户请求 (User prompt)                                 │
└──────────────────┬─────────────────────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  task-router (Opus    │  ◀── 判断复杂度，决定拆解策略
       │    / GPT-4 / ……)      │
       └─────────┬─────────────┘
                 │
   ┌─────────────┼──────────────┬──────────────┐
   │ Simple      │ Medium       │ Complex      │
   │ (单 agent)  │ (2-4 并行)   │ (5-10 fresh) │
   ▼             ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────────────────────┐
│ corp     │  │ corp     │  │ corp / family / ip / tax  │
│specialist│  │ +tax     │  │ +labor +compliance +...   │
└──────────┘  └──────────┘  └──────────┬───────────────┘
                                       │
                                       ▼
                          ┌────────────────────────┐
                          │ aggregator (整合输出)   │
                          └──────────┬─────────────┘
                                     │
                                     ▼
                          ┌────────────────────────┐
                          │ citation/consistency    │
                          │ checker (二次复核)      │
                          └──────────┬─────────────┘
                                     │
                                     ▼
                              最终 deliverable
```

详见 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 与 [`docs/DECOMPOSITION_GUIDE.md`](docs/DECOMPOSITION_GUIDE.md)。

---

## Document Operations · 文档工作（Doc-Ops）

真实律师 30-50% 时间花在文档处理上：对比、起草、审查、编辑、格式化、提取条款、OCR、版本管理。本项目把这些做成 **可调度的 skill 矩阵**，由 `document-master` agent 统一编排成 pipeline。

### 5 个 doc-ops agent

| Agent | 职责 |
| --- | --- |
| `document-master` | 文档任务总协调员 |
| `contract-redliner` | 合同对比 / redline 风险标注 |
| `document-formatter` | 中文律所文风规范化 |
| `evidence-organizer` | 证据 / 附件清单管理 |
| `template-librarian` | 模板库 + 字段化填空 |

### 26 个 doc-ops skill（按类）

- **对比 / Redline (4)**：`/compare-documents` `/redline-contract` `/compare-versions-batch` `/diff-clauses`
- **抽取 / Extraction (4)**：`/extract-contract-terms` `/extract-tables` `/extract-signatures` `/extract-citations`
- **OCR / 格式 (5)**：`/ocr-document` `/pdf-to-docx` `/docx-to-markdown` `/merge-documents` `/split-document`
- **编辑 / 审查 (5)**：`/format-legal-document` `/check-citations` `/repair-cross-references` `/audit-boilerplate` `/check-consistency`
- **注释 / 标注 (3)**：`/annotate-document` `/redact-document` `/bilingual-side-by-side`
- **模板 / 生成 (4)**：`/fill-template` `/generate-from-notes` `/generate-table-of-contents` `/paginate-document`
- **翻译 (1)**：`/translate-legal-zh-en`

### 典型 Pipeline（扫描合同审查）

```
扫描件 → /ocr-document → /extract-contract-terms → /extract-citations
       → /check-citations → /audit-boilerplate
       → contract-specialist 实质审查
       → /annotate-document → /format-legal-document
       → 律师交付稿
```

### 律所模板库

`templates/` 含 10 个常用模板（NDA / 服务合同 / 股东协议 / 婚前协议 / 离婚协议 / 劳动合同 / 律师函 / 委托书 / 起诉状 / 隐私政策骨架），通过 `/fill-template` 字段化填充。

详见 [`docs/DOC_OPS_GUIDE.md`](docs/DOC_OPS_GUIDE.md) 与 [`templates/README.md`](templates/README.md)。

新增 examples：
- [`examples/redline-contract-example.md`](examples/redline-contract-example.md)
- [`examples/extract-terms-example.md`](examples/extract-terms-example.md)
- [`examples/full-doc-review-pipeline.md`](examples/full-doc-review-pipeline.md)


---

## 项目结构 / Project layout

```
agentic-china-lawyer/
├── README.md                       ← 你正在看
├── CLAUDE.md                       ← Agent / runner 项目入口（Claude Code 自动加载）
├── LICENSE                         ← MIT
├── DISCLAIMER.md                   ← 法律免责
├── .claude/                        ← Claude Code 约定路径（后续提供 .agent/ 通用版）
│   ├── agents/                     ← 23 China-law specialist + 5 doc-ops agent
│   │   └── doc-ops/                ← document-master + contract-redliner + formatter + ...
│   ├── skills/                     ← 28 China-law skill + 26 doc-ops skill
│   │   └── doc-ops/                ← compare / extract / OCR / format / template / translate
│   ├── mcp.json                    ← MCP 配置
│   └── hooks/                      ← 可选：PIPL 出库检查等
├── mcp-servers/                    ← MCP server 实现（标准 MCP，跨 runner 通用）
│   ├── wenshu/                     ← 裁判文书网
│   ├── samr/                       ← 国家市场监督管理总局
│   ├── cnipa/                      ← 国家知识产权局
│   └── statutes-rag/               ← 本地法规 RAG（民法典/公司法/PIPL…）
├── scripts/
│   ├── prepare-statutes.sh         ← 用户本机跑：下载法规原文
│   └── verify.sh                   ← 项目结构自检
├── templates/                      ← 律所文书模板库（10 模板，可扩展）
├── requirements.txt                ← Python 依赖（doc-ops 用）
├── claude-for-legal-integration/   ← 可选：与 Anthropic 官方 plugin pack 协同
├── docs/                           ← 架构 / 拆解规则 / Skill 目录 / MCP 目录 / 免责
└── examples/                       ← 三档复杂度示例
```

> 关于 `.claude/`：这是 Claude Code 的约定目录名（不是品牌引用，是工程约定）。
> 后续 Roadmap 中的 `runners/openai/`、`runners/gemini/` 会读取 `agents.yaml` 与
> `mcp.json`，向其他 AI 框架暴露同一份 agent / skill / MCP 定义。

---

## SEO 友好功能索引 / Feature Index

### Multi-Agent AI for Chinese Lawyer · 中国律师 AI 助手 · 个人律师 · 独立律师 · 青年律师工具

* 中文法律检索（裁判文书网 + 北大法宝兼容接口）
* 中文合同起草与审查（NDA / 股东协议 / 劳动合同 / 婚前协议 / 离婚协议）
* 民法典 / 公司法 / 劳动合同法 / PIPL / 反垄断法条款查询
* 律师函 / 停止侵权函 / 民事起诉状 / 答辩状起草
* PIPL 合规自评 + 数据出境合规
* 劳动合规 + 经济补偿金计算
* 商标 / 专利 / 著作权检索
* 工商企业信用信息查询
* 股权激励方案设计
* 个税 / 继承税务计算
* 跨境离婚 / 涉外婚姻 checklist
* 外商投资准入查询（负面清单）

### Document Operations · OCR · Contract Redline · Legal Document Extraction · 律师文档自动化

* 中文 OCR（PaddleOCR / Tesseract）— 扫描件 / 拍照件秒变可编辑文本
* 合同 redline 按风险标色（金额 / 管辖 / IP / 保密 重点标红）
* 关键条款抽取为 JSON，30 份合同 summary 表格一键出
* 中文律所文风规范化（段首缩进 / 法条引用 / 中英标点）
* 律所模板库 + 字段化填空 + 自动目录 + 页眉页脚
* 涉密信息脱敏（身份证 / 手机号 / 银行卡 / 邮箱）
* 中英法律文档双语对照排版

### Agentic AI · Multi-Agent · Task Decomposition · Model-Agnostic · MCP

* 强制拆解高复杂任务，每子任务 fresh context
* Specialist 并行执行（公司 / 家事 / IP / 劳动 / 税务 / 合规 / 合同 / 诉前）
* Aggregator 去重 + 整合
* Citation Checker + Consistency Checker 二次复核
* Agent / Skill 定义模型无关，可在 Claude / GPT / Gemini / 国产模型间迁移
* MCP 标准协议，跨 runner 共享数据源

### 即插即用 · 零配置 · GitHub 开源

* `git clone && <runner>` 三行启动
* MIT License
* 中英双语 README + 中英文 skill / agent 文档

---

## 与 [`Claude-Code-Law-Firm`](https://github.com/huodebing-alt/Claude-Code-Law-Firm) 的关系

| 维度 | `Claude-Code-Law-Firm`（律所完整版） | `agentic-china-lawyer`（个人律师轻量版） |
| --- | --- | --- |
| 定位 | 完整律所运营 | 单兵作战 |
| 复杂度 | 复杂 ERP + DMS + LSO | 零配置 |
| Agent 数 | 90+ | 23 |
| Skill 数 | 100+ | 28 |
| MCP | 集成律所主流系统（iManage / NetDocuments） | 中国法律数据库 |
| 模型绑定 | Claude Code 强绑定 | **Model-agnostic** |
| 文档操作 (Doc-Ops) | 集成（依赖律所 DMS） | **内置 5 agent + 26 skill + 模板库**，零依赖 |
| 适合人群 | 律所合伙人 / 律所信息化 | **个人律师 / 青年律师 / 独立律师** |

---

## 与 Anthropic [`claude-for-legal`](https://github.com/anthropics/claude-for-legal) 的关系

`claude-for-legal` 是 Anthropic 官方的全球律所版 plugin pack（12 plugin / 80+ agent / 20 MCP）。

**本项目对它友好，但不依赖**：

- 若你用 Claude Code 且安装了 `claude-for-legal` → 本项目 specialist 自动复用其英文起草 / redline / 判例分析能力，叠加中国元素
- 若你用其他 runner（OpenAI / Gemini / 国产模型）→ 本项目独立运行，不依赖 `claude-for-legal`
- 本项目内置 **doc-ops 模块**（OCR / redline / 抽取 / 模板填充 / 翻译等 26 个 skill），不依赖任何 Claude-specific plugin

详见 [`claude-for-legal-integration/README.md`](claude-for-legal-integration/README.md)。

---

## 中国法规索引 / China Law Index

| 法规 | 本地 RAG | 章节级检索 | Skill |
| --- | --- | --- | --- |
| 民法典 | ✅ | ✅ | `/lookup-civil-code` |
| 公司法 | ✅ | ✅ | `/lookup-statute 公司法` |
| 劳动合同法 | ✅ | ✅ | `/check-labor` |
| 个人信息保护法 (PIPL) | ✅ | ✅ | `/check-PIPL` |
| 数据安全法 | ✅ | ✅ | `/check-data-export` |
| 反垄断法 | ✅ | ✅ | `/check-antitrust-merger` |
| 商标法 | ✅ | ✅ | `/search-trademark` |
| 专利法 | ✅ | ✅ | `/search-patent` |
| 著作权法 | ✅ | ✅ | — |
| 个人所得税法 | ✅ | ✅ | `/calculate-pit` |
| 婚姻家庭编（民法典第五编） | ✅ | ✅ | `/draft-marriage-agreement`、`/draft-divorce-settlement` |
| 继承编（民法典第六编） | ✅ | ✅ | `/draft-will`、`/calculate-inheritance` |
| 外商投资法 | ✅ | ✅ | `/check-foreign-investment` |

完整目录见 [`mcp-servers/statutes-rag/statutes/_INDEX.md`](mcp-servers/statutes-rag/statutes/_INDEX.md)。

---

## 示例 / Examples

* **Simple**：[`examples/simple-statute-lookup.md`](examples/simple-statute-lookup.md) — 查民法典某条
* **Medium**：[`examples/medium-contract-review.md`](examples/medium-contract-review.md) — 审一份股东协议（3 个 agent 并行）
* **Complex**：[`examples/complex-full-due-diligence.md`](examples/complex-full-due-diligence.md) — 完整尽调一家公司（6 个 specialist + aggregator + 2 checker）

---

## 重要免责 / Disclaimer

**本项目仅供律师本人辅助使用**，输出**不构成法律意见**，律师对外签字盖章前须**亲自复核**。详见 [`DISCLAIMER.md`](DISCLAIMER.md) 与 [`docs/COMPLIANCE_DISCLAIMER.md`](docs/COMPLIANCE_DISCLAIMER.md)。

---

## License

MIT — 见 [`LICENSE`](LICENSE)。

---

## 贡献 / Contributing

欢迎 PR：
- 新增中国法 skill
- 补充法规 RAG 文本
- 接入新 MCP（如版权登记 / SAMR 处罚库 / 企业信用 / 海关 / 等）
- 新增 runner 适配（`runners/openai/`、`runners/gemini/`、`runners/qwen/`）

提交前请：

1. 在 `examples/` 中演示该功能
2. 在 `docs/SKILL_CATALOG.md` 或 `docs/MCP_CATALOG.md` 中登记
3. 通过 `aggregator` + `citation-checker` 流程跑通至少一次
4. 通过 `bash scripts/verify.sh`

---

> 🇨🇳 为独立律师的中国法实战而生 · 模型无关 · Multi-Agent · MCP-Standard

# Skill 目录 / Skill Catalog

> 共 28 个中国法专属 skill。每个 skill 在 `.claude/skills/<name>/SKILL.md` 中详述。

## 检索 / Research

| Skill | 一句话功能 | 路由 |
| --- | --- | --- |
| `/research-wenshu` | 裁判文书网案例检索 | research-specialist-wenshu |
| `/lookup-statute` | 通用法规条款查询 | research-specialist-statute |
| `/lookup-civil-code` | 民法典专用条款查询 | research-specialist-statute |
| `/search-company-info` | 工商企业信息查询 | corporate-specialist |
| `/search-trademark` | 商标查询 | ip-specialist |
| `/search-patent` | 专利查询 | ip-specialist |

## 起草 / Drafting

| Skill | 一句话功能 | 路由 |
| --- | --- | --- |
| `/draft-lvshihan` | 律师函起草 | contract-specialist + litigation-prep-specialist |
| `/draft-NDA-cn` | 中文保密协议 | contract-specialist |
| `/draft-marriage-agreement` | 婚前 / 婚内财产协议 | family-specialist |
| `/draft-divorce-settlement` | 离婚协议 | family-specialist + tax-specialist |
| `/draft-will` | 遗嘱起草 | family-specialist |
| `/draft-employment-contract` | 劳动合同 | labor-specialist |
| `/draft-equity-incentive` | 股权激励方案 | corporate-specialist + tax-specialist |
| `/draft-cease-and-desist` | 停止侵权函 | ip-specialist + litigation-prep-specialist |
| `/draft-power-of-attorney` | 授权委托书 | contract-specialist |
| `/draft-litigation-complaint` | 民事起诉状 | litigation-prep-specialist |
| `/draft-loan-agreement` | 借款合同 | contract-specialist |

## 审查 / Review

| Skill | 一句话功能 | 路由 |
| --- | --- | --- |
| `/review-contract-cn` | 中文合同综合审查 | contract-specialist (+ 视类型其他) |
| `/review-shareholder-agreement` | 股东协议专项审查 | contract-specialist + corporate-specialist |

## 合规 / Compliance

| Skill | 一句话功能 | 路由 |
| --- | --- | --- |
| `/check-PIPL` | PIPL 合规自评 | data-protection-specialist |
| `/check-data-export` | 数据出境合规路径 | data-protection-specialist + cross-border-specialist |
| `/check-labor` | 劳动用工合规 | labor-specialist |
| `/check-foreign-investment` | 外商投资负面清单 | foreign-investment-specialist |
| `/check-antitrust-merger` | 经营者集中申报评估 | antitrust-specialist |

## 计算 / Calculation

| Skill | 一句话功能 | 路由 |
| --- | --- | --- |
| `/calculate-pit` | 个税测算 | tax-specialist |
| `/calculate-severance` | 经济补偿金 / 违法解除赔偿金 | labor-specialist |
| `/calculate-inheritance` | 继承财产分配 + 税务测算 | family-specialist + tax-specialist |

## Checklist

| Skill | 一句话功能 | 路由 |
| --- | --- | --- |
| `/cross-border-divorce-checklist` | 跨境离婚 checklist | cross-border-specialist + family-specialist |

## 命名约定

- `/research-*` — 检索类
- `/lookup-*` — 法规精确查询类
- `/search-*` — 数据库类查询
- `/draft-*` — 起草类
- `/review-*` — 审查类
- `/check-*` — 合规自评类
- `/calculate-*` — 计算类

## 新增 skill

1. 在 `.claude/skills/<name>/` 下建目录
2. 写 `SKILL.md`（参考既有 skill）
3. 在本目录登记
4. 写至少一个 `examples/` 示例

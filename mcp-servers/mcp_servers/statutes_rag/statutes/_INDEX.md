# 中国法规库索引 · `statutes-rag` Local Statute Index

> ⚠️ **本目录默认仅包含 placeholder**。请运行 `bash scripts/prepare-statutes.sh` 从官方源下载法规原文。

## 收录范围

| 文件 | 法规全称 | 主管 | 官方源 |
| --- | --- | --- | --- |
| `civil_code.md` | 《中华人民共和国民法典》 | 全国人大 | https://flk.npc.gov.cn/detail2.html?ZmY4MDgwODE3MjFiNzM4ZDAxNzIxYjcxYTE3ZjAwMDE |
| `company_law.md` | 《中华人民共和国公司法》(2023 修订) | 全国人大 | https://flk.npc.gov.cn/ |
| `labor_contract_law.md` | 《中华人民共和国劳动合同法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `pipl.md` | 《中华人民共和国个人信息保护法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `data_security_law.md` | 《中华人民共和国数据安全法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `cybersecurity_law.md` | 《中华人民共和国网络安全法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `antitrust_law.md` | 《中华人民共和国反垄断法》(2022 修订) | 全国人大 | https://flk.npc.gov.cn/ |
| `anti_unfair_competition_law.md` | 《中华人民共和国反不正当竞争法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `trademark_law.md` | 《中华人民共和国商标法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `patent_law.md` | 《中华人民共和国专利法》(2020 修订) | 全国人大 | https://flk.npc.gov.cn/ |
| `copyright_law.md` | 《中华人民共和国著作权法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `individual_income_tax_law.md` | 《中华人民共和国个人所得税法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `enterprise_income_tax_law.md` | 《中华人民共和国企业所得税法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `vat_law.md` | 《中华人民共和国增值税法》(2025) | 全国人大 | https://flk.npc.gov.cn/ |
| `foreign_investment_law.md` | 《中华人民共和国外商投资法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `civil_procedure_law.md` | 《中华人民共和国民事诉讼法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `arbitration_law.md` | 《中华人民共和国仲裁法》 | 全国人大 | https://flk.npc.gov.cn/ |
| `criminal_law.md` | 《中华人民共和国刑法》(2024 修正) | 全国人大 | https://flk.npc.gov.cn/ |

## 部门规章与司法解释（建议补充）

| 文件 | 标题 |
| --- | --- |
| `interp_civil_code_marriage.md` | 最高人民法院关于适用《民法典》婚姻家庭编的解释 |
| `interp_civil_code_inheritance.md` | 最高人民法院关于适用《民法典》继承编的解释 |
| `cross_border_data_measures.md` | 数据出境安全评估办法 / 标准合同办法 |
| `merger_review_rules.md` | 经营者集中审查规定 |

## 使用方法

1. 首次运行：

   ```bash
   bash scripts/prepare-statutes.sh
   ```

2. 脚本会从全国人大官方法律法规数据库 (`flk.npc.gov.cn`) 等官方源下载并落地为 markdown
3. 重新启动 Claude Code，`statutes-rag` MCP 即可检索

## 格式约定（如手工补充）

每个法规一个 `.md`：

```
# 《XXX 法》

> 颁布日期：YYYY-MM-DD
> 最新修订：YYYY-MM-DD
> 来源：<官方 URL>

## 第 1 条
（条文原文）

## 第 2 条
（条文原文）

...
```

`server.py` 使用正则 `## 第 N 条` 拆条建索引。

## 法律免责

本项目本身不分发任何法规原文。法规原文以官方网站为准。运行 `prepare-statutes.sh` 后下载的文本仅供律师本人辅助检索使用，**最终引用必须以官方渠道为准**。

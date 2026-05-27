# Templates · 模板库

> 律师常用文书模板。**所有模板均为框架**，不含真实客户案例数据。
> 由 `template-librarian` agent 管理，通过 `/fill-template` skill 填充。

## 模板分类

```
templates/
├── contract/        合同类
├── corporate/       公司类（股东协议 / 股权激励 / 章程）
├── family/          婚姻家事 / 继承
├── labor/           劳动用工
├── litigation/      诉讼 / 律师函 / 授权委托
└── compliance/      合规 / 隐私政策 / DPA
```

## 占位符约定

每个 `*.template.md` 中用 `{{字段名|默认值|提示}}`：

```
甲方：{{甲方全称|未填|公司全称含统一社会信用代码}}
合同金额：人民币 {{金额数字|0}} 元（大写：{{金额大写|零元}}）
签订日期：{{签订日期|YYYY 年 MM 月 DD 日}}
```

每个模板配一个 `*.fields.json` 列出所有字段的类型与必填性。

## 添加模板

```bash
# 1. 写 markdown 模板
vim templates/contract/my-new-template.template.md

# 2. 写字段元信息
vim templates/contract/my-new-template.fields.json

# 3. 写示例（可选）
vim templates/contract/my-new-template.example.md
```

## 使用

```
/fill-template my-new-template data.json
```

## 已收录模板（首发）

| 路径 | 用途 |
| --- | --- |
| `contract/nda-cn.template.md` | 中文保密协议 |
| `contract/service-agreement-cn.template.md` | 中文服务合同（骨架） |
| `corporate/shareholder-agreement.template.md` | 股东协议（骨架） |
| `family/marriage-agreement.template.md` | 婚前财产协议 |
| `family/divorce-settlement.template.md` | 离婚协议 |
| `labor/employment-contract.template.md` | 劳动合同 |
| `litigation/lvshihan.template.md` | 律师函 |
| `litigation/power-of-attorney.template.md` | 授权委托书 |
| `litigation/complaint-civil.template.md` | 民事起诉状 |
| `compliance/privacy-policy.template.md` | 隐私政策（骨架） |

## 红线

- **不含真实案例 / 真实客户数据**
- **不替代律师起草判断**（模板仅是脚手架）
- **填充后必须经 `/format-legal-document` + 律师亲自审阅**

## License

模板（不含填充数据）遵循 MIT，与项目同。

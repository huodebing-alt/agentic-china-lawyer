# `.agent/` — Runner-Agnostic 配置（路线图）

> 当前为占位目录。本项目目前默认通过 `.claude/` 跑在 Claude Code 上。
>
> 计划中此目录会包含：
>
> - `agents.yaml` — agent 清单（统一格式，跨 runner）
> - `skills.yaml` — skill 清单
> - `mcp.json` — MCP 配置（与 `.mcp.json` 同结构，可符号链接）
> - `prompts/` — agent / skill 的 markdown 提示词（与 `.claude/agents/`、`.claude/skills/` 同源）
>
> 以及对应的 runner 适配层：
>
> - `runners/openai/` — OpenAI Responses API + function calling
> - `runners/gemini/` — Google Gemini / Vertex AI
> - `runners/qwen/` — 通义千问 / DashScope
> - `runners/deepseek/` — DeepSeek API
> - `runners/kimi/` — Moonshot Kimi
>
> 在那之前，所有 agent / skill 定义都在 `.claude/` 中维护，通过 `CLAUDE.md` 加载。

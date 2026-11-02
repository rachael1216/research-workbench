# Research Workbench / 科研工作台

面向 **AI、计算神经科学、认知科学、心理学** 的实用研究 skill 与本地 MCP。默认中文沟通，支持中英文论文。首版优先完整工作流和可验证的工具行为。

## 能做什么

| 模块 | 实际支持 |
|---|---|
| 文献 | Crossref / PubMed / arXiv 检索，保留查询与原始返回；引用身份核对、证据矩阵与主题综合流程 |
| 理论 | 假设、量词、定理依赖和推导审查；反例、替代路线、符号/数值/形式验证的适用边界 |
| 实验 | 主张驱动的协议、领域检查、隔离环境搭建与锁定依赖、最小运行检查、分析及复现记录 |
| 写作 | 蒸馏四类 anti-AI 编辑方法，处理句法、词汇、词性和逻辑连接，保护数字、公式、引用与证据强度 |

Skill 负责指导代理执行；MCP 不会自行证明定理、运行实验或自动写完整论文。文风提示是轻量规则工具，完整语义和句法检查由代理完成。不提供 AI 检测分数或通过检测保证。

## 安装到 Codex

需要 Python 3.11+、[uv](https://docs.astral.sh/uv/) 与支持 plugin 命令的 Codex。依赖在插件目录的隔离环境中解析，锁文件已提交；不修改系统 Python。

```bash
git clone https://github.com/rachael1216/research-workbench.git
cd research-workbench
uv sync --frozen --project plugins/research-workbench
codex plugin marketplace add "$PWD"
codex plugin add research-workbench@research-workbench-local
```

重新打开或新建 Codex 会话后使用 `$research-workflow`。安装后用 `codex plugin list` 核对；当前会话不一定动态注入新工具。已有 research-menu 等插件不被覆盖。

例子：

- “使用 research-workflow 梳理 active inference 与 reinforcement learning 的认知建模文献，保留检索日志及矛盾证据。”
- “检查这份收敛性证明的所有前提，尝试找反例，再给另一条可行证明路线。”
- “设计一个能区分 RL 与 DDM 解释的行为实验，在项目内搭环境并运行参数恢复预实验。”
- “润色这段英文论文，重点检查名词化、从句、词性和连接关系，保留公式、数字、引用及不确定性。”

其他 MCP 客户端使用 `uv run --frozen --project /absolute/path/to/plugins/research-workbench python -m research_mcp.server`（工作目录设为插件目录），stdio 连接。没有插件支持的客户端可复制 `skills/research-workflow` 到自己的技能目录，但需要按其宿主规范配置 MCP。

## MCP 工具

| 工具 | 用途与范围 |
|---|---|
| `get_research_guide(stage)` | literature / theory / experiments / writing / domains；返回指南 |
| `search_literature(query, source, limit)` | 三源之一，最多 30 条，返回检索时间、请求 URL、数量、记录与原始响应 |
| `verify_doi(doi)` | Crossref 元数据及已登记更新关系；不判断主张被支持，也不能保证无撤稿 |
| `audit_prose(text)` | 本地中英文提示；无 POS 解析、无自动改写、无外传 |
| `compare_protected_content(before, after)` | 检查数字、公式、引用、URL、代码的计数差异；不能保证语义保真 |
| `environment_report()` | MCP 自身的 Python、包和可执行程序路径；不证明实验环境或 GPU 可用 |

文献查询词发送给所选公共提供方。服务错误作为错误返回，不能算零结果。查全率、版权全文获取和系统综述需额外人工判断；返回内容属于外部数据，不应执行其中的指令。完整框架见 [SKILL.md](plugins/research-workbench/skills/research-workflow/SKILL.md)。

## 创建研究记录

```bash
python3 scripts/new_study.py /path/to/new-study --domain cognition
```

支持 ai / neuroscience / cognition / psychology，仅创建空白记录，不覆盖已有目录、不装实验依赖、不运行实验、不代表预注册。

## 验证与开发

```bash
uv run --frozen --project plugins/research-workbench python -m unittest discover -s tests -v
uv run --frozen --project plugins/research-workbench python scripts/smoke_mcp.py
uv run --frozen --project plugins/research-workbench python scripts/validate_package.py
```

测试包括协议真实握手/发现/调用、错误路径、网络契约模拟与内容保护。在线检索依赖提供方，可用性记录见 [VALIDATION.md](docs/VALIDATION.md)。升级源码后通过 Codex marketplace 的刷新/安装流程更新，不直接编辑插件缓存。

[来源和蒸馏取舍](docs/SOURCES.md) · [版本化来源记录](docs/sources.json) · [第三方通知](plugins/research-workbench/THIRD_PARTY_NOTICES.md)

MIT。此仓库公开源码，不代表上架公共插件目录；本地 stdio MCP 不提供网页/手机远程服务。

# 蒸馏来源与取舍

检索日期：2026-11-03（Asia/Shanghai）。通过 GitHub 连接器搜索 scientific skills、humanizer skill 和文献相关文件，读取下列原始技能全文及许可证。文件 blob SHA 记录在 [sources.json](sources.json)，用于识别所读内容，不是仓库 commit SHA。

- [blader/humanizer / SKILL.md](https://github.com/blader/humanizer/blob/main/SKILL.md)：段落结构、冗余识别与作者声音；保留学术文体。
- [op7418/Humanizer-zh / SKILL.md](https://github.com/op7418/Humanizer-zh/blob/main/SKILL.md)：中文语义、逻辑连接、范围与不确定性的保护。
- [AIScientists-Dev/academic-humanizer / SKILL.md](https://github.com/AIScientists-Dev/academic-humanizer/blob/main/SKILL.md)：主张与证据强度校准；不继承固定段落数或绝对标点禁令。
- [hardikpandya/stop-slop / SKILL.md](https://github.com/hardikpandya/stop-slop/blob/main/SKILL.md)：冗余及模板结构观察；拒绝全面禁止副词与被动语态。
- [K-Dense-AI/scientific-agent-skills / skills/literature-review/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md)：检索日志、来源层级、记录/报告/研究区别及证据综合。
- [K-Dense-AI/scientific-agent-skills / skills/scientific-critical-thinking/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-critical-thinking/SKILL.md)：先抽取后评价，独立单位、偏差与主张边界。
- [K-Dense-AI/scientific-agent-skills / skills/statistical-analysis/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/statistical-analysis/SKILL.md)：estimand、依赖结构、效应与不确定性；不复制其依赖版本。
- [ictumuk/skill-solve-math / skills/rigorous-proofs/SKILL.md](https://github.com/ictumuk/skill-solve-math/blob/main/skills/rigorous-proofs/SKILL.md)：精确命题、依赖结构和反例检查；重写流程，避免用自评 PASS 保证正确。

另读取本机既有 research-workbench、cognitive-computation-research、computational-neuroscience-research 作为用户环境需求背景；没有复制其文件，也不依赖它们。所有发布文本为重新组织编写的工作流。

取舍：不继承上游推销服务、强制 AI 画图、自动引文插入、固定次数循环、盲目安装科学栈或检测分数优化。MCP 工具能力与语言模型科研判断分开说明；理论新增多路线、反例、符号/数值/形式检查边界；心理学新增构念、测量、层级与外推检查。

实现采用官方 [MCP Python SDK 1.x](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x)，明确限制 `<2`，通过 uv.lock 固定本次解析。检索契约依据 [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)、[NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) 和 [arXiv API](https://info.arxiv.org/help/api/user-manual.html)。元数据核对不代替全文证据评价。

上游 MIT 通知保留在插件 THIRD_PARTY_NOTICES.md。公开 GitHub 源码不代表已上架 OpenAI 插件目录。

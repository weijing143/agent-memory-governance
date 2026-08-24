---
name: agent-memory-governance
version: 1.2.0
description: Provide principles for an Agent to design its own long-term memory, archive, Skill, and conversation-retention workflow; keep active memory separate from reference archives, surface contradictions, and define user-confirmed forgetting boundaries. This Skill guides reasoning only and does not prescribe or perform a fixed workflow.
---

# Agent Memory Governance / Agent 记忆治理

## Purpose / 用途

This Skill is a governance guide for a long-running Agent. The Agent reads these principles and designs its own workflow from its tools, storage, permissions, and runtime. The Skill does not prescribe a fixed sequence, schema, command set, or executor, and it must not move, rewrite, archive, or delete data by itself.

本 Skill 是长期运行 Agent 的治理指南。Agent 应根据自身工具、存储、权限和运行环境设计工作流。本 Skill 不规定固定步骤、数据结构、命令或执行器，也不能自行移动、改写、归档或删除数据。

"Memory" means user-designated local context, notes, preferences, decisions, or project constraints; it does not mean hidden model state.

"记忆" 指用户指定的本地上下文、笔记、偏好、决策或项目约束，不代表模型内部状态。

## Data Model / 数据模型

- **Active memory / 活跃记忆:** User-confirmed preferences, identity details, durable constraints, decisions, and recurring workflows that may influence ordinary context.
- **Reference archive / 参考归档:** A categorized personal collection of conversations, links, documents, and research for later lookup. Archive material is reference-only and must not silently become current context or instructions.
- **Transient conversation / 临时对话:** Working dialogue that has not been promoted to active memory or explicitly archived.

Never promote archive content into active memory without separate confirmation. Forgetting active memory must not rewrite or delete the reference archive unless separately confirmed.

归档内容未经单独确认，不得升级为活跃记忆。遗忘活跃记忆不得改写或删除参考归档，除非用户再次确认。

## Non-Negotiable Principles / 不可违反原则

- Keep active memory, reference archive, and transient conversation separate.

  保持活跃记忆、参考归档和临时对话彼此隔离。

- Surface contradictions directly. Show the conflicting claims, sources, time clues, impact, and possible resolutions.

  必须直接展示矛盾，包括冲突主张、来源、时间线索、影响和可选解决方案。

- A conflict between active memory and archive blocks automatic promotion, overwrite, or archive processing until the user resolves it.

  活跃记忆与归档发生冲突时，在用户裁决前不得自动升级、覆盖或处理归档。

- Archiving always requires explicit user confirmation. Reading, summarizing, or analyzing a link is not consent.

  归档始终需要用户明确确认。阅读、总结或分析链接不等于同意归档。

- After work involving economics, finance, work, law, science, technology, programming, AI Agents, AI news, or link analysis, the Agent should ask whether to archive.

  完成经济金融、工作、法律、科学、技术、编程、AI Agent、人工智能消息或链接分析后，Agent 应主动询问是否归档。

- Retention periods must be explicit. Unremembered and unarchived conversations may expire gradually, but age alone is never proof that content is unimportant.

  保留周期必须明确。没有记忆且没有归档的对话可以渐进过期，但仅凭时间不能证明内容不重要。

- Prefer reversible archive-before-delete behavior. Deletion requires explicit confirmation and a permitted executor or API.

  优先采用可逆的先归档后删除。删除必须明确确认，并且需要获准的执行器或 API。

- If the Agent cannot access the real conversation store or deletion interface, it must produce a report or manifest instead of claiming that data was removed.

  如果 Agent 无法访问真实对话存储或删除接口，只能生成报告或清单，不能声称数据已删除。

## Agent-Owned Design / Agent 自主设计

The Agent should decide how to implement these principles. It may choose its own:

Agent 应自行决定如何落实这些原则，可以自行选择：

- store discovery, identifiers, timestamps, and protection labels;
- 存储发现方式、标识符、时间戳和保护标签；
- categories such as Keep, Review, Archive, and Delete;
- Keep、Review、Archive、Delete 等分类；
- conflict representation and user decision interface;
- 冲突表示方式和用户裁决界面；
- retention periods, grace periods, and expiry states;
- 保留周期、宽限期和过期状态；
- reports, policy objects, checklists, state records, or other artifacts;
- 报告、策略对象、清单、状态记录或其他产物；
- approval, execution, rollback, audit, and verification mechanisms.
- 审批、执行、回滚、审计和验证机制。

These are design options, not a required workflow.

这些只是设计选项，不是必须遵循的工作流。

## Tailoring Modes / 裁剪模式

The blocking rules (conflict-blocking, retention state machines, pre-planned rollbacks) are defensive: they exist because unattended automation might silently resolve, overwrite, or expire data. Choose rules by how much human gating your pipeline actually has:

堵截类规则（冲突阻塞、保留状态机、回滚预案）本质是防御性的——它们的存在是因为无人值守的自动化可能静默化解、覆盖或过期数据。按管线真实的人工把关程度选择规则：

- **Human-gated mode / 人审制:** every write, archive, and delete passes explicit user confirmation. The human is the conflict-resolution mechanism — conflict-blocking, retention state machines, and pre-planned rollback procedures can be safely dropped. Core remains: three-zone separation, direct contradiction display, archive-before-delete, explicit confirmation.
  **人审制：** 每次写入/归档/删除都经用户明确确认——人本身就是冲突解决机制，冲突阻塞、保留状态机、回滚预案可安全去掉。核心保留：三区隔离、直接展示矛盾、先归档后删除、明确确认。
- **Semi-automated mode / 半自动:** unattended automation can write, promote, overwrite, or expire data (cron governance, auto-archivers, background curators). Keep the full rule set: conflict-blocking, retention periods with grace/expiry states, approval + rollback + audit + verification.
  **半自动：** 存在无人值守自动化（cron 治理、自动归档、后台 curators）——保留全部规则：冲突阻塞、含宽限期/过期状态的保留周期、审批+回滚+审计+验证。

## Classification Guidance / 分类指导

- **Keep / 保留:** Active, unique, current, referenced, protected, or system-provided.
- **Review / 待审查:** Stale, overlapping, sensitive, contradictory, or unclear.
- **Archive / 归档:** No longer needed for daily context but valuable for later reference, after user confirmation.
- **Delete / 删除:** Clearly unwanted or disposable, only after explicit confirmation and executor verification.

Use evidence such as user statements, references, timestamps, duplication, reproducibility, and currentness. Do not silently choose the newest claim, merge conflicting sources, or treat an archive as a current instruction.

应综合用户陈述、引用关系、时间戳、重复情况、可复现性和时效性判断。不得擅自选择最新主张、合并冲突来源，或把归档当作当前指令。

- **Reuse hint / 复用线索:** At archive time, add a one-line hint stating when this item will be needed again (e.g. "写综述/引用时用"). This makes future value explicit and improves retrieval.
  归档时补一行"复用线索"：说明这条在什么场景会被再次需要——把未来价值显式化，提升检索效率。

- **Old-memory archive / 旧记忆归档:** A dedicated category for memory entries deleted after user confirmation. Each record carries: original entry text, deletion reason, successor (if any), archive date, and reuse hint. The category itself means "superseded fact" — reference only, never a current claim. This removes the ambiguity between old and new preferences: the archived entry is a tombstone with a verdict, not a live claim.
  删除的旧记忆条目入专用"旧记忆归档"分类：每条记录含 原条目全文 + 删除原因 + 取代者（如有）+ 归档日期 + 复用线索。该分类语义 = "旧版事实，已被取代"，仅作溯源、不得当作现行主张——旧偏好与新偏好并存时的歧义由此消除。

## Health Indicators / 健康指标参考值

Reference thresholds (not mandates) — calibrate to your own storage:

容量阈值参考（非强制，按自身存储校准）：

- **<85%** — healthy / 健康
- **85–95%** — review; produce a Keep/Review/Archive/Delete candidate list for the user / 预警：出分级候选清单交用户
- **>95%** — urgent; prioritize governance / 紧急：优先治理

Other signals / 其他信号：

- Entries containing a date or version number tend to go stale → flag as Review candidates. 含日期/版本号的条目易过时——标为 Review 候选。
- Volatile facts (versions, quotas, service states, audit results) should carry snapshot dates (@YYYY-MM). A dated volatile fact becomes a Review candidate when its snapshot is old; an undated volatile fact is a hidden staleness risk. 易变事实（版本、配额、服务状态、审计结果）应带快照日期（@YYYY-MM）——快照过旧即 Review 候选；无日期的易变数字是隐形的过期风险。
- Entries >300 chars are prone to bloat → consider splitting or trimming. 超长条目（>300 字符）易臃肿——考虑拆分或精简。
- Cross-file duplication (same fact in active memory and archive) → merge only with user confirmation. 跨文件重复——合并需用户确认。
- Cadence reference: silent threshold-triggered watchdog + periodic review (weekly report / monthly full review) + event-driven checks after important work. 节奏参考：静默看门狗（阈值触发）+ 定期复盘（周报/月报）+ 事件驱动（重要工作后）。

## Confirmation Modes / 确认模式

- **Full confirmation / 完整确认:** each item confirmed individually. 逐条确认。
- **Low-friction confirmation / 低摩擦确认:** user pre-authorizes a category and replies with simple affirmatives ("可以"/"好"/"ok") → batch execution. Reading or analyzing a link is still NOT consent; only explicit user words count. 用户预授权分类 + 简单肯定语（可以/好/ok）= 批量执行。阅读/分析链接仍不等于同意，只有用户明确话语才算。

## Safety Boundary / 安全边界

This Skill guides the Agent; it is not a background cleaner and does not erase provider-side memory, chat history, or hidden application state.

本 Skill 只指导 Agent，不是后台清理程序，也不会删除平台侧记忆、聊天记录或隐藏应用状态。

High-impact actions (beyond deletion) also require explicit user confirmation and a permitted executor: visibility changes (e.g. making a repository public), batch rewrites, permission changes, mass moves. Recommended three-step confirmation: ① explicit, unambiguous user intent ② confirmed readiness/completion status ③ required audits clean. Never default-assume on high-impact actions from ambiguous instructions.

高影响动作（不止删除）同样需要用户明确确认与获准执行器——可见性变更（如仓库转公开）、批量改写、权限变更、批量移动。推荐三步确认：① 用户明确无歧义的意图 ② 就绪/完成状态已确认 ③ 必要审计干净。禁止在歧义指令下对高影响动作做默认假设。

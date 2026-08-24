# Hermes Agent Integration / Hermes 落地说明

This document explains how to apply `agent-memory-governance` on Hermes Agent (Nous Research). Hermes has its own memory, skill, and session systems, so the governance principles map onto real storage as follows:

本文件说明如何在 Hermes Agent 上落地 `agent-memory-governance`。Hermes 有自己的记忆、技能与会话系统，治理原则与实际存储的映射如下：

## Storage Mapping / 三区映射

| Governance concept / 治理概念 | Hermes counterpart / Hermes 对应物 |
|---|---|
| Active memory / 活跃记忆 | `~/.hermes/memories/MEMORY.md` + `USER.md` (managed via the `memory` tool) |
| Reference archive / 参考归档 | `~/wiki` (llm-wiki collections), paper-visual-notes, session history (session_search) |
| Transient conversation / 临时对话 | Current conversation context |

## Delivered Artifacts / 落地产物

A companion Hermes skill implements these principles as an executable workflow:

配套的 Hermes 技能将这些原则实现为可执行工作流：

- **Skill: `memory-governance`** — health check → Keep/Review/Archive/Delete classification → candidate list for user decision → batch execution only after user confirmation. Never auto-deletes.
  **技能 `memory-governance`** — 健康检查 → Keep/Review/Archive/Delete 分级 → 候选清单交用户裁决 → 用户确认后批量执行。绝不自动删除。
- **Script: `scripts/memory_health.py`** — per-file entry count, char usage, capacity %, flags stale-prone (year-bearing) and overlong entries. Pure stdlib. The repo copy is authoritative; the Hermes skill embeds the same file.
  **脚本 `scripts/memory_health.py`** — 统计条目数、字符占用、容量百分比，标记含日期（易过期）与超长条目。纯标准库。仓库副本为权威源，Hermes 技能内置同款。
- **Cron watchdog: `~/.hermes/scripts/memory_watchdog.py`** — monthly; silent unless a memory file reaches ≥90% of its char limit, then reports and suggests governance.
  **定时看门狗 `~/.hermes/scripts/memory_watchdog.py`** — 每月运行；记忆文件容量 ≥90% 才发预警报告并建议治理，平时静默。

## Invocation / 触发方式

Unlike the OpenClaw setup (user-invocable only, `disable-model-invocation: true`), Hermes loads skills by relevance. `memory-governance` triggers on phrases like "整理记忆 / 记忆健康 / 记忆满了" or when memory usage ≥85%. The skill only produces recommendations and executes user-confirmed changes — it never cleans up in the background.

与 OpenClaw 配置（仅用户可调用、禁止模型自动调用）不同，Hermes 按相关性加载技能。`memory-governance` 在用户说"整理记忆 / 记忆健康 / 记忆满了"或记忆容量 ≥85% 时触发。技能只产出建议、执行用户确认的动作，绝不在后台自行清理。

## Three-Zone Routing / 三区路由与升降级

The isolation boundary is made executable via a routing table and promotion/demotion channels (implemented in the `memory-governance` skill under "三区路由与升降级"):

隔离边界通过路由表与升降级通道可执行化（实现于 `memory-governance` 技能"三区路由与升降级"章节）：

- **Routing** / 路由：long-term preferences, identity, environment facts, tool usage, active project state → active memory (`MEMORY.md`); concrete content, sources, analysis, one-off conclusions → archive (`~/wiki`) or session history. Anything retrievable via session_search is NOT duplicated into active memory (pointer at most).
  **路由**：长期偏好、身份、环境事实、工具用法、活跃项目状态 → 活跃记忆（`MEMORY.md`）；具体内容、来源、分析、一次性结论 → 归档（`~/wiki`）或会话历史。session_search 可检索的内容不重复写入活跃记忆（最多留指针）。
- **Demotion** / 降级：during governance cleanup, Review/Delete candidates are archived to `~/wiki` first (after user confirmation), then removed — archive before delete.
  **降级**：治理清理时，Review/Delete 候选先归档到 `~/wiki`（用户确认后）再移除——归档先于删除。
  Deleted memory entries go to the dedicated 旧记忆归档 category (`~/wiki/wiki/collections/memory-archive.md`) with a full record (original text, reason, successor, date, reuse hint) — the category itself means "superseded". 删除的旧记忆入专用"旧记忆归档"分类（`~/wiki/wiki/collections/memory-archive.md`），带完整记录（原条目/原因/取代者/日期/复用线索）——分类语义即"已被取代"。
- **Promotion** / 晋升：a stable fact recurring in wiki/sessions is promoted to active memory only after explicit user confirmation.
  **晋升**：wiki/会话中反复出现且已稳定的关键事实，仅在用户明确确认后升级为活跃记忆。
- **Snapshot dating** / 快照标注：volatile facts in active memory carry snapshot dates (@YYYY-MM); as they age, the health script flags them as Review candidates. 活跃记忆中的易变事实带快照日期（@YYYY-MM）；随时间变旧，健康脚本将其标记为 Review 候选。

## Archive Workflow Linkage / 归档流程联动

The "ask whether to archive" principle is merged with Hermes' existing wiki collection workflow (llm-wiki, `~/wiki`) into a single channel: after economics/finance/work/law/science/tech/programming/AI/link-analysis work, the Agent proactively suggests `归档到[分类]？`; a simple affirmative (可以/好/行) triggers the full collection flow (collections page + raw/notes snapshot + index/log). The user may change the category or decline — no repeated prompting.

"主动问归档"原则与 Hermes 现有 wiki 收藏流程（llm-wiki，`~/wiki`）合并为一条通道：经济/金融/工作/法律/科学/技术/编程/AI/链接分析类工作后，Agent 主动建议 `归档到[分类]？`；用户简单肯定（可以/好/行）即触发完整收藏流程（collections 收藏页 + raw/notes 快照 + index/log）。用户可改分类或拒绝，不重复追问。

This is implemented in the `memory-governance` skill under "与 llm-wiki 归档联动".

## Non-Negotiable Principles Carried Over / 继承的不可违反原则

- Three-zone isolation: active memory, reference archive, transient conversation.
  三区隔离：活跃记忆、参考归档、临时对话。
- Surface contradictions for user decision; never silently pick the newest claim or merge conflicting sources.
  冲突展示给用户裁决；不静默选最新主张、不合并冲突来源。
- Archive before delete; deletion requires explicit user confirmation.
  归档先于删除；删除必须用户明确确认。
- After economics/finance/work/law/science/tech/programming/AI/link-analysis work, ask whether to archive.
  经济/金融/工作/法律/科学/技术/编程/AI/链接分析类工作后，主动询问是否归档。
- Age alone is never proof that content is unimportant.
  仅凭时间不能证明内容不重要。

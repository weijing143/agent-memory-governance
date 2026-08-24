# Hermes 落地实践报告 / Hermes Practice Report

Date: 2026-08-24
Environment: Hermes Agent v0.19.0, Linux, 2GB RAM cloud server, QQ Bot platform

This report records how the principles in `SKILL.md` were actually implemented on Hermes Agent, the measured results, and the lessons learned. Companion to `hermes-integration.md` (which is the "how to install" guide; this is the "did it work" report).

本报告记录 `SKILL.md` 原则在 Hermes Agent 上的实际落地、量化结果与经验教训。与 `hermes-integration.md`（安装指南）互为补充——本篇回答"落地后是否有效"。

## Implemented / 落地清单

1. **`memory-governance` skill** — health check → Keep/Review/Archive/Delete classification → candidate list for user decision → batch execution only after confirmation. Includes:
   - `scripts/memory_health.py` (stdlib): per-file entry count, char usage, capacity %, flags stale-prone (year-bearing) and overlong entries.
   - Archive linkage with the existing wiki collection workflow (llm-wiki): after important work, agent proactively suggests archiving; a simple affirmative triggers the batch collection flow.
   - Three-zone routing & promotion/demotion channels (routing table on write; demote-before-delete; promote only after explicit confirmation).
2. **Cron scheduling system (6 jobs)** — daily session retention (silent), weekly system health report, monthly memory watchdog (silent, alerts at ≥90%), monthly memory governance review (list for user), monthly repo secret re-audit, monthly maintenance candidate list. Design rule: script-only jobs run silent (zero tokens); reporting jobs post stable formats; governance jobs only produce lists for user decision; **no high-impact action is ever automated**.
3. **Mandatory pre-publish confirmation** added to the companion security audit flow: changing repo visibility to public requires (a) explicit unambiguous user intent, (b) confirmed project completion status, (c) all 4 audit layers clean.

## Measured Results / 量化成果

- **Memory usage**: MEMORY.md 99% → 79% capacity (after governance), USER.md 88% → 80%. Both out of the warning zone.
- **Retrieval verification**: a single topic (e.g. "DeepMind software engineering") returns hits across 4 zones (raw/concepts/entities/sources) — the taxonomy is not siloed. Deleted memory entries were fully recovered from session history (session_search) — "archive before delete" and session-history-as-fallback proven in practice.
- **Classification visualization**: knowledge-base tree diagram + archive flow diagram generated as PNGs (graphviz) and delivered as media — the taxonomy became directly viewable.

## Lessons Learned / 经验教训

1. **Ambiguous trigger + high-impact action = must confirm first.** The word "开源" (open-source) is ambiguous — it can mean "go ahead" or "make the repo public". A misinterpretation briefly made a private repo public before being reverted. Fix: the audit skill now requires three explicit confirmations before any visibility change. General rule: agents must never default-assume on high-impact actions from ambiguous instructions.
2. **Archive classification value is real though hard to quantify.** "Hard to quantify ≠ low value" — classification quality directly determines future retrieval efficiency. Add a one-line "reuse hint" (when will this be needed again) at archive time to make the future value explicit.
3. **Auxiliary-model auto-detection pitfall.** Hermes' auxiliary chain (auto mode) probes providers in order (main provider → OpenRouter → Nous Portal → …). If credentials exist but are unfunded, every probe logs payment/credit errors. Fix: explicitly pin `auxiliary.<task>.provider` to the main provider.
4. **Memory grows on its own.** A background curator promotes session facts into memory automatically; without a governance cadence the file drifts toward the cap. The watchdog + monthly review provide the missing cadence.
5. **Approval defense line must be verified.** `approvals.mode: off` (yolo) means no command ever prompts. After an incident, it was set to `smart` (auto-approve low-risk, deny high-risk, prompt when uncertain) — and the change requires a gateway restart to take effect.

## Scope Boundary / 边界说明

This report contains methods, metrics, and process lessons only — no private memory contents, no server internals, no personal data. The repository itself remains private until the project is complete.

本报告仅含方法、指标与流程教训——不含任何隐私记忆内容、服务器内部信息或个人数据。仓库在项目完成前保持私有。

## Update 2026-08-24 — v1.2.0 / 更新

- **Old-memory archive landed** / 旧记忆归档落地：deleted memory entries now go to a dedicated 旧记忆归档 category with a full record (original text + deletion reason + successor + date + reuse hint); the "superseded" semantics resolves old-vs-new preference ambiguity.
- **Snapshot dating landed** / 快照标注落地：volatile facts (versions, quotas, service states, audit results) carry @YYYY-MM markers; the health script flags them as Review candidates as they age — staleness is visible by design.
- **Tailoring decision** / 裁剪决策：three repo rules (conflict-blocking, retention state machine, rollback plan) were deliberately NOT adopted. This pipeline is fully human-gated (every write/archive/delete passes user confirmation), so blocking rules are redundant — the human is the conflict-resolution mechanism. Now documented as "Tailoring Modes" in SKILL.md v1.2.0.
- **Current measured state** / 当前水位：MEMORY.md 82.5% / USER.md 80.1%, both healthy; all governance scripts verified exit-0.

### New lessons / 新教训

5. **Whole-entry replacement trap.** The `memory` tool's `replace` identifies an entry by substring but replaces the ENTIRE entry — a partial edit accidentally truncated entry content (restored same day). Fix: on replace, always supply the complete new entry text. 整条替换陷阱：replace 按子串定位但整条替换——须提供完整新条目文本。
6. **Tailor rules to automation level.** Generic governance rules are defensive; a fully human-gated pipeline can safely drop blocking rules. Applying universal rules without checking the pipeline's gating adds ceremony without protection. 规则按自动化程度裁剪：人审制管线可安全去掉堵截类规则。

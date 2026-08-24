# Changelog

All notable changes to this project.

## [1.2.3] - 2026-08-24

### Added

- Semi-automated deployment reference (`references/semi-automated-pattern.md`): conflict-blocking state machine, minimal conflict detection, rollback and audit patterns for unattended pipelines — 半自动落地参考：冲突阻塞状态机、最小冲突检测、回滚与审计
- Source snapshot retention principle (SKILL.md + blueprint §5b): keep dated raw API/HTML snapshots and cited PDFs alongside conclusions, with naming rules; process artifacts excluded — 原始资料留存原则：结论随附带日期的原始快照与引用 PDF
- Expanded `references/openclaw-invocation.md`: three-zone path mapping, zero-token cron executors, health-check adaptation, deployment checklist — OpenClaw 部署参考扩充
- Runtime-adaptation note in `scripts/memory_health.py` (Hermes conventions vs other runtimes) — health 脚本多运行时适配说明

### Fixed

- Version number consistency: SKILL.md frontmatter bumped from 1.2.0 to 1.2.3 to match CHANGELOG — 版本号一致

## [1.2.2] - 2026-08-24

### Added

- Practice report lesson 8: dangling terminal cwd (cd out before deleting directories) — 实践报告第 8 条教训（终端 cwd 悬空）

### Fixed

- Duplicate lesson numbering in the practice report (new lessons renumbered 5→6, 6→7) — 实践报告新教训编号与原有 1–5 撞号，已改为 6/7
- README lesson count corrected to 8 (5 original + 3 new) — README 教训计数修正为八条

## [1.2.1] - 2026-08-24

### Fixed

- README repository layout now lists `references/implementation-blueprint.md` and `scripts/` — 目录结构补全
- README lesson count corrected 5 → 6 (v1.2.0 added two lessons) — 教训计数修正
- Dangling `scripts/memory_health.py` reference resolved: script now ships in the repo as the authoritative copy — 悬空脚本引用修复
- Blueprint scope note: blocking rules (§4) apply to semi-automated deployments; Hermes runs human-gated — 蓝图适用范围注明

### Removed

- Unverified `agents/openai.yaml` (OpenClaw format never tested); OpenClaw config documented solely in `openclaw-invocation.md` until verified — 移除未经实测的 OpenClaw 配置

## [1.2.0] - 2026-08-24

### Added

- Old-memory archive design: dedicated category for deleted memory entries with a full record (original text, reason, successor, date, reuse hint); category semantics = "superseded" — 旧记忆归档设计（带完整裁决记录，语义"已被取代"）
- Snapshot dating for volatile facts (@YYYY-MM), making staleness detectable by health checks — 易变事实快照日期标注，时效性可检测
- Tailoring Modes: human-gated vs semi-automated pipelines, and when blocking rules can be safely dropped — 裁剪模式：人审制 vs 半自动
- Hermes practice report updated with v1.2.0 results and two new lessons (whole-entry replace trap; tailoring by automation level) — 实践报告更新

## [1.1.0] - 2026-08-24

### Added

- Quantified health indicator thresholds (`<85%` healthy / `85–95%` review / `>95%` urgent; stale-date and overlong flags) — 量化健康指标阈值
- Reuse hint as a standard element of archiving — 归档复用线索标准要素
- Confirmation modes: full vs low-friction batch (simple affirmatives) — 确认模式：完整 vs 低摩擦批量
- High-impact action boundary: visibility changes, batch rewrites, permission changes, mass moves — with recommended three-step confirmation — 高影响动作边界与三步确认
- Implementation blueprint (`references/implementation-blueprint.md`) — 实施蓝图
- Platform verification status in README (Hermes verified; OpenClaw/Codex pending) — 平台验证状态

## [1.0.0] - 2026-08

### Added

- Initial bilingual governance skill (SKILL.md) — 初始双语治理技能
- OpenClaw agent interface config + invocation notes — OpenClaw 适配与部署说明
- Hermes Agent integration guide — Hermes 落地指南
- Hermes practice report (landing results & lessons) — Hermes 实践报告
- Bilingual README + MIT license — 双语 README 与 MIT 协议

# Changelog

All notable changes to this project.

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

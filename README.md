# Agent Memory Governance / Agent 记忆治理

A governance guide for long-running AI agents: keep active memory separate from reference archives, surface contradictions, and define user-confirmed forgetting boundaries.

长期运行 Agent 的记忆治理指南：活跃记忆与参考归档隔离、冲突必须展示、遗忘边界由用户确认。

## Why / 为什么需要

Agents accumulate memory without discipline — bloat, silent overwrites, contradictory claims. This repository provides **principles, not a fixed workflow**: each agent designs its own implementation from its own tools, storage, and runtime.

Agent 的记忆会无纪律地膨胀——臃肿、静默覆盖、自相矛盾。本仓库提供**原则而非固定流程**：每个 Agent 基于自身工具与存储自行设计实现。

## Core Principles / 核心原则

1. **Three-zone isolation** — active memory / reference archive / transient conversation stay separate. 三区隔离：活跃记忆 / 参考归档 / 临时对话。
2. **Surface contradictions** — show conflicting claims, sources, time clues; the user decides. 冲突必须展示，用户裁决。
3. **Archive requires confirmation** — reading a link is not consent. 归档必须明确确认，阅读≠同意。
4. **Archive before delete** — deletion needs explicit confirmation and a permitted executor. 归档先于删除，删除需确认。
5. **Age is not evidence** — old content can still matter. 仅凭时间不能证明内容不重要。

## Repository Layout / 目录结构

```
├── SKILL.md                        # The governance guide itself / 治理指南本体
├── scripts/
│   └── memory_health.py            # Health-check script (stdlib, reference impl) / 健康检查脚本
└── references/
    ├── implementation-blueprint.md # Implementation templates / 实施模板
    ├── openclaw-invocation.md      # OpenClaw deployment notes / OpenClaw 部署说明
    ├── hermes-integration.md       # Hermes Agent integration guide / Hermes 落地指南
    └── hermes-practice-report.md   # Measured results & lessons (2026-08-24) / 实践验证报告
```

## Platform Support / 平台适配

| Platform | How it fits / 接入方式 | Verified / 验证状态 |
|---|---|---|
| **OpenClaw** | User-invocable only, model-invocation disabled (`$agent-memory-governance`) — see `openclaw-invocation.md` | ⏳ 待验证 |
| **Codex** | `SKILL.md` uses standard frontmatter — drop it into your skills dir | ⏳ 待验证 |
| **Hermes Agent** | Companion `memory-governance` skill + health scripts + cron cadence — see `hermes-integration.md` | ✅ 已验证 2026-08-24（见 practice report） |

## Verified in Practice / 实践验证

Landing on Hermes Agent (2026-08-24): memory capacity **99% → 79%**, retrieval across taxonomy zones verified, deleted entries recoverable from session history. Full details and eight hard-won lessons in [`references/hermes-practice-report.md`](references/hermes-practice-report.md).

已在 Hermes Agent 实际落地验证（2026-08-24）：记忆占用 **99% → 79%**，跨分类区检索验证通过，已删条目可从会话历史找回。完整细节与八条经验教训见[实践报告](references/hermes-practice-report.md)。

# OpenClaw Invocation & Deployment / OpenClaw 部署参考

> 配套 `hermes-integration.md`，说明本 Skill 在 OpenClaw 运行时的调用方式与三区落地。OpenClaw 与 Hermes 的注入模型不同：多个根级 markdown 文件自动注入 system prompt，不只有 MEMORY/USER。

## 1. Skill 元数据

OpenClaw 的 skill 元数据放在 `SKILL.md` frontmatter（注意：Codex 风格的校验器只接受它支持的 key，OpenClaw 专属字段放在 `metadata.openclaw` 下）：

```yaml
---
name: agent-memory-governance
version: 1.2.3
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin"]}}
---
```

- `user-invocable: true`：作为 `/agent-memory-governance` 斜杠命令暴露给用户。
- `disable-model-invocation: true`：**不进模型 system prompt**，只在用户调用或深度审计时加载。治理的"底线规则"应写进每次注入的 AGENTS.md，而不是靠加载这个 skill。

## 2. 三区路径映射

| 区 | OpenClaw 路径 | 注入方式 | 保留 |
|---|---|---|---|
| 活跃记忆 | `MEMORY.md` `AGENTS.md` `TOOLS.md` `SOUL.md` `USER.md` `IDENTITY.md` `HEARTBEAT.md` | 自动注入 system prompt | 永久，经确认改 |
| 参考归档 | `analysis/<科目>/YYYY-MM/` `qa-archive/<科目>/YYYY-MM/` `memory/tombstone/` | 不注入，memory_search/grep 按需检索 | 长期 |
| 临时对话 | `memory/YYYY-MM-DD.md` | 当日文件存在时注入 | N 天后归档 |

科目分类用「主题 + 性质」双轴：目录按主题科目（如 ai-tech/medical/ops），文件头用 `类型：研究/论文解读` 这类性质标签。

## 3. 执行器（零 token 脚本 + cron）

治理检查尽量用纯 shell/python 脚本跑在系统 cron 上，**不消耗模型 token**：

- 归档清理：每日移动超期 daily note → `memory/archive/`，再按 TTL 软删（文件名日期判定，不依赖 relatime）。
- 候选扫描：每日扫 T-7 前的对话，产出待归档清单（只出清单，不归档）。
- 健康检查：每周一统计注入文件容量%、标记含年份/超长/跨文件重复，超 85% 预警。
- 周/月报：每周一汇总状态；每月初出 Keep/Review/Archive/Delete 候选。
- wiki 树：随周报刷新静态导航页（`analysis/WIKI.md`）。

关键经验：**不要把归档扫描挂在 heartbeat/模型对话上**——心跳可能因 target-none 等原因跳过，导致候选长期空转。独立 cron + 状态游标（`scannedThrough`）更可靠。

## 4. health check 适配

官方 `scripts/memory_health.py` 按 Hermes 约定只读 MEMORY/USER、用 `§` 分隔条目。OpenClaw 注入文件更多且没有 `§` 约定，需要：

- 文件列表改为实际注入的 7 个根级 md；
- 条目分隔按自身结构（标题行/列表项），或退化为按行/按容量统计；
- 容量阈值按各文件大小独立设（不同文件上限不同）；
- 脚本应始终 `exit 0`（看门狗/cron 友好，预警靠输出内容不靠非零退出）。

## 5. 落地检查清单

- [ ] 底线规则写入每次注入的 AGENTS.md（三区隔离、展示矛盾、先归档后删、确认）
- [ ] skill 设 `disable-model-invocation: true`，仅审计时加载
- [ ] 归档目录结构与游标文件就位
- [ ] cron 脚本零 token、稳定 exit 0、写日志
- [ ] 删除走回收站/软删，失败不回退 `rm -f`
- [ ] 易变事实带 `@YYYY-MM`；被替换的旧记忆入 tombstone
- [ ] 高影响动作（公开仓库/批量改写/权限变更/推 GitHub/外发消息）三步确认

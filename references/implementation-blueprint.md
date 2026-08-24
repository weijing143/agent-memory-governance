# Implementation Blueprint / 实施蓝图

Practical templates validated on Hermes Agent (2026-08-24, see `hermes-practice-report.md`). Use these as starting points and adapt to your own runtime — they are examples, not mandates.

在 Hermes Agent 上实践验证过的落地模板（2026-08-24，见实践报告）。以此为起点，按自身运行环境调整——是示例而非规定。

## 1. Classification Decision Table / 分级决策表

| Suggestion / 建议 | Signals / 信号 |
|---|---|
| **Keep** | Active project state, tool usage, environment facts, user preferences, in-use experience / 活跃项目状态、工具用法、环境事实、用户偏好、复用中的经验 |
| **Review** | Contains date/version, conflicts with current state, duplicated across files, overlong (>300 chars) / 含日期版本号、与现状冲突、跨文件重复、超长 |
| **Archive** | Low reuse but potentially valuable; move to reference zone after user confirmation / 低复用但有价值；用户确认后移入参考区 |
| **Delete** | Outdated and worthless; only after explicit user confirmation / 过时无价值；仅用户明确确认后 |

## 2. Health Check Essentials / 健康检查要点

- Metrics: entry count, total chars, capacity % (current / limit). 指标：条目数、总字符、容量百分比（当前/上限）。
- Flags: entries containing a year (stale-prone), entries >300 chars (overlong). 标记：含年份（易过期）、超长（>300 字符）。
- Output: one health line per file + flagged-entry list. 输出：每文件一行健康行 + 可疑条目标记列表。
- Pure-stdlib scripts keep this runnable anywhere with zero dependencies. 纯标准库脚本，零依赖随处可跑。

## 3. Candidate List Template / 候选清单模板

```
| 条目摘要 | 建议 | 理由 |
|---|---|---|
| <entry> | Keep/Review/Archive/Delete | <why> |
```

Rules: show the list, wait for user decision, never act on it yourself. 只出清单等用户裁决，绝不自行执行。

## 4. Conflict Display Template / 冲突展示模板

```
冲突：<claim A> vs <claim B>
来源：<source, time clue>
影响：<what breaks>
可选解决：<options>
```

Rules: never silently pick the newest claim; never merge conflicting sources; block automatic processing until the user decides. 不静默选最新、不合并冲突来源，用户裁决前阻塞自动处理。

## 5. Archive Confirmation Dialogue / 归档确认对话

```
Agent: 建议归档到[分类]？（复用线索：什么场景会再次需要）
User:  可以/好/行        → batch execution / 批量执行
       <改分类>          → follow user category / 按用户分类
       拒绝              → no repeated prompting / 不重复追问
```

## 6. Governance Cadence / 治理节奏

| Cadence | Action |
|---|---|
| Daily | Silent retention cleanup / 静默清理 |
| Weekly | Health report (auto-collected data + short summary) / 健康周报 |
| Monthly | Full Keep/Review/Archive/Delete review, candidate list for user / 完整分级复盘，清单交用户 |
| Event-driven | After economics/finance/work/law/science/tech/programming/AI/link-analysis work, ask whether to archive / 重要工作后主动问归档 |

Design rule: script-only jobs run silent (zero tokens); governance jobs only produce lists for user decision; no high-impact action is ever automated. 设计原则：纯脚本任务静默（零 token）；治理任务只出清单；高影响动作绝不自动。

## 7. High-Impact Action Checklist / 高影响动作检查清单

Before any visibility change (repo public), batch rewrite, permission change, or mass move:

任何可见性变更（仓库转公开）、批量改写、权限变更、批量移动前：

1. User intent explicit and unambiguous — ask first if the instruction is ambiguous. 用户意图明确无歧义——歧义先问。
2. Readiness/completion status confirmed. 就绪/完成状态已确认。
3. Required audits (e.g. secret scan) clean. 必要审计（如密钥扫描）干净。

If the user later objects, revert immediately if possible; bounded exposure requires the audits from step 3. 用户事后反对立即回退；步骤 3 的审计保证暴露风险可控。

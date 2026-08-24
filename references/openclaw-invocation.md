# OpenClaw Invocation / OpenClaw 调用

Configure this Skill in OpenClaw as user-invocable and model-invocation disabled. Use the equivalent OpenClaw metadata:

在 OpenClaw 中将此 Skill 设置为用户可调用，并禁止模型自动调用。使用对应元数据：

```yaml
user-invocable: true
disable-model-invocation: true
```

Recommended triggers are `$agent-memory-governance` and `/agent-memory-governance`. Do not load the Skill for ordinary conversation. When the trigger is present, follow `SKILL.md`; otherwise treat the Skill as inactive.

推荐触发方式是 `$agent-memory-governance` 和 `/agent-memory-governance`。普通对话不要加载此 Skill；只有出现触发词时才读取 `SKILL.md`。

Keep the two metadata fields in the OpenClaw-specific manifest or deployment copy rather than Codex `SKILL.md`, because Codex's Skill validator accepts only its supported frontmatter keys.

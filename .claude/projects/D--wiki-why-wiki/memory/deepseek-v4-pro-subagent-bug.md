---
name: deepseek-v4-pro-subagent-bug
description: deepseek-v4-pro 模型无法启动子 agent（Agent/Workflow 均失败）
metadata:
  type: project
---

deepseek-v4-pro 模型带有 `reasoning_effort` 参数。当 Claude Code 尝试启动子 agent（Agent 工具）时，API 层会传 `thinking: {type: "disabled"}`，与父模型的 `reasoning_effort` 冲突，报错：`thinking options type cannot be disabled when reasoning_effort is set`。

所有子 agent 类型（claude-code-guide、general-purpose、Explore）均受影响，Workflow 同样不可用。

**Why:** deepseek-v4-pro 的 reasoning_effort 与 Claude Code 子 agent 默认禁用 thinking 的行为不兼容。

**How to apply:** 需要子 agent 或 Workflow 时，切换到 deepseek-v4-flash 或原生 Claude 模型（Opus 4.8、Sonnet 4.6 等）。

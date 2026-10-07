---
type: entity
title: "v2rayN"
tags: [v2rayN, Windows, proxy]
related: ["[[codex]]", "[[codex-remote-proxy]]", "[[local-2026-codex-remote-vpn]]"]
created: 2026-10-07
updated: 2026-10-07
---

# v2rayN

在 [[local-2026-codex-remote-vpn]] 的 Windows 案例中，v2rayN 提供 [[codex]] 代理启动所使用的本地代理。

## 本 wiki 关注点

- 系统代理模式与 TUN 是否启用，是判断应用网络路径的不同条件。
- 应用能否实际经过本地代理，需要结合显式请求、后台连接日志及最终使用结果验证，见 [[codex-remote-proxy]]。
- 该案例的端口与使用步骤集中在 [[local-2026-codex-remote-vpn]]，迁移时应核对实际监听设置。

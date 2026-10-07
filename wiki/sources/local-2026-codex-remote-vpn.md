---
type: source
title: "Windows Codex 手机远程连接：代理配置与排障记录"
authors: []
year: 2026
url: ""
venue: "本机操作记录"
tags: [Codex, remote, Windows, v2rayN, proxy, troubleshooting]
related: ["[[codex]]", "[[v2rayn]]", "[[codex-remote-proxy]]"]
created: 2026-10-07
updated: 2026-10-07
---

# Windows Codex 手机远程连接：代理配置与排障记录

> 原文：`raw/articles/Codex-Remote-VPN.md`（原样归档）。原文件位于 `C:\Users\Administrator\.codex\scripts\Codex-Remote-VPN.md`；实施日期为 2026-10-01，原文整理日期为 2026-10-06（Asia/Shanghai）。原文未署名。

适用环境：Windows [[codex]] 桌面 App、[[v2rayn]] 本地代理，以及手机 ChatGPT 的 Codex/Remote 入口。本文保留当时的本机操作方案；可复用的判断方法见 [[codex-remote-proxy]]。

## 核心结论

1. 电脑开启远程控制时提示“无法启用远程控制，请确保仅有一个 ChatGPT 实例在运行”，重启 App 后仍未解决。进程与登录会话检查没有发现第二个主实例，后台日志则显示远程连接持续超时。
2. 显式通过 v2rayN 访问同一服务端接口可以收到 HTTP 响应。补充代理启动配置并重启后，用户确认手机连接成功，并从手机在原聊天中发送消息。
3. 只启用 Windows 系统代理，未必让所有后台连接使用代理。本次同时启用了系统代理支持、代理环境变量和浏览器代理参数，**没有逐项隔离测试**，无法确定哪一项单独足以修复。
4. 手机与电脑的 VPN 保持原样，仍然连接成功；本次没有证据要求两端换成相同 VPN。

## 排查证据与结论边界

| 检查 | 当时结果 | 能说明什么 |
|---|---|---|
| 桌面进程与父子关系 | 一个 `ChatGPT.exe` 主实例，其余为渲染、网络等辅助进程 | 不能仅按进程数量判断多个 App 实例 |
| Windows 登录会话 | 只有一个活动会话 | 当时未发现另一登录会话运行 App |
| v2rayN 配置 | 系统代理为 `127.0.0.1:10808`，TUN 关闭 | 使用本地代理模式，没有接管全部流量 |
| 后台远程控制日志 | 连接 `wss://chatgpt.com/backend-api/wham/remote/control/server`，反复出现 `os error 10060` | 电脑端到远程控制服务的连接超时 |
| 不走代理的 HTTPS 请求 | 连接超时 | 当时直连该接口不可达 |
| 显式走代理的 HTTPS 请求 | 返回 HTTP `426` | 通过代理能到达服务端，不代表认证或 WebSocket 握手完成 |
| 修改后实际使用 | 用户确认手机连接成功，并从手机发送消息 | 整体方案在这台电脑上实际有效 |

后台连接未正确经过代理，是这些证据支持的最有力解释。但没有追踪每条网络连接，也没有确认界面为何把故障显示成“多个实例”。以上是原记录的验证结果，本次收录没有重新执行连接测试。

## 本机配置方案

### Codex 用户配置

在 `%USERPROFILE%\.codex\config.toml` **现有**的 `[features]` 段中添加一项，保留其他配置，不要重复创建该段：

```toml
[features]
respect_system_proxy = true
```

当时 Codex 后台版本为 `0.159.2`，此项在 `features list` 中标为 `under development`。升级后需要重新检查支持情况，不能视为永久稳定接口。这是用户级 Codex 配置，使用同一配置的 CLI 等入口也可能受影响。

### 代理启动脚本

原电脑的脚本路径：`%USERPROFILE%\.codex\scripts\Start-Codex-WithProxy.ps1`。

脚本先通过 `Get-AppxPackage -Name OpenAI.Codex` 查找安装包，避免固定特定版本的安装目录；再测试现有代理能否到达服务端。探测失败时停止，不重启 App。通过探测后，在启动脚本的进程环境中设置：

```text
HTTP_PROXY=http://127.0.0.1:10808
HTTPS_PROXY=http://127.0.0.1:10808
ALL_PROXY=http://127.0.0.1:10808
NO_PROXY=localhost,127.0.0.1,::1
```

启动桌面 App 时另传入：

```text
--proxy-server=http://127.0.0.1:10808
```

环境变量由新启动的 Codex 及正常继承环境的子进程使用，没有写入 Windows 用户或系统的永久环境变量。该设置没有按域名限定代理范围，子进程的其他联网操作也可能使用代理。

当时脚本在 `$proxyUrl` 和 `--proxy-server` 参数两处固定使用 `10808`，修改 v2rayN 监听端口时必须同步修改。

### 启动入口与辅助文件

桌面快捷方式 **Codex (VPN).lnk** 通过隐藏的 Windows PowerShell 窗口运行启动脚本。旧快捷方式或开始菜单入口不会自动获得脚本设置的环境变量，日常应使用 **Codex (VPN)**。

快捷方式的图标引用了当时 App 的版本目录。升级后如果仅图标失效，可更新图标路径；启动脚本仍动态查找安装包。

| 原电脑上的文件 | 用途 |
|---|---|
| `%USERPROFILE%\.codex\scripts\Start-Codex-WithProxy.ps1` | 代理启动、可选重启与验证 |
| `%USERPROFILE%\.codex\scripts\check-codex-remote-proxy.py` | 只读查询日志 SQLite 数据库，检查指定时间之后的远程连接状态 |
| `%USERPROFILE%\.codex\scripts\codex-proxy-status.txt` | 最近一次脚本启动及可选检查结果 |
| `%USERPROFILE%\.codex\proxy-setup-backup-20261001\config.toml.before-proxy` | 修改前的配置备份 |

本次 wiki 收录仅归档 Markdown 原文，上述脚本、状态文件、快捷方式和备份未作为附件收录。以下命令依赖原电脑已有的脚本。

首次实施曾启动一次延迟约 30 秒的重启辅助进程，没有创建持续运行的代理服务或定时任务；没有修改 VPN 节点、手机 VPN、Tailscale、系统代理注册表或防火墙，也没有开启 TUN。

## 日常使用

1. 启动 v2rayN，确保 `127.0.0.1:10808` 可用。
2. 如果 Codex 已在运行，先从托盘彻底退出。普通启动脚本会拒绝在已有主实例运行时启动，避免新环境没有生效。
3. 双击桌面 **Codex (VPN)**。
4. 在手机 Codex/Remote 中选择电脑，继续原任务或新建任务。
5. 工作期间保持电脑唤醒、联网，并保持 Codex 与 v2rayN 运行。

需要重启并检查时，在独立 PowerShell 窗口运行：

```powershell
& "$env:USERPROFILE\.codex\scripts\Start-Codex-WithProxy.ps1" -Restart -Verify
```

`-Restart` 会核对主进程路径与创建时间，再强制结束 App 进程树，正在运行的任务会中断。运行前应保存手动编辑内容，并等待其他任务结束。不要在即将被重启的 Codex 内执行此命令，并期待当前工具调用保持连续。

## 验证与排障

查看最近一次启动记录：

```powershell
Get-Content "$env:USERPROFILE\.codex\scripts\codex-proxy-status.txt"
```

使用 `-Verify` 时，脚本每 5 秒检查一次，最多约 60 秒。只有检测到日志中的 `next_status=Connected` 才输出 `CONNECTED`；否则可能输出 `FAILED` 或 `PENDING`。

| 验证层次 | 成功信号 | 仍不能证明 |
|---|---|---|
| 服务端可达 | 启动探测收到 HTTP 响应，如 `426` | 认证与 WebSocket 连接已经完成 |
| 后台连接 | 日志出现 `next_status=Connected` | 手机已配对、之后一直可用 |
| 手机实际使用 | 手机连接电脑并成功发送消息 | 将来或其他电脑也始终可用 |

状态文件每次启动都会覆盖。原文在 2026-10-06 核对时，文件只保留了 2026-10-03 的启动记录与 HTTP `426`，不能替代此前用户对手机连接成功的确认。

`-Verify` 当时固定使用原电脑上的 Python 3.12 安装路径，迁移时需要修改；普通启动不依赖 Python。日志检查还依赖当时的 SQLite 表结构与状态字段，App 升级后可能需要调整。

再次失败时依次检查：

1. 是否从 **Codex (VPN)** 启动。
2. v2rayN 是否运行，监听端口是否仍为 `10808`。
3. 状态文件是否报告代理不可达，后台日志是否再次出现 `10060`。
4. App 是否更新、电脑是否休眠、两端是否仍使用相同账号和工作区。

再次出现“多个实例”提示时，应先核对进程树与连接日志，再决定后续处理，避免直接重置 App 或删除登录数据。

## 恢复原设置

1. 从当前 `config.toml` 的 `[features]` 段删除本次新增的 `respect_system_proxy = true`。
2. 完全退出 Codex，再从原来的开始菜单或快捷方式启动，以清除脚本带来的进程环境。
3. 不再需要时，可删除 **Codex (VPN)** 快捷方式、本次新增的启动脚本、检查脚本与状态文件。

备份用于对照。**不要直接用 2026-10-01 的完整备份覆盖当前配置**，否则可能丢失之后新增的插件、项目等设置；优先只撤销本次新增项。

## 迁移前需要确认

- 新版本是否仍支持 `respect_system_proxy`，是否仍需要组合配置？原记录没有单项验证结果。
- 新电脑的代理端口、安装包名称、Python 路径以及日志数据库结构是否相同？
- “多个实例”提示与实际网络故障的映射是否已在新版 App 中改变？原记录没有确认其内部原因。

## 原文列出的官方参考

- [Remote connections](https://learn.chatgpt.com/docs/remote-connections)：配对、电脑可用性要求及安全中继说明。
- [Codex Remote](https://learn.chatgpt.com/docs/remote)：手机启动、引导、审批和查看电脑端任务。

本文是本机方案与历史验证记录，不是自动加载的 Codex 指令或通用 skill。

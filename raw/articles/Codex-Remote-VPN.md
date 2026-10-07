# Windows Codex 手机远程连接：代理配置记录

整理日期：2026-10-06（Asia/Shanghai）  
实施日期：2026-10-01  
适用环境：Windows Codex 桌面 App、v2rayN 本地代理、手机 ChatGPT 的 Codex/Remote 入口。

## 已验证的结论

电脑启用远程控制时曾提示“无法启用远程控制，请确保仅有一个 ChatGPT 实例在运行”。重启应用后问题仍然存在。

排查确认电脑只有一个 Codex 桌面主实例。后台远程控制连接持续超时，而显式经过 v2rayN 代理后，同一服务端接口可以返回 HTTP 响应。为 Codex 增加代理启动环境并重启后，用户成功从手机连接电脑，并在原聊天中发送消息。

可复用的经验是：**看到实例冲突提示时，应同时核对进程关系和后台日志；只开启 Windows 系统代理，未必足以让应用所有后台连接走代理。**

电脑和手机使用不同 VPN 并非本次修复必须改变的条件。两端 VPN 保持原样，连接仍然成功。

## 排查证据与结论边界

| 检查 | 当时结果 | 能说明什么 |
|---|---|---|
| 桌面进程及父子关系 | 一个 `ChatGPT.exe` 主实例，其余为渲染、网络等辅助进程 | 不能仅按进程数量判断多个 App 实例 |
| Windows 登录会话 | 只有一个活动会话 | 当时未发现另一个登录会话运行 App |
| v2rayN 配置 | 系统代理为 `127.0.0.1:10808`，TUN 关闭 | 采用本地代理模式，没有接管全部网络流量 |
| 后台远程控制日志 | 连接 `wss://chatgpt.com/backend-api/wham/remote/control/server`，反复出现 `os error 10060` | 电脑端到远程控制服务的连接超时 |
| 不走代理的 HTTPS 请求 | 连接超时 | 当时直连该接口不可达 |
| 显式走代理的 HTTPS 请求 | 返回 HTTP `426` | 通过代理能到达服务端；不代表已完成认证或 WebSocket 握手 |
| 修改后实际使用 | 用户确认手机连接成功，并从手机发送消息 | 整体方案在这台电脑上实际有效 |

结合这些证据，后台连接未正确经过代理是本次故障最有力的解释。不过，没有追踪每条网络连接，也没有确认为什么界面把故障显示成“多个实例”。

本次一起启用了系统代理支持、代理环境变量和浏览器代理参数，没有逐项隔离测试，不能声称其中某一项单独就足以修复。

## 实际修改了什么

### 1. Codex 用户配置

在 `%USERPROFILE%\.codex\config.toml` 的现有 `[features]` 段新增：

```toml
[features]
respect_system_proxy = true
```

只添加这一项，保留其他配置。不要复制示例时重复创建 `[features]` 段。

当时使用的 Codex 后台版本为 `0.159.2`，该开关在 `features list` 中标为 `under development`。升级后如行为变化，应重新检查支持情况，不能把它视为永久稳定的接口。

这是用户级 Codex 配置，同样使用该配置的 CLI 等入口也可能受影响；它不是 Windows 全局代理设置。

### 2. 代理启动脚本

创建了 [Start-Codex-WithProxy.ps1](Start-Codex-WithProxy.ps1)。主要行为：

1. 通过 `Get-AppxPackage -Name OpenAI.Codex` 查找已安装 App，避免将特定版本的安装目录固定在启动逻辑中。
2. 先测试现有 v2rayN 代理能否到达服务端。连接失败时停止，不重启 App。
3. 在启动脚本的进程环境中设置：

   ```text
   HTTP_PROXY=http://127.0.0.1:10808
   HTTPS_PROXY=http://127.0.0.1:10808
   ALL_PROXY=http://127.0.0.1:10808
   NO_PROXY=localhost,127.0.0.1,::1
   ```

4. 启动桌面 App 时传入：

   ```text
   --proxy-server=http://127.0.0.1:10808
   ```

环境变量由新启动的 Codex 及其正常继承环境的子进程使用，没有写入 Windows 用户或系统的永久环境变量。这不是按域名限定的代理规则，Codex 子进程的其他联网操作也可能使用该代理。

脚本当前有两个地方固定使用 `10808`：`$proxyUrl` 和启动参数中的 `--proxy-server`。如修改 v2rayN 的监听端口，两处都要修改。

### 3. 桌面快捷方式

创建 `Codex (VPN).lnk`，通过隐藏的 Windows PowerShell 窗口运行上述脚本。

普通开始菜单或旧快捷方式不会自动获得这段脚本设置的环境变量。日常使用应从 **Codex (VPN)** 启动。

快捷方式的图标位置使用当时 App 的版本目录。升级后如果只有图标失效，应更新图标路径；实际启动脚本仍会动态查找安装包。

### 4. 检查脚本、状态文件和备份

| 文件 | 用途 |
|---|---|
| [check-codex-remote-proxy.py](check-codex-remote-proxy.py) | 只读查询 Codex 的日志 SQLite 数据库，检查指定时间之后的远程连接状态 |
| [codex-proxy-status.txt](codex-proxy-status.txt) | 记录最近一次脚本启动及可选检查结果 |
| `../proxy-setup-backup-20261001/config.toml.before-proxy` | 修改前的 Codex 配置备份 |

首次实施时，还启动了一次延迟约 30 秒的重启辅助进程，让新设置生效。这是一次操作，没有创建持续运行的代理服务或定时任务。

没有修改 VPN 节点、手机 VPN、Tailscale、系统代理注册表或防火墙，也没有开启 TUN。

## 日常使用

1. 启动 v2rayN，确保本地代理 `127.0.0.1:10808` 可用。
2. 如果 Codex 已经运行，先从托盘彻底退出。普通脚本会拒绝在已有主实例运行时启动，以免新环境没有生效。
3. 双击桌面的 **Codex (VPN)**。
4. 在手机 Codex/Remote 中选择这台电脑，继续原任务或新建任务。
5. 远程工作期间，保持电脑唤醒、联网，并让 Codex 和 v2rayN 持续运行。

需要脚本重启并检查时，可在独立 PowerShell 窗口运行：

```powershell
& "$env:USERPROFILE\.codex\scripts\Start-Codex-WithProxy.ps1" -Restart -Verify
```

`-Restart` 会核对主进程路径和创建时间，再强制结束该 App 的进程树；正在运行的任务会中断。运行前应保存手动编辑的内容并等待其他任务结束。不要从要被重启的 Codex 内直接执行这一命令来期待当前工具调用保持连续。

## 如何验证与排障

查看最近一次启动记录：

```powershell
Get-Content "$env:USERPROFILE\.codex\scripts\codex-proxy-status.txt"
```

使用 `-Verify` 时，启动脚本每 5 秒检查一次，最多检查约 60 秒。检测到日志中的 `next_status=Connected` 才输出 `CONNECTED`；否则可能是 `FAILED` 或 `PENDING`。

注意检查的边界：

- 启动探测收到 HTTP 响应，只证明接口可达，不证明远程连接完成。
- 日志出现 `CONNECTED` 证明服务端连接曾成功，不保证手机已经配对，也不保证连接以后一直可用。
- 状态文件在每次启动时会被覆盖。2026-10-06 核对时，文件只保留了 2026-10-03 的启动记录和 HTTP `426`，不能代替之前用户确认的手机连接成功。
- `-Verify` 当前固定使用原电脑上的 Python 3.12 安装路径。迁移到其他电脑时需要修改；普通启动不依赖 Python。
- 日志检查依赖当时的 SQLite 表结构和状态字段，App 升级后可能需要调整。

再次失败时，按以下顺序检查：

1. 是否从 **Codex (VPN)** 启动，而不是旧入口。
2. v2rayN 是否运行，端口是否仍为 `10808`。
3. 状态文件是否报告代理不可达，后台日志是否再次出现 `10060`。
4. App 是否更新、电脑是否休眠、两端是否仍使用相同账号和工作区。

不要因为界面再次提示“多个实例”，就直接重置 App 或删除登录数据。先核对进程树及连接日志。

## 恢复原设置

1. 从当前 `config.toml` 的 `[features]` 段删除本次新增的 `respect_system_proxy = true`。
2. 完全退出 Codex，随后用原来的开始菜单或快捷方式启动，清除代理启动脚本带来的进程环境。
3. 不再需要时，可删除 **Codex (VPN)** 快捷方式及本次新增的代理脚本、检查脚本和状态文件。

备份可用于对照。**不要直接用 2026-10-01 的完整备份覆盖现在的配置**，否则可能丢失之后新增的插件、项目和其他设置。优先只撤销本次新增的配置项。

## 官方参考

- [Remote connections](https://learn.chatgpt.com/docs/remote-connections)：配对、电脑可用性要求及安全中继说明。
- [Codex Remote](https://learn.chatgpt.com/docs/remote)：手机启动、引导、审批和查看电脑端任务。

本文是本机方案及已验证经验的操作记录，不是自动加载的 Codex 指令或通用 skill。迁移到其他环境时，应重新确认代理端口、安装包名称、Python 路径和 App 版本。

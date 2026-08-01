---
type: concept
title: BSIM 模型家族
tags: [BSIM, MOSFET, compact-model, BSIM3v3, BSIM4, BSIM-CMG, short-channel-effects]
related: ["[[spice]]", "[[spice-model-extraction]]", "[[xinhaishiyi-2026-spice-model]]"]
created: 2026-08-01
updated: 2026-08-01
---

# BSIM 模型家族

> Berkeley Short-channel IGFET Model

BSIM 是 UC Berkeley 开发的 MOSFET 紧凑模型标准，它的演化史本身就是一部半导体工艺缩放史。

## 模型演化

| 模型 | SPICE Level | 参数数 | 工艺节点 | 关键突破 |
|------|-------------|--------|----------|----------|
| BSIM1 | Level 13 | ~60 | >1μm | 首次引入短沟道效应经验参数 |
| BSIM2 | Level 39 | ~100 | 0.5-1μm | 改进的迁移率模型和亚阈值模型 |
| **BSIM3v3** | **Level 49** | **~180** | **0.18-0.5μm** | **统一连续可微电流表达式** |
| BSIM4 | Level 54 | 300+ | <0.13μm | 栅隧穿电流、RSCE、Halo 效应 |
| BSIM-CMG | Level 72 | 500+ | FinFET | 多栅极（Common Multi-Gate）器件 |

## BSIM3v3：收敛性革命

BSIM3v3 的核心突破在于用一个**统一的、连续的、可微的电流表达式**覆盖亚阈值、线性区、饱和区三个工作区。

在此之前，不同工作区用不同公式拼接，边界处导数不连续：

$$I_{ds} = \begin{cases} f_1(V_{gs}, V_{ds}) & \text{subthreshold} \\ f_2(V_{gs}, V_{ds}) & \text{linear} \\ f_3(V_{gs}, V_{ds}) & \text{saturation} \end{cases}$$

这种分段拼接导致牛顿迭代在跨区时雅可比矩阵不可求，仿真器频繁收敛失败。BSIM3v3 的**平滑函数（smoothing function）**设计使 $I_{ds}$ 处处可微，牛顿迭代始终有雅可比矩阵可求。

## BSIM4：深亚微米补丁

BSIM4 补齐了 BSIM3v3 在深亚微米节点的物理短板：

- **栅隧穿电流**：$T_{ox} < 2nm$ 时电子直接隧穿氧化层，产生不可忽略的栅电流
- **Halo/Pocket 注入**：抑制短沟道效应的同时引入**反向短沟道效应（RSCE）**——中等沟道长度器件的 $V_{TH}$ 反而比长沟道更高
- **专门参数组**（DVT0、DVT1、DVT2 等）捕捉 RSCE 反直觉行为

## BSIM-CMG：FinFET 时代

BSIM-CMG 面向 FinFET 多栅极器件，参数突破 500 个，是当前先进节点（7nm 及以下）的建模标准。

## 典型模型参数示例

以 BSIM3v3 Level 49 为例，一个 NMOS 的核心参数组：

| 参数 | 含义 | 影响域 |
|------|------|--------|
| `vth0` | 长沟道阈值电压 | 阈值 |
| `u0` / `ua` / `ub` / `vsat` | 迁移率与速度饱和 | 驱动能力 |
| `pclm` / `pdiblc1` / `pdiblc2` | 沟道长度调制 / DIBL | 饱和区输出电导 |
| `dvt0` / `dvt1` / `dvt2` | 短沟道 VTH 滚降 | 短沟道效应 |
| `cgso` / `cgdo` / `cj` | 寄生电容 | 动态特性 / 开关速度 |

**直觉建模法**（而非死背参数）：建立"参数 → 器件曲线 → 电路性能"的三级映射。例如，环形振荡器偏快 → 先检查重叠电容和结电容，而非迁移率。

## 来源

- [[xinhaishiyi-2026-spice-model]]

---
type: concept
title: SPICE 仿真器
tags: [SPICE, EDA, circuit-simulation, compact-model, Newton-Raphson]
related: ["[[donald-pederson]]", "[[bsim-model]]", "[[spice-model-extraction]]", "[[xinhaishiyi-2026-spice-model]]"]
created: 2026-08-01
updated: 2026-08-01
---

# SPICE 仿真器

> Simulation Program with Integrated Circuit Emphasis

## 什么是 SPICE

SPICE 本质上是一个**数值求解器**，用牛顿-拉夫逊（Newton-Raphson）迭代法求解非线性电路方程组。它的输出精度不取决于自身，而取决于喂给它的器件模型（SPICE Model）的精度：

> 一个设计团队用再好的仿真器，如果挂了一个质量低劣的 SPICE Model，结果是 garbage in, garbage out。

## 历史

| 版本 | 年代 | 里程碑 |
|------|------|--------|
| SPICE1 | 1973 | [[donald-pederson]] 团队在 UC Berkeley 开发，Fortran 实现 |
| SPICE2 | 1975 | 功能完善，成为行业标准 |
| SPICE3 | 1985 | C 语言重写，X11 图形界面 |

商用 EDA 公司基于 SPICE 内核进行了各自的增强和封装：

| 仿真器 | 公司 | 定位 |
|--------|------|------|
| **HSPICE** | Synopsys | 工业界黄金标准，精度优先 |
| **Spectre** | Cadence | 模拟/RF 仿真主流 |
| **Eldo** | Siemens EDA | 混合信号仿真 |
| **ADS** | Keysight | RF/微波仿真 |

## 紧凑模型（Compact Model）

SPICE 的核心依赖是**紧凑模型**——在物理精度和计算效率之间的 trade-off：

| 方法 | 原理 | 精度 | 速度 |
|------|------|------|------|
| **TCAD** | 有限元求解泊松方程 + 载流子连续性方程 | 极高 | 极慢（1000 晶体管需数小时） |
| **Compact Model** | 解析公式 + 经验拟合参数 | 足够好 | 快（数万晶体管秒级） |
| 行为模型 | 理想化行为描述 | 低 | 最快 |

紧凑模型就是 SPICE 找到的那个"足够好"的平衡点。随着工艺微缩，紧凑模型的参数数量持续膨胀：BSIM3v3 ~180 个 → BSIM4 300+ 个 → BSIM-CMG 500+ 个。

## 牛顿-拉夫逊迭代

SPICE 求解非线性电路方程组的核心算法。每一步迭代需求解雅可比矩阵（Jacobian）。**BSIM3v3 的里程碑意义在于**：用统一、连续、可微的电流表达式覆盖所有工作区，保证雅可比矩阵始终可求，从而大幅提高收敛性。在此之前，不同工作区用不同公式拼接，边界处导数不连续，导致仿真器频繁收敛失败。

## 来源

- [[xinhaishiyi-2026-spice-model]]

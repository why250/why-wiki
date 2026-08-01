---
type: source
title: "什么是SPICE Model：从零开始手把手教你搭建一个仿真模型"
authors: [芯海拾遗]
year: 2026
url: "https://mp.weixin.qq.com/s/j6PYhONV9-4jmXr_L6SMIg"
venue: "微信公众号·芯海拾遗"
tags: [SPICE, BSIM, compact-model, process-corner, WAT, Monte-Carlo, parameter-extraction]
related: ["[[spice]]", "[[bsim-model]]", "[[spice-model-extraction]]", "[[process-corner]]", "[[wat]]", "[[monte-carlo-simulation]]", "[[donald-pederson]]", "[[transistor-mismatch]]"]
created: 2026-08-01
updated: 2026-08-01
---

# 什么是SPICE Model：从零开始手把手教你搭建一个仿真模型

> 芯海拾遗公众号，2026-07-30

## 核心要点

1. **SPICE 的起源与本质**：1973 年 Berkeley 的 [[donald-pederson]] 教授开发了第一版 SPICE——一个 Fortran 实现的牛顿-拉夫逊非线性电路方程求解器。仿真精度取决于器件模型而非求解器本身。
2. **紧凑模型的 trade-off**：TCAD 基于有限元求解泊松方程，精确但极慢（1000 晶体管需数小时）；SPICE 紧凑模型是精度与速度之间的平衡点。
3. **BSIM 模型家族**：从 BSIM3v3（~180 参数）→ BSIM4（300+ 参数）→ BSIM-CMG（500+ 参数）。BSIM3v3 的里程碑在于首次用统一、连续、可微的电流表达式覆盖亚阈值/线性/饱和三个区，消除了边界导数不连续导致的收敛问题。
4. **SPICE Model 完整开发流程**：Testkey 设计（200-500 DUT）→ DC I-V 测量 → CV 测量 → 四温度点扫描 → Corner Split → 分步参数提取 → 环形振荡器验证 → 签核，全程 3-6 个月。
5. **SPICE Model 的非永恒性**：模型只是特定工艺窗口内、特定优化策略下的统计拟合结果。同一 FAB 同一节点五年后重提模型会有差异。仿真与 silicon 有差异是正常的，一切以实测为准。

## 关键概念

- [[spice]] — SPICE 仿真器：历史、牛顿-拉夫逊求解器、紧凑模型理念
- [[bsim-model]] — BSIM 模型家族：从 BSIM1 到 BSIM-CMG 的演化
- [[spice-model-extraction]] — 从 Testkey 到 Sign-off 的完整参数提取流程
- [[process-corner]] — 工艺角（Corner）建模：TT/SS/FF/SF/FS 与 PVT 分析
- [[wat]] — WAT（Wafer Acceptance Test）及其三个天生局限
- [[monte-carlo-simulation]] — 蒙特卡洛仿真在电路良率分析中的应用
- [[transistor-mismatch]] — 晶体管失配：Pelgrom 模型与局部随机变异

## 待探究的问题

- BSIM-CMG（FinFET 模型）与 BSIM4 在建模方法论上的核心差异是什么？
- 工艺角模型能否用 ML 方法（如 Gaussian Process）替代传统的分 corner 方法？
- WAT 测试能否扩展到 AC/RF 参数的晶圆级筛选？

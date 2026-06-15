---
type: concept
title: DAC Glitch Asymmetry
tags: [DAC, glitch, dynamic-performance, behavioral-modeling]
related: ["[[andersson-vesterbacka-2005-glitch-asymmetry]]", "[[dac-dynamic-performance]]", "[[dac-timing-errors]]"]
created: 2026-06-15
updated: 2026-06-15
---

# DAC Glitch Asymmetry

电流舵 DAC 中开关单元 rise 和 fall 瞬态不对称导致的输出 glitch 现象。当开关控制信号的上升沿和下降沿不是完全互补时，差分输出的总和不为零，产生净 glitch 能量。

## Andersson & Vesterbacka 模型（2005）

[[andersson-vesterbacka-2005-glitch-asymmetry]] 建立了一个通用行为模型：

### 核心原理

理想的差分 CS-DAC 中，一个单元开启（$s_{on}(t)$）的同时另一个关闭（$s_{off}(t)$），若二者完全对称则 glitch 抵消。实际上：

$$s_{on}(t) \neq s_{off}(t)$$

差分输出应为 $s_D(t) = s_{on}(t) - s_{off}(t)$，但由于开关信号的有限斜率差异，$s_{on}(t) \neq 1 - s_{off}(t)$，出现 glitch。

### Glitch 比例关系

Glitch 的大小与切换的单元数量 g(n) 成正比：

$$glitch(n, t) \propto g(n) \cdot e(t)$$

其中 e(t) 是单位 glitch 脉冲形状，g(n) = |w(n) − w(n−1)| 是相邻采样点之间切换的单元数。

### Input-Referred Glitch 概念

Andersson 提出了"input-referred glitch"概念——将 glitch 建模为添加在离散时间输入信号上的误差序列，将连续时间的 glitch 问题转化为离散时间信号处理问题。

Glitch 建模为输入码差 ΔX(n) 通过线性滤波器 h(k)：

$$y(n) = \sum_k h(k) \cdot \Delta X(n-k)$$

### 频域特性

- Thermometer-coded DAC 中，glitch 主导的 SFDR 以 20 dB/dec 随频率衰减
- SFDR ∝ 1/f²（即输入频率每翻倍，SFDR 下降约 20 dB）
- Binary-weighted DAC 中 glitch 产生偶数阶失真
- Thermometer-coded DAC 中 glitch 产生奇数阶失真为主

### 差分输出的共模误差

即使差分输出理想，common-mode 输出中可能存在 glitch 能量。这在差分设计中常被忽略但实际影响系统级性能（如驱动变压器或 balun 时的共模抑制问题）。

## 与 Doris 时序误差框架的对比

| 方面 | [[dac-timing-errors]]（Doris） | Glitch Asymmetry（Andersson） |
|------|------|------|
| 误差源 | 开关时序偏差（静态失配） | rise/fall 不对称（动态开关行为） |
| 建模域 | 统计模型 + TNL | 信号处理模型 + 单位 glitch 脉冲 |
| 依赖 | 失配 spread σ | 开关信号斜率不对称 |
| SDR 公式 | 闭合解析公式 | 比例常数需仿真标定 |

两种机制在高频下同时作用，实际设计中需要综合考虑。

## 与其他概念的关系

- [[dac-dynamic-performance]]：glitch 是动态性能中的非线性失真来源
- [[dac-switching-schemes]]：thermometer vs binary 编码决定了 g(n) 的统计分布
- [[current-steering-dac]]：CS-DAC 架构中差分开关的物理实现决定了 glitch 严重程度
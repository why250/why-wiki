---
type: concept
title: DAC 动态性能四大影响因素
tags: [DAC, dynamic-performance, glitch, feedthrough, synchronization, output-impedance]
related: "[[bosch-2004-dac-limitations-ch-05-dynamic-behaviour]], [[dac-dynamic-performance]], [[dac-output-impedance]]"
created: 2026-06-08
updated: 2026-06-08
---

# DAC 动态性能四大影响因素

## 综述

电流舵 DAC 的动态性能由四个因素共同决定。前三个可通过精心设计的**同步开关驱动电路**一并解决，第四个（输出阻抗频率依赖性）是高分辨率设计的核心瓶颈。

| # | 因素 | 机理 | 解决方案 |
|---|------|------|---------|
| 1 | 开关不同步 | 差分开关切换时刻不匹配 | 同步锁存器 |
| 2 | 数字馈通 | $C_{GD}$ 耦合数字沿到输出 | 减小摆幅 / 加 cascode |
| 3 | 漏极电压跳动 | 开关同时关断 → $C_0$ 放电 → glitch | 特殊开关驱动 |
| 4 | $Z_{imp}$ 频率依赖性 | 输出阻抗随频率下降 → 信号依赖失真 | cascode 结构 |

## 核心瓶颈：因素 4

前三个因素是**设计层面**可解决的。因素 4 是高分辨率 DAC（> 10 bit）的真正瓶颈——随着分辨率增加，面积增大，互连寄生电容 $C_0$ 增大，$Z_{imp}$ 的极点向低频移动，SFDR 带宽受限。

## 来源

- [[bosch-2004-dac-limitations-ch-05-dynamic-behaviour]] — Bosch et al. (2004) Ch 5

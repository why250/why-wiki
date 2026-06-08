---
type: concept
title: Cascode 电流单元
tags: [DAC, cascode, output-impedance, SFDR, current-cell, frequency-response]
related: "[[bosch-2004-dac-limitations-ch-05-dynamic-behaviour]], [[dac-dynamic-factors]], [[dac-output-impedance]]"
created: 2026-06-08
updated: 2026-06-08
---

# Cascode 电流单元

## 动机

基本电流单元的 $Z_{imp}$ 在高频下降（极点 $f_p = 1/(2\pi C_0 r_{0cs})$），限制了高分辨率 DAC 的 SFDR 带宽。Cascode 结构通过增加阻抗来提升带宽。

## 三种 Cascode 方案

### 1. Cascoded Current Source

在电流源管上加 cascode 管 → 提高 $r_{0cs}$ → 降低极点频率（方向不对！）

实际效果：提高 DC 阻抗（有利于 INL），但 $C_0$ 增加 → 极点更低。

### 2. Cascoded Switch

在开关管上加 cascode 管 → 提供额外的阻抗隔离 → 有利高频表现。

### 3. Double Cascode

电流源 + 开关均加 cascode → 最佳高频阻抗，但消耗更多电压裕度（低电压设计受限）。

## 分析框架

每种结构的 $Z_{imp}$ 通过零极点分析评估：
- **零点**：由 cascode 管的 $g_m$ 和 $C_0$ 决定 → 越高越好
- **极点**：由输出阻抗和寄生电容决定 → 需推到信号带宽之外

## 来源

- [[bosch-2004-dac-limitations-ch-05-dynamic-behaviour]] — Bosch et al. (2004) Ch 5

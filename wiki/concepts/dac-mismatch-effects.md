---
type: concept
title: DAC 电流源失配效应
tags: [DAC, mismatch, SFDR, yield, process-variation, current-source]
related: [[wikner-tan-1997-dac-imperfections]], [[dac-dynamic-performance]], [[ti-calibration]], [[binary-weighted-dac]]
created: 2026-06-07
updated: 2026-06-07
---

# DAC 电流源失配效应

## 两类失配

### A) 确定性失配

单个电流源存在相对误差 $\Delta_i$（例如 MSB 电流源偏差 1%）。失配电流：

$$\Delta I_i = I_{LSB} \cdot 2^{i-1} \cdot \Delta_i \cdot b_i$$

- **高位电流源失配影响更大**：误差电流 $\propto 2^{i-1}$
- 由于数字比特的脉冲波特性，产生奇次谐波
- SFDR 近似：

$$SFDR(i, \Delta_i) \approx 13.5 + 6(N - i) - 20\log\Delta_i \text{ [dB]}$$

> 示例：14-bit DAC 中 MSB 失配 1% → SFDR ≈ 53dB

- 低比特位的小失配可能被噪声淹没，不直接贡献失真

### B) 统计失配

每个电流源的偏差来自制造过程中的随机波动，建模为正态分布：

- LSB 误差电流：$\sigma_{LSB}$
- 第 i 位误差电流：$\sigma_i = 2^{i-1} \sigma_{LSB}$
- 假设各电流源间不相关

SFDR 期望值：

$$E\{SFDR(N, \sigma_{LSB})\} \approx 3N + 7.5 - 20\log\sigma_{LSB}$$

## 良率分析

论文通过 1000 样本 Monte Carlo 仿真给出了 90% 良率的 SFDR 曲线，表明：
- 给定工艺偏差 → 可以预测良率
- 给定良率目标 → 可以反推所需匹配精度

## 与 ADC 失配校准的关系

ADC 中也存在类似的电容/电流源失配问题（参见 [[ti-calibration]]）。DAC 的失配建模方法与 ADC 共享相似的统计分析框架，但 DAC 面临的核心挑战是失配直接产生输出杂散，而 ADC 的失配影响的是量化阈值。

## 来源

- [[wikner-tan-1997-dac-imperfections]]

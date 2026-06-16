---
type: concept
title: AMUX-DAC (Analog Multiplexing DAC)
tags: [DAC, AMUX, analog-multiplexer, bandwidth-extension, high-speed, behavioral-modeling]
related: ["[[schmidt-2018-amux-behavioral-model]]", "[[current-steering-dac]]", "[[dac-behavioral-modeling]]", "[[ti-dac]]"]
created: 2026-06-16
updated: 2026-06-16
---

# AMUX-DAC (Analog Multiplexing DAC)

## 基本原理

AMUX-DAC 是一种通过**模拟复用器 (Analog Multiplexer, AMUX)** 组合多路 DAC 输出以突破单 DAC 带宽/采样率限制的架构。

- 两路 DAC 以 **180° 相移**时钟驱动
- AMUX 在每符号**中心**切换，将当前稳定输出的那路 DAC 信号接通到输出
- 一路 DAC 输出被接通时，另一路执行信号 transition
- 效果：**采样率和带宽各翻倍**

## 与其他带宽扩展方案的比较

| 方案 | 原理 | 关键硬件 |
|------|------|----------|
| **AMUX-DAC** | 模拟复用器在时域交替选通多路 DAC | 高速 AMUX IC（SiGe/InP） |
| **TI-DAC** (Time Interleaving) | 多路 DAC 时域交织，类似 TI-ADC | 精确时钟相位控制 |
| **FI-DAC** (Frequency Interleaving) | 频域分割，用模拟带宽交织 | 模拟滤波器组 |

## AMUX 集成电路架构

参考实现：[[schmidt-2018-amux-behavioral-model]] 中的 SiGe-HBT BiCMOS SG13G2 AMUX

### 子模块

1. **AMUX 核心**：两个跨导放大器 + 时钟电流开关对 + cascode + 负载电阻。时钟控制开关对选通对应输入端口，未选通端口电流导入 dummy load。

2. **时钟缓冲 (Clock Buffer)**：多级高增益 Cherry-Hooper 放大器，被输入时钟过驱动以生成陡峭的准矩形时钟信号。

3. **输出放大器**：两级射极跟随器 + 线性化差分跨导 cascode 级。补偿 AMUX 损耗使总增益为 1，同时匹配输出阻抗。

### 典型参数

- 输入：64 GS/s × 2 DAC → 128 GBd 输出
- AMUX 时钟：64 GHz（半时钟频率）
- 输入 LPF：4 阶 Butterworth, 120 GHz
- 输出 LPF：4 阶 Butterworth, 125 GHz
- 时钟 LPF：6 阶 Butterworth, 80 GHz

## 行为级建模

见 [[schmidt-2018-amux-behavioral-model]] 详情。核心方法：

- **准线性模型**（数据路径无非线性失真）
- 低通滤波器建模带宽限制（Bessel/Butterworth/Gaussian 标准滤波器）
- tanh 特性 + LPF 级联建模时钟缓冲放大链路
- 馈通隔离 + AWGN 建模寄生和噪声

### 关键仿真发现

1. **输入 LPF 带宽变化**：低带宽时在半时钟频率处出现凹陷 + 64 GHz 附近出现混频平台
2. **时钟 LPF 带宽变化**：低带宽时 64 GHz 处凹陷明显
3. **时钟 offset**：归一化幅度 > 0.3 → EVM > 10%；offset 导致奇偶采样质量不对称

## 来源

- [[schmidt-2018-amux-behavioral-model]] — 2:1 AMUX 行为级模型（MWSCAS 2018）
- [[tannert-2017-amux]] — SiGe-HBT 2:1 AMUX IC 设计（BCTM 2017）
- Yamazaki et al. (2016) — Digital-preprocessed analog-multiplexed DAC
- Ferenci, Grözing, Berroth (2011) — 25 GHz AMUX in InP DHBT

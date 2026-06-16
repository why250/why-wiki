---
type: source
title: Behavioral Model for a High-Speed 2:1 Analog Multiplexer
authors: [Christian Schmidt, Patrick Zielonka, Volker Jungnickel, Ronald Freund, Tobias Tannert, Markus Grözing, Manfred Berroth, Friedel Gerfers]
year: 2018
url: "https://doi.org/10.1109/MWSCAS.2018.8623931"
venue: "2018 IEEE 61st International Midwest Symposium on Circuits and Systems (MWSCAS)"
tags: [AMUX, DAC, behavioral-modeling, analog-multiplexer, high-speed, MATLAB]
related: ["[[amux-dac]]", "[[dac-behavioral-modeling]]", "[[tannert-2017-amux]]"]
created: 2026-06-16
updated: 2026-06-16
---

# Behavioral Model for a High-Speed 2:1 Analog Multiplexer

## 核心要点

1. **AMUX-DAC 行为级模型**：为高速 2:1 模拟复用器 (AMUX) 提出了一种准线性行为级模型，仿真速度比晶体管级 EDA 工具快 **3 个数量级以上**（2²⁰ 样本 < 1 分钟 vs 2¹⁷ 样本约 2 天），NMSE < -20 dB。

2. **建模方法**：数据路径采用低通滤波器（Butterworth）建模传输线和跨导放大器的带宽限制；时钟路径用 tanh 特性 + 低通滤波器级联（Cherry-Hooper 放大器链）生成两路反相矩形时钟；同时建模了馈通隔离和 AWGN。

3. **参数拟合**：两步法——先对子系统做 LS 信道估计得到初值，再暴力搜索多参数组合优化。拟合目标为 128 GBd PAM-8 输出信号（64 GS/s × 2 DAC 输入）。

4. **关键参数研究**：输入 LPF 带宽降低 → 半时钟频率处出现凹陷 + 混频平台；时钟 LPF 带宽降低 → 64 GHz 处明显凹陷；时钟 offset 归一化幅度 > 0.3 → EVM 超 10%。

## 关键概念

- [[amux-dac]] — AMUX-DAC 架构：用模拟复用器组合多路 DAC 输出以翻倍带宽
- [[dac-behavioral-modeling]] — DAC 行为级建模的通用方法论
- **AMUX 核心**：跨导放大器 + 时钟电流开关对 + cascode + 负载电阻
- **时钟缓冲**：多级 Cherry-Hooper 放大器过驱动生成陡峭矩形时钟
- **输出放大器**：两级射极跟随器 + 线性化差分跨导 cascode

## 实际芯片

- 工艺：IHP SiGe-HBT BiCMOS SG13G2
- 设计用于：64 GS/s × 2 DAC → 128 GBd 输出
- AMUX 工作频率：64 GHz（半时钟）
- 全差分设计，包含 AMUX 核心、时钟缓冲、线性输出放大器

## 模型参数（Tab. I）

| 参数 | 值 |
|------|-----|
| DataIn LPF | 4 阶 Butterworth, f_c = 120 GHz |
| DataIn 隔离 | 50 dB |
| DataOut LPF | 4 阶 Butterworth, f_c = 125 GHz |
| Clock LPF | 6 阶 Butterworth, f_c = 80 GHz |
| Tanh 参数 a | 2.5 |
| 放大器级联数 n | 1 |
| Clock 隔离 | 60 dB |

## 待探究的问题

- 高频段模型精度仍需改善（Fig. 4c 显示快速信号 transition 时 squared error 不可忽略）
- 模型需用实测数据（而非仅仿真数据）验证
- [[ti-dac]] 与 AMUX-DAC 的架构比较：各自在带宽、功耗、复杂度上的权衡
- 4:1 AMUX 的行为级建模扩展（参考文献中已有 2025 年 ISCAS 后续工作）

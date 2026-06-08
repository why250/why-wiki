---
type: source
title: "Static and Dynamic Performance Limitations for High Speed D/A Converters — Ch 2: Functionality and Specifications"
book: "[[bosch-2004-dac-limitations]]"
chapter: 2
authors: [Anne Van den Bosch, Michiel Steyaert, Willy Sansen]
year: 2004
url: ""
venue: "Book Chapter, Springer"
tags: [DAC, specifications, SNR, INL, DNL, quantization, SFDR]
related: "[[dac-static-performance]], [[dac-dynamic-performance]], [[quantization-noise]], [[sinc-distortion]]"
created: 2026-06-08
updated: 2026-06-08
---

# Ch 2: The D/A Converter — Functionality and Specifications

## 核心要点

1. **DAC 基本功能**：将 N-bit 数字序列转换为模拟量（电荷/电压/电流）$Y_{out}(B) = B \cdot Y_{ref}$，其中 $B = \sum 2^i b_i$

2. **量化噪声**：有限比特数产生的固有误差 $P_{noise} = \Delta^2/12$，导出 SNR 上限 $SNR = 6.02N + 1.76\text{ dB}$——这是评估 DAC 性能的基准线。

3. **Sinc 失真（零阶保持效应）**：DAC 输出在采样间隔内保持恒定 → 频域出现 $\text{sinc}(f_{in}/f_s)$ 响应 → Nyquist 频率处振幅衰减 3.92 dB。

4. **静态指标体系**：Offset Error、Gain Error、DNL、INL、Monotonicity。其中 INL 曲线形状可以预示频域的谐波特征。

5. **动态指标体系**：Update Rate、Settling Time、Glitch Energy、Clock Feedthrough、SNR、SNDR、SFDR、THD。不同应用侧重点不同——仪表看重 INL/DNL，通信看重 SFDR/IMD。

## 静态规格一览

| 指标 | 定义 | 是否引入非线性 |
|------|------|:---:|
| Offset Error | 零码时的 DC 偏移 | 否 |
| Gain Error | 传递曲线斜率偏差 | 否 |
| DNL | 相邻码步长与 1LSB 的最大偏差 | **是** |
| INL | 实际输出与理想直线的最大偏差 | **是** |
| Monotonicity | 输出是否随输入单调递增 | — |

## 动态规格一览

| 指标 | 描述 |
|------|------|
| Update Rate | DAC 每秒更新次数 |
| Settling Time | 输出稳定到 ±0.5LSB 所需时间 |
| Glitch Energy | 码切换时输出瞬态尖峰的面积 |
| Clock Feedthrough | 时钟信号通过寄生电容耦合到输出 |
| SNR | 信号与噪声之比（不含谐波）|
| SNDR/SINAD | 信号与噪声+失真之比 |
| SFDR | 信号与最大杂散之比 |
| THD | 总谐波失真 |

## 与其他章节的关系

本章建立的概念体系在整个专著中被反复引用：
- Ch 4 聚焦 **静态性能** 的物理来源（晶体管失配）
- Ch 5 聚焦 **动态性能** 的物理来源（开关瞬态、输出阻抗）

## 来源

- [[bosch-2004-dac-limitations]] — Bosch et al. (2004) Ch 2

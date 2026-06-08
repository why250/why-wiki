---
type: source
title: Influence of Circuit Imperfections on the Dynamic Performance of DACs
authors: [J. Jacob Wikner, Nianxiong Tan]
year: 1997
url: ""
venue: Linköping University / Ericsson Components AB
tags: [DAC, dynamic-performance, SFDR, mismatch, noise, output-impedance, CMOS]
related: "[[dac-dynamic-performance]], [[dac-output-impedance]], [[dac-mismatch-effects]], [[dac-circuit-noise]], [[jacob-wikner]], [[nianxiong-tan]]"
created: 2026-06-07
updated: 2026-06-07
---

# Influence of Circuit Imperfections on the Dynamic Performance of DACs

## 核心要点

1. **DAC 的动态性能是通信应用的核心指标**。传统静态指标（INL、DNL、offset error、gain error）不适用于通信场景，真正决定质量的是 SFDR、IMD、SNR、SNDR（SINAD）。

2. **三种电路非理想因素的建模**：
   - **输出阻抗变化**：电流源有限输出阻抗随输入码变化 → 信号依赖失真 → 推导了 SFDR 的闭式近似公式
   - **失配**：分为确定性失配（单个电流源误差，影响高比特位）和统计失配（随机过程偏差，可建模为正态分布），给出了 SFDR 期望值和良率曲线
   - **电路噪声**：CMOS 电流源的热噪声主导 SNR，当 LSB 电流较小时噪声限制明显

3. **设计指导价值**：为每种非理想因素提供了定量公式，使设计者能够根据目标 SFDR/SNR 反推电路参数（如输出阻抗比、匹配精度、偏置电流）。

4. **统计失配的良率视角**：不仅计算 SFDR 均值，还给出了 90% 良率曲线，对量产设计有实际指导意义。

## 关键概念

- [[dac-dynamic-performance]] — DAC 动态性能指标：SFDR、IMD、SNR、SNDR
- [[dac-output-impedance]] — 输出阻抗随信号变化引起的失真机理
- [[dac-mismatch-effects]] — 确定性失配与统计失配对 SFDR 的影响
- [[dac-circuit-noise]] — 电流源热噪声对 DAC SNR 的限制
- [[binary-weighted-dac]] — 二进制加权 DAC 架构基础

## 关键实体

- [[jacob-wikner]] — Linköping University，DAC 建模研究者
- [[nianxiong-tan]] — Ericsson Components，高性能 CMOS DAC 设计者

## 待探究的问题

- 这些 DAC 动态性能模型是否适用于先进工艺节点（FinFET、GAA）？
- 分段式 DAC（segmented）相比二进制加权在动态性能上有多少改善？
- 与现有 wiki 中的 ADC 校准概念 [[ti-calibration]] 能否统一为数据转换器失配的一般性理论？

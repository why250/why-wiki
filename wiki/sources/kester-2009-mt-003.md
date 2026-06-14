---
type: source
title: "Understand SINAD, ENOB, SNR, THD, THD + N, and SFDR so You Don't Get Lost in the Noise Floor"
authors: [Walt Kester]
year: 2009
url: ""
venue: "Analog Devices Tutorial (MT-003)"
tags: [ADC, dynamic-performance, SINAD, ENOB, SNR, THD, SFDR, FFT, tutorial]
related: "[[sinad]], [[enob]], [[adc-dynamic-metrics]], [[quantization-noise]], [[dac-dynamic-performance]], [[walt-kester]]"
created: 2026-06-14
updated: 2026-06-14
---

# MT-003: ADC 动态性能指标

> Analog Devices Tutorial MT-003 by Walt Kester (2009)

## 核心要点

1. **六大 ADC 动态指标**：SINAD、ENOB、SNR、THD、THD + N、SFDR — 均基于 FFT 分析
2. **SINAD vs SNR 的本质区别**：SINAD 包含谐波失真，SNR 排除谐波；部分厂商混用这两个术语
3. **ENOB = (SINAD − 1.76) / 6.02**：直接从理想 ADC SNR 公式推出，可视为 ADC 的"等效分辨率"
4. **SINAD/SNR/THD 数学关系**：SINAD = −10·log(10^(−SNR/10) + 10^(−THD/10))，三者可互推（式 12–14）
5. **FFT 过程增益 = 10·log(M/2)**：解释了为何 FFT 图中噪声 floor 比理论 SNR 低

## 关键概念

- [[sinad]] — SINAD 定义与 ENOB 导出
- [[enob]] — 有效位数 (Effective Number of Bits)
- [[adc-dynamic-metrics]] — ADC 动态性能指标全景（SFDR、THD、THD+N 定义与 FFT 测试方法）
- [[quantization-noise]] — SNR = 6.02N + 1.76 dB 的理论基础

## 待探究的问题

- ADC 与 DAC 的动态指标定义是否完全一致？SFDR 的 dBFS vs dBc 在不同应用场景中的选用
- 非满幅输入时 ENOB 修正公式（式 2）的实用边界 — 多低信号时该修正失效？

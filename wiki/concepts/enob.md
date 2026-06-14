---
type: concept
title: "ENOB（有效位数）"
tags: [ENOB, SINAD, ADC, dynamic-performance, resolution, data-converter]
related: "[[sinad]], [[kester-2009-mt-003]], [[quantization-noise]], [[adc-dynamic-metrics]]"
created: 2026-06-14
updated: 2026-06-14
---

# ENOB (Effective Number of Bits)

## 定义

ENOB 将 ADC 的实际动态性能（SINAD）映射为等效的理想 ADC 分辨率：

$$ENOB = \frac{SINAD - 1.76 \text{ dB}}{6.02}$$

该公式从理想 N-bit ADC 的 SNR 公式 $SNR = 6.02N + 1.76$ 解出 $N$，并用 SINAD 替代 SNR。

**直觉**：一个标称 12-bit 的 ADC，若 SINAD = 62 dB，则 ENOB ≈ 10 位——相当于只有 10 个"有效"比特。

## 非满幅输入修正

式 1 假设满幅输入。若信号幅度降低，需加入修正项（来自 [[kester-2009-mt-003]] 式 2）：

$$ENOB = \frac{SINAD_{MEASURED} - 1.76 + 20\log\left(\frac{\text{Fullscale Amplitude}}{\text{Input Amplitude}}\right)}{6.02}$$

该修正将 ENOB "归一化"到满幅等效值。

## 与理想分辨率的区别

| 概念 | 含义 |
|------|------|
| 标称分辨率（N） | ADC 的数字输出位数 |
| ENOB | 考虑噪声和失真后的**等效**位数 |
| 两者差值 N − ENOB | 噪声+失真造成的分辨率损失 |

## 来源

- [[kester-2009-mt-003]] — 式 1 和式 2 的定义与修正
- [[quantization-noise]] — SNR = 6.02N + 1.76 的理论推导

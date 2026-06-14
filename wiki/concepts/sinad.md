---
type: concept
title: "SINAD（信号-噪声-失真比）"
tags: [SINAD, SNR, THD, ADC, dynamic-performance, data-converter, ENOB]
related: "[[kester-2009-mt-003]], [[enob]], [[adc-dynamic-metrics]], [[quantization-noise]], [[dac-dynamic-performance]]"
created: 2026-06-14
updated: 2026-06-14
---

# SINAD (Signal-to-Noise-and-Distortion Ratio)

## 定义

SINAD（或 S/(N+D)）是信号功率与噪声+失真总功率之比：

$$SINAD = 20 \log\left(\frac{S}{N+D}\right) \quad \text{(dB)}$$

其中 $S$ 为基频信号 rms 值，$N+D$ 为所有其他频谱分量（谐波 + 噪声，不含直流）的根均方和。

## 与 THD+N 的关系

当测量带宽一致（均为 Nyquist 带宽 dc ~ f<sub>s</sub>/2）时：

$$SINAD = THD+N$$

这是 FFT 分析中的典型情况。**注意**：在音频应用中，THD+N 的测量带宽可能不是 Nyquist 带宽，此时两者不等。

## 与 SNR 的区别

| 指标 | 包含谐波？ | 含义 |
|------|-----------|------|
| SINAD | ✓ 包含 | 综合动态性能 |
| SNR | ✗ 排除 | 仅噪声限制 |

**陷阱**：部分 ADC 数据手册将 SINAD 标注为 SNR，阅读时需确认是否包含谐波。

## SINAD / SNR / THD 数学关系

已知三者定义（均为 dB，同一频率和幅度下测量）：

$$SNR = 20\log\left(\frac{S}{N}\right), \quad THD = 20\log\left(\frac{S}{D}\right), \quad SINAD = 20\log\left(\frac{S}{N+D}\right)$$

可推导出互推公式（来自 [[kester-2009-mt-003]]）：

$$SINAD = -10 \log\left[10^{-SNR/10} + 10^{-THD/10}\right] \quad \text{(式 12)}$$

$$SNR = -10 \log\left[10^{-SINAD/10} - 10^{-THD/10}\right] \quad \text{(式 13)}$$

$$THD = -10 \log\left[10^{-SINAD/10} - 10^{-SNR/10}\right] \quad \text{(式 14)}$$

**前提**：三者必须在相同输入频率和幅度下测量。

## 高频下的 SINAD 退化

SINAD 随输入频率升高而退化（通常快于 SNR），因为高频下谐波失真增加。SINAD vs 频率曲线是评估 ADC 交流性能的核心图形，尤其对欠采样应用（输入频率远超 Nyquist）。

## 来源

- [[kester-2009-mt-003]] — Walt Kester, MT-003 (2009)
- [[dac-dynamic-performance]] — DAC 侧也使用 SNDR/SINAD，物理来源不同

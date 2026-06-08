---
type: concept
title: 时间交织 ADC (Time-Interleaving ADC)
tags: [ADC, time-interleaving, SAR, mismatch, architecture]
related: [[gutietieqiu-2024-8bit-high-speed-sar-adc]], [[ti-calibration]], [[high-speed-sar-adc]]
created: 2026-06-07
updated: 2026-06-07
---

# 时间交织 ADC (Time-Interleaving ADC)

## 基本原理

当单通道 ADC 的采样速度无法满足系统需求时，使用 N 路 ADC 以乒乓方式交替采样。每路子 ADC 工作在 fs/N 频率，系统总采样率为 fs。代价是各路之间的失配（mismatch）会引入杂散。

**关键公式**：时钟 jitter 对 SNR 的影响 — SNDR_jitter = −20 log(2π · f_in · σ_j)

## 失配类型

| 类型 | 特性 | 杂散位置 | 频率相关性 |
|------|------|----------|-----------|
| Offset | 静态 | N×fs/M ± f_in | 无关 |
| Gain | 静态 | N×fs/M ± f_in | 无关 |
| Skew (采样时间) | 动态 | N×fs/M ± f_in | 相关，高频恶化 |
| Bandwidth | 动态 | N×fs/M ± f_in | 相关，高频恶化 |

参见 [[ti-calibration]] 了解校准方法。

## 分级交织

当交织数 N > 8 时，单级 TI 面临输入负载过大、多相时钟难以产生的问题，需采用分级交织。

**Direct Sampling**（两级）：buffer1 → SHA (T/H switch + buffer2) → sub-ADC array。第一级 SHA 决定带宽，增加设计自由度（N1×N2、占空比、保持时间）。

**Inline Demux Sampling**（三级）：N1×N2×N3，Kull (2016) 用 4×4×4 实现 64 路交织，带宽 >20GHz。本题（32 路）用两级足够。

## 架构选择指南

- Speed > 10GSPS：必须用 TI
- 交织数选 2^N：方便分频和占空比/相位校正
- 相同总速率，加倍通道数优于加倍单通道速率（后者设计难度非线性增长）
- 相同通道数，尽量提升单通道速率以提升总速率

## 参考文献

- [2] G. Manganaro, "An Introduction to High Sample Rate Nyquist ADCs," IEEE OJSSC, 2022.
- [3] L. Kull et al., "Implementation of Low-Power 6–8 b 30–90 GS/s Time-Interleaved ADCs," JSSC, 2016.

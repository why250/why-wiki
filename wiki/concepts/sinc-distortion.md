---
type: concept
title: Sinc 失真（零阶保持效应）
tags: [DAC, sinc, sample-and-hold, frequency-response, reconstruction]
related: "[[bosch-2004-dac-limitations-ch-02-specifications]], [[dac-dynamic-performance]], [[quantization-noise]]"
created: 2026-06-08
updated: 2026-06-08
---

# Sinc 失真 (Zero-Order Hold / Sinc Distortion)

## 物理来源

DAC 在信号重建过程中相当于一个采样保持电路——输出在采样间隔 $t_s$ 内保持不变。这在时域表现为一系列调制矩形脉冲，在频域产生 $\text{sinc}(x)$ 响应。

## 频率响应

$$|H(2\pi f_{in})| \sim \frac{\sin(\pi f_{in}/f_s)}{\pi f_{in}/f_s}$$

- $f_s$：采样/更新频率
- $f_{in}$：信号频率

## 关键数值

| 条件 | 衰减 |
|------|------|
| $f_{in} \ll f_s$（窄带） | 可忽略 |
| $f_{in} = f_s/2$（Nyquist） | $2/\pi$ ≈ **−3.92 dB** |
| $f_{in} = f_s$ | 零点（完全衰减） |

## 工程应对

- 窄带信号：sinc 衰减可能已足够抑制镜像频率
- 宽带信号：需在 DAC 后加**模拟重建滤波器**，或使用**逆 sinc 滤波器/均衡器**补偿振幅失真

## 来源

- [[bosch-2004-dac-limitations-ch-02-specifications]] — Bosch et al. (2004) Ch 2

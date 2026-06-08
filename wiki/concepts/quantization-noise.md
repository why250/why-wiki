---
type: concept
title: 量化噪声
tags: [quantization, noise, DAC, ADC, SNR, data-converter]
related: [[bosch-2004-dac-limitations-ch-02-specifications]], [[dac-dynamic-performance]]
created: 2026-06-08
updated: 2026-06-08
---

# 量化噪声 (Quantization Noise)

## 来源

用有限比特数表示连续幅度信号时引入的不可逆误差。量化误差 $\varepsilon$ 可视为白噪声。

## 基本公式

假设 $\varepsilon$ 在 $[-\Delta/2, \Delta/2]$ 上均匀分布且与信号无关：

$$P_{noise} = E(\varepsilon^2) = \frac{1}{\Delta} \int_{-\Delta/2}^{\Delta/2} \varepsilon^2 d\varepsilon = \frac{\Delta^2}{12}$$

对于 N-bit DAC（$N \ge 5$），正弦输出的 SNR：

$$SNR = 6.02N + 1.76 \text{ dB}$$

## 设计含义

- 量化噪声是**任何理想数据转换器的性能上限**
- 每增加 1 位分辨率 → SNR 提升约 6 dB
- 实际电路的噪声/失真会使 SNR 低于此理论值

## 来源

- [[bosch-2004-dac-limitations-ch-02-specifications]] — Bosch et al. (2004) Ch 2

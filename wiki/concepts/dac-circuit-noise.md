---
type: concept
title: DAC 电路噪声与 SNR 限制
tags: [DAC, noise, thermal-noise, SNR, current-source, CMOS]
related: "[[wikner-tan-1997-dac-imperfections]], [[dac-dynamic-performance]], [[binary-weighted-dac]]"
created: 2026-06-07
updated: 2026-06-07
---

# DAC 电路噪声与 SNR 限制

## 噪声来源

CMOS DAC 中，晶体管的**热噪声**通常占主导。单个电流源的噪声谱密度：

$$\overline{i_n^2}/\Delta f = \frac{8}{3}kTg_m$$

其中 $g_m$ 由偏置电流和晶体管尺寸决定：

$$g_m \approx \sqrt{2\mu_0 C_{ox}(W/L) I_{LSB}}$$

## SNR 公式

理想 N-bit DAC 的量化 SNR：
$$SNR_{ideal} = 6.02N + 1.76 \text{ [dB]}$$

考虑热噪声后的 SNR：

$$SNR \approx 15\log I_{LSB} + 3N - 5\log \frac{W}{L} - 10\log BW - 5\log K' - 10\log(kT) - 7 \text{ [dB]}$$

## 设计含义

- **LSB 电流足够大时**：热噪声 < 量化噪声，SNR 接近理论值
- **LSB 电流较小时**：热噪声主导，SNR 远低于理论值
- **增加晶体管尺寸（W/L）**：降低噪声但增加面积和寄生
- **带宽（BW）**：更宽的带宽 → 更大的积分噪声功率 → 更低的 SNR

## 来源

- [[wikner-tan-1997-dac-imperfections]]

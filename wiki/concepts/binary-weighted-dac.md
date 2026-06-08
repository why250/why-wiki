---
type: concept
title: 二进制加权 DAC
tags: [DAC, binary-weighted, current-steering, architecture, CMOS]
related: [[wikner-tan-1997-dac-imperfections]], [[dac-dynamic-performance]], [[dac-output-impedance]], [[dac-mismatch-effects]]
created: 2026-06-07
updated: 2026-06-07
---

# 二进制加权 DAC

## 基本结构

N-bit 二进制加权 DAC 使用 N 个二进制加权电流源（$I_{LSB}, 2I_{LSB}, \dots, 2^{N-1}I_{LSB}$），由数字输入码的对应比特控制开关。

输出电流：

$$I_{out}(X) = I_{LSB}[b_1 + 2b_2 + \dots + 2^{N-1}b_N] = I_{LSB}X$$

其中 $b_1$ 为 LSB，$b_N$ 为 MSB。

## 特点

| 优点 | 缺点 |
|------|------|
| 结构简单，开关控制逻辑少 | MSB 电流源面积大，匹配要求高 |
| 无需解码器 | 高位切换时 glitch 能量大 |
| 适合中低分辨率 | SFDR 受 MSB 失配、输出阻抗变化限制 |

## MSB 分段

为减少 glitch 能量 [3, 10, 11]，可将高几位（MSB）分段为多个等权重电流源（thermometer coding）。但 Wikner & Tan 的分析集中在纯二进制加权结构。

## 关键非理想因素

见 [[wikner-tan-1997-dac-imperfections]]，包括：
- [[dac-output-impedance]] — 输出阻抗的信号依赖性
- [[dac-mismatch-effects]] — 电流源失配（确定性和统计性）
- [[dac-circuit-noise]] — 热噪声对 SNR 的限制

## 来源

- [[wikner-tan-1997-dac-imperfections]]

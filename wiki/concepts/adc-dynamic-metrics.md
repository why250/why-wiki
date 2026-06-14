---
type: concept
title: "ADC 动态性能指标"
tags: [ADC, dynamic-performance, SFDR, THD, SNR, FFT, data-converter, testing]
related: "[[kester-2009-mt-003]], [[sinad]], [[enob]], [[dac-dynamic-performance]], [[quantization-noise]]"
created: 2026-06-14
updated: 2026-06-14
---

# ADC 动态性能指标

## 概述

ADC 动态性能通过 FFT 分析量化。六个核心指标（来自 [[kester-2009-mt-003]]）：

| 指标 | 全称 | 定义 |
|------|------|------|
| **SINAD** | Signal-to-Noise-and-Distortion | 信号 / (噪声+谐波)，综合动态性能 |
| **SNR** | Signal-to-Noise Ratio | 信号 / 噪声（不含谐波） |
| **ENOB** | Effective Number of Bits | SINAD 换算的等效位数 |
| **THD** | Total Harmonic Distortion | 信号 / 谐波根均方和（通常取前 5 次） |
| **THD+N** | THD + Noise | 信号 / (谐波+噪声)，带宽 = Nyquist 时 = SINAD |
| **SFDR** | Spurious-Free Dynamic Range | 信号 / 最差杂散（不一定是谐波） |

## FFT 测试方法论

### 测试框架

通用 FFT 测试设置：信号源 → 抗混叠滤波器 → ADC → 缓冲存储器 (M 点) → FFT 处理器 → 频谱输出

### FFT 过程增益

FFT 等效为一个带宽为 f<sub>s</sub>/M 的窄带频谱分析仪在全频段扫描。噪声被"推低"一个等于**过程增益**的量：

$$\text{Process Gain} = 10 \log\left(\frac{M}{2}\right)$$

其中 $M$ 为 FFT 点数。这解释了为何 FFT 图中的噪声 floor 看起来低于理论 SNR。

**注意事项**：
- 对多次 FFT 取平均可平滑频谱变化，但**不改变平均噪声 floor**
- 噪声 floor = 理论 SNR + 过程增益（均为 dB）

## SFDR（无杂散动态范围）

$$SFDR = 20 \log\left(\frac{S_{rms}}{\text{Worst Spur}_{rms}}\right) \quad \text{(dB)}$$

- 最差杂散可能是谐波，也可能不是
- 可参考满幅（dBFS）或参考信号（dBc）
- 通信系统中代表能从强阻塞信号中分辨的最小信号

## THD（总谐波失真）

$$THD = 20 \log\left(\frac{S_{rms}}{\sqrt{\sum_{n=2}^{6} H_n^2}}\right) \quad \text{(dB or dBc)}$$

- 通常只取前 5 次谐波（第 2~6 次），高阶谐波贡献可忽略
- 一般以 dBc（相对载波）表示；音频应用中可表示为百分比
- 近满幅时测量（一般 −0.5 ~ −1 dBFS 以避免削波）

### 谐波的频率位置

采样导致谐波混叠，第 n 次谐波出现在：

$$f_{alias} = |\pm K f_s \pm n f_a|$$

其中 $K = 0, 1, 2, 3, \dots$

## 与 DAC 动态性能的对比

| 维度 | ADC | DAC |
|------|-----|-----|
| 核心限制 | 量化噪声 + 采样抖动 + 比较器噪声 | 电流源失配 + 输出阻抗变化 + 开关瞬态 |
| SFDR 来源 | 前端非线性 + 时钟抖动 | 电流源失配（确定性+统计）+ 输出阻抗 |
| SNR 限制 | 量化噪声 + 热噪声 + 抖动 | 电流源热噪声（[[dac-circuit-noise]]） |
| 共同点 | 共享 SFDR/SNR/SNDR 概念框架；ENOB 概念仅用于 ADC |

## 来源

- [[kester-2009-mt-003]] — Walt Kester, MT-003 (2009), 六项指标的定义与 FFT 测试方法
- [[dac-dynamic-performance]] — DAC 侧的动态性能概念对偶
- [[quantization-noise]] — SNR = 6.02N + 1.76 的理论上限

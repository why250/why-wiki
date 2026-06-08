---
type: concept
title: DAC 动态性能
tags: [DAC, dynamic-performance, SFDR, SNR, IMD, SNDR, telecommunications]
related: "[[wikner-tan-1997-dac-imperfections]], [[dac-output-impedance]], [[dac-mismatch-effects]], [[dac-circuit-noise]], [[binary-weighted-dac]]"
created: 2026-06-07
updated: 2026-06-07
---

# DAC 动态性能

## 定义

对于通信应用中的 DAC，传统的静态性能指标（offset error、gain error、INL、DNL）不直接适用。取而代之的是动态性能指标：

| 指标 | 全称 | 含义 |
|------|------|------|
| **SFDR** | Spurious-Free Dynamic Range | 无杂散动态范围 — 信号与最大杂散功率之比 |
| **IMD** | Inter-Modulation Distortion | 互调失真 — 多音信号时的非线性产物 |
| **SNR** | Signal-to-Noise Ratio | 信噪比 — 信号与噪声功率之比 |
| **SNDR/SINAD** | Signal-to-Noise-and-Distortion Ratio | 信号与噪声+失真总功率之比 |

## 为何静态指标不够？

静态指标（INL、DNL）描述的是 DC 传输特性，但通信系统关心的是频域行为——信号经过 DAC 后在频谱上的纯净度。一个 INL 很好的 DAC 可能因为高频下的输出阻抗变化而产生严重的杂散。

## 影响因素（来自 Wikner & Tan）

1. **输出阻抗变化** → 信号依赖失真 → 影响 SFDR
2. **电流源失配** → 谐波和杂散 → 确定性 SFDR 公式 + 统计良率
3. **电路噪声** → 热噪声限制 SNR → 与小信号电流直接相关

## 与 ADC 动态性能的关系

DAC 和 ADC 共享类似的频域指标概念（SFDR、SNR、SNDR），但物理来源不同。DAC 关注电流源的输出特性，ADC 关注采样和量化过程。

## 来源

- [[wikner-tan-1997-dac-imperfections]]

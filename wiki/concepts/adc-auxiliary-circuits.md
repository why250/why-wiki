---
type: concept
title: 辅助电路（高速ADC）
tags: [ADC, input-buffer, clock-generation, reference-buffer, auxiliary-circuits]
related: "[[gutietieqiu-2024-8bit-high-speed-sar-adc]], [[high-speed-sar-adc]], [[time-interleaving-adc]]"
created: 2026-06-07
updated: 2026-06-07
---

# 辅助电路（高速ADC）

高速 ADC 中除单通道核心外的关键电路：Input Buffer、Clock Generation、Reference Buffer。三者常被论文一笔带过，但在实际设计中决定系统性能上限。

## Input Buffer

### 必要性

TI 结构中，子 ADC 采样开关的 kickback 相互干扰，且输入负载电容随交织数增加。需在采样开关前加高带宽高线性度 buffer。

### 基本结构

buffer1 → SHA (T/H Switch + buffer2) → sub-ADC array

T/H Switch：Bootstrap switch / MOS switch + cross-couple switch。

### 带宽拓展技术

**基于电感**：Inductive peaking、T-coil peaking

**基于反馈**：
- Flipped Voltage Follower (FVF)
- Super Source Follower (SSF)
- Class AB Super Source Follower

**ADI 方案**（Ali, 2014/2020 JSSC）：Cascode bootstrap Vds → 抑制 rds 变化 → 提升线性度。结合 Class AB 提升 gm 和 SR。

## Clock Generation

### Divider 方案（推荐）

DFF 链进行 2^N 分频，产生多相时钟。简单实用，但：
- 占空比和相位需校正
- 工作在 2× 期望频率，功耗大
- 用 CML latch 替代 DFF 可提速（输入无需满摆幅）

### 注入锁定环形振荡器（MPIL-ROSC）

多相注入锁定环形振荡器 + QDLL（正交延迟锁相环）：
- 优势：功耗面积小、IQ 误差低、jitter 极低（58.8 fs_rms @7GHz）
- 劣势：设计难度大

### 实用建议

第一级用 divider 产生主时钟 + DCC + 相位校正；第二级用控制逻辑实现各通道时钟。

## Reference Buffer

### 问题

高速 SAR 的 CDAC 从参考电压快速充放电。片外提供 → 寄生电感导致振铃。需片内集成。

### 要求

- 低输出阻抗（快速恢复 Vref）
- 高 PSRR（抑制电源纹波）
- 快瞬态响应
- 大去耦电容（几十~几百 pF，面积大）

### 冗余技术

二进制重组冗余 → 降低高位建立精度 → 降低 ref buffer 功耗 + 提升速度。在高速 ADC 中应作为基本技术使用。

## 参考文献

- [4][5] Ali et al. (ADI), "12-b 18-GS/s RF Sampling ADC," JSSC 2020; "14 Bit 1 GS/s RF Sampling Pipelined ADC," JSSC 2014.
- [6] Z. Wang et al., "Multi-Phase Clock Generation," JSSC, 2022.
- [7] C. C. Liu et al., "10 bit 320 MS/s Low-Cost SAR ADC," JSSC, 2015.

---
type: concept
title: 高速 SAR ADC 设计
tags: [SAR-ADC, high-speed, switching-path, reset-path, multi-bit-per-cycle, comparator]
related: "[[gutietieqiu-2024-8bit-high-speed-sar-adc]], [[time-interleaving-adc]]"
created: 2026-06-07
updated: 2026-06-07
---

# 高速 SAR ADC 设计

## 速度限制因素

SAR ADC 单次转换周期 = T_comp（比较器）+ T_logic（控制逻辑）+ T_dac（DAC建立）+ T_reset（比较器复位）

- 高位时：DAC 建立时间主导
- 低位时：比较器复位时间主导（可达几十 ps，电路层面难进一步优化）

## Switching Path 优化（降低 T_logic + T_dac）

### 控制逻辑

- 经典：C. C. Liu (2010 JSSC) 基于 DFF 链的逻辑，清晰但延时大
- 优化：Pre-determined 技术 + Transparent Latch，降低逻辑门级数
- 澳门大学 CICC 2022：不匹配 N/PMOS 尺寸 + 功耗延迟优化，28nm 下 10bit 700MSPS，FoM=2.02 fJ/conv

### DAC 开关算法

先进算法降低单位电容总数（而非功耗——DAC 切换功耗占比较小）：

| 算法 | 特点 |
|------|------|
| Monotonic Switching | C. C. Liu 2010，电容减半 |
| Vcm-based | 单端电容进一步减半 |
| 顶板采样 | 消除一个采样电容 |
| 二进制冗余/重组 | 降低高位建立精度要求，提升容错和速度 |

## Reset Path 优化（降低 T_reset）

### Ping-pong Comparator

两个比较器交替工作（比较 vs 复位）。比较器1完成后触发其复位 + 比较器2启动。需保证 CDAC 建立在冗余要求的限度内。

**代表工作**：Kull et al., 8b 1.2GS/s Single-Channel, 32nm SOI, JSSC 2013.

### Loop Unrolled SAR

使用 N 个比较器，无需复位（每次转换用不同比较器）。T_bit = T_comp + T_dac，无逻辑延时，无复位时间。代价：多个比较器失调 mismatch 需单独校准。

**代表工作**：Jiang et al., 6b 1.25GS/s Single-Channel, 40nm, JSSC 2012.

### Multi-bit/cycle

单次比较 2~5 bit，降低转换次数 N。需多个比较器 + 多个 CDAC 提供多阈值。

**代表工作**：澳门大学 28nm 5bit/cycle → 9b 1.4GS/s 单通道，交织至 2.8GS/s, SNDR 51.8dB.

### 混合架构

高 4 位 Loop unrolled（高速）+ 低 4 位 latch-based（低功耗），ISSCC 2023 [8].

## 关键文献

- [10] C. C. Liu et al., "10-bit 50-MS/s SAR ADC With Monotonic Switching," JSSC, 2010.
- [9] M. Guo et al., "10b 700MS/s 1b/cycle SAR ADC," CICC, 2022.
- [13] L. Kull et al., "8b 1.2GS/s Async SAR With Alternate Comparators," JSSC, 2013.
- [14] T. Jiang et al., "1.25-GS/s 6-bit Async SAR ADC," JSSC, 2012.
- [8] Wang & Chang, "7b 4.5-GS/s 4× Interleaved SAR ADC," ISSCC, 2023.

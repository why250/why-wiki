---
type: source
title: 第八届集创赛赛题点评之"8位高速 SAR ADC的设计"
authors: ["Q总", "Y总"]
year: 2024
url: "https://mp.weixin.qq.com/s/zNVgPspcgMC3C-CxfhNmhQ"
venue: "微信公众号：固推铁球"
tags: [SAR-ADC, time-interleaving, calibration, input-buffer, clock-generation, reference-buffer, 集创赛, tutorial]
related: "[[gutietieqiu]], [[zhangtuoken-2026-adc-calibration]]"
created: 2026-06-07
updated: 2026-06-07
---

# 第八届集创赛赛题点评之"8位高速 SAR ADC的设计"

固推铁球团队的 Q 总（研一）和 Y 总（大四）历时三个月完成的集创赛赛题深度点评。针对 16GSPS / 8bit / 40nm 的赛题指标，从架构选择到电路实现再到校准算法，给出了系统性的指导。

## 核心要点

1. **架构定案**：32 路 TI 交织 + 单通道 ≥500MSPS SAR ADC。2 级 Direct sampling 足够满足 10GHz 带宽，无需 3 级 Inline Demux Sampling。2^N 路交织有利于时钟分频和相位校正。

2. **三大辅助电路**：
   - **Input Buffer**：buffer1 + SHA (T/H switch) + buffer2，Source Follower 及其改进型（Flipped VF、Super SF、Class AB），ADI 的 cascode bootstrap Vds 方案
   - **Clock Generation**：divider + DCC + 相位校正最简单实用；注入锁定环形振荡器（MPIL-ROSC）性能更优但设计难度大
   - **Reference Buffer**：需片内集成，低输出阻抗、高 PSRR、快瞬态响应。冗余技术可降低功耗和解耦电容需求

3. **单通道 SAR 速度优化**：
   - Switching path：DFF→latch 降低控制逻辑延时；先进开关算法（Monotonic、Vcm-based）降低单位电容总数
   - Reset path：Ping-pong comparator（交替比较+复位）、Loop unrolled（N 个比较器无复位）
   - Multi-bit/cycle：2~5 bit/cycle，澳门大学 28nm 下 5bit/cycle 实现 1.4GSPS 单通道
   - 混合架构：高 4 位 Loop unrolled + 低 4 位 latch-based

4. **TI 校准算法**：
   - **Offset/Gain**：成熟的统计法（均值+方差），工程实现为主
   - **Skew**：基于自相关的算法（需大量采样点，收敛慢）vs 导数法（需参考通道）
   - **2024 新趋势**：Dither-based 一次性校准 offset/gain/skew（清华 ISSCC 2024、澳门大学 ISSCC 2024）

5. **竞赛策略**：
   - 三人分工：单通道 SAR + 辅助电路 + TI 校准
   - 初赛：原理图 + MATLAB 离线校准即可
   - 一等奖：需版图 + 混合仿真 + 能效优化

## 关键概念

- [[time-interleaving-adc]] — 时间交织架构、失配类型、分级交织
- [[ti-calibration]] — Offset/Gain/Skew/Bandwidth 校准算法
- [[high-speed-sar-adc]] — 单通道 SAR 速度优化的全部技术栈
- [[adc-auxiliary-circuits]] — Input buffer、Clock gen、Reference buffer

## 参考文献亮点

- [2] Manganaro 2022: TI ADC 综述（IEEE OJSSC）
- [3] Kull 2016: 64 路交织 Inline Demux Sampling，带宽 >20GHz
- [4][5] Ali (ADI) 2014/2020: Input buffer cascode bootstrap Vds 技术
- [8] Wang & Chang ISSCC 2023: 7b 4.5GS/s unrolled+latch 混合架构
- [9] 澳门大学 CICC 2022: 不匹配 N/PMOS 尺寸优化，FoM=2.02 fJ/conv
- [20] 清华 ISSCC 2024: Dither-based 一体化校准
- [21] 澳门大学 ISSCC 2024: 12GS/s 12b TI-Pipelined ADC

## 待探究的问题

- 注入锁定环形振荡器 vs divider 方案的实际设计折中如何量化？
- Dither-based 校准相比自相关法在收敛速度上有多大优势？
- 冗余技术（二进制重组）对 ref buffer 功耗的具体改善幅度？

---
type: concept
title: TI 校准算法
tags: [ADC, calibration, time-interleaving, offset, gain, skew, bandwidth, dither]
related: [[time-interleaving-adc]], [[gutietieqiu-2024-8bit-high-speed-sar-adc]], [[dac-mismatch-effects]]
created: 2026-06-07
updated: 2026-06-07
---

# TI 校准算法

## Offset & Gain 校准

**方法**：统计各通道输出的均值和方差，算法成熟。

- Offset：比较各通道均值 → 调整各通道 ADC 的失调补偿
- Gain：比较各通道方差 → 调整各通道增益系数

工程实现为主，算法创新空间小。校正可在模拟域（调整参考电压/偏置）或数字域（乘加运算）。

## Skew 校准（核心难点）

采样时间失配产生的杂散功率与输入频率和幅度相关，高频时尤为严重。

### 误差检测

**自相关法**（最广泛）：利用平稳信号自相关函数只与时间差相关的性质。优点是不需参考通道，缺点是需要大量采样点保证统计特性平稳，收敛时间长。ADI 2017 年论文使用此方案。

**导数法**：理想采样值与实际采样值之差 = 导数 × 采样时刻偏差。需要参考通道，可能引入 kickback 和 ringing。

### 误差校正

- **模拟域**：VDL（可变延迟线）调节采样时钟相位。注意：反馈环路稳定性、增加的 jitter、收敛时间
- **数字域**：一阶线性近似 + 导数补偿。增加电路复杂度，带宽受限

## Bandwidth 失配

输入前端建模为低通滤波器 H(jω)，各通道传递函数不同。可分解为频率相关的等效增益和 skew 失配，处理更复杂。

## Dither-based 校准（2024 前沿）

在 input buffer 中注入 dither 信号，一次性校准 offset、gain、skew。

| 特性 | Dither-based | 自相关/导数法 |
|------|-------------|-------------|
| 校准范围 | 一次覆盖 offset/gain/skew | 通常分开处理 |
| 收敛速度 | 快 | 慢（需大量采样点） |
| 参考通道 | 不需要 | 导数法需要 |
| 电路开销 | 需注入/检测电路 | 纯数字/VDL |

**代表性工作**：
- 清华 ISSCC 2024 [20]：4.8GS/s 7-ENoB TI-SAR，dither-based skew + bit-distribution offset
- 澳门大学 ISSCC 2024 [21]：12GS/s 12b 4× TI-Pipelined，全面校准 + linearized input buffer

## 参考文献

- [16] J. Fang et al., "A 5-GS/s 10-b 76-mW TI-SAR ADC in 28 nm CMOS," TCAS-I, 2017.
- [17] B. Razavi, "Design Considerations for Interleaved ADCs," JSSC, 2013.
- [20] Y. Tao et al. (清华), ISSCC 2024.
- [21] Y. Cao et al. (澳门大学), ISSCC 2024.

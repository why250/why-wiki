---
type: source
title: "Modeling of Glitches due to Rise/Fall Asymmetry in Current-Steering Digital-to-Analog Converters"
authors: ["K. Ola Andersson", "Mark Vesterbacka"]
year: 2005
url: ""
venue: "IEEE Transactions on Circuits and Systems I: Regular Papers"
tags: [DAC, glitch, rise-fall-asymmetry, behavioral-modeling, SFDR]
related: ["[[wikner-tan-1997-dac-imperfections]]", "[[doris-2003-mismatch-timing-errors]]"]
created: 2026-06-15
updated: 2026-06-15
---

# Modeling of Glitches due to Rise/Fall Asymmetry in Current-Steering DACs

## 核心要点

- 建立了由电流源**上升/下降沿不对称**引起的 Glitch 的通用行为模型：s_on(t) ≠ s_off(t) 为任意函数（泛化了前人用阻尼正弦波建模的方法）
- 推导出 glitch 大小**正比于切换单元总数 g(n)**：I_out,g(t) = I_u · p_g(t) · n_tot
- 提出 **"input-referred glitch"** 概念：将 glitch 在频域中等效为输入端的离散时间信号，简化频域分析
- Thermometer-coded DAC：glitch 产生**偶次谐波**（以二次谐波为主），SFDR 随信号频率 20dB/dec 下降
- 差分输出中 rise/fall 不对称 glitch 是**共模信号**，理想差分对消，但实际失配会导致残留

## 关键概念

- **glitch 能量最小化**：选择 s(t) = (s_on + s_off)/2 作为名义开关函数，最小化非线性失真部分的 glitch 能量
- **g(n) 作为编码方案比较指标**：g(n) = Σ w_l · |b_l(n) − b_l(n-1)| 是每次采样切换的单元电流源总数，Thermometer 编码的 g(n) 远小于二进制编码
- **输入参考 glitch 频谱**：G_ir(e^{jωT}) = [P_g(ω)/P(ω)] · G(e^{jωT})，在 Nyquist 频带内等效
- **二进制 vs Thermometer**：8-bit 仿真中二进制加权 DAC glitch 远大于 Thermometer-coded DAC
- **SFDR 分析**：SFDR ∝ 1/ω²，频率每增加 10 倍下降 20dB

## 与已有内容的关联

- 与 [[doris-2003-mismatch-timing-errors]] 互补：Doris 关注失配导致的时序误差（统计框架），Andersson 关注开关不对称导致的 glitch（确定性行为模型）
- glitch 产生的非线性失真是 [[dac-dynamic-performance]] 中 SFDR 劣化的重要机制之一
- 差分输出分析补充了 [[current-steering-dac]] 的讨论

## 待探究的问题

- 将 rise/fall 不对称 glitch 模型与 Doris 的失配时序误差框架统一
- 其他 glitch 源（如数字串扰、时钟偏斜）与 rise/fall 不对称的相互作用
- DEM（动态元件匹配）对 glitch 功率谱的塑形效果

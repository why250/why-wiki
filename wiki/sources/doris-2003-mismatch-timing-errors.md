---
type: source
title: "Mismatch-Based Timing Errors in Current Steering DACs"
authors: ["Konstantinos Doris", "Arthur van Roermund", "Domine Leenaerts"]
year: 2003
url: ""
venue: "IEEE ISCAS 2003, Bangkok, Thailand"
tags: [DAC, timing-errors, mismatch, segmentation, SFDR]
related: ["[[wikner-tan-1997-dac-imperfections]]", "[[bosch-2004-dac-limitations]]"]
created: 2026-06-15
updated: 2026-06-15
---

# Mismatch-Based Timing Errors in Current Steering DACs

## 核心要点

- 建立了 CS-DAC **时序误差的统一数学框架**，按信号依赖性/空间分布（局部 vs 全局）/时间尺度进行分类
- **核心洞察**：时序误差的信号误差由切换链条的**平均值**决定，而不是幅度误差的累加机制——这是大数定律的体现
- 推导出等效时序误差方差 σ²_Tε = σ²/|Δw|：切换的单元越多，等效时序误差越小，性能越好
- SDR 公式：SDR = 3(N-1) − 20log₁₀(σ·BW) − 10log₁₀(OSR) − 12.03 dB
  - 每位分辨率提升 3dB
  - 随 σ 以 20dB/dec 下降
  - 随信号频率和采样率以 10dB/dec 下降（与时钟抖动相反——提高 OSR 反而恶化性能）
- 12-bit 100MHz Nyquist DAC 需要 σ≈1 psec 的时序精度
- **分段最优化**：在 12-bit DAC 中，Thermometer 段至少需要 8-bit 才能在 100MHz 达到 12-bit 精度

## 关键概念

- **时序误差分类**：局部（local）vs 全局（global）、确定性 vs 随机、时变 vs 时不变
- **等效时序误差 Tε**：将开关电荷误差等效为时序偏移，Tε(w₀,w₁) = 平均切换链条的时序误差
- **TNL (Timing Non Linearity)**：时域中的 INL 类比——描述时序误差随输入码的传递函数
- **脉冲持续时间调制 (PDM)**：所有时序误差对输出信号的通用调制机制
- **大数定律效应**：σ²_Tε ∝ 1/|Δw|，增加分段可以缩小等效时序误差
- **σΔ 调制器的困境**：噪声整形增加了 Δw/ΔT，反而放大了时序误差功率

## 与已有内容的关联

- 与 [[wikner-tan-1997-dac-imperfections]] 互补：Wikner 侧重于电路级非理想因素的性能影响，Doris 提供了时序误差的数学框架
- 与 [[bosch-2004-dac-limitations]] 互补：Bosch 全面讨论 DAC 静态/动态性能限制，Doris 深入时域误差机制
- 分段最优化的结论与 Bosch Ch 4-5 中的讨论一致：最大化 Thermometer 分段比

## 待探究的问题

- 全局时序误差（如时钟抖动）与局部失配时序误差之间的交互效应
- 在 CT-ΣΔ 调制器中应用该框架的实际设计案例
- 校准技术能否将有效的 σ 降低到 1 psec 以下

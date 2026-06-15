---
type: concept
title: DAC Timing Errors
tags: [DAC, timing-errors, dynamic-performance, mismatch]
related: ["[[doris-2003-mismatch-timing-errors]]", "[[dac-mismatch-effects]]", "[[dac-dynamic-performance]]"]
created: 2026-06-15
updated: 2026-06-15
---

# DAC Timing Errors

电流舵 DAC 中由晶体管失配引起的开关时序偏差。输出瞬态的定时因 cell 差异而变化，导致非线性失真，是高速 DAC 动态性能的关键限制因素。

## Doris 框架（2003）

[[doris-2003-mismatch-timing-errors]] 建立了统一的数学分类体系：

### 误差分类
| 维度 | 类型 | 说明 |
|------|------|------|
| 空间范围 | Local vs Global | 单个 cell 偏差 vs 所有 cell 系统性偏移 |
| 可预测性 | Deterministic vs Stochastic | 梯度/IR-drop 等确定性因素 vs 随机失配导致 |
| 时间依赖 | Time-invariant vs Time-variant | 固定偏差 vs 随信号/温度波动 |

### 关键概念

**等效时序误差 Tε**：DAC 差分输出之间的相对定时精度，定义为每个开关输出波形之间等效时序误差的方差。Doris 证明 Tε 的方差由失配功率与差分输入活性之比的定律决定（大数定律形式）：

$$\sigma^2_{T_\varepsilon} = \frac{\sigma^2}{|\Delta w|}$$

其中 σ² 是单位电流源的失配功率，Δw 是差分输入编码的切换活性。

**Timing Non-Linearity (TNL)**：时域中的 INL 类比。在时域中定义为实际与理想非线性误差功率的函数，数值上等同时域中非线性误差功率与线性部分功率之比（对数尺度）。

**Pulse Duration Modulation (PDM)**：失配导致脉冲宽度调制——正的时序误差使脉冲增宽，负的使脉冲变窄。PDM 效应随信号频率升高而放大。

### SDR 公式

Doris 推导出封闭形式的 SDR（Signal-to-Distortion Ratio）：

$$SDR = 3(N-1) - 20\log_{10}(\sigma \cdot BW) - 10\log_{10}(OSR) - 12.03 \text{ dB}$$

- N：分辨率（bit）
- σ：单位失配 spread（百分比）
- BW：信号带宽（Hz）
- OSR：过采样比

### 分段优化

Segmentation 的时序误差动力取决于：时序误差由局部失配决定（比率随分段度 β 增加而提高），但平均效应由大数定律控制。分段优化需要在减少失配误差（更多 thermometer 位）和减少时序误差（更多 binary 位以减少切换活动）之间平衡。

## 与 Gaasch 模型的对比

与 Gaasch & Peyton (1998) 的数值方法不同，Doris 框架提供了解析公式，可直接指导设计决策。

## 与其他动态效应的关系

- [[dac-mismatch-effects]]：时序误差是失配效应的动态表现之一
- [[dac-dynamic-performance]]：TNL 和 PDM 是动态性能的重要组成部分
- [[dac-glitch-asymmetry]]：rise/fall 不对称是 glitch 的来源，与 timing mismatch 有互补关系
- [[dac-switching-schemes]]：开关方案直接影响时序误差的大小和分布
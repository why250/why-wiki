---
type: concept
title: INL 良率 (INL Yield)
tags: [DAC, INL, yield, mismatch, Monte-Carlo, statistics]
related: [[bosch-2004-dac-limitations-ch-04-static-behaviour]], [[dac-static-performance]], [[transistor-mismatch]]
created: 2026-06-08
updated: 2026-06-08
---

# INL 良率 (INL Yield)

## 定义

INL_yield = 在给定工艺失配条件下，INL < 0.5 LSB 的 DAC 芯片占总产量的百分比。

## 四种建模方法

### 1. Lakshmikumar (1986) — 过于保守

$$INL\_yield = \prod_{i=2}^{2^N-1} \text{erf}(Q_i/\sqrt{2})$$

假设各输出码之间不相关 → 独立概率相乘 → 低估良率 → 过度设计（晶体管过大）。

### 2. Lakshmikumar 修正 (1988) — 过于乐观

仅考虑 MSB 跳变前后两个输出码 → 高估良率 → 设计不足。

### 3. Monte Carlo — 准确但慢

对每个 $\sigma(I)$ 重复 > 100 次随机仿真。14-bit DAC 需要数小时 CPU 时间。

### 4. Bosch 新公式 — 准确且快

核心洞察：当随机游走过程 |Y(j)| 达到 0.5 LSB 时，有 50% 概率继续增大、50% 减小。

$$P(\exists j: |Y(j)| \ge 0.5) = 2 \cdot P(|Y(2^N)| \ge 0.5)$$

用 erf 函数表达为闭合形式，与 Monte Carlo 高度吻合，速度快 1000+ 倍。

## 设计意义

- 给定工艺 → 预测可达分辨率下的良率
- 给定目标良率 → 反推所需 $\sigma(I)/I$ → 确定晶体管尺寸

## 来源

- [[bosch-2004-dac-limitations-ch-04-static-behaviour]] — Bosch et al. (2004) Ch 4

---
type: source
title: "Static and Dynamic Performance Limitations for High Speed D/A Converters — Ch 4: Static Behaviour of Current Steering D/A Converters"
book: "[[bosch-2004-dac-limitations]]"
chapter: 4
authors: [Anne Van den Bosch, Michiel Steyaert, Willy Sansen]
year: 2004
url: ""
venue: "Book Chapter, Springer"
tags: [DAC, static-performance, INL, yield, mismatch, Monte-Carlo, gradients, switching-schemes]
related: "[[dac-static-performance]], [[transistor-mismatch]], [[inl-yield]], [[dac-switching-schemes]]"
created: 2026-06-08
updated: 2026-06-08
---

# Ch 4: Static Behaviour of Current Steering D/A Converters

## 核心要点

1. **INL 良率概念**：INL_yield = INL < 0.5 LSB 的合格芯片百分比。工艺偏差使不同芯片的 INL 随机变化，需要统计框架预测良率。

2. **三种 INL 良率建模方法**：

| 方法 | 精度 | 速度 | 问题 |
|------|:---:|:---:|------|
| Lakshmikumar (1986) | 过于保守 | 快 | 假设各输出独立，不成立 |
| Lakshmikumar 修正 (1988) | 过于乐观 | 快 | 仅考虑 MSB 跳变 |
| Monte Carlo | 准确 | **慢**（14-bit 需数小时） | CPU 时间巨大 |
| **新公式** (Bosch) | 准确 | **快**（千倍于 MC） | — |

3. **新 INL 良率公式的核心思想**：当 |Y(j)| 达到 0.5 LSB 时，有 50% 概率继续增大、50% 概率减小。因此：
   $$P(\exists j: |Y(j)| \ge 0.5) = 2 \cdot P(|Y(2^N)| \ge 0.5)$$

   使用 erf 函数给出闭合表达式，与 Monte Carlo 仿真吻合良好。

4. **系统误差（梯度）**：
   - 来源：热梯度（功耗器件发热）、电梯度（电源压降）、工艺梯度（氧化层厚度渐变）
   - 解决：**开关方案**——通过物理布局排列使每个电流源的梯度误差被平均化

## 关键概念

- [[inl-yield]] — INL 良率的四种建模方法
- [[dac-switching-schemes]] — 消除系统梯度的开关方案
- [[transistor-mismatch]] — 电流源失配是静态性能的根本限制

## 来源

- [[bosch-2004-dac-limitations]] — Bosch et al. (2004) Ch 4

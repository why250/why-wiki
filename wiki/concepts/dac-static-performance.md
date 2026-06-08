---
type: concept
title: DAC 静态性能
tags: [DAC, static-performance, INL, DNL, mismatch, offset, gain-error]
related: [[bosch-2004-dac-limitations-ch-01-introduction]], [[dac-dynamic-performance]], [[transistor-mismatch]], [[current-steering-dac]]
created: 2026-06-08
updated: 2026-06-08
---

# DAC 静态性能

## 定义

静态性能描述 DAC 的 DC 传输特性——理想 DAC 输出与输入码呈线性关系，实际电路存在偏差。

## 主要指标

| 指标 | 全称 | 描述 |
|------|------|------|
| **Offset Error** | 偏移误差 | 零输入码时的非零输出 |
| **Gain Error** | 增益误差 | 传输曲线斜率的偏差 |
| **DNL** | Differential Non-Linearity | 相邻码之间的步长与理想 LSB 的偏差 |
| **INL** | Integral Non-Linearity | 实际输出与理想直线之间的最大偏差 |
| **Monotonicity** | 单调性 | 输出是否始终随输入码增大而增大 |

## 静态性能的关键限制

对于电流舵 DAC，静态性能**主要受电流源晶体管失配（mismatch）限制**。

- 随机失配 → INL 良率公式
- 系统误差（梯度） → 可通过开关方案优化

详见 [[bosch-2004-dac-limitations-ch-01-introduction|Bosch Ch 4]]。

## 与动态性能的对比

| | 静态 | 动态 |
|------|------|------|
| 频率 | DC | 宽频带 |
| 应用 | 仪表、测量 | 通信系统 |
| 关键指标 | INL、DNL | SFDR、SNR、IMD |
| 主要限制 | 晶体管失配 | 输出阻抗、开关瞬态 |

## 来源

- [[bosch-2004-dac-limitations-ch-01-introduction]] — Bosch et al. (2004)

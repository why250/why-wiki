---
type: concept
title: 晶体管失配
tags: [mismatch, transistor, CMOS, process-variation, Pelgrom, Lakshmikumar]
related: "[[bosch-2004-dac-limitations-ch-01-introduction]], [[dac-static-performance]], [[dac-mismatch-effects]]"
created: 2026-06-08
updated: 2026-06-08
---

# 晶体管失配 (Transistor Mismatch)

## 概述

由于制造过程中的工艺波动，两个名义上相同的晶体管在实际电特性上存在随机差异。这种失配是高精度模拟电路（如 DAC、ADC）性能的根本限制之一。

## 主要模型（按时间演进）

| 模型 | 提出者 | 年份 | 特点 |
|------|--------|------|------|
| Lakshmikumar | Lakshmikumar et al. | 1986 | 基础模型：$\sigma(V_T)$ 和 $\sigma(\beta)$ 与面积成反比 |
| Pelgrom | Pelgrom et al. | 1989 | 经典 $A_{VT}/\sqrt{WL}$ 公式，广泛引用 |
| Drennan-McAndrew | Drennan, McAndrew | — | 深亚微米修正 |
| Croon | Croon et al. | — | 关注短沟道和窄沟道效应 |

Pelgrom 公式：
$$\sigma(V_T) = \frac{A_{VT}}{\sqrt{WL}}, \quad \sigma(\beta) = \frac{A_\beta}{\sqrt{WL}}$$

## 对 DAC 的影响

- 电流源晶体管的 $V_T$ 和 $\beta$ 失配 → 输出电流误差 → INL/DNL 退化
- MSB 电流源的失配影响远大于 LSB（误差 $\propto 2^{i-1}$）

详见 [[bosch-2004-dac-limitations-ch-01-introduction|Bosch Ch 4 & Ch 8]] 和 [[dac-mismatch-effects]]。

## 来源

- [[bosch-2004-dac-limitations-ch-01-introduction]] — Bosch et al. (2004) Ch 8

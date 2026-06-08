---
type: concept
title: 电容型 DAC
tags: [DAC, capacitor, charge-redistribution, architecture]
related: "[[bosch-2004-dac-limitations-ch-03-architectures]], [[current-steering-dac]], [[resistor-dac]]"
created: 2026-06-08
updated: 2026-06-08
---

# 电容型 DAC

## 原理

通过开关控制电容底板在 GND 和 $V_{ref}$ 之间切换，实现电荷重分布。二进制版本通过调整电容值实现位权重。

## 关键限制

- 电容失配：$\Delta C/C = \Delta W/W + \Delta L/L - \Delta t_{ox}/t_{ox}$
- 底版寄生电容影响精度
- 开关电荷注入引入误差

## 来源

- [[bosch-2004-dac-limitations-ch-03-architectures]] — Bosch et al. (2004) Ch 3

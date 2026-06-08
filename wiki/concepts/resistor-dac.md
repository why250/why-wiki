---
type: concept
title: 电阻型 DAC
tags: [DAC, resistor, architecture, resistor-string, R-2R]
related: "[[bosch-2004-dac-limitations-ch-03-architectures]], [[current-steering-dac]], [[capacitor-dac]]"
created: 2026-06-08
updated: 2026-06-08
---

# 电阻型 DAC

## 三种实现

| 类型 | 原理 | 特点 |
|------|------|------|
| Resistor String | 参考电压分压到 $2^N-1$ 个抽头 | 天然单调，但 10+ 位时面积过大 |
| Binary Weighted | 每位一个电阻，值 $\propto 2^i$ | 电阻少，但阻值范围宽，不保证单调 |
| R-2R | 仅用 R 和 2R 两种值 | 面积小、精度高，但时序差异引入 glitch |

## 关键限制

- INL 直接与电阻匹配精度相关：$INL \propto V_{ref}/\sqrt{4N} \cdot \Delta R/R$
- 开关网络延迟限制更新速率
- 电阻非线性（电压系数）引入失真

## 来源

- [[bosch-2004-dac-limitations-ch-03-architectures]] — Bosch et al. (2004) Ch 3

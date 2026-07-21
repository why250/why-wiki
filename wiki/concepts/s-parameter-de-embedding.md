---
type: concept
title: S 参数去嵌
tags:
  - S-parameters
  - de-embedding
  - network-parameters
  - microwave-measurement
  - FET-modeling
related:
  - [[dambrine-1988-fet-equivalent-circuit]]
  - [[fet-small-signal-equivalent-circuit]]
  - [[cold-fet-extraction]]
created: 2026-07-21
updated: 2026-07-21
---

# S 参数去嵌

## 概念

S 参数去嵌（De-embedding）是指从测量的**外器件**（含寄生）S 参数中，通过矩阵变换逐层剥离已知的寄生元件，最终得到**本征器件**的 S/Y/Z 参数的过程。

## Dambrine 的 4 步去嵌法

已知所有寄生元件值后，通过 5 组矩阵操作剥离寄生：

```
[S_ext] → [Z_ext]
             ↓ 减去串联 Lg, Ld
           [Z']
             ↓ Z → Y
           [Y']
             ↓ 减去并联 Cpg, Cpd
           [Y'']
             ↓ Y → Z
           [Z'']
             ↓ 减去串联 Rg, Rs, Ls, Rd
           [Z''']
             ↓ Z → Y
           [Y_int] → 本征 Y 参数
```

### 每步的物理意义

| 步骤 | 操作 | 剥离的寄生 |
|------|------|-----------|
| 1 | Z 参数减去 jωLg, jωLd | 栅/漏引线电感 |
| 2 | Y 参数减去 jωCpg, jωCpd | 栅/漏 pad 对地电容 |
| 3 | Z 参数减去 Rg, Rs, jωLs, Rd | 栅/源/漏串联电阻和源电感 |
| 4 | 得到本征 Y 参数 | — |

## 前置条件

- 必须先通过 [[cold-fet-extraction]] 获取所有寄生元件值
- 测量频率范围需满足低频近似（D ≈ 1, ωτ ≪ 1）
- 对于超短栅长 / 小栅宽器件，需将测量频段整体上移以确保 Y 参数不过小

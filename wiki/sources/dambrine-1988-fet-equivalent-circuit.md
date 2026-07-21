---
type: source
title: "A New Method for Determining the FET Small-Signal Equivalent Circuit"
authors:
  - Gilles Dambrine
  - Alain Cappy
  - Frédéric Heliodore
  - Edouard Playez
year: 1988
url: ""
venue: "IEEE Transactions on Microwave Theory and Techniques, Vol. 36, No. 7, pp. 1151–1159"
tags:
  - FET
  - small-signal-model
  - equivalent-circuit
  - S-parameters
  - parasitic-extraction
  - cold-FET
related:
  - [[berroth-1990-fet-broadband]]
created: 2026-07-21
updated: 2026-07-21
---

# A New Method for Determining the FET Small-Signal Equivalent Circuit

## 核心要点

### 问题

传统 FET 小信号等效电路提取依赖宽频 S 参数优化拟合，有三个缺点：
- 需要精确的宽频 S 参数测量
- 优化结果依赖初值和算法选择
- 部分参数（如 Rg、Lg）需要预先已知才有物理意义

### 方法

提出**直接测量法**：在低频段（1–5 GHz）通过两个特殊偏置条件分步提取所有寄生参数，再用矩阵操作剥离出本征 Y 参数，进而直接求解本征元件值。

**两步寄生提取：**

1. **Vds=0 + 正向栅极电流**（~5×10⁷ A/m²）→ 栅极电容效应消失，从 Z 参数虚部斜率提取 Ls/Lg/Ld，从实部关系解 Rs/Rg/Rd/Rc
2. **Vds=0 + Vgs < Vp（夹断）** → 沟道导电性消失，从 Y 参数虚部提取 Cpg、Cpd、Cb

**本征参数提取（4 步矩阵操作）：**
1. S → Z，减去串联 Lg、Ld
2. Z → Y，减去并联 Cpg、Cpd
3. Y → Z，减去串联 Rg、Rs、Ls、Rd
4. Z → Y，得到本征 Y 矩阵

### 低频近似

在 F < 5 GHz 条件下：
- D = 1 + ω²Cgs²Ri² ≈ 1（误差 < 1%）
- exp(-jωτ) ≈ 1 - jωτ

简化后的 Y 参数表达式使本征参数可直接求解，无需迭代优化。

### 精度

| 参数 | 估计精度 |
|------|----------|
| gm, gd, Cgs, Cgd, Cds | 2–3% |
| Ri | 可达 50%（Re(y11) 值极小，对噪声敏感） |
| τ（渡越时间） | 约 20% |

### 验证

低频提取的等效电路计算出的 S 参数在 **1–26.5 GHz** 范围内与实测 S11/S21/S22 吻合良好。S12 偏差较大，属预期。

---

## 关键概念

- [[fet-small-signal-equivalent-circuit]] — FET 小信号等效电路的标准拓扑与本征/寄生参数分类
- [[cold-fet-extraction]] — Vds=0 条件下的寄生参数提取技术
- [[s-parameter-de-embedding]] — 通过矩阵变换剥离外寄生参数、还原本征参数的过程

## 开创性意义

这是 FET 小信号建模领域的**奠基性论文之一**（截至 2024 年引用超 3000 次），首次提出无需宽频 S 参数优化即可完整、直接地确定所有等效电路元件值的方法。该方法特别适合 wafer-probing 系统，为工艺表征和大规模器件建模铺平了道路。

## 局限性

- Ri 和 τ 提取精度有限
- 要求器件 D≈1 假设成立（F < 5 GHz），对亚微米栅长器件可能需要调整频段
- 高栅极金属化电阻时需考虑分布效应
- S12 在宽频范围的拟合不如其他 S 参数

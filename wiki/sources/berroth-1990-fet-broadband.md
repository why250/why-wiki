---
type: source
title: "Broad-Band Determination of the FET Small-Signal Equivalent Circuit"
authors:
  - Manfred Berroth
  - Roland Bosch
year: 1990
url: ""
venue: "IEEE Transactions on Microwave Theory and Techniques, Vol. 38, No. 7, pp. 891–895"
tags:
  - FET
  - small-signal-model
  - equivalent-circuit
  - S-parameters
  - parasitic-extraction
  - cold-FET
  - MESFET
  - HEMT
related:
  - [[dambrine-1988-fet-equivalent-circuit]]
  - [[fet-small-signal-equivalent-circuit]]
  - [[cold-fet-extraction]]
  - [[s-parameter-de-embedding]]
  - [[manfred-berroth]]
  - [[fraunhofer-hhi]]
created: 2026-07-21
updated: 2026-07-21
---

# Broad-Band Determination of the FET Small-Signal Equivalent Circuit

## 核心要点

### 对 Dambrine 方法的改进

[[dambrine-1988-fet-equivalent-circuit]] 将本征参数提取限制在 **F < 5 GHz**（依赖 D≈1 和 ωτ≪1 近似）。Berroth & Bosch 去除了这两个近似，给出**全频段解析公式**（公式 6-12），可以在任意频点或频段内求解 7 个本征元件。

### 全频段解析解（7 个本征元件）

$$C_{gd} = -\frac{\operatorname{Im}(Y_{12})}{\omega}$$

$$C_{gs} = \frac{\text{Im}(Y_{11}) - \omega C_{gd}}{\omega} \left[ 1 + \frac{(\text{Re}(Y_{11}))^2}{(\text{Im}(Y_{11}) - \omega C_{gd})^2} \right]$$

$$R_{i} = \frac{\text{Re}(Y_{11})}{(\text{Im}(Y_{11}) - \omega C_{gd})^{2} + (\text{Re}(Y_{11}))^{2}}$$

$$g_m = \sqrt{\left((\text{Re}(Y_{21}))^2 + (\text{Im}(Y_{21}) + \omega C_{gd})^2\right)\left(1 + \omega^2 C_{gs}^2 R_i^2\right)}$$

$$\tau = \frac{1}{\omega} \arcsin\left(\frac{-\omega C_{gd} - \operatorname{Im}(Y_{21}) - \omega C_{gs} R_i \operatorname{Re}(Y_{21})}{g_m}\right)$$

$$C_{ds} = \frac{\operatorname{Im}(Y_{22}) - \omega C_{gd}}{\omega}$$

$$g_{ds} = \operatorname{Re}(Y_{22})$$

**关键区别：** Dambrine 方法在低频假设下将公式化简（如 gm 直接从 Im(y21) 读取），Berroth 保留了全部频率相关项，使公式在全频段有效。

### 模型自验证

这是本文的重要贡献之一：**通过考察提取参数是否频率无关来验证等效电路的有效性**。如果 gm、gds 等在整个频段内保持恒定，说明等效电路拓扑正确。这在之前的工作中未被系统性地展示。

### 对低频异常器件的处理

观察到 inverted HEMT 在夹断条件下的 Y 参数虚部呈现两段不同斜率（Fig. 4），归因于掺杂 AlGaAs 层中的并联导电通路。提出了考虑这一效应的改进等效电路（Fig. 5），用高频段斜率确定 pad 电容。

### 冷管 HEMT 修正

将 Hower-Bechtel Rs+Rd 提取法从 MESFET 推广到 HEMT：对线性传输函数器件，用 $1/(1-\eta)$ 替代 $1/(1-\sqrt{\eta})$ 绘图。

## 实验验证

- 器件范围：HEMT (lg=0.6μm, Wg=50μm)、MESFET、inverted HEMT (lg=1μm, Wg=250μm)
- 频段：50 MHz – 25 GHz（远超过 Dambrine 的 5 GHz 限制）
- 寄生电感从 Z 参数虚部提取，在 1–25 GHz 内非常恒定
- S 参数拟合：Berroth 方法在高频端明显优于 Dambrine 方法
- $g_m$ 和 $g_{ds}$ 高频下仍保持恒定，证明等效电路在高频仍有效

## 与 Dambrine 1988 的关系

| 维度 | Dambrine 1988 | Berroth & Bosch 1990 |
|------|---------------|----------------------|
| 频段限制 | < 5 GHz（D≈1 近似） | 无限制（全解析解） |
| 公式复杂度 | 简化（近似后） | 完整（含 D 因子和 arcsin） |
| τ 提取 | Im(y21) 斜率 | arcsin 解析式 |
| 自验证 | 无 | 频率无关性检验 |
| 低频异常器件 | 未涉及 | 有专门处理 |
| 适用频率上限 | 26.5 GHz（验证） | 26.5 GHz（验证），可更高 |

---
type: concept
title: FET 小信号等效电路
tags:
  - FET
  - small-signal-model
  - equivalent-circuit
  - microwave
  - device-modeling
related:
  - [[dambrine-1988-fet-equivalent-circuit]]
  - [[cold-fet-extraction]]
  - [[s-parameter-de-embedding]]
created: 2026-07-21
updated: 2026-07-21
---

# FET 小信号等效电路

## 标准拓扑

FET 的小信号等效电路分为两部分：

### 本征元件（Intrinsic，偏置相关）
位于沟道区域，受 Vgs/Vds 控制：

| 元件 | 含义 | 典型位置 |
|------|------|----------|
| gm | 跨导 | 栅-源电压控制的电流源 |
| gd | 输出电导 | 漏-源之间的并联电导 |
| Cgs | 栅-源本征电容 | 栅-源之间 |
| Cgd | 栅-漏电容（含寄生） | 栅-漏之间 |
| Cds | 漏-源电容 | 漏-源之间 |
| Ri | 输入电阻 | 与 Cgs 串联（充电电阻） |
| τ | 渡越时间延迟 | gm 的相位延迟因子 |

### 寄生元件（Extrinsic，偏置无关）
位于本征器件之外，由封装、pad、引线等引入：

| 元件 | 含义 |
|------|------|
| Lg, Ls, Ld | 栅/源/漏串联电感 |
| Rg, Rs, Rd | 栅/源/漏串联电阻 |
| Cpg, Cpd | 栅/漏 pad 对地寄生电容 |

## 本征 Y 参数

本征 FET 呈 π 型拓扑，适合用 Y 参数描述：

$$y_{11} = \frac{R_i C_{gs}^2 \omega^2}{D} + j\omega\left(\frac{C_{gs}}{D} + C_{gd}\right), \quad D = 1 + \omega^2 C_{gs}^2 R_i^2$$

$$y_{12} = -j\omega C_{gd}$$

$$y_{21} = \frac{g_m \exp(-j\omega\tau)}{1 + jR_i C_{gs}\omega} - j\omega C_{gd}$$

$$y_{22} = g_d + j\omega(C_{ds} + C_{gd})$$

## 提取方法分类

| 方法 | 代表工作 | 特点 |
|------|----------|------|
| 低频近似提取 | [[dambrine-1988-fet-equivalent-circuit]] | D≈1, ωτ≪1 近似，F<5GHz |
| 宽带解析提取 | [[berroth-1990-fet-broadband]] | 无近似，保留 D 因子和 arcsin 项，全频段有效 |
| 优化拟合 | 传统方法 | 宽频 S 参数最小二乘拟合，依赖初值 |

### 宽带解析公式（Berroth & Bosch 1990）

去除低频近似后，7 个本征参数的全频段解析解：

$$C_{gs} = \frac{\text{Im}(Y_{11}) - \omega C_{gd}}{\omega} \left[ 1 + \frac{(\text{Re}(Y_{11}))^2}{(\text{Im}(Y_{11}) - \omega C_{gd})^2} \right]$$

$$R_{i} = \frac{\text{Re}(Y_{11})}{(\text{Im}(Y_{11}) - \omega C_{gd})^{2} + (\text{Re}(Y_{11}))^{2}}$$

$$g_m = \sqrt{\left((\text{Re}(Y_{21}))^2 + (\text{Im}(Y_{21}) + \omega C_{gd})^2\right)\left(1 + \omega^2 C_{gs}^2 R_i^2\right)}$$

$$\tau = \frac{1}{\omega} \arcsin\left(\frac{-\omega C_{gd} - \operatorname{Im}(Y_{21}) - \omega C_{gs} R_i \operatorname{Re}(Y_{21})}{g_m}\right)$$

## 模型自验证

等效电路有效性的判断标准：提取的参数应在全频段内**保持恒定**。若 gm、gds 随频率显著变化，说明等效电路拓扑需改进。这一方法由 [[berroth-1990-fet-broadband]] 首次系统性提出。

---
type: concept
title: Cold-FET 寄生参数提取
tags:
  - FET
  - parasitic-extraction
  - cold-FET
  - device-characterization
  - S-parameters
related:
  - [[dambrine-1988-fet-equivalent-circuit]]
  - [[fet-small-signal-equivalent-circuit]]
  - [[s-parameter-de-embedding]]
created: 2026-07-21
updated: 2026-07-21
---

# Cold-FET 寄生参数提取

## 定义

Cold-FET 指在 **Vds = 0**（零漏源偏压）条件下对 FET 进行测量，此时器件没有放大功能（gm 不生效），但保留了无源寄生网络。通过选择不同的栅极偏置（正向导通 / 夹断），可以分别暴露不同类型的寄生参数。

## Dambrine 方法的两步提取

### Step 1: 正向栅极偏置（Vds=0，正向 Ig）

**条件：** 栅极正向导通，栅电流密度 ~5×10⁷–10⁸ A/m²

**物理原理：** 栅极电流增大使 Schottky 结的动态电阻 $R_{dy} = \frac{nkT}{qI_g}$ 急剧减小，$R_{dy}C_g\omega \to 0$，栅极电容效应消失。

**提取内容：**
- $Im(Z_{12})$ → $L_s$
- $Im(Z_{11})$ → $L_s + L_g$ → $L_g$
- $Im(Z_{22})$ → $L_s + L_d$ → $L_d$
- 三个实部关系 + 附加条件 → $R_s$、$R_g$、$R_d$、$R_c$

附加条件可选：$R_s+R_d$ 测量值、pad-to-pad Rg 直流测量、dc Rs/Rd 测量、沟道参数推导 Rc。

**注意：** 正向栅极电流下的 Rg 与正常放大偏置下的 Rg 存在分布效应差异（≤10%，常规金属化电阻下）。

### Step 2: 夹断偏置（Vds=0，Vgs < Vp）

**条件：** 栅极电压低于夹断电压，沟道完全耗尽

**物理原理：** 沟道导电性消失，本征 Cgs 消失，剩余的是 pad 寄生电容和边缘电容 Cb。

**提取内容：**
- $Im(Y_{11}) = j\omega(C_{pg} + 2C_b)$
- $Im(Y_{12}) = Im(Y_{21}) = -j\omega C_b$
- $Im(Y_{22}) = j\omega(C_{pd} + C_b)$

三个方程解三个未知数：$C_{pg}$、$C_{pd}$、$C_b$。

## 意义

- 两大寄生参数类别（串联 R/L + 并联 C）在同一 **Vds=0** 条件下完成提取
- 避免了优化拟合的初值依赖和多解问题
- 适合 wafer-probing，低频即可完成，速度快
- 提取出的寄生参数与偏置无关，可用于后续任意偏置点的本征参数提取

## HEMT 修正（Berroth & Bosch 1990）

[[berroth-1990-fet-broadband]] 将冷管技术推广到 HEMT 器件：

- **Rs+Rd 提取：** Hower-Bechtel 方法原用于 MESFET（quadratic 传输特性），对于线性传输特性的 HEMT，改用 $1/(1-\eta)$ 替代 $1/(1-\sqrt{\eta})$ 绘图
- **低频异常处理：** inverted HEMT 夹断时 Y 参数虚部出现两段斜率，源于掺杂 AlGaAs 层寄生并联通路；通过高频段斜率确定 pad 电容

## Dambrine 方法的两步提取

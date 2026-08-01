---
type: concept
title: SPICE 模型参数提取
tags: [SPICE, parameter-extraction, testkey, corner-modeling, IC-CAP, BSIMPro, WAT]
related: ["[[spice]]", "[[bsim-model]]", "[[process-corner]]", "[[wat]]", "[[xinhaishiyi-2026-spice-model]]"]
created: 2026-08-01
updated: 2026-08-01
---

# SPICE 模型参数提取

一套工艺节点的 SPICE Model 从零到 release，标准流程通常持续 **3-6 个月**，涉及器件设计、工艺集成、测试、建模四个团队的配合。

## 完整流程

### 1. Testkey 设计

RD 团队完成工艺开发后，设计专门的 SPICE 建模用测试结构（testkey），包含各种尺寸变体的独立器件：

- **MOSFET**：W 从最小尺寸到 10μm，L 从最小尺寸到 20μm，覆盖 20-50 个 W/L 组合
- **多指器件**：评估 finger 数对寄生参数的影响
- **不同阱接触布局**：评估衬底电阻网络效应
- **电容测试结构**：提取 Cgg、Cov、Cj 等寄生电容
- **辅助器件**：二极管、电阻、BJT 等

典型规模：200-500 个 DUT（Device Under Test）。尺寸 step 越细 → 精度越高，但流片面积和测量时间线性增长。

### 2. DC 测量（I-V 特性）

用精密半导体参数分析仪对每个 DUT 进行直流扫描：

| 曲线 | 扫描方式 | 提取参数 |
|------|----------|----------|
| Id-Vg | Vd = 0.05V（线性区）和 Vd = Vdd（饱和区），Vg 扫 0→Vdd | VTH、SS、Gm、Ioff |
| Id-Vd | Vg 从 VTH→Vdd（4-6 step），Vd 扫 0→Vdd | Idsat、Gds、BV |

每个 DUT 至少测 20 个重复单元取平均值，消除随机测量噪声。整套 DC 测量可产生数千条曲线。

### 3. CV 测量（电容-电压特性）

用 LCR 表在不同频率（通常 100kHz、1MHz）下扫描栅压，提取：

- **Cgg-Vg**：总栅电容 → Tox 和 Poly Depletion 效应
- **Cgc/Cgs/Cgd 分离**：RF 建模的寄生电容分配
- **Cj-Vr**：PN 结电容与反向偏压的关系

### 4. 温度扫描

所有 DC 和 CV 测量至少在 4 个温度点重复：

| 温度 | 用途 |
|------|------|
| -40°C | 低温极端条件 |
| 25°C | 室温 typical |
| 85°C | 高温工作条件 |
| 125°C | 可靠性边界 |

温度影响：$V_{TH}$ 约 -1mV/°C，迁移率约 $T^{-1.5}$，漏电流约每 10°C 翻一倍——这是所有 PVT（Process-Voltage-Temperature）corner 分析的基础。

### 5. 参数提取（Parameter Extraction）

将数千条 I-V 和 C-V 原始数据导入模型提取软件（IC-CAP、BSIMPro+、Mystic 等），采用**分步策略**（Stepwise Extraction）：

1. **长沟道器件优先**：短沟道效应可忽略，先确定基本参数（VTH0、U0、VSAT 等）
2. **固定基本参数，逐级提取短沟道参数**：DVT0/DVT1（VTH 滚降）、ETA0/ETAB（DIBL）、PCLM/PDIBL（输出电导）
3. **电容参数单独提取**：从 CV 数据提取 COX、CJ、MJ、CGSO、CGDO 等
4. **全局优化微调**：Levenberg-Marquardt 或遗传算法全局优化

**拟合权重是多目标优化的核心难题**：饱和区权重大 → 线性区漂；亚阈值区权重大 → 强反型漂。不存在"所有区域同时最优"的解，权重分配由建模工程师手动决定。

### 6. Corner Split（工艺角分拆）

工艺制造存在全局变异（lot-to-lot、wafer-to-wafer），必须覆盖工艺角。详见 [[process-corner]]。

### 7. 验证与签核（Verification & Sign-off）

- **WAT 对标**：模型预测的 Vt、Idsat、Ioff 必须与 [[wat|WAT]] 数据在 spec 范围内一致
- **环形振荡器验证**：模型仿真频率必须匹配硅实测值（误差 < 5%）
- **客户基准电路验证**：用客户典型电路跑仿真，波形必须与硅实测值吻合

## 参数拟合的优化困境

参数提取本质上是一个**多目标优化问题**：

$$\min_{\theta} \sum_i w_i \cdot \mathcal{L}_i(\theta)$$

其中 $\mathcal{L}_i$ 是第 $i$ 个工作区的 loss，$w_i$ 是建模工程师手动分配的权重。不存在所有权重同时最优的解——这是 SPICE Model 作为"统计拟合结果"的根本原因之一。

## 来源

- [[xinhaishiyi-2026-spice-model]]

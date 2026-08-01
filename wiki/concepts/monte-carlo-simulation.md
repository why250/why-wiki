---
type: concept
title: 蒙特卡洛仿真（电路良率）
tags: [Monte-Carlo, statistical-modeling, yield, mismatch, process-variation, corner]
related: ["[[process-corner]]", "[[transistor-mismatch]]", "[[inl-yield]]", "[[wat]]", "[[xinhaishiyi-2026-spice-model]]"]
created: 2026-08-01
updated: 2026-08-01
---

# 蒙特卡洛仿真（电路良率）

蒙特卡洛（Monte Carlo, MC）仿真是评估电路良率的统计方法：在工艺变异空间中随机抽样，对每个样本跑一次 SPICE 仿真，统计结果分布。

## Corner vs Monte Carlo

| 方法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| **Corner** | 5 个固定工艺边界点 | 快速（5 次仿真） | 过于保守，不反映真实分布 |
| **Monte Carlo** | 工艺空间随机抽样 | 真实反映良率分布 | 慢（1000-10000 次仿真） |

Corner 假设整片芯片上所有晶体管同向偏快或偏慢——这在现实中几乎不可能。MC 仿真允许每个晶体管独立随机扰动，更接近真实硅行为。

## MC 模型的两层结构

现代 SPICE MC 流程叠加两层变异：

1. **全局变异层（Global/Process）**：来自 corner model，同一芯片上所有晶体管同向偏移
2. **局部失配层（Mismatch/Local）**：基于 Pelgrom 模型，相邻同尺寸晶体管间的随机差异

$$\Delta V_{TH} = \Delta V_{TH}^{global} + \frac{A_{VT}}{\sqrt{WL}} \cdot \mathcal{N}(0,1)$$

## 局部失配的物理来源

- **RDF**（Random Dopant Fluctuation）：沟道区掺杂原子数量的随机涨落
- **LER**（Line Edge Roughness）：栅极线条边缘的原子级粗糙度
- **WFV**（Work Function Variation）：金属栅晶粒取向的随机分布

这三者均随器件面积缩小而增大，即 Pelgrom 公式的物理根源。

## 典型应用

- **运放 offset**：MC 仿真确定输入失调电压的 3σ 分布范围
- **DAC INL/DNL 良率**：详见 [[inl-yield]]
- **SRAM 读写容限**：6 管单元在 mismatch 下的读写稳定性
- **Bandgap 精度**：MC 确定输出电压的 σ 值和 trim 需求

## 与 INL 良率的关系

在 DAC 领域，MC 仿真可用于 INL 良率评估，但计算开销极大（14-bit DAC 需数小时）。Bosch 等人提出了基于 erf 函数的 INL 良率闭合公式，与 MC 高度吻合且速度快 1000+ 倍。详见 [[inl-yield]]。

## 来源

- [[xinhaishiyi-2026-spice-model]]
- [[bosch-2004-dac-limitations-ch-04-static-behaviour]] — INL 良率闭合公式 vs MC

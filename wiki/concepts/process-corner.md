---
type: concept
title: 工艺角（Process Corner）
tags: [process-corner, PVT, corner-modeling, global-variation, mismatch, Monte-Carlo]
related: ["[[spice-model-extraction]]", "[[monte-carlo-simulation]]", "[[wat]]", "[[transistor-mismatch]]", "[[xinhaishiyi-2026-spice-model]]"]
created: 2026-08-01
updated: 2026-08-01
---

# 工艺角（Process Corner）

工艺角（Process Corner）是半导体制造中用于捕捉**全局工艺变异**的建模方法。同一片晶圆上，不同位置的晶体管可能系统性偏快或偏慢——这是由薄膜厚度、刻蚀速率、掺杂浓度等工艺参数的 wafer-level 梯度引起的。

## 五种标准 Corner

| Corner | NMOS | PMOS | 含义 |
|--------|------|------|------|
| **TT** | Typical | Typical | 标称工艺条件 |
| **FF** | Fast | Fast | NMOS/PMOS 同向偏快（Idsat 偏高） |
| **SS** | Slow | Slow | NMOS/PMOS 同向偏慢（Idsat 偏低） |
| **SF** | Slow | Fast | NMOS 偏慢、PMOS 偏快 |
| **FS** | Fast | Slow | NMOS 偏快、PMOS 偏慢 |

所有 corner 还需叠加电压（±10%）和温度（-40°C / 25°C / 125°C），构成完整的 **PVT（Process-Voltage-Temperature）** 分析矩阵。

## 全局变异 vs 局部失配

| 变异类型 | 来源 | 空间尺度 | 建模方法 |
|----------|------|----------|----------|
| **全局变异** | lot-to-lot, wafer-to-wafer 工艺漂移 | 整片晶圆 | Corner Model（TT/SS/FF/SF/FS） |
| **局部失配** | RDF、LER、WFV 等随机涨落 | 相邻器件 | Pelgrom 模型：$\sigma(V_{TH}) = A_{VT}/\sqrt{WL}$ |

传统五 corner 模型假设**整颗芯片上所有晶体管同向偏快或偏慢**。这过于保守，导致 over-design。

## 统计模型：从 Corner 到 Monte Carlo

现代 SPICE 流程在 corner model 之上叠加 mismatch 模型，跑 Monte Carlo 仿真评估良率。详见 [[monte-carlo-simulation]]。

## Corner 的局限性

- 只覆盖工艺边缘，不覆盖中间态分布
- 对某些电路（如运放 offset），SS/FF corner 组合可能过于保守
- 5 个 corner 无法捕捉多维工艺参数的联合分布

## 来源

- [[xinhaishiyi-2026-spice-model]]

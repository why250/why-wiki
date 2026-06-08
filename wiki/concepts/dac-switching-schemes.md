---
type: concept
title: DAC 开关方案
tags: [DAC, switching-schemes, gradients, systematic-errors, layout, current-steering]
related: "[[bosch-2004-dac-limitations-ch-04-static-behaviour]], [[dac-static-performance]], [[current-steering-dac]]"
created: 2026-06-08
updated: 2026-06-08
---

# DAC 开关方案 (Switching Schemes)

## 问题

电流源阵列中的系统误差（热梯度、电梯度、工艺梯度）在空间上呈线性或二次分布，若电流源按顺序排列，梯度误差会累积导致系统 INL 退化。

## 梯度误差模型

线性梯度在 x-y 平面上产生空间变化的电流误差：
$$\Delta I(x,y) = g_x x + g_y y + \text{higher order terms}$$

## 开关方案分类

| 方案 | 原理 | 梯度抑制 |
|------|------|---------|
| Sequential（顺序） | 电流源按比特顺序排列 | 差 — 梯度直接累积 |
| Conventional Symmetrical | 关于中心对称排列 | 中 — 一次梯度消除 |
| Hierarchical Symmetrical | 分级对称 | 好 — 高阶梯度消除 |
| 2-D Centroid（质心对称） | 每电流源的中心在全局质心 | 最佳 |
| Q² Random Walk | 随机游走排列 | 优 — 梯度转为噪声 |

## 设计原理

- **不依赖译码器的方案**：物理布局直接实现对称，不增加数字逻辑
- **解析优化**：通过数学分析确定最优电流源位置，最小化 INL 在给定梯度下的期望值

## 来源

- [[bosch-2004-dac-limitations-ch-04-static-behaviour]] — Bosch et al. (2004) Ch 4

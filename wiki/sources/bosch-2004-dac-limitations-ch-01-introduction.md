---
type: source
title: "Static and Dynamic Performance Limitations for High Speed D/A Converters — Ch 1: Introduction"
book: "[[bosch-2004-dac-limitations]]"
chapter: 1
authors: [Anne Van den Bosch, Michiel Steyaert, Willy Sansen]
year: 2004
url: ""
venue: "Book Chapter, Springer"
tags: [DAC, current-steering, introduction, overview]
related: [[current-steering-dac]], [[dac-dynamic-performance]], [[dac-static-performance]], [[transistor-mismatch]]
created: 2026-06-08
updated: 2026-06-08
---

# Ch 1: Introduction

## 核心要点

1. **研究背景**：通信市场（尤其是移动通信）在过去十年中快速增长，对高精度、高速、低功耗的数据转换器需求日益迫切。

2. **本书聚焦**：电流舵（current steering）DAC 的静态和动态性能限制——这是目前 CMOS 工艺下兼顾速度、精度和功耗的最佳架构。

3. **静态性能**：主要取决于电流源晶体管的匹配行为（mismatch），包含随机误差（工艺偏差）和系统误差（热/电/工艺梯度）。

4. **动态性能**：除了已知的三个因素（开关同步、数字馈通、漏极电压变化），本书引入第四个关键因素——**输出阻抗的频率依赖性**。

## 全书结构

- Ch 2 — DAC 功能描述与性能规格（静态+动态）
- Ch 3 — DAC 拓扑概述（电阻型、电容型、电流舵型）
- Ch 4 — 电流舵 DAC 的静态行为（随机+系统误差）
- Ch 5 — 电流舵 DAC 的动态行为（输出阻抗频率效应）
- Ch 6 — 设计流程（分段策略、译码器、开关驱动、单元尺寸）
- Ch 7 — 实现案例（12-bit → 14-bit → 10-bit 1GS/s → 12-bit 500MS/s）
- Ch 8 — 晶体管失配模型演进（Lakshmikumar → Pelgrom → 深亚微米）

## 关键实体

- [[anne-van-den-bosch]], [[michiel-steyaert]], [[willy-sansen]] — KU Leuven, 作者

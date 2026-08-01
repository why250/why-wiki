---
type: concept
title: WAT（Wafer Acceptance Test）
tags: [WAT, wafer-test, manufacturing, scribe-line, DC-test]
related: ["[[spice-model-extraction]]", "[[process-corner]]", "[[xinhaishiyi-2026-spice-model]]"]
created: 2026-08-01
updated: 2026-08-01
---

# WAT（Wafer Acceptance Test）

WAT（Wafer Acceptance Test）是每片晶圆出货前必须通过的测试：在晶圆划片槽（scribe line）上的 testkey 器件上测量 DC 参数，超出 spec 则整片报废。

## 测试内容

WAT 主要测量 DC 参数：
- **Vt**（阈值电压）
- **Idsat**（饱和漏电流）
- **Ioff**（关态漏电流）
- **BV**（击穿电压）

## 三个天生局限

### 1. 位置偏差

划片槽位于晶圆边缘，工艺条件（薄膜厚度、刻蚀速率、热预算）与芯片核心区域不完全一致。WAT 数据不能精确代表芯片内部的器件行为。

### 2. 只测 DC，不测 AC

WAT 不测以下关键参数：
- **fT**（特征频率 / 截止频率）
- **NFmin**（最小噪声系数）
- **Matching**（器件匹配对特性）

一颗 LNA 的噪声系数偏离 spec 2dB 是**完全可能的**，即使 WAT 全部合格。

### 3. 只测 nominal structure

WAT testkey 的尺寸和结构有限，客户的特殊器件（如高压 LDMOS、RF FET）可能没有被覆盖。

## WAT 与 SPICE Model 的关系

WAT 是 SPICE Model 签核的必要条件，但不是充分条件：
- WAT 通过 ≠ 模型准确（只能保证 DC nominal 行为）
- WAT 通过 ≠ AC/RF 性能达标
- WAT 通过 ≠ 客户特殊器件被覆盖

**WAT 不是模型的「终极仲裁者」**。

## 来源

- [[xinhaishiyi-2026-spice-model]]

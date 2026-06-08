---
type: source
title: "Static and Dynamic Performance Limitations for High Speed D/A Converters — Ch 3: CMOS D/A Converter Architectures"
book: "[[bosch-2004-dac-limitations]]"
chapter: 3
authors: [Anne Van den Bosch, Michiel Steyaert, Willy Sansen]
year: 2004
url: ""
venue: "Book Chapter, Springer"
tags: [DAC, architectures, resistor, capacitor, current-steering, binary, thermometer, segmented]
related: [[current-steering-dac]], [[binary-weighted-dac]], [[resistor-dac]], [[capacitor-dac]]
created: 2026-06-08
updated: 2026-06-08
---

# Ch 3: CMOS D/A Converter Architectures

## 核心要点

1. **三大 DAC 架构**：按参考量类型分为电阻型（电压分压）、电容型（电荷重分布）、电流舵型（加权电流求和）。

2. **电阻型 DAC**：电阻串结构简单、天然单调，但 10+ 位时面积过大（1023 个电阻+开关）。INL 与电阻匹配精度直接相关：$INL \propto V_{ref} / \sqrt{4N} \cdot \Delta R/R$。R-2R 是常用折中方案。

3. **电容型 DAC**：与 ADC 中的电荷重分布原理相同，电容失配 $\Delta C/C$ 来自尺寸和氧化层厚度偏差。底版寄生电容和开关电荷注入是额外误差源。

4. **电流舵型 DAC**（本书主角）：
   - 二进制：结构简单，但 MSB 开关 glitch 大
   - 温度计码（Unary）：单调性好，需译码器
   - 分段：高位温度计码 + 低位二进制，实际芯片最常用

## 三种架构对比

| | 电阻型 | 电容型 | 电流舵型 |
|------|--------|--------|---------|
| 参考量 | 电压 | 电荷 | 电流 |
| 分辨率上限 | ~10 bit（面积限制） | ~12 bit | 14+ bit |
| 速度 | 低（开关网络延迟） | 中 | 高 |
| 单调性 | 电阻串保证单调 | 受失配影响 | 温度计码部分保证 |
| 主要限制 | 电阻匹配 | 电容匹配 + 寄生 | 晶体管失配 + 输出阻抗 |

## 来源

- [[bosch-2004-dac-limitations]] — Bosch et al. (2004) Ch 3

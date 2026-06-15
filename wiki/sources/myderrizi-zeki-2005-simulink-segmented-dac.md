---
type: source
title: "Behavioral Model of Segmented Current-Steering DAC by Using SIMULINK"
authors: ["Indrit Myderrizi", "Ali Zeki"]
year: 2005
url: ""
venue: "Conference Paper"
tags: [DAC, behavioral-modeling, SIMULINK, segmented-architecture]
related: []
created: 2026-06-15
updated: 2026-06-15
---

# Behavioral Model of Segmented Current-Steering DAC by Using SIMULINK

## 核心要点

- 用 SIMULINK 搭建了完整的 12-bit 分段电流舵 DAC 行为级模型（8-bit 二进制 + 4-bit Thermometer 解码）
- 模型包含所有关键子模块：二进制-温度计译码器、摆幅缩减驱动器 SRD、开关+电流源核心单元
- 在最坏情况下（电流源失配 + 时序偏差 + 延迟差异）仿真 INL/DNL 和 SFDR（1GS/s, 100MHz 输出时 SFDR≈23dB）
- 强调行为级建模在晶体管级设计之前的价值——可以提前评估架构选择和 worst-case 性能

## 关键概念

- **分段架构**：12-bit DAC 分为 8-bit 二进制加权（LSB）+ 4-bit Thermometer（MSB），兼顾面积与性能
- **Swing Reduced Driver (SRD)**：将开关栅极驱动电压摆幅从 0–3.3V 压缩到 1.8–2.2V，减少时钟馈通，提升开关速度
- **Binary-to-Thermometer Decoder**：4-to-15 NOR-based 译码器，模拟真实电路实现
- **Core Cell**：开关+电流源的 SIMULINK 行为模型，根据 SRD 输出决定导通/关断
- **最坏情况仿真**：通过调整时钟信号和电流源值来模拟非同步操作、失配和延迟差异

## 性能验证结果

- 静态：通过 MATLAB 仿真 INL/DNL（给出 INL/DNL 归一化公式）
- 动态：100MHz 正弦输入、1GS/s 更新率下 SFDR = 23dB（worst-case）

## 待探究的问题

- SIMULINK 行为模型与晶体管级仿真的精度对比
- 该模型是否可以扩展到更高分辨率（14-bit+）的 DAC
- SRD 参数的自动优化方法

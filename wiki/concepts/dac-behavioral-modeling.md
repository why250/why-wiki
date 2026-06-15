---
type: concept
title: DAC Behavioral Modeling
tags: [DAC, behavioral-modeling, SIMULINK, simulation]
related: ["[[myderrizi-zeki-2005-simulink-segmented-dac]]", "[[dac-mismatch-effects]]", "[[dac-dynamic-performance]]", "[[current-steering-dac]]"]
created: 2026-06-15
updated: 2026-06-15
---

# DAC Behavioral Modeling

在晶体管级仿真之前，用行为级模型快速评估 DAC 架构选择和关键设计参数的方法。行为模型允许在短时间内仿真完整的 INL/DNL/SFDR 性能，而晶体管级仿真则不可行。

## Myderrizi & Zeki SIMULINK 方法（2005）

[[myderrizi-zeki-2005-simulink-segmented-dac]] 为 12 位分段电流舵 DAC 建立了完整的 SIMULINK 模型：

### 模型架构

1. **Binary-to-Thermometer Decoder**：将二进制输入转换为分段编码（6 MSB thermometer + 6 LSB binary）
2. **Swing Reduced Driver (SRD)**：降低开关驱动信号的电压摆幅以减少 feedthrough 和 charge injection
3. **Core Cell**：建模电流源单元，包括输出阻抗和开关行为
4. **电流源失配建模**：用正态分布随机变量注入失配

### 行为模型的价值

- 几分钟内完成整个 DAC 的 INL/DNL 仿真（晶体管级需要数小时到数天）
- 支持最坏情况（worst-case）仿真以快速评估架构的极限性能
- 允许设计空间探索：分段比例、电流源尺寸、SRD 参数等的 sweep

### 性能验证

该 12 位模型仿真结果：
- 无失配时 INL/DNL 基本为零（理想行为）
- 引入 0.1% 电流源失配后 SFDR 降至约 23 dB（worst-case 信号频率）

## 行为建模的典型框架

| 工具/方法 | 特点 | 代表工作 |
|-----------|------|----------|
| SIMULINK | 图形化、快速原型 | Myderrizi & Zeki (2005) |
| Verilog-A | 可直接与 Spectre/HSPICE 混合仿真 | 工业界常用 |
| MATLAB 数值模型 | 灵活但无图形化 | [[wikner-tan-1997-dac-imperfections]] |
| SystemC/SystemVerilog | 系统级验证 | 现代 AMS 流程 |

## 与其他概念的关系

- [[dac-mismatch-effects]]：行为模型中必须注入的失配统计
- [[dac-dynamic-performance]]：行为模型验证 SFDR 等动态指标
- [[current-steering-dac]]：行为模型的目标架构
- [[dac-switching-schemes]]：分段编码方案是行为模型的关键输入
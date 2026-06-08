---
type: concept
title: 电流舵 DAC
tags: [DAC, current-steering, architecture, CMOS, binary-weighted, thermometer-coded]
related: "[[bosch-2004-dac-limitations-ch-01-introduction]], [[dac-dynamic-performance]], [[binary-weighted-dac]], [[transistor-mismatch]]"
created: 2026-06-08
updated: 2026-06-08
---

# 电流舵 DAC (Current Steering DAC)

## 基本原理

将数字输入码控制的一组加权电流源并联到输出节点，电流之和即为模拟输出。核心元件：电流源晶体管 + 开关晶体管 + 负载电阻。

$$I_{out}(X) = I_{LSB}[b_1 + 2b_2 + \dots + 2^{N-1}b_N] = I_{LSB}X$$

## 三种实现方式

| 类型 | 原理 | 特点 |
|------|------|------|
| **二进制** (Binary) | 每位一个电流源，权重 $2^{i-1}$ | 结构简单，但 MSB 开关 glitch 大 |
| **单位** (Unary/Thermometer) | 所有电流源等权重，用温度计码控制 | 单调性好，但需要译码器 |
| **分段** (Segmented) | 高位用温度计码，低位用二进制 | 折中方案，实际芯片最常用 |

## 关键非理想因素

- **静态**：电流源晶体管失配 → INL/DNL 限制 → 见 [[bosch-2004-dac-limitations-ch-01-introduction|Ch 4]]
- **动态**：输出阻抗频率依赖性 → SFDR 限制 → 见 [[bosch-2004-dac-limitations-ch-01-introduction|Ch 5]]
- **噪声**：晶体管热噪声 → SNR 限制

## 来源

- [[bosch-2004-dac-limitations-ch-01-introduction]] — Van den Bosch, Steyaert, Sansen (2004)

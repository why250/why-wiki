---
type: concept
title: DAC 输出阻抗与信号依赖失真
tags: [DAC, output-impedance, SFDR, distortion, current-source]
related: "[[wikner-tan-1997-dac-imperfections]], [[dac-dynamic-performance]], [[binary-weighted-dac]]"
created: 2026-06-07
updated: 2026-06-07
---

# DAC 输出阻抗与信号依赖失真

## 物理机制

在二进制加权电流源 DAC 中，不同数量的电流源根据输入数字码连接到输出节点。每个电流源有有限的输出阻抗 → 总输出阻抗随输入码变化 → 产生信号依赖性失真。

## 数学模型

输出电流的负载关系：

$$I_{load} = \frac{R_{out}}{R_{out} + R_{load}} I_{out}$$

引入信号依赖的输出电导 $G_{out}(X) = 1/R_{out}(X)$：

$$I_{load}(X) = \frac{1}{1 + G_{out}(X)/G_{load}} I_{out}(X)$$

对于二进制加权 DAC：
$$G_{out}(X) = G_{LSB} \cdot X$$

最终 SFDR 表达式：

$$SFDR \approx \frac{(R_{LSB}/R_{load})^2}{2^{2(N-2)}} = 20\log(R_{LSB}/R_{load}) - 6(N-2) \text{ [dB]}$$

## 设计含义

- **低 $R_{LSB}/R_{load}$ 比**：输出阻抗效应强，SFDR 受限于阻抗变化
- **高 $R_{LSB}/R_{load}$ 比**：杂散被量化噪声掩盖
- **分辨率越高（N 越大）**：对输出阻抗的要求越苛刻（每增加 1 位，SFDR 降约 6dB）

## 来源

- [[wikner-tan-1997-dac-imperfections]]

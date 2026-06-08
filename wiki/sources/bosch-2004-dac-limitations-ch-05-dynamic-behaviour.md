---
type: source
title: "Static and Dynamic Performance Limitations for High Speed D/A Converters — Ch 5: Dynamic Behaviour of Current Steering D/A Converters"
book: "[[bosch-2004-dac-limitations]]"
chapter: 5
authors: [Anne Van den Bosch, Michiel Steyaert, Willy Sansen]
year: 2004
url: ""
venue: "Book Chapter, Springer"
tags: [DAC, dynamic-performance, SFDR, output-impedance, cascode, glitch, feedthrough]
related: "[[dac-dynamic-performance]], [[dac-output-impedance]], [[dac-dynamic-factors]], [[cascoded-current-cell]]"
created: 2026-06-08
updated: 2026-06-08
---

# Ch 5: Dynamic Behaviour of Current Steering D/A Converters

## 核心要点

1. **影响动态性能的四大因素**：

| # | 因素 | 机理 | 解决方案 |
|---|------|------|---------|
| 1 | 开关控制信号不同步 | 差分开关切换时间不匹配 → 输出 glitch | 同步锁存器置于开关前 |
| 2 | 数字馈通 ($C_{GD}$) | 开关管栅漏电容耦合数字信号到输出 | 减小开关输入电压摆幅 / 加 cascode |
| 3 | 电流源漏极电压变化 | 两开关同时关断 → $C_0$ 放电 → 恢复电流产生 glitch | 特殊开关驱动电路 |
| 4 | **输出阻抗频率依赖性** | $Z_{imp}$ 随频率变化 → 信号依赖失真 | **cascode 结构**（本章核心贡献） |

2. **输出阻抗的频率响应**：
   $$Z_{imp} = r_{0sw}(1 + g_{msw}r_{0cs}) \left(\frac{1 + j\omega C_0/g_{msw}}{1 + j\omega C_0 r_{0cs}}\right)$$

   - 极点：$f_p = 1/(2\pi C_0 r_{0cs})$，零点：$f_z = g_{msw}/(2\pi C_0)$
   - $C_0$ 由互连线寄生主导（远大于本征电容）→ 高分辨率 DAC 的面积大 → 互连线长 → $C_0$ 大 → 带宽受限

3. **SFDR-带宽限制公式**：
   $$Z_{imp,req} = \frac{S Z_L}{4}(Q - 2) \approx \frac{S Z_L Q}{4}$$

   其中 S = 电流源总数，$Z_L$ = 负载阻抗，Q = 信号与二次谐波之比

4. **优化实现**：三种 cascode 结构提升 $Z_{imp}$ 的高频表现：
   - Cascoded current source → 分析零极点
   - Cascoded switch → 分析零极点
   - 双 cascode → 最佳但电压裕度紧张

## 与 Wikner-Tan 的关系

Wikner-Tan ([[wikner-tan-1997-dac-imperfections]]) 是本书 Ch 5 输出阻抗分析的前驱工作之一（本书参考文献 [12]）。Wikner-Tan 分析了输出阻抗变化对 SFDR 的低频模型，Bosch 进一步扩展到频率依赖性。

## 来源

- [[bosch-2004-dac-limitations]] — Bosch et al. (2004) Ch 5

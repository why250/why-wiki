# Wiki Index

## Overview

- [[overview]] — High-level summary of the wiki's scope and current state
- [[purpose]] — 项目目标、研究问题与范围

## Entities

<!-- Named things: people, tools, organizations, datasets -->
- [[zhangtuoken]] — 张托肯，ADC 权重前台校准算法开源项目作者
- [[gutietieqiu]] — 固推铁球公众号，模拟/RF IC 深度技术内容
- [[jacob-wikner]] — Linköping University，DAC 动态性能建模研究者
- [[nianxiong-tan]] — Ericsson Components，高性能 CMOS DAC 设计者
- [[anne-van-den-bosch]] — KU Leuven，高速高精度 CMOS 电流舵 DAC
- [[michiel-steyaert]] — KU Leuven，模拟/混合信号 IC 设计
- [[willy-sansen]] — KU Leuven，模拟 IC 设计经典教材作者
- [[walt-kester]] — Analog Devices，数据转换器技术教程作者
- [[indrit-myderrizi]] — Dogus University，SIMULINK 分段 DAC 行为建模
- [[ali-zeki]] — Istanbul Technical University，模拟/混合信号 IC 设计
- [[konstantinos-doris]] — TU Eindhoven/NXP，DAC 时序误差理论框架
- [[arthur-van-roermund]] — TU Eindhoven 教授，模拟与混合信号 IC
- [[domine-leenaerts]] — Philips Research，模拟/混合信号 IC 设计
- [[ola-andersson]] — Linköping University，DAC glitch 行为模型
- [[mark-vesterbacka]] — Linköping University 教授，混合信号系统设计
- [[christian-schmidt]] — Fraunhofer HHI / TU Berlin，AMUX 行为级建模与高速 DAC 架构
- [[manfred-berroth]] — University of Stuttgart 教授，高速集成电路设计
- [[fraunhofer-hhi]] — Fraunhofer Heinrich-Hertz-Institute，光子网络与系统

## Concepts

<!-- Ideas, techniques, phenomena, frameworks -->
- [[time-interleaving-adc]] — 时间交织 ADC 架构、失配类型、分级交织
- [[ti-calibration]] — TI Offset/Gain/Skew/Bandwidth 校准算法
- [[high-speed-sar-adc]] — 单通道高速 SAR ADC 速度优化技术
- [[adc-auxiliary-circuits]] — Input Buffer、Clock Gen、Reference Buffer
- [[dac-dynamic-performance]] — DAC 动态性能指标：SFDR、IMD、SNR、SNDR
- [[dac-output-impedance]] — DAC 输出阻抗随信号变化引起的失真机理
- [[dac-mismatch-effects]] — DAC 电流源确定性失配与统计失配的 SFDR 影响
- [[dac-circuit-noise]] — 电流源热噪声对 DAC SNR 的限制
- [[binary-weighted-dac]] — 二进制加权电流源 DAC 架构基础
- [[current-steering-dac]] — 电流舵 DAC 架构、三种实现方式、非理想因素
- [[dac-static-performance]] — DAC 静态性能指标：INL、DNL、Offset/Gain Error
- [[transistor-mismatch]] — CMOS 晶体管失配模型（Pelgrom、Lakshmikumar 等）
- [[quantization-noise]] — 量化噪声的统计模型与 SNR = 6.02N + 1.76 dB
- [[sinc-distortion]] — DAC 采样保持导致的 sinc 频率响应与幅度衰减
- [[resistor-dac]] — 电阻型 DAC 三种实现（电阻串、二进制加权、R-2R）
- [[capacitor-dac]] — 电容型 DAC 电荷重分布原理与失配限制
- [[inl-yield]] — INL 良率建模：从 Lakshmikumar 到 Bosch 闭合公式
- [[dac-switching-schemes]] — 消除系统梯度的电流源开关方案
- [[dac-dynamic-factors]] — 影响动态性能的四大因素：同步/馈通/漏极/阻抗
- [[enob]] — 有效位数：将 SINAD 映射为等效 ADC 分辨率
- [[sinad]] — SINAD（信号-噪声-失真比）定义及其与 SNR/THD 的数学关系
- [[adc-dynamic-metrics]] — ADC 六大动态性能指标（SFDR/THD/SINAD/SNR/ENOB）与 FFT 测试方法
- [[cascoded-current-cell]] — Cascode 电流单元：零极点分析与高频阻抗优化
- [[dac-timing-errors]] — CS-DAC 时序误差的 Doris 框架：TNL, PDM, SDR 闭合公式
- [[dac-glitch-asymmetry]] — rise/fall 不对称导致的 glitch：Andersson & Vesterbacka 模型
- [[amux-dac]] — AMUX-DAC：用模拟复用器组合多路 DAC 以翻倍带宽的架构
- [[dac-behavioral-modeling]] — SIMULINK/MATLAB 行为级 DAC 与 AMUX 建模方法

## Sources

<!-- Papers, articles, talks, books, blog posts -->
- [[zhangtuoken-2026-adc-calibration]] — 用 AI 实现并开源 ADC 权重前台校准算法
- [[gutietieqiu-2024-8bit-high-speed-sar-adc]] — 第八届集创赛赛题点评：8位高速 SAR ADC
- [[wikner-tan-1997-dac-imperfections]] — 电路非理想因素对 DAC 动态性能的影响
- [[kester-2009-mt-003]] — MT-003：ADC 动态性能指标详解（SINAD/ENOB/SNR/THD/SFDR）
- [[bosch-2004-dac-limitations]] — Bosch DAC 专著全书总览（章节索引）
- [[bosch-2004-dac-limitations-ch-01-introduction]] — Bosch DAC 专著 Ch 1：全书导论与结构概览
- [[bosch-2004-dac-limitations-ch-02-specifications]] — Bosch DAC 专著 Ch 2：DAC 功能描述与静动态规格
- [[bosch-2004-dac-limitations-ch-03-architectures]] — Bosch DAC 专著 Ch 3：电阻/电容/电流舵 DAC 架构比较
- [[bosch-2004-dac-limitations-ch-04-static-behaviour]] — Bosch DAC 专著 Ch 4：静态行为——随机误差 INL 良率与系统梯度
- [[bosch-2004-dac-limitations-ch-05-dynamic-behaviour]] — Bosch DAC 专著 Ch 5：动态行为——四大因素与输出阻抗频率效应
- [[myderrizi-zeki-2005-simulink-segmented-dac]] — Myderrizi & Zeki：12位分段CS-DAC的SIMULINK行为模型
- [[doris-2003-mismatch-timing-errors]] — Doris, van Roermund, Leenaerts：CS-DAC失配时序误差统一框架
- [[andersson-vesterbacka-2005-glitch-asymmetry]] — Andersson & Vesterbacka：rise/fall不对称导致的glitch行为模型
- [[schmidt-2018-amux-behavioral-model]] — Schmidt et al.：高速 2:1 AMUX MATLAB 行为级模型（MWSCAS 2018）

## Queries

<!-- Open questions under active investigation -->

## Comparisons

<!-- Side-by-side analysis of related entities -->

## Synthesis

<!-- Cross-cutting summaries and conclusions -->

---
type: overview
title: Project Overview
tags: []
related: "[]"
created: 2026-06-06
updated: 2026-07-21
---

# Overview

本 wiki 是一个基于 LLM Wiki 模式构建的个人知识库，专注于模拟/混合信号集成电路设计、数据转换器技术、高速器件建模以及 AI 辅助工程方法。

## 当前状态

项目已摄入 14 篇源文章/章节，覆盖 26 个技术概念和 21 个实体。

### 数据转换器（ADC/DAC）

**源文章**：
- [[kester-2009-mt-003]] — ADC 动态性能指标详解
- [[bosch-2004-dac-limitations]] — Bosch DAC 专著全书总览
- [[wikner-tan-1997-dac-imperfections]] — 电路非理想因素对 DAC 动态性能的影响
- [[myderrizi-zeki-2005-simulink-segmented-dac]] — SIMULINK 分段 DAC 行为模型
- [[doris-2003-mismatch-timing-errors]] — CS-DAC 失配时序误差框架
- [[andersson-vesterbacka-2005-glitch-asymmetry]] — rise/fall glitch 不对称模型
- [[schmidt-2018-amux-behavioral-model]] — 2:1 AMUX 行为级模型

**ADC 源文章**：
- [[zhangtuoken-2026-adc-calibration]] — AI 辅助 ADC 校准算法
- [[gutietieqiu-2024-8bit-high-speed-sar-adc]] — 高速 SAR ADC 设计

### 器件建模（FET）

- [[dambrine-1988-fet-equivalent-circuit]] — FET 小信号等效电路 Dambrine 直接提取法

## 核心主题

- **DAC 架构与建模**：电流舵 DAC、二进制加权、行为级建模、失配/时序误差/glitch 模型
- **ADC 架构与校准**：SAR ADC、TI 交织、前台/后台校准
- **器件表征**：FET 小信号等效电路提取、S 参数去嵌、冷管寄生提取
- **AI 辅助工程**：vibe coding、LLM 辅助硬件设计、开源工具链

## 阅读指南

- 从 [[index]] 按类别浏览所有页面
- 从 [[log]] 按时间线查看项目进展
- 通过 [[purpose]] 了解项目的研究目标和范围

---
type: source
title: 用 AI 实现并开源 ADC 权重前台校准算法
authors: [张托肯]
year: 2026
url: "https://mp.weixin.qq.com/s/IFFsfBBhwCjeAmttofoRBg"
venue: "微信公众号"
tags: [ADC, calibration, open-source, AI, vibe-coding]
related: "[[zhangtuoken]], [[ti-calibration]], [[gutietieqiu-2024-8bit-high-speed-sar-adc]]"
created: 2026-06-07
updated: 2026-06-07
---

# 用 AI 实现并开源 ADC 权重前台校准算法

张托肯团队通过数月时间，借助 vibe coding 将多年积累的 ADC 校准和分析代码整理为开箱即用的开源工具，提供 Python（PyPI 包）和 MATLAB 双版本。

## 核心要点

1. **问题背景**：几乎所有 ADC 论文都提到"通过数字校正补偿电容失配"，但具体实现细节往往语焉不详，各课题组和公司的代码被视为独门秘籍。
2. **开源动机**：学术上并非新发现，主要目的是提供开箱即用的公开基线，降低初学者门槛，减少因代码不透明导致的审稿质疑。
3. **双版本策略**：Python 版本封装为 PyPI 包（pip install），MATLAB 版本直接提供源码，覆盖不同用户群体。
4. **AI 辅助开发**：借助 vibe coding 将内部可跑脚本整理为工程化工具，填补了"能跑的脚本"到"别人能用的工具"之间的工程鸿沟。

## 关键概念

- [[ti-calibration]] — 此文章关注单通道 ADC 内部电容失配的权重前台校准，区别于 TI 系统的通道间校准
- [[high-speed-sar-adc]] — ADC 单通道核心架构

## 待探究的问题

<!-- Open questions raised by this source -->

- ADC 前台校准 vs 后台校准的适用场景和优劣对比？
- Python vs MATLAB 在硬件校准工具生态中的定位差异？

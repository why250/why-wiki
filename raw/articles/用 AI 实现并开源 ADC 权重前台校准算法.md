---
title: "用 AI 实现并开源 ADC 权重前台校准算法"
source: "https://mp.weixin.qq.com/s/IFFsfBBhwCjeAmttofoRBg"
author:
  - "[[张托肯]]"
published:
created: 2026-06-07
description: "权重校准，易如反掌。"
tags:
  - "clippings"
---
张托肯 *2026年5月26日 13:57*

几乎每篇关于 ADC 的论文都会写：“通过数字校正补偿电容失配。”但具体怎么校准、代码长什么样，论文里通常语焉不详。这可能是各课题组、各公司心照不宣的独门秘籍。

我们组长期也积累了大量代码。每次看到小红书上有人求校准代码，我们都觉得这东西早该被开源。只是从内部能跑的脚本到别人能用的工具之间差着一大截，一直没人有精力去填这个坑。

正好赶上 vibe coding，我们花了数月时间，把积累多年的校准和分析代码整理成了开箱即用的工具，完整开源。

这在学术上不是什么新东西。主要目的，是让大家开箱即用，也给后续讨论提供一个公开的基线。

希望以后不再有人因为校准代码不透明而被审稿人质疑，也希望初学者不用再到处求一份能跑的参考实现。

01 先上干货：双版本开源

我们提供 Python 和 MATLAB 两个开源版本。

1）Python 版本封装为 PyPI 包，可以通过 pip install 安装。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/uNbm926YM3rfQ1iaITicOSUo0wYmaq9vzJPfWWV1zaCVe2QqbOvNWqzjE5urKmEaeic9BPBq29ibHPzOmhPmVqPZAYqX1A1sk2pTUW47TF781JE/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

其中提供两个校准函数：

calibrate\_weight\_sine 是完整增强版，适合芯片测试；

calibrate\_weight\_sine\_lite 是简化版，适合原理学习与快速验证。

它们可以与频谱分析函数 analyze\_spectrum 搭配使用。

假设 bits 是 ADC 的输出数字码（二进制矩阵），那么对它进行校准和分析的样例代码如下：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

是的，只需要把你的ADC二进制数据原封不动丢进去，校准就完成了！甚至不用多填一个参数。校准前后的频谱对比如下图所示。

![5 percent mismatch spectrum](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

5 percent mismatch spectrum

图：5% 单位电容失配，权重校准将 ENOB 从 12.50 恢复到 15.99

可以手工使用这些代码，但最推荐的方法是让 Agent 使用。例如：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

2）Matlab 版本封装为工具箱，可以在 Adds-On 中下载。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 在这个版本中，我们提供的校准函数是 wcalsin。它可以与频谱分析函数

plotspec 搭配使用。

使用方法与前面的 python 样例相似。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

以上两种校准方法，都能安装即用，傻瓜式操作。

下面以 Python 版本为例，展示两个实际应用。

第一个例子关注的是：当 SAR ADC 存在电容失配时，数字权重校准到底能恢复多少动态性能？

本次实验分别选取两种 16 比特 SAR 权重结构：严格二进制结构，以及非二进制冗余结构（radix 约为 1.8）。对两者的实际 CDAC 权重施加不同强度的单位电容失配，并在每个失配强度下做 32 次 Monte Carlo 仿真。

每次仿真中，ADC 转换都使用失配后的实际 CDAC 权重。

校准前，数字端仍用 nominal 权重重构输出。

校准后，数字端改用 calibrate\_weight\_sine 估计出的权重重构输出。

为了避免过拟合，权重训练和测试使用不同输入频点，二者 FFT 点数均为 8192。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图：虚线为校准前，实线为校准后；蓝色为无冗余，红色为有冗余

这个例子的核心结果是：随着电容失配增大，未校准的 ENOB 会明显下降；而经过权重校准后，两种结构的 ENOB 都能显著恢复。

这说明在 CDAC mismatch 主导误差的场景下，我们提供的数字权重校准方法可以有效补偿实际 CDAC 权重偏差，是恢复 SAR ADC 动态性能的关键手段。

样例代码见：

examples/05\_debug\_digital/exp\_d16\_sar\_unit\_cap\_mismatch\_mc.py

第二个例子关注的是：为了实现稳定、可信的权重校准效果，需要多少训练数据量？

实验继续使用 16 比特非二进制冗余 SAR ADC 权重结构，以及符合 Pelgrom 规律的单位电容失配模型，失配强度固定为 sigma\_Cu = 1%。每次随机生成一组失配后的实际 CDAC 权重，并使用不同起始相位的正弦波作为校准样本。

校准所用的样本点数从 2^4 扫描到 2^14，也就是从 16 点到 16384 点。完成权重校准后，再用另一条固定为 16384 点、起始相位不同的正弦波做转换和频谱分析。每个训练点数重复 32 次 Monte Carlo，最终画出 ENOB 的分布包络。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图：训练样本数越多，校准后的有效位数越趋近于理论值（16 比特）

结果表明，校准点数太少时，校准方程会欠定或病态。从 32 点开始虽然可以得到结果，但稳定性和可信度都很低，很容易过拟合。

随着校准点数增加，校准结果快速收敛：128 点后已经接近 15.9 ENOB，512 点以上基本稳定在接近 16 ENOB。

这个实验说明，在该 16 比特冗余 SAR ADC 场景下，约 256 到 1024 个训练样本已经足以稳定校准主要权重误差。

样例代码见：

examples/05\_debug\_digital/exp\_d18\_sar\_redundant\_mismatch\_training\_length\_sweep.py

上述两个例子，展示了权重校准的效果与威力。

我们用神奇的校准函数，让 ADC 用正确的权重起死回生。

问题的关键在于，如何找到正确的权重？

02 权重校准的方法与原理

ADC 权重校准可以拆解为训练和推理两个步骤，或者称为校准与应用。在校准阶段训练每一位的真实权重；正式工作时用校准后的权重重构输出。

权重校准有若干方法，例如有 split-ADC、offset-double-sampling（采样一次，注入上下两次dither）、低位校准高位等等。不同方法各有优劣，有前台校准，有后台校准，有些需要改变电路或者时序，有些需要外部输入正弦波。

如果系统允许正式工作前输入一次正弦波，那么用正弦波加最小二乘做一次前台权重校准通常就够了，因为电容相对失配随 PVT 基本不变，没必要为此引入复杂的后台校准。

这在 20 年前就是成熟技术了。参考文献：A. Glibbery, “Method of and apparatus for characterizing an analog to digital converter,” U.S. Patent 7 129 879 B1, Oct. 31, 2006.

输入正弦波时，ADC 输出码加权后也应该逼近正弦波。通过把 sin(ωn + φ) 拆成 cos(ωn) 和 sin(ωn) 两个正交基，原本带相位的非线性拟合问题就变成了线性最小二乘问题。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

为了求解，需要把线性关系整理成标准形式：Ax = b。

这里有三种构造方法：假设 MSB 的权重等于 1，或者假设 cos 项的系数等于 1，或者假设 sin 项的系数等于 1。

它们本质上都是先固定一个参考尺度，再把剩下的未知量放进 x 里。

通常方程数 N 远大于未知数个数。比如 16 比特 ADC，采样 1024 点时，矩阵 A 就是 1024 行、18 列。

所以这通常是典型的超定方程组，可以直接用最小二乘法求解。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

朴素算法很短，不到 30 行就能跑起来。我在仓库中保留了一个 lite 版本，大家感兴趣可以看看。

但真实 ADC 数据会遇到秩亏、病态矩阵、数值稳定性、频率估计误差、过拟合等问题，所以工程实现远比原型复杂。ADCToolbox 里为这些问题做了大量增强，包含双基假设、秩亏补丁、数值预缩放、两级频率搜索策略、多数据集多频率联合校准、谐波基扩展等等。

最终代码量接近 1000 行。

具体工程细节本文不展开，感兴趣的读者可以私信或者留言交流。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

03 远不止此：ADCToolbox

今天分享的校准工具，只是开源项目 ADCToolbox 的一小部分。

这个工具箱，其实比我的自媒体早得多。

它的原始算法内核，来自清华大学揭路教授的 Matlab 版本。

从 2021 年开始，它经历了多轮迭代，服务过数十颗芯片的仿真、测试和 debug。

在 2025 年，我通过 vibe coding 将其迁移为 Python 版本，进行了大量整理和验证，添加了测试框架、使用样例、PyPI 发版、CI/CD，以及 Agent skills。

这是我 [用 Claude Code 写的第一个项目](https://mp.weixin.qq.com/s?__biz=Mzg2MzA1Mjg1Mw==&mid=2247484897&idx=1&sn=efa7ecf7d955a3f7338f13204a05699f&scene=21#wechat_redirect) ，当时用的主力模型还是 claude sonnet 4.5。

巧的是，我最早做自媒体，很大一部分动机就是想推广 ADCToolbox。但真正开始写之后，其他文章先火了。

ADCToolbox 仍在持续更新，迄今更新已近 600 次。

里面还有很多内容没有展开介绍，欢迎大家试用、探索和反馈！

开源仓库地址：

https://github.com/Arcadia-1/ADCToolbox

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图：GitHub 仓库截图

希望 ADCToolbox 能为 ADC 的 AI 化分析与设计提供一点开源贡献，也给大家的 Agent，多准备几件趁手的工具。

04 预告：ADC 校准的更多玩法

权重的训练可以通过前台校准在片外实现。但对于实时工作的 ADC，推理更应该在片上实现。

也就是说，校准阶段可以用 Python 或 MATLAB 等程序在片外把权重算出来，再把这组权重写入 Efuse、SRAM 或寄存器等片上存储，正式工作时，在片上数字电路中用校准后的权重完成实时加权重构。

在这个基础上，就可以再往前走一步：让 AI 帮忙做这个实时数字权重重构后端的实现、验证、综合与 PNR。

经常被 JSSC 拒的人都知道，很多 reviewer 喜欢喷 calibration cost，但其实权重校准的乘累加过程并不是什么可怕的东西，无论是实现难度还是功耗面积代价都相对可控，更重要的是现在我们完全可以vibe一个！（彻底堵住 reviewer 的嘴）

10天前，我 vibe 实现了一个 12-bit sub-radix-2 SAR ADC 的数字权重重构后端，5 级 pipeline @ 1 GHz DCLK。它能把前台校准之后的权重，用于新数字输出的权重重建。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

方法与之前做的 [attention head 原型芯片](https://mp.weixin.qq.com/s?__biz=Mzg2MzA1Mjg1Mw==&mid=2247484808&idx=1&sn=c5ea31200dc094c9db6d818a789badf8&scene=21#wechat_redirect) 相同，一路基本是顺利的。

综合后 + 布线后两套后仿（含 SDF 反标）全部 PASS。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图：12-bit sub-radix-2 SAR ADC 的数字权重重构电路版图

这部分其实 10 天之前已经做出来了。但是最近各类事务繁忙，耽误了写文进度。具体内容近期将会进一步整理开源，敬请期待。

除此之外，这套校准方法看似是只校准权重失配，实际上还有非常多神奇的用法，可以用于分析更多问题，例如增益误差、非线性、回踢等等。

后续将慢慢介绍，请大家持续关注，点赞催更～

**微信扫一扫赞赏作者**

张托肯用AI · 目录

阅读原文

继续滑动看下一个

张托肯用AI

向上滑动看下一个
---
title: "第八届集创赛赛题点评之“8位高速 SAR ADC的设计"
source: "https://mp.weixin.qq.com/s/zNVgPspcgMC3C-CxfhNmhQ"
author:
  - "[[固推: Q总+Y总]]"
published:
created: 2026-06-07
description:
tags:
  - "clippings"
---
固推: Q总+Y总 *2024年3月31日 20:29*

我们的上一篇集创赛的赛题点评发引发了超出我们预期的关注和反响. 很多订阅者给我们发私信, 请我们也写一篇点评“8-bit 高速 SAR ADC 的设计”这道赛题的文章. 说老实话, 我们在很早之前就已经开始写这篇文章了, 但鉴于时间限制和有限的经验,所以这篇文章一再难产. 在近三个月的努力之后, 我们团队的正在读 **大四** 的 Y 总(初稿)和读 **研一** 的 Q 总(终稿)终于完成这篇点评. Y 总和 Q 总虽然都是研究高速 ADC 的, 但是他们尚属初窥门径, 所以本文里的错漏之处还是烦请各位读者不吝指正.

***1***

**赛题分析**

我们先来看赛题描述：设计一款可以用于高速数据采集的 8 位 SAR ADC，可以是纯 SAR ADC 架构，也可以是 SAR ADC 与其他类型的混合架构。其核心指标如下表所示：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/AtVXyzot7mw0tgOicGmF6D93ZJCliaY4LVGZ4SFat64UmxGxFYoHb6C1YXjlnyCFyXEjibbbFOJS1pHy27v4HIib8Q/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

Tab. 1. 赛题给出的设计指标.

我们首先看最核心的精度和速度指标. 显然这是个中低精度高速 ADC. 一般而言, 在 CMOS 工艺里, 速度超过 10GSPS 的 ADC 必须采用时间交织（TI: time interleaving）结构. 谈到 TI, 这个题目要考虑的因素就有很多, 比如如何实现多路交织、交织的数量、单通道的架构和速度，这些都需要仔细考虑。

我们首先考虑单通道 ADC 的架构，要做一个 8bit 几百 MSPS 的 ADC，40nm 下 SAR、pipeline、pipelined sar 都能轻松做到，首先是多 stage 的传统 pipeline 结构功耗很大，在能效上显然不占优势；单通道单比较器 1b/cycle 的 SAR 极限速度为 1GSPS 左右，而两级 pipelined sar 的速度虽然比较容易超过 1GSPS，但不仅功和面积耗较大，还要考虑非线性和增益误差的优化和校准。因此我们选择做一个高速单通道的 SAR ADC 基本是本题的最优选择。

单通道速度应该如何设计和选取呢？它其实和总速率和通道数都有关系，16GSPS 可以设计成：16 路交织+单通道 1GSPS，也可以设计成 32 路交织+单通道 500MSPS，校准思路相同的情况下，前者的功耗和面积较小，能效方面前者有显著优势，但单通道设计的难度也要大很多，因此我们的建议有两个：1，总速率相同情况下，加倍单通道速率和加倍通道数，建议选择加倍通道数量；2，在通道数相同的情况下，尽量去提升单通道速率以提升总速率。这里还有个问题，为什么大部分论文都用 2^N 路交织？这和时钟电路有关，通常我们只有一个外部时钟，需要经过分频产生内部的不同频率和不同相位的时钟，而很显然 2、4、8 分频较容易实现，且比较好做占空比校正和相位校正。确定架构后，即 32 路交织+单通道≥500MSPS，当然降低指标也可以做 16 路交织+单通道≥625MSPS~825MSPS，本设计的难点主要在于三方面：TI 结构的选取、辅助电路（input buffer、clock gen 和 reference buffer），单通道高速 SAR，TI 校准算法。

在进行深入剖析之前，有两点必须再补充一下，当我们这个赛题后。我们肯定要大量阅读文献，看看最新的研究进展。

首先就是高速 SAR ADC 的一个很重要的场景是高速串行接口:SerDes, 也叫 wireline transceiver,目前基于 DAC 和 ADC 的 DSP 方案已经成为其主流方案，因此很多 SerDes 的论文也会讲到 TI SAR 的结构和设计；clock gen 模块一般 ADC 的论文只会一带而过，而在 SerDes 的论文中会更加详细介绍；还有很多论文专门针对 clock gen 和 buffer 进行分析和设计，因此想设计好一款超高速 ADC,需要广泛涉猎。

然后我们再来简单分析已经发表的文献，下图统计了基于平面 CMOS 工艺的 TI ADC，可以看到电压域和 SAR 结构占据了主导地位，当然我们不难发现电压域的 ADC 的功耗相对很低有显著优势，但是其存在 PVT 不稳定的劣势，且和电压域 ADC 设计思路不同，因此不建议各位轻易选择。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Tab. 2. 基于平面 COMS 工艺的 TI ADC \[1\].

我们还注意到最新论文主流的工艺都小于赛题要求的 40nm，简单仿真 TSMC 的 28nm 和 40nm 的本征频率。对比发现并没有很大的差距，最大差距不到 30GHz，因此在部分电路的极限速度上两种工艺也不会有特别大的差距，在完成本赛题时可以广泛参考现有的先进平面工艺设计。接下来我们开始详细剖析赛题难点并提供建议。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 2. TSMC 40/28nm CMOS工艺的MOS管在Vds = 0.9V/1.0V时ft~Vgs的对比.

***2***

**TI 结构的选取**

首先我们来直观认识 TI 结构，通常一个 ADC 的工作都可以分为采样和量化两部分，在没有其他假设的情况下，ADC 必须在一个时间段 ts 内完成量化(图 1)。然而，当速度要求太高时，ts 将太短，ADC 无法完成量化过程。如果只从系统的角度考虑，时间交织是一个可行的解决方案。最简单的交织形式是两路交织。两个 ADC 以类似乒乓的方式工作。然后，为了满足 fs=1/ts 的采样率，每个 ADC 有 2ts 的时间来完成采样和量化。如果我们推广这一想法并以 N 的因子进行交织，那么每个子 ADC 的采样时间需求减少到 N\*ts。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 3. TI 的基本工作原理.

在通用的 TI ADC 系统中（图 2），每个 ADC 在 fs/N 的采样频率下工作，采样点平均间隔为 ts。阵列中的 ADC 以循环方式工作：ADC2 在 ADC1 之后采样，ADC3 在 ADC 之后 2 采样，以此类推，最后是 ADCN 进行采样。然而时间交织不是无代价的。由于 PVT 变化，每个子 ADC 可能具有不同的性能。这些子系统的不匹配会严重限制整个系统的性能，这些偏差和校准策略我们会在第四节中说明。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 4. 通用的 TI ADC 结构和波形图.

下面我们来讨论 TI 的架构，如果我们直接使用上图架构来实现本题，现在需要 32 路交织，如果直接按传统 SAR ADC 的做法，输入 10GHz 的信号，无论什么形式的采样开关，带宽都达不到；此外不同开关的 kickback 会对输入产生干扰以及相互之间也会产生串扰，因此我们必须要在采样开关前加一个高带宽高线性度的 buffer，如下图所示。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 5. 带 input buffer 的单级 TI 结构 \[2\].

我们再考虑不同开关的时序问题，如果不同开关的采样时间有重合，较大的交织路数会导致较大的信号分布树，有很多寄生电容和电组，使得输入负载电容较大，带宽仍然受限。如果不同开关的采样时间无重合，负载电容的问题会得到改善，但采样时钟 1/32 的占空比意味着只有 62.5ps 的采样时间，这对开关的速度提出了很高的要求；此外也难以产生 32 相 low-jitter 时钟：高速 ADC 中，时钟的 jitter 对系统的影响尤为明显，一个基本的公式是 SNDRjitter = −20 log(2πfinσj)，因此在交织数较大时（N＞8）时，通常考虑使用分级交织,如下图所示。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 6. 带 input buffer 和 SHA 的两级 TI 结构 \[2\].

基本的分级交织结构为 buffer1+SHA(T/H switch+buffer2)+sub-ADC，这时第一级的 SHA 来决定子 ADC 的输入带宽，并增加了许多设计自由度（SHA 的级数、T/H 时间和时钟的选择）,分级交织不仅可以减轻前面强调的输入互连限制，还可以缓解由于 skew 和 BW mismatch 产生的频谱杂散。更深入的研究提出了 Direct sampling 和 Inline Demux Sampling 的建模和比较，即考虑将第一级交织 N1×N2 分为两级，通过调整两级的级数 N1 和 N2、第一级开关同时闭合的数量 N1c、保持时间等自由度，研究最大输入带宽，详细的分析可以去看 Lukas Kull 的 JSSC。文中为了实现较大的输入带宽，使用了 4×4×4 结构实现了 64 路交织，-3dB 带宽超过 20GHz。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 7. Direct sampling 和 Inline Demux Sampling 的结构图 \[3\].

对于本题的 32 路交织和 10GHz 带宽的要求，则没有必要使用 3 级交织的 Inline Demux Sampling，2 级交织的 Direct sampling 足够。因为显然 3 级交织的时序和开关实现更复杂，而 2 级交织已经足够满足本设计的带宽要求。至于选取 4×8 还是 8×4 的交织结构，以及不同时钟的占空比和保持时间的选取，则需要仔细权衡。

***3***

**辅助电路设计**

我们将除了单通道 SAR ADC 核心电路的以外的电路称为辅助电路，可以分为三个部分，input buffer、clock generation、reference buffer。

***3.1***

****Input buffer****

Input buffer 如前文分析由 buffer1+SHA(T/H switch+buffer2), T/H switch 用 bootstrap switch/mos switch+cross couple switch 就能解决，设计重点则是 buffer 的带宽和线性度，对于一个电压 buffer，我们最常用的电路就是 Source Follower，但其带宽和线性度可能不符合要求。基于电感的常规带宽拓展技术有 Inductive peaking 和 T - coil peaking，基于反馈的常规带宽拓展技术有 Flipped Voltage Follower、Super Source Follower、class AB Super Source Follower，他们都是 Source Follower 的改进型。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 8. Source Follower 及各种改进电路.

对于 Source Follower，其主要非线性来自于 Vds 的变化导致 rds 变化，影响线性度，ADI fellow Ali 在 2020 年提出了一种使用 cascode 来 bootstrap vds，并结合 class ab 技术提升 gm 和 SR，有效提升能效和线性度，感兴趣的可以去看看他的两篇 JSSC。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 9. ADI 提出的一种 input buffer 的电路结构 \[4\], \[5\].

***3.2***

****Clock Generation****

Clock Gen 最简单的方法就是使用 divider，输入给一个高频时钟，几个 DFF 互相连接进行时钟分频，下图展示了二分频和四相时钟产生电路，其中 latch 通常使用 cml latch,输入无需满摆幅就能工作，比传统的 DFF 要快。但这种分频产生的时钟存在占空比和相位严重不匹配的问题，并且其工作在两倍的期望频率，功耗较大。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 10. 二分频电路和波形图.

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 11. 四相时钟产生电路和波形.

更有效的做法是使用时钟注入锁定环形振荡器，使得环形振荡器输出频率与输入频率相同，它不仅功耗和面积小，而且减小了 IQ 误差，缓解了校准的压力。下图展示了一个带占空比校正和相位校正的完整 8 相时钟发生器，该时钟发生器基于多相注入锁定环形振荡器(MPIL-ROSC)和正交延迟锁相环(QDLL)。QDLL 调节环形振荡器(ROSC)的自振荡频率(f0),并向其提供多相注入信号,最终实现了小于-1◦的八相精度和 58.8 fsrms@7GHz 的 jitter(100 kHz 到 1 GHz),仅消耗 15.6 mW。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 12. 时钟注入环形振荡器的完整电路 \[6\].

虽然多相注入锁定环形振荡器有显著的优势，但其设计难度比 divider 大了太多，本题更实际的做法还是使用第一级时钟使用 divider 产生主时钟，并辅助占空比校正和相位校正，第二级使用控制逻辑实现时钟。

***3.3***

****Reference buffer****

ref buffer 通常指的产生 CDAC 所接参考电压的 buffer, 对于高速 SAR,其转换依赖于开关电容 DAC 从参考中减去输入，因此需要快速的 DAC 切换以实现高速和高分辨率。当 ref 电压在片外提供时，由于焊线、PCB 走线的寄生电感和相邻焊线的互感的影响，DAC 建立会恶化减慢速度。通过电感从片外基准电压汲取的大充电电流会导致充电的 DAC 电容节点振铃。这又会导致 DAC 输出振铃。

因此我们需要在片内集成 ref buffer，下图给出了一个最简单的示例子，对其要求是输出阻抗低、电源抑制比高、瞬态响应快，但其足够低的输出阻抗以实现快速参考电压恢复会导致大量的功耗，很多论文中计算功耗时会忽略这部分；此外还需要引入大的去耦电容(几十到几百 pF)来抑制参考电压的开关纹波，这会导致很大的面积。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 13. 一个简单的 ref buffer 示例.

目前已经有很多电荷补偿和校准方案来改善高功耗和大的去耦合电容，但它们无疑都会增加时序逻辑的复杂度并影响速度，所以最理想的方案是在不影响速度的情况下降低 ref buffer 的功耗和速度。最常见的方案是使用冗余技术，它不仅通过降低高位的建立精度来降低 ref buffer 的功耗，还能提升容错范围提升转换的速度，因此在高速 ADC 中应该是一个基本的技术。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 14. 二进制重组冗余结构 \[7\].

***4***

**单通道高速 SAR**

***4.1***

****SAR ADC 整体分析****

SAR ADC 由于其无源化和数字化程度高，它比其他 ADC 架构从工艺进步中受益更多，成为先进工艺下的高速 ADC 的主流单通道结构，过去年 15 内关于高速 SAR 的研究已经很多，下面我们将对一些常用的技术进行简单介绍。

首先我们使用 ISSCC2023 中一篇论文的一页 slide 来说明 SAR ADC 的速度限制因素，图中展示了传统异步逻辑的详细时序图，在采样结束后，比较器进行比较，比较完成后再 switching path 上通过数字逻辑将比较结果传至 DAC 控制开关进行 DAC 的建立，在 reset path 上通过数字逻辑产生控制信号使得比较器复位，我们可以直观的发现，在高位时速度的主要限制因素是 DAC 建立时间，在低位时速度的主要限制因素是复位时间.

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 15. SAR ADC 的速度限制分析 \[8\].

实际上图中关于 reset path 的描述略有些不妥，因为比较器比较完成后再到控制其复位的过程肯定是有延迟的，不过比较器输出到 DAC 的时间通常大于比较结束后产生复位时钟时间的，我们需要优化的正是这一部分，为了方便描述，我们将数字逻辑的时间统一起来，构建下面的公式，我们很自然地想到，如果要提升速度，必须提升比较器的速度，降低控制逻辑时间，降低 DAC 的建立时间，此外还可以尝试降低转换次数 N。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

数字逻辑部分我们通常在先进工艺下都会使用标准单元库，有利于设计迭代和版图绘制，因此关于单一逻辑门（inv、or、and、dff）的优化不在本文的阐述部分，不过在 2022 年的 CICC 上澳门大学提出了在控制逻辑中使用不匹配的 N/PMOS 尺寸与功耗延迟优化技术，不仅提升了速度，还降低了功耗，最终在 28nm 下实现了 10bit 700MSPS 的单通道单比较器 1b/cycle 的 SAR ADC，在奈奎斯特频率附近实现 SNDR 为 56.4 dB，仅消耗 2.02 mW，FoMw=2.02 fJ/conv-step。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 16. 使用不匹配 N/PMOS 优化的控制逻辑 \[9\].

***4.2***

****4.2 Switching path 速度优化****

对于控制逻辑部分，最经典的结构就是 C. C. Liu 在 2010 年的 JSSC 中提出的基于 DFF 链的逻辑，比较器比较完成后产生 valid，经过控制逻辑产生 clkc 控制比较器复位和比较，同时产生 clk1~10 控制 DAC 逻辑传输比较结果进行控制 DAC 的建立。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 17. C. C. Liu 经典 JSSC 时序逻辑 \[10\].

上述逻辑十分清晰易懂，但比较器完成后输出到 DAC 开始建立的时间实在太长了，下面展示了一种优化思路，使用 pre-determined(SCk)技术和 transparent latch 降低了延时，更多的优化思路各位可以阅读论文去发掘。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 18. 基于 DFF 和基于 latch 的时序控制 \[11\].

对于 DAC 建立时间，我们结合 DAC 的开关算法一起讨论，为了降低 SAR 转换过程中的开关切换功耗，学者在传统切换算法的基础上提出电容分裂算法、单调开关算法、Vcm-based、Bi-directional 等开关算法，较传统算法降低了大量功耗，如下图所示。但实际上 DAC 的切换功耗在整体功耗中占比很小，这些开关算法更有吸引力的是降低了单位电容总数，这意味着每一位电容都减小了 1/2 或者 1/4，配合前文提到的二进制冗余补偿/重组技术，再配合顶板采样技术，大大降低了 DAC 建立时间。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 19. 不同 DAC 开关算法对比 \[12\].

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 20. strong arm 和 double tail conparator \[12\].

***4.3***

****Reset path 速度优化****

上述的所有优化我们都在尝试降低 switching path 的延时，对于 reset path 的延时，当转换 LSB 几位时，Tset 其成为主导因素（一般为几十 ps），这在电路层面很难进一步提升速度，因此在架构方面学者提出了多比较器技术：ping pong comparator 和 Loop unrolled SAR，分别使用了两个比较器和 N 个比较器，实现了单通道速度＞1GSPS。

ping pong comparator 使用两个比较器交替工作（比较和复位），比较器 1 的比较结束被检测到并用于触发比较器 1 的复位和比较器 2 的启动，似乎这个时候比较器 2 会对其输入敏感，但只需要保证 CDAC 已建立在冗余开关方案要求的建立限制内就可以。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 21. 基于 ping pong comparator 的 SAR ADC 结构和时序图 \[13\].

Loop unrolled SAR 使用了 N 个比较器，只看时序就发现它无需复位，因为比较完后，本次 SAR 转换就不工作了。实际上一次比较的延时就变成 Tcomp+Tdac,无逻辑延迟，无比较器复位，缺点是多个比较器失调存在 mismatch，需要单独校准。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 22. Loop unrolled SAR ADC 结构和时序图 \[14\].

上述工作都是单次转换 1bit，我们能否单次转换 2bit 甚至多 bit 来降低转换次数 N？实际上我们已经使用了多个比较器，如果再加上多个 CDAC，单次提供多个参考阈值，便能完成比较，一个简单的示意图如下：三个比较器可以将输入与三个模拟估计值进行比较，从而提供 2 位信息。但是如何在连续的周期中产生模拟估计值呢？如图 11 所示，每个估计值必须由一个 DAC 产生。在第一个转换周期中，我们设置 Vdac1 = 3Vref/4、Vdac2 = Vref/2 和 Vdac3 = Vref/4。例如，如果比较器确定 Vref3/4＜Vin＜Vref，则 DAC 输出的下一个值将分别设置为（15/16）Vref、（14/16）Vref 和（13/16）Vref。但是这个电路的复杂性、面积和输入电容显著增加，而且比较器和 DAC 都仍存在失调的 mismatch，都需要校准。it/cycle 的技术已经发展到了 2.6 bit/cycle、3 bit/cycle、4 bit/cycle 和 5 bit/cycle，澳门大学在 28nm 下用 5 bit/cycle 实现了单通道 9bit 1.4GSPS，并交织成 2.8GSPS，在奈奎斯特频率下实现了 51.8 dB 的 SNDR。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 23. 一个 2bit/cycle 控制逻辑的示例 \[15\].

最后在前文提到的 ISSCC 2023 silde 中的工作上提出了高四位使用 Loop unrolled，低四位使用 latch based 的混合架构来获得速度-功耗的协调优化。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 24. unrolled SAR+latch based 混合 SAR ADC \[8\].

***5***

**TI 校准算法**

***5.1***

****TI 失配分析****

上述我们花了大量的篇幅去讨论电路模块，但实际上对于一个超高速 ADC 来说，即使单通道性能做的再好,在时间交织大大提升速度之后，其最终性能会因为各种失配变得糟糕无比。

TI-ADC 的误差可以分为静态和动态类型。静态路径失配包括增益失配（gain）和失调（offset）失配，它们的影响在理想情况下与输入信号的频率无关。相比之下，动态失配误差—TI 的采样保持 (S/H) 网络之间采样时间（skew）和带宽失配（bandwidth）是和频率相关的；随着输入频率的增加，由动态失配产生的寄生谐波的功率相应增加，这可能会限制高频输入的频谱性能。它们通常也比静态误差更难处理，因为输入的衍生信息通常不可用。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 25. 含各种失配的 TI ADC 示例.

我们可以简单进行理论分析，大部分 TI 硕博论文都有推导过程，下面只说明结论：

> - 失调失配导致数字输出频谱在 N×fs/M±fin 处会有杂散，其幅度和 fin 无关；
> - 增益失配导致数字输出频谱在 N×fs/M+fin 处会有杂散，其幅度和 fin 无关；
> - 失配导致数字输出频谱在 N×fs/M+fin 处会有杂散，其幅度和 fin 无关；

对于带宽失配，ADC 的输入前端可以被建模为一个低通滤波器（或任何传递函数）。每个 ADC 的前端可能有一个不同的传递函数 H(jw)，其可以分解为幅度和相位响应，这可以被认为是增益和采样时间失配，但等效的增益和偏斜失配是与频率有关的。

***5.2***

****Offset&Gain 校准****

通道间的失调和增益失配误差具有静态误差特性，这使得它们比采样时刻的失配更容易校准。Offset 和 Gain 的校准通常采用一种广泛应用的成熟方法，该算法依赖于分析 TIADC 各通道子 ADC 输出的统计特性来估计和修正误差。通过统计输出的均值和方差，可以方便地得到 Offset 和 Gain。下图为一种校准方案，实际上大部分 Offset 和 Gain 的校准都差不多，这方面的算法创新较少，主要工作在于工程实现。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 26. 利用输出的统计特性校准 offset 和 gain \[16\].

***5.3***

****Skew 校准****

采样时间失配对 ADC 产生的杂散功率不仅与输入信号的幅度和频率有关，而且其出现的具体位置也与输入频率紧密相关。这一特性尤其在 ADC 处理高频输入信号时显得尤为严重，因而大大增加了采样时刻失配校准的难度。Skew 的校正主要分为两步：误差检测和校正。校正有两种方式，一种是在数字域中校正，这种校正方式需要得到信号的导数，对信号在采样点附近进行一阶线性近似，从而对输出数据进行补偿，会增加电路的复杂度，信号的带宽也会收到限制。现在比较多的是在通过 VDL 在模拟域中进行校正，该方案有几点问题需要注意：（1）存在反馈环路，可能会引起稳定性问题（2）可变延时线的存在会增加时钟抖动（3）需要较长的收敛时间。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig. 27. 利用参考通道提取信号导数并校正 \[17\].

skew 失配检测技术因其高难度和灵活性而备受关注。其中，基于信号自相关的算法是应用最为广泛的一种方法。这种方法利用了一个关键性质：平稳信号的自相关函数只与信号的时间差相关，使得可以通过自相关函数提取信号采样时刻的偏差信息。然而，它对信号自相关函数的形状和信号的统计特性提出了严格的要求；其次，为了保证输入信号的统计特性在校准周期内保持相对平稳，需要收集大量的采样点。因此，校准的精度在很大程度上依赖于采样点的数量。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig.28. 基于信号自相关的算法 \[18\].

另一类检测算法则是利用信号的导数来提取采样时刻偏差的信息，由于理想时刻的采样值与实际采样值之差为该处导数与采样时刻偏差之积，通过计算导数以及相关采样点的差值则可得到采样时刻偏差的信息。

在失配检测算法中，有些需要使用到额外的参考 ADC，这也会引起 sampling kickback，input ringing 以及 bandwidth mismatch 等问题。

在工业界中，ADI2017 年的论文\[19\]，使用的是基于自相关的检测算法，该方案不需要参考通道，但是需要的校准点数较多，收敛所需要的时间比较多。这种校准方案较为简单，个人认为可以尝试一下。还有许多文章提出了一些很有意思的算法，如果有时间可以尝试一下。参考文献\[21\]-\[29\]给出了一些 TI 校准算法的参考文献，主要是基于自相关的算法, 大家可以自行研究。

此外最近几年比较火的 ditter based 算法也值得去研究，清华大学\[20\]和澳门大学\[21\]分别在 2024 年的 ISSCC 上提出在 input buffer 中注入 ditter 来一次性校准 offset、gain、skew，下图对比了基于 ditter 和基于导数和自相关的优劣，可以看出其具有很大的优势。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Fig.29. ditter based 与其他校正算法对比 \[20\].

***6***

**总结**

***6.1***

****我们的建议****

本文从赛题指标出发，确定了 TI SAR 的架构、交织级数和单通道速度，并通过对 TI 结构、辅助电路、高速单通道 SAR ADC 和 TI 校准算法的讨论详细分析了设计难点。比赛已经报名截止，对一个三人队伍来说，在几个月的时间内完成这样一个大系统的原理设计就很有挑战性，因此必须分工明确，我们建议团队这样分工：三人合作确定系统架构，并分别研究和实现单通道 SAR、辅助电路设计、TI 校正算法。

如果目标仅是初赛获奖，仿照几篇文献复现电路完成模拟部分的 TI SAR 原理图设计，并将数据导出至 Matlab 进行校准，验证算法的有效性，做到这部分就足够了。

如果目标是一等奖甚至最高奖，则需要对单通道 SAR 的模块速度和功耗进行优化，实现高能效；在辅助电路部分改进现有的结构或者提出新的结构，input buffer 和 ref buffer 的优化应该是较容易的；选择或者提出一种速度快、精度高、电路开销小的 TI 校准算法，并完成数字部分再进行混合仿真；完成 TI SAR 的版图设计并进行后仿真。

***6.2***

****参考文献****

\[1\] 董磊,王晓飞,严伟,等.超高速模数转换器研究进展\[J\].微电子学,2022。

\[2\] G. Manganaro, "An Introduction to High Sample Rate Nyquist Analog-to-Digital Converters," in *IEEE Open Journal of the Solid-State Circuits Society,* vol. 2, pp. 82-102, 2022.

\[3\] Kull L, Implementation of Low-Power 6–8 b 30–90 GS/s Time-Interleaved ADCs With Optimized Input Bandwidth in 32 nm CMOS\[J\].IEEE Journal of Solid-State Circuits, 2016.

\[4\] A. M. A. Ali et al., "A 12-b 18-GS/s RF Sampling ADC With an Integrated Wideband Track-and-Hold Amplifier and Background Calibration," in IEEE Journal of Solid-State Circuits, vol. 55, no. 12, pp. 3210-3224, Dec. 2020.

\[5\] A. M. A. Ali et al., "A 14 Bit 1 GS/s RF Sampling Pipelined ADC With Background Calibration," in IEEE Journal of Solid-State Circuits, vol. 49, no. 12, pp. 2857-2867, Dec. 2014.

\[6\] Z. Wang, Y. Zhang, Y. Onizuka and P. R. Kinget, "Multi-Phase Clock Generation for Phase Interpolation With a Multi-Phase, Injection-Locked Ring Oscillator and a Quadrature DLL," in *IEEE Journal of Solid-State Circuits*, vol. 57, no. 6, pp. 1776-1787, June 2022.

\[7\] C. -C. Liu, C. -H. Kuo and Y. -Z. Lin, "A 10 bit 320 MS/s Low-Cost SAR ADC for IEEE 802.11ac Applications in 20 nm CMOS," in \*IEEE Journal of Solid-State Circuits\**,* vol. 50, no. 11, pp. 2645-2654, Nov. 2015.

\[8\] Yi-Hu Wang Soon-Jyh Chang, A 7b 4.5-GS/s 4× Interleaved SAR ADC with Fully On-Chip Background Timing-Skew Calibration, in ISSCC 2023 Slides.

\[9\] M. Guo, "A 10b 700MS/s single-channel 1b/cycle SAR ADC using a monotonic-specific feedback SAR logic with power-delay-optimized unbalanced N/P-MOS sizing," 2022 IEEE Custom Integrated Circuits Conference (CICC), Newport Beach, CA, USA, 2022.

\[10\] C. -C. Liu, S. -J. Chang, G. -Y. Huang and Y. -Z. Lin, "A 10-bit 50-MS/s SAR ADC With a Monotonic Capacitor Switching Procedure," in *IEEE Journal of Solid-State Circuits*, vol. 45, no. 4, pp. 731-740, April 2010.

\[11\] 李福乐，集成电路设计实践课程设计-SAR ADC，2019。

\[12\] X. Tang *et al*., "Low-Power SAR ADC Design: Overview and Survey of State-of-the-Art Techniques," in *IEEE Transactions on Circuits and Systems I: Regular Papers*, vol. 69, no. 6, pp. 2249-2262, June 2022.

\[13\] L. Kull et al., "A 3.1 mW 8b 1.2 GS/s Single-Channel Asynchronous SAR ADC With Alternate Comparators for Enhanced Speed in 32 nm Digital SOI CMOS," in IEEE Journal of Solid-State Circuits, vol. 48, no. 12, pp. 3049-3058, Dec. 2013.

\[14\] T. Jiang, W. Liu, F. Y. Zhong, C. Zhong, K. Hu, and P. Y. Chiang, “A single-channel, 1.25-GS/s, 6-bit, 6.08-mW asynchronous successive-approximation ADC with improved feedback delay in 40-nmCMOS,” IEEE J. Solid-State Circuits, vol. 47, no. 10, pp. 2444–2453,Oct. 2012.

\[15\] B. Razavi, "A Tale of Two ADCs: Pipelined Versus SAR," in IEEE Solid-State Circuits Magazine, vol. 7, no. 3, pp. 38-46, Summer 2015.

\[16\] Fang J, Thirunakkarasu S, Yu X, et al. A 5-GS/s 10-b 76-mW time-interleaved SAR ADC in 28 nm CMOS\[J\]. IEEE Transactions on Circuits and Systems I: Regular Papers, 2017.

\[17\] B. Razavi, "Design considerations for interleaved ADCs," *IEEE Journal of Solid-State Circuits,* vol. 48, no. 8, pp. 1806-1817, 2013.

\[18\] B. Razavi, "Problem of timing mismatch in interleaved ADCs," in Proceedings of the IEEE 2012 Custom Integrated Circuits Conference, 2012.

\[19\] S. Devarajan *et al*., "A 12-b 10-GS/s Interleaved Pipeline ADC in 28- nm CMOS Technology," in IEEE Journal of Solid-State Circuits, vol. 52, no. 12, pp. 3204-3218, Dec. 2017.

\[20\] Y. Tao, M. Gu, B. Chi, Y. Zhong, L. Jie and N. Sun, "22.4 A 4.8GS/s 7-ENoB Time-Interleaved SAR ADC with Dither-Based Background Timing-Skew Calibration and Bit-Distribution-Based Background Ping-Pong Comparator Offset Calibration," 2024 IEEE International Solid-State Circuits Conference (ISSCC),San Francisco, CA, USA, 2024.

\[21\] Y. Cao, M. Zhang, Y. Zhu, R. P. Martins and C. -H. Chan, "22.1 A 12GS/s 12b 4× Time-Interleaved Pipelined ADC with Comprehensive Calibration of TI Errors and Linearized Input Buffer," 2024 IEEE International Solid-State Circuits Conference (ISSCC), San Francisco, CA, USA, 2024.

\[22\] C.-Y. Lin, Y.-H. Wei, and T.-C. Lee, "A 10-bit 2.6-GS/s time-interleaved SAR ADC with a digital-mixing timing-skew calibration technique," IEEE Journal of Solid-State Circuits, vol. 53, no. 5, pp. 1508-1517, 2018.

\[23\] H. Wei, P. Zhang, B. D. Sahoo, and B. Razavi, "An 8 bit 4 gs/s 120 mW CMOS ADC," IEEE Journal of Solid-State Circuits, vol. 49, no. 8, pp. 1751-1761, 2014.

\[24\] S. Devarajan et al., "A 12-b 10-GS/s interleaved pipeline ADC in 28-nm CMOS technology," IEEE Journal of Solid-State Circuits, vol. 52, no. 12, pp. 3204-3218, 2017.

\[25\] X. Wang, F. Li, W. Jia, and Z. Wang, "A 14-bit 500-MS/s time-interleaved ADC with autocorrelation- based time skew calibration," IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 66, no. 3, pp. 322-326, 2018.

\[26\] M. Ni, X. Wang, F. Li, W. Rhee, and Z. Wang, "A 13-bit 2-GS/s time-interleaved ADC with improved correlation-based timing skew calibration strategy," IEEE Transactions on Circuits and Systems I: Regular Papers, vol. 69, no. 2, pp. 481-494, 2021.

\[27\] H.-W. Kang, H.-K. Hong, W. Kim, and S.-T. Ryu, "A time-interleaved 12-b 270-MS/s SAR ADC with virtual-timing-reference timing-skew calibration scheme," IEEE Journal of Solid-State Circuits, vol. 53, no. 9, pp. 2584-2594, 2018.

\[28\] Y. Zhou, B. Xu, and Y. Chiu, "A 12-b 1-GS/s 31.5-mW time-interleaved SAR ADC with analog HPF- assisted skew calibration and randomly sampling reference ADC," IEEE Journal of Solid-State Circuits, vol. 54, no. 8, pp. 2207-2218, 2019.

\[29\] D. Luu et al., "Background calibration using noisy reference ADC for a 12 b 600 MS/s 2× TI SAR ADC in 14nm CMOS FinFET," in ESSCIRC 2017-43rd IEEE European Solid State Circuits Conference, 2017: IEEE, pp. 183-186.

继续滑动看下一个

固推铁球

向上滑动看下一个
---
title: "什么是SPICE Model：从零开始手把手教你搭建一个仿真模型"
source: "https://mp.weixin.qq.com/s/j6PYhONV9-4jmXr_L6SMIg"
author:
  - "[[芯海拾遗]]"
published:
created: 2026-08-01
description: "区别于应用场景，本文从 Fab 视角，来看一个仿真模型是如何搭建的"
tags:
  - "clippings"
---
芯海拾遗 芯海拾遗 *2026年7月30日 08:30*

想象你手里有一本 400 页的 PDF，每一页都密密麻麻写着几十个参数名和一串浮点数：VTH0 = 0.423、U0 = 0.0382、VSAT = 9.53e4、DVT0 = 2.21、ETA0 = 0.08、PCLM = 1.35……这些数字加起来不超过 20KB，但它们的质量直接决定了一颗价值数百万美元的芯片是「一次流片成功」还是「回来全是废片」。

这就是 SPICE Model。

---

## 一、SPICE：从伯克利地下室的 Fortran 程序到全球标准

1973 年，加州大学伯克利分校的 Donald Pederson 教授带领团队写出了第一版SPICE。

> Simulation Program with Integrated Circuit Emphasis

当时它只是一个跑在大型机上的 Fortran 程序，核心功能是用牛顿-拉夫逊迭代法求解非线性电路方程组。

在这之前，模拟电路设计只能靠面包板搭原型、焊 PCB、上示波器调。但集成电路的晶体管数量每两年翻一番，到 1970 年代末已经没人能手工验证一个芯片的行为。SPICE 的出现，第一次让工程师可以「在流片之前看到芯片的波形」。

从 SPICE1到 SPICE2再到 SPICE3，Berkeley 打完地基之后，商用 EDA 公司基于 SPICE 内核进行了各自的增强和封装：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Oumia2QDGwr02aUxMCDIXqbgo2quUdColkibUDhibUU3GerKdibkPc38fic7VLjTCZM3KoicfZuYzicSaep7z2CgUFgfM18xWhDXCsbC7TJ4jPibcWs/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

这些工具本质上都是 **数值求解器** ，它们的输出精度不取决于自身，而取决于喂给它们的 **器件模型** 的精度。一个设计团队用再好的仿真器，如果挂了一个质量低劣的 SPICE Model，结果照样是 garbage in, garbage out。

---

## 二、一个 MOSFET 到底需要多少参数来描述？

任何一个学过半导体物理的人都能写出 MOSFET 的最基本电流方程——萨支唐模型：

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/Oumia2QDGwr0Y6HXRCT7owL684eIsRHIoub2icvagSJibVMW29GODpxsVvytFUEX8fiaZteKlia8DGrsYNzibI9N05phC0Sd1FkwMfJDjTQJYyvqE/640?wx_fmt=webp&from=appmsg&watermark=1#imgIndex=1)

这个公式只有 4 个工艺参数（μn、Cox、W/L、VTH），但它隐含了至少六个在真实器件中完全不成立的假设：

1. 迁移率 μn 是常数 —— 实际上载流子迁移率随垂直电场和横向电场剧烈变化
2. 沟道长度调制不存在 —— 实际上漏极电压会挤压耗尽区，等效沟道长度随 VDS 缩短
3. 阈值电压 VTH 是常数 —— 实际上 VTH 随沟道长度（SCE）、漏极电压（DIBL）、衬底偏压（Body Effect）变化
4. 亚阈值电流为零 —— 实际上 VGS < VTH 时仍有指数级微弱电流，这在低功耗设计中至关重要
5. 源漏寄生电阻为零 —— 实际上深亚微米器件的 Rs/Rd 可达数百欧姆，严重退化驱动电流
6. 没有栅电流 —— 实际上当 Tox < 2nm 时，直接隧穿电流大到不可忽略

这些非理想效应每一项都需要至少一个、多则七八个参数来描述。到 BSIM3v3（Level 49）时代，一套完整模型大约 180 个参数；到 BSIM4（Level 54），膨胀到了 300+ 个；到了 FinFET 所用的 BSIM-CMG，更是突破了 500 个。

**这就是 SPICE Model 的本质矛盾——物理精度和计算效率的 trade-off。** 用 TCAD（Technology CAD，基于有限元求解泊松方程和载流子连续性方程）可以模拟单个晶体管的全部物理行为，但仿真一个只有 1000 个晶体管的小电路就要花几个小时。紧凑模型（Compact Model）就是在精度和速度之间找到的那个「足够好」的平衡点。

---

## 三、BSIM 模型家族：一场持续四十年的「打补丁」竞赛

BSIM是 Berkeley 大学开发的 MOSFET 紧凑模型标准，它的演化史本身就是一部半导体工艺缩放史。

> Berkeley Short-channel IGFET Model

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Oumia2QDGwr1NwL432XTiccEwxdicTBTpY1IAoZxic06p4AiauRFIC41w4oP7YohjGIDAVpd2QGFtM9djTTudwoysjBkAFI9LmLoUdJQibGEJXpVQ/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=3)

BSIM3v3 之所以成为行业里程碑，不仅仅是因为它精确——而是因为它用一个 **统一的、连续的、可微的电流表达式** 覆盖了亚阈值、线性区、饱和区三个工作区。在此之前，不同工作区用不同公式拼接，边界处导数不连续，导致仿真器收敛失败。BSIM3v3 的「平滑函数」设计使得牛顿迭代始终有雅可比矩阵可求，收敛性大幅提高。

BSIM4 在这个基础上补齐了深亚微米的物理短板：当栅氧厚度缩到 2nm 以下，电子可以直接隧穿氧化层，产生不可忽略的栅电流——这完全不在 BSIM3v3 的建模范围内。此外，为了抑制短沟道效应而引入的 Halo/Pocket 注入会产生 **反向短沟道效应** （RSCE）：中等沟道长度的器件阈值电压反而比长沟道更高。BSIM4 用专门的参数组（DVT0、DVT1、DVT2 等）来捕捉这个反直觉的行为。

---

## 四、从硅片到模型文件：一套 SPICE Model 的完整诞生流程

一套工艺节点的 SPICE Model 从零到 release，标准流程通常持续 3~6 个月，涉及器件设计、工艺集成、测试、建模四个团队的配合。以下是完整流程：

### 4.1 测试结构设计（Testkey Layout）

RD 团队完成工艺开发后，需要专门设计一套 SPICE 建模用的测试结构（testkey）。这套 testkey 不是产品芯片，而是包含了各种尺寸变体的独立器件：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Oumia2QDGwr27SYWSotGw2z4eQ7iaB9T3QD9ct7XsU7KibuHZSDDxYCgNETY7DLG4TVl0w9O97c0vhnPLhcdAI3nHogic9Hb7vyYgS1nHjMA55E/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=4)
- MOSFET：W 从最小尺寸到 10μm，L 从最小尺寸到 20μm，覆盖 20~50 个不同 W/L 组合
- 多指（multi-finger）器件：评估 finger 数对寄生参数的影响
- 不同阱接触布局：评估衬底电阻网络效应
- 电容测试结构：用于提取 Cgg、Cov、Cj 等寄生电容
- 二极管、电阻、BJT 等辅助器件

尺寸 step 越细，模型精度越高——但流片面积和测量时间也线性增长。通常一个节点的 SPICE testkey 会有 200~500 个 DUT（Device Under Test）。

### 4.2 DC 测量（I-V 特性）

晶圆回来后，用精密半导体参数分析仪对每个 DUT 进行直流扫描：

- Id-Vg 曲线：固定 Vd = 0.05V（线性区）和 Vd = Vdd（饱和区），扫描 Vg 从 0 到 Vdd，获取阈值电压 VTH、亚阈值斜率 SS、跨导 Gm、关态电流 Ioff
- Id-Vd 曲线：固定 Vg 从 VTH 到 Vdd（4~6 个 step），扫描 Vd 从 0 到 Vdd，获取饱和电流 Idsat、输出电导 Gds、击穿电压 BV

每个 DUT 至少测 20 个重复单元取平均值，以消除随机测量噪声。整套 DC 测量可能产生数千条曲线。

### 4.3 CV 测量（电容-电压特性）

用 LCR 表在不同频率（通常 100kHz 和 1MHz）下扫描栅压，提取：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Oumia2QDGwr161uv6ic83vjjpxouLeyCibVaHcpf0KvOaSPiaSQ1HwMeG2zNZyIrdOQuicBg0tI42eR7tuhN9KkMGtw6DtneibK4e50rMAY1ic4G0Y/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=5)
- Cgg-Vg：总栅电容，用于确定 Tox 和 Poly Depletion 效应
- Cgc/Cgs/Cgd 分离：用于 RF 建模的寄生电容分配
- Cj-Vr：PN 结电容与反向偏压的关系

### 4.4 温度扫描

以上所有 DC 和 CV 测量，至少在 4 个温度点重复：

- \-40°C（低温极端条件）
- 25°C（室温 typical）
- 85°C（高温工作条件）
- 125°C（可靠性边界）

温度影响 VTH（约 -1mV/°C）、迁移率（约 T^(-1.5)）、漏电流（约每 10°C 翻一倍），是所有 PVT corner 分析的基础。

### 4.5 工艺角 Split（Corner Modeling）

这是整个流程中最容易被低估的部分。工艺制造本身存在 **全局变异** （lot-to-lot、wafer-to-wafer）——同一片晶圆上 NMOS 可能偏快（Idsat 偏高）、PMOS 可能偏慢（Idsat 偏低），反之亦然。因此必须覆盖四种工艺角：

![图片](https://mmbiz.qpic.cn/mmbiz_png/Oumia2QDGwr3cZpxT1SibDPArJIuSxEq4AWibqmW7wawgbzjSWS77vEXVo4iclcjs8WbiabOK3J20SK7IicJmef0OnBuhbYsQO4zOeko99hHXwZCo/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=6)

Corner详细资料参考 [什么是 Corner？为什么要做 Corner 验证？芯片设计中的工艺角深度解析](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483868&idx=1&sn=338dbb4822a8fd0aca36e329d2f1658b&scene=21#wechat_redirect)

### 4.6 参数提取（Parameter Extraction）

将数千条 I-V 和 C-V 原始数据导入模型提取软件（IC-CAP、BSIMPro+、Mystic 等），同时输入工艺基本信息（Tox、Xj、Nsub 等）。提取过程通常采用分步策略：

1. 长沟道器件先提取：长沟道器件的短沟道效应可以忽略，优先确定基本参数（VTH0、U0、VSAT 等）
2. 固定基本参数，逐级提取短沟道参数：DVT0/DVT1（短沟道 VTH 滚降）、ETA0/ETAB（DIBL）、PCLM/PDIBL（输出电导）
3. 电容参数单独提取：从 CV 数据中提取 COX、CJ、MJ、CGSO、CGDO 等
4. 全局优化微调：用 Levenberg-Marquardt 或遗传算法对所有参数做最后微调，确保在所有 W/L、所有温度、所有 corner 下误差最小

软件可以自动提取，但 **拟合权重** （loss function 中各 region 的比重）是建模工程师手动决定的。饱和区权重大，线性区就漂；亚阈值区权重大，强反型就漂。这本质上是一个多目标优化问题，并且不存在「所有区域同时最优」的解。

### 4.7 验证与签核（Verification & Sign-off）

提取完成后的模型必须通过以下验证才能 release：

- WAT 对标：模型预测的 Vt、Idsat、Ioff 必须与 WAT数据在 spec 范围内一致
- Ring Oscillator 验证：用模型仿真一个环形振荡器，其频率必须匹配硅实测值（误差 < 5%）
- 客户基准电路验证：用客户提供的典型电路跑仿真，波形必须与硅实测值吻合
	![图片](https://mmbiz.qpic.cn/mmbiz_png/Oumia2QDGwr2HfXdvHFzdicYNdocs5UjjPrK1ic3nsg1xrzd3riaQ91tdPSaUlOold17oyU1KGfG65QvSDDFUnM947peUibn6cP2bgq7Ld6LZs38/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=8)

---

## 五、WAT、统计建模和模型的边界

### 5.1 WAT 不是模型的「终极仲裁者」

WAT（Wafer Acceptance Test）是每片晶圆出货前必须通过的测试——在晶圆划片槽（scribe line）上的 testkey 器件上测量 Vt、Idsat、Ioff、BV 等 DC 参数，超出 spec 则报废。

但 WAT 有三个天生局限：

1. 位置偏差：划片槽在晶圆边缘，工艺条件（薄膜厚度、刻蚀速率、热预算）与芯片核心区域不完全一致
2. 只测 DC，不测 AC：WAT 不测 fT（特征频率）、NFmin（最小噪声系数）、Matching（器件匹配对）。一颗 LNA 的噪声系数偏离 spec 2dB 是完全可能的，即使 WAT 全部合格
3. 只测 nominal structure：WAT testkey 的尺寸和结构有限，客户的特殊器件（如高压 LDMOS、RF FET）可能没有被覆盖

### 5.2 统计模型：从「五个 corner」到「一万个 Monte Carlo 点」

传统的五 corner（TT/SS/FF/SF/FS）模型是 **全局 corner** ——假设整颗芯片上所有晶体管同向偏快或偏慢。这显然过于保守（导致 over-design）。真实情况是 **局部失配** （mismatch）：两个相邻的同尺寸晶体管，VTH 可能有几毫伏的随机差异。这种差异由随机掺杂涨落（RDF）、线边缘粗糙度（LER）、功函数变异（WFV）等引起。

现代 SPICE 流程用 **统计模型** （Statistical Model）来捕捉这一层：在 corner model 的基础上叠加 mismatch 模型（通常用 Pelgrom 模型，VTH 失配与 1/√(WL) 成正比），然后跑 Monte Carlo 仿真（通常 1000~10000 次随机抽样）来评估电路的良率。

蒙特卡洛参考文章 [什么是蒙特卡洛？蒙特卡洛与工艺角的区别是什么？有Corner的情况下为什么还要做MC](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483943&idx=1&sn=bcae4c046de5cad2faca42b85c4a615a&scene=21#wechat_redirect)

### 5.3 模型非永恒

同一个 FAB、同一个工艺节点，五年后重新提取的模型与五年前的版本一定存在差异。原因包括：

- 工艺的长期漂移（设备老化、原材料供应商更换）
- 测量设备升级（新一代 SMU 的精度和噪声 floor 不同）
- 拟合算法改进（更先进的全局优化策略）
- 客户反馈驱动的针对性调整

**SPICE Model 不是一个描述理想晶体管的物理公式，而是在特定工艺窗口内、特定优化策略下、与特定批次的实测数据最贴近的一个统计拟合结果。所以不要迷信仿真模型，仿真与silicon有差异是正常的，一切以实测为准。**

---

## 六、举个例子

下面是一份虚构的 5 V NMOS 教学模型

```
.model NMOS5V NMOS level=49  
+ version = 3.3  
+ tnom = 25  
+ tox = 1.15e-8  
+ xj = 2.5e-7  
+ nch = 1.3e17  
+ vth0 = 0.72  
+ k1 = 0.62  
+ k2 = -0.04  
+ u0 = 420  
+ ua = 2.5e-9  
+ ub = 6.0e-19  
+ vsat = 8.0e4  
+ dvt0 = 1.8  
+ dvt1 = 0.45  
+ dvt2 = -0.02  
+ pclm = 1.1  
+ pdiblc1 = 0.08  
+ pdiblc2 = 0.005  
+ rdsw = 180  
+ lint = 3.0e-8  
+ wint = 1.5e-8  
+ cgso = 3.0e-10  
+ cgdo = 3.0e-10  
+ cgbo = 1.2e-10  
+ cj = 7.0e-4  
+ cjsw = 3.5e-10  
+ pb = 0.88  
+ mj = 0.48  
+ ute = -1.5  
+ kt1 = -0.12
```

完整 BSIM 模型可能包含数百个参数，设计人员不必逐个背诵，先建立几组直觉更重要。

vth0、k1、k2主要关联阈值和体效应。源极跟随器中，Source 电位抬高而 Bulk 保持不变，阈值会上升，输出摆幅往往比固定阈值估算得更差。

u0、ua、ub、vsat影响驱动能力。把开关管宽度放大十倍，导通电阻不会永远严格缩小十倍，因为速度饱和、源漏电阻、接触和互连都在参与限制。

pclm 和 DIBL 相关参数影响饱和区斜率。放到电流镜里看，输出端 VDS 改变时，电流不会保持绝对不变，这直接影响模拟增益和偏置精度。

cgso、cgdo、cj、cjsw主要关联动态特性。单管 DC 全部正确，环形振荡器却明显偏快，问题很可能不在迁移率，而在重叠电容、结电容或版图寄生。

这也是读 Model Card 最实用的方法：不要孤立地背参数名，而要建立“参数—器件曲线—电路性能”的联系。

## 六、总结

SPICE Model 是半导体产业链中最不起眼、也最容易被低估的环节。它不过是一个 20KB 的文本文件，但它决定了电路设计师眼中的虚拟硅片长什么样。模型差 5%，芯片可能只是功耗超标；模型差 20%，芯片直接功能出错。

这个模型的背后，是测试工程师在探针台上测了三个月的数千条 I-V/C-V 曲线，是建模工程师在拟合软件里调了几十版的 loss function 权重，是 RD/PE/建模三方为了一个参数偏差是「模型有问题」还是「工艺Shift」拉扯了无数封邮件的判断。

理解 SPICE Model 的局限性，比背下它的参数列表更重要。因为当你意识到你的仿真结果不是「预测」而是一个「在特定假设下的估计」时，你才会真正理解为什么要用 design margin，为什么要 cover corner，以及——为什么一块芯片从仿真到流片，中间总隔着一万个「万一」。

---

## 缩略词对照表

---

![图片](https://mmbiz.qpic.cn/mmbiz_png/Oumia2QDGwr2ic9lzaFgsPZm2BmDAoZn9w532EPbtjD55fSaZcunBzX2Pp5liaibn1tkjRMwAia156jvneo8NO8nlW1pia24TGpxzQPia6VtU85vXc/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=9)

## 精彩回顾

[什么是工艺整合，从Process Flow 到WAT/CP，一篇文章讲透PIE全链路思维](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247484005&idx=1&sn=ca6a5fed7b26aa7ea9a6ce76e5827740&scene=21#wechat_redirect)

[OTP技术全解析：嵌入式存储的未来与全球竞争格局](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247484004&idx=1&sn=605fba6994423675c5b7cbb6db816aa6&scene=21#wechat_redirect)

[MOSCAP、MIM、MOM：片上电容到底怎么选？一篇文章带你看懂工作原理和差异](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483976&idx=1&sn=45314474a57f9d891e0d623588e22a59&scene=21#wechat_redirect)

[什么是蒙特卡洛？蒙特卡洛与工艺角的区别是什么？有Corner的情况下为什么还要做MC](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483943&idx=1&sn=bcae4c046de5cad2faca42b85c4a615a&scene=21#wechat_redirect)

[华为“韬定律”到底是什么：新瓶装旧酒，还是一场革命性创新](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483925&idx=1&sn=bf6c39d971a9e68d7a9ca5947f1fb061&scene=21#wechat_redirect)

[什么是 Corner？为什么要做 Corner 验证？芯片设计中的工艺角深度解析](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483868&idx=1&sn=338dbb4822a8fd0aca36e329d2f1658b&scene=21#wechat_redirect)

[从平房到摩天楼：一文看懂晶体管 50 年进化](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483778&idx=1&sn=59bb55bbee472f862a023ba9f8d8a84a&scene=21#wechat_redirect)

[N+1/N+2？国产先进制程代工产能背后的真实逻辑](https://mp.weixin.qq.com/s?__biz=MzY5NTM3MjM5Mg==&mid=2247483763&idx=1&sn=9863d95d6019ca8866097c763285c734&scene=21#wechat_redirect)

科普文章 · 目录

作者提示: 个人观点，仅供参考
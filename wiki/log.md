# Research Log

## [2026-07-21] ingest | Broad-Band Determination of the FET Small-Signal Equivalent Circuit (Berroth & Bosch, IEEE TMTT 1990)

- Created source page: [[berroth-1990-fet-broadband]]
- Created entity: [[roland-bosch]]
- Updated entities: [[manfred-berroth]] — added early career at Fraunhofer IAF and FET modeling paper
- Updated concepts: [[fet-small-signal-equivalent-circuit]] — added broadband analytic formulas and model self-validation; [[cold-fet-extraction]] — added HEMT modifications
- Cross-references: linked to Dambrine 1988, fixed forward reference in source page
- Source: raw/paper/Broad-band_determination_of_the_FET_small-signal_equivalent_circuit/

## [2026-07-21] ingest | A New Method for Determining the FET Small-Signal Equivalent Circuit (Dambrine et al., IEEE TMTT 1988)

- Created source page: [[dambrine-1988-fet-equivalent-circuit]]
- Created entities: [[gilles-dambrine]], [[alain-cappy]], [[centre-hyperfrequences-et-semiconducteurs]]
- Created concepts: [[fet-small-signal-equivalent-circuit]], [[cold-fet-extraction]], [[s-parameter-de-embedding]]
- New domain: FET 器件建模与等效电路提取（wiki 首个非 ADC/DAC 方向的论文）
- Cross-references: all new pages interlinked
- Source: raw/paper/A_new_method_for_determining_the_FET_small-signal_equivalent_circuit/

## [2026-06-16] ingest | Behavioral Model for a High-Speed 2:1 AMUX (Schmidt et al., MWSCAS 2018)

- Created source page: [[schmidt-2018-amux-behavioral-model]]
- Created concept: [[amux-dac]] — AMUX-DAC 架构与行为级建模
- Created entities: [[christian-schmidt]], [[manfred-berroth]], [[fraunhofer-hhi]]
- Updated concept: [[dac-behavioral-modeling]] — 添加 Schmidt 等 MATLAB AMUX 行为模型章节
- Cross-references added to 1 existing page

## [2026-06-15] ingest | 3 DAC papers: SIMULINK behavioral model, timing errors, glitch asymmetry

- **Paper 1 — Myderrizi & Zeki**: [[myderrizi-zeki-2005-simulink-segmented-dac]], SIMULINK 分段 DAC 行为模型
- **Paper 2 — Doris, van Roermund, Leenaerts**: [[doris-2003-mismatch-timing-errors]], 失配时序误差统一框架（TNL, PDM, SDR 公式）
- **Paper 3 — Andersson & Vesterbacka**: [[andersson-vesterbacka-2005-glitch-asymmetry]], rise/fall 不对称 glitch 行为模型
- Created entities: [[indrit-myderrizi]], [[ali-zeki]], [[konstantinos-doris]], [[arthur-van-roermund]], [[domine-leenaerts]], [[ola-andersson]], [[mark-vesterbacka]]
- Created concepts: [[dac-timing-errors]], [[dac-glitch-asymmetry]], [[dac-behavioral-modeling]]
- Updated concepts: [[dac-mismatch-effects]], [[dac-dynamic-performance]], [[current-steering-dac]] — cross-referenced new sources
- Index updated with 13 new pages (3 sources + 7 entities + 3 concepts)
- Sources: raw/paper/02_BehavModelSegCurSteerDAC/, raw/paper/03_Mismatch-based_timing_errors_in_current_steering_DACs/, raw/paper/04_Modeling_of_glitches_due_to_rise_fall_asymmetry_in_current-steering_digital-to-analog_converters/

## [2026-06-14] ingest | MT-003: Understand SINAD, ENOB, SNR, THD, THD+N, SFDR

- Created source page: [[kester-2009-mt-003]]
- Created entity: [[walt-kester]]
- Created concepts: [[sinad]], [[enob]], [[adc-dynamic-metrics]]
- Updated concepts: [[quantization-noise]] (added ENOB section), [[dac-dynamic-performance]] (added ADC cross-refs)
- Index updated with 5 new pages
- Source: raw/paper/00_MT-003.pdf → raw/paper/00_MT-003/00_MT-003.md

## [2026-06-08] ingest | Bosch DAC Book — Ch 5: Dynamic Behaviour of Current Steering D/A Converters

- Created source page: [[bosch-2004-dac-limitations-ch-05-dynamic-behaviour]]
- Created concepts: [[dac-dynamic-factors]], [[cascoded-current-cell]]
- Cross-linked to [[dac-output-impedance]] and [[wikner-tan-1997-dac-imperfections]]

## [2026-06-08] ingest | Bosch DAC Book — Ch 4: Static Behaviour of Current Steering D/A Converters

- Created source page: [[bosch-2004-dac-limitations-ch-04-static-behaviour]]
- Created concepts: [[inl-yield]], [[dac-switching-schemes]]

## [2026-06-08] ingest | Bosch DAC Book — Ch 3: CMOS D/A Converter Architectures

- Created source page: [[bosch-2004-dac-limitations-ch-03-architectures]]
- Cross-linked to [[current-steering-dac]]

## [2026-06-08] ingest | Bosch DAC Book — Ch 2: Functionality and Specifications

- Created source page: [[bosch-2004-dac-limitations-ch-02-specifications]]
- Created concepts: [[quantization-noise]], [[sinc-distortion]]
- Cross-linked to existing DAC concept pages

## [2026-06-08] ingest | Bosch DAC Book — Ch 1: Introduction

- Created source page: [[bosch-2004-dac-limitations-ch-01-introduction]]
- Created entities: [[anne-van-den-bosch]], [[michiel-steyaert]], [[willy-sansen]]
- Created concepts: [[current-steering-dac]], [[dac-static-performance]], [[transistor-mismatch]]

## [2026-06-07] ingest | Influence of Circuit Imperfections on the Dynamic Performance of DACs

- Preprocessed PDF → MD via marker: `raw/paper/Influence_of_Circuit_Imperfections_on_the_Performa.pdf`
- Created source page: [[wikner-tan-1997-dac-imperfections]]
- Created entities: [[jacob-wikner]], [[nianxiong-tan]]
- Created concepts: [[dac-dynamic-performance]], [[dac-output-impedance]], [[dac-mismatch-effects]], [[dac-circuit-noise]], [[binary-weighted-dac]]
- Updated [[ti-calibration]] with cross-link to [[dac-mismatch-effects]]

## [2026-06-07] ingest | 第八届集创赛赛题点评：8位高速 SAR ADC

- Created source page: [[gutietieqiu-2024-8bit-high-speed-sar-adc]]
- Created entity: [[gutietieqiu]]
- Created concepts: [[time-interleaving-adc]], [[ti-calibration]], [[high-speed-sar-adc]], [[adc-auxiliary-circuits]]
- Updated [[zhangtuoken-2026-adc-calibration]] with cross-links to new concept pages
- Updated [[zhangtuoken]] with related links

## [2026-06-07] create | Wiki structure initialized

- Created wiki subdirectories for all page types (entities, concepts, sources, queries, comparisons, synthesis)
- Created CLAUDE.md with ingest/query/lint workflows per LLM Wiki pattern
- Enhanced schema.md with workflow definitions
- Created source page for ADC calibration article

## [2026-06-06] create | Project created

- Wiki repository initialized
- Base schema and purpose templates created

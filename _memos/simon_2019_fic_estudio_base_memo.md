# Simon et al. 2019 - Estudio Base: Política Pública Regional de Acuicultura Sustentable (Biobío)

## Source

Simon, J.; Quiñones, R.; Soto, D.; Dresdner, J.; González, N.; Troncoso, L.; Ceballos, A.; León, J.; Montes, R.; Santis, O.; Sanhueza, A.; y Figueroa, Y. (2019). *Estudio Base: Política Pública Regional para el Desarrollo de la Acuicultura Sustentable. Sistematización de conocimiento tácito y explícito para la promoción de la acuicultura sustentable en la Región del Bío-Bío: Una aproximación mediante la aplicación de lógica difusa.* Programa Fondo de Innovación para la Competitividad Regional, Proyecto FIC-R 2017 (FIC 4000116), Centro Interdisciplinario para la Investigación Acuícola (INCAR), Universidad de Concepción, Chile. December 2019. 59 pages (1 ANTECEDENTES + DIAGNÓSTICO + PROPUESTA + REFERENCIAS + 3 ANEXOS).

Local source inspected: `market_act_es/FIC-estudiobase-políticapública-final.pdf` (59 pp.).

Metadata note: The report's own self-citation field (page 2) says "xxx páginas + Anexos" — the page-count was left as a placeholder in the published PDF. Actual page count from `pdfinfo`: 59. The companion methodology pre-report (`Estructura Metodología FIC_final.pdf`, 51 pp.) documents the fuzzy-logic methodology that this Estudio Base distills into its strategic matrix. The original Spanish is in UTF-8; `pdftotext` requires the `-enc UTF-8` flag to preserve accented characters.

## What This Paper Is

A government-funded baseline study underpinning a proposed regional public policy for sustainable aquaculture development in the Biobío and Ñuble regions of southern Chile. The report systematizes explicit (literature, regulations, sectoral data) and tacit (stakeholder) knowledge, applies an ecosystem-approach (EEA/EAA) framework, diagnoses ecological / socioeconomic / governance gaps, evaluates three strategic options, and concludes with a logical-framework matrix and a public–private governance proposal. Produced by INCAR / Universidad de Concepción under FIC-R 2017 project FIC 4000116.

## Research Question

How can the Biobío region develop sustainable aquaculture as a complementary then principal economic activity, in a way that aligns with FAO's ecosystem approach (EEA) and the region's existing planning instruments?

Subquestions implicit in the document:

- What is the current state of aquaculture in Biobío/Ñuble (production, sites, actors)?
- Which international, national, and regional norms condition the policy space?
- What are the binding ecological, socioeconomic, and governance gaps?
- Among small-scale, offshore, and recirculating land-based (RAS) aquaculture, which strategic options fit the regional conditions?
- What problem statement, vision, logical-framework matrix, and governance scheme should the regional policy adopt?

## Motivation

The Biobío region has incipient aquaculture activity, multiple competing uses of the coastal zone, and a fragmented regulatory landscape. The regional government (through the FIC-R program) commissioned a baseline study to inform the design of a regional aquaculture policy that aligns with FAO sustainability standards and the regional development strategy. The report responds to a perceived gap: existing analyses focus on Los Lagos / Patagonia salmon production and on the national policy framework, with no comparable diagnosis for Biobío / Ñuble.

## Setting / Data / Context

**Geography.** Biobío and Ñuble regions, southern Chile. As of the 2017 census, the combined population is 2,037,414 (51.73% women); 84.6% urban; 34.4% live in coastal zones. The region has 24,026 artisanal fishers (66% men). Biobío's GDP in 2016 was CLP 10,155 billion (7.06% of national GDP). Manufacturing leads at 21.3% of regional output; fisheries contribute only 0.97%.

**Aquaculture inventory (2019).** 51 active aquaculture units in Biobío. 29 are pisciculturas (freshwater hatchery / smolt facilities) dedicated to salmonids. 11 are coastal sites used for algae and molluscs, and 12 are research / experimentation centres. Ownership concentrated in 39 holders (mix of small, medium, large firms; artisanal fisher organisations; municipalities; universities).

**Production scale.** Up to 2010 the dominant activity was algae cultivation (mainly Gracilaria chilensis / pelillo), averaging ~6,000 t/year. After the 2010 earthquake, algae harvests collapsed (~22 t in 2013, ~19 t in 2017). Pisciculture in the regional interior dispatched 1,905 t in 2017, of which 98.5% was salmonid first-stage product: reproductors 7.5%, ovas 0.1%, alevines 57%, smolts 34%. The remaining 1.5% was rainbow trout (Oncorhynchus mykiss) at portion / "pan size" — down from over 1,000 t in 2008. Biobío contributes about 4% of national salmonid juvenile / smolt supply.

**Coastal-zone tenure (June 2018).** ~138 AMERB (Areas of Management and Exploitation of Benthic Resources) covering 44,287 ha, of which 75 are operative (55 fisher organisations, >3,600 fisher members). 8 ECMPO (Coastal Marine Spaces of Native Peoples) requests totaling >238,000 ha, mostly in Arauco province and Bahía de Concepción. 88 marine concession requests totaling ~1,600 ha (72 salmonid projects on 1,239 ha; 13 molluscs on 338 ha; 3 algae on 18 ha). 282 indigenous communities (14,966 members) and 64 indigenous associations (2,500 members) in Biobío (CONADI 2018).

**SEIA (Environmental Impact Assessment) pipeline, 1997–2017.** 30 aquaculture projects via DIA pathway, total investment USD 82.19M. 10 approved (USD 36.61M), 12 in evaluation (USD 29.60M). Concentrated in Inversiones Pelicano S.A. (11 projects, USD 16.74M), Pacific Seafoods S.A. (3 projects, USD 10.77M), Foodcorp Chile S.A. (1 project, USD 16.74M).

**National context.** Chile is the principal aquaculture producer in the Americas and a top-10 global producer; >1M t/year. Salmonid farming accounts for ~70% of national harvest, mytilids ~29%, both concentrated in Los Lagos / Patagonia. Salmon export value rose from ~USD 500M to >USD 5,157M between roughly 2000 and 2018, while volume grew from ~100,000 t to >700,000 t.

## Methods / Model

The Estudio Base is the substantive output of a multi-method approach detailed in the companion Metodología pre-report. Three methodological stages:

1. **Knowledge collection and systematization (tacit + explicit).** Literature review; review of national and regional regulations; review of FIPA, FAO, OECD, Banco Mundial, INE, SERNAPESCA, SUBPESCA, SEA databases; press review (2013–2018); stakeholder map (Mapa de Involucrados); semi-structured interviews + closed-form survey on 59 variables (24 ecological, 24 socioeconomic, 11 governance).
2. **Mamdani-type fuzzy logic model.** Variables fuzzified into membership functions; expert and stakeholder judgements encoded as if-then rules; defuzzification via centre-of-gravity aggregation in MATLAB; sustainability indices for each EEA dimension. Sensitivity analysis reduces the 59 input variables to 22 critical variables.
3. **Strategic prioritization and project profiles.** Identification of sensitive (high-leverage) variables → 4 strategic axes → portfolio of project profiles and policy instruments.

The Estudio Base reports the substantive findings of Stage 1 (diagnosis), the conclusions of Stage 3 (strategic axes, logical-framework matrix), and the governance proposal. The technical machinery of Stage 2 (fuzzy logic) is documented in the separate Metodología report.

## Key Variables or Constructs

**Ecosystem-approach (EEA / EAA) dimensions (FAO 2010, 2011):**

1. *Ecological wellbeing* — biodiversity, water quality, sediment quality, dispersion of nutrients and chemicals, escapes.
2. *Socioeconomic sustainability for surrounding communities* — employment, income, gender equity, productive linkages, education, access to credit, access to technology.
3. *Collaborative governance for social coexistence and territorial resilience* — institutional framework, regulatory compliance, public–private coordination, decentralization, participation.

**Production options evaluated:**

- *Acuicultura de Pequeña Escala (APE)* — small-scale aquaculture, mostly molluscs and algae, sited in AMERB and existing concessions.
- *Acuicultura Offshore* — large-scale finfish farming far from the coast; no current Chilean regulation defines suitable offshore areas.
- *Piscicultura Cerrada con Recirculación de Agua (RAS)* — land-based closed recirculation systems; controlled environmental parameters; high CAPEX/OPEX.

**Classification of the national legal framework (after FAO 2017):** strategic development; territorial ordering; site selection; site management; other criteria.

**Logical-framework matrix:** 4 sub-problems → 4 strategic axes → critical variables with baseline and target values for years 1–4.

## Setting-specific findings

### Ecological gaps for coastal aquaculture in Biobío / Ñuble

- **Industrial and domestic contamination.** Coastal Biobío / Ñuble shows above-national-average concentrations of organic matter and total Kjeldahl nitrogen (NTK). High fishing-industry activity plus weak wastewater treatment. Few coastal bays are suitable; most either have heavy industrial use (Bahía San Vicente, Bahía Concepción) or upstream pressure on the Itata watershed.
- **Trace metals.** Cadmium, chromium, copper, mercury, lead, zinc detected (1999–2014) in water column and sediments in Itata, Talcahuano, San Vicente, Coronel, Lota, Arauco, Tubul–Raqui. Concentrations declined 2011–2014 to levels mostly below detection limits.
- **Coastal upwelling and anoxic events.** Optimal salmon growth requires 13–17 °C. Punta Lavapié (south Golfo de Arauco) is the most active upwelling centre in Biobío / Ñuble, generating cool, nutrient-rich but low-oxygen waters during 1–7-day events mostly in spring/summer. Hypoxia / anoxia events recurrent and well-documented.
- **Biodiversity.** Three marine ecoregions (two coastal), 13 marine ecosystems (10 coastal), 5 macro-ecosystems. State of marine ecosystems and resources is largely unknown. Cuarto Informe Nacional de Biodiversidad (2009) flags fishing pressure as the principal driver of marine biodiversity loss.

### Socioeconomic gaps

- **Poverty.** Biobío is the third-most-income-poor region (17.6% in 2015). Multidimensional poverty 19.2%; the largest contributing dimension is "work and social security."
- **Education.** 33% of working-age population has only basic education vs. OECD average ~23%. Only one university in the region (Universidad de Concepción) still offers an aquaculture specialty. Four technical high schools (Penco, Tirúa, Llico, Lebu) have aquaculture tracks.
- **Credit access.** Small producers commonly need initial public financing because private credit is restricted.
- **Technology adoption.** Conditioned on technology characteristics, economic factors, farm characteristics, sociodemographic and institutional factors.

### Governance gaps

- Chile ranks in the top 20% globally on the Banco Mundial governance indicators (2016).
- OECD/CEPAL (2016) flag the water and biodiversity governance systems as fragmented and complex.
- FAO (2016) reviewed the General Law of Fisheries and Aquaculture (LGPA) for responsible fisheries governance; aquaculture governance was not covered. No published academic governance study of aquaculture in Biobío. Chávez et al. (2019) covers only Los Lagos salmon.
- The CRUBC (Comisión Regional de Uso del Borde Costero, established 1997) coordinates coastal-zone planning; aquaculture is barely mentioned in the regional ordering instrument (PROT).
- 54 municipalities across the two regions have limited capacity to respond to aquaculture-related emergencies.

## Results

### Strategic Options

**Small-scale aquaculture (APE).** Feasible mostly within AMERBs (up to 40% of surface area) and existing concessions. Estuarine zones (Río Biobío, Río Itata mouths) are productive but contamination-sensitive. Upwelling zones suitable for molluscs but also subject to anoxic events. FIP project 2013-24 identified 15 candidate APE zones in Biobío totalling 7,093.55 ha (Pingueral Norte; Dichato; Dichato–Coliumo Sur; Coliumo–El Morro; Cocholgue Norte; Cocholgue–Los Bagres; Tomé–Quichiuto–La Cata; La Tosca–Playa Negra; Candelaria–Cantera; Lenga; El Burro; Colcura–Laraquete; Tubul sectors B and C; Llico; Isla Santa María).

**Offshore aquaculture.** Reviewed literature: environmental benefits (waste dispersion, reduced coastal interaction, lower disease risk) vs. uncertainty about fish-migration corridors and benthic-habitat response. High CAPEX/OPEX; potentially higher returns than nearshore systems. No Chilean regulation defines AAA (Áreas Aptas para la Acuicultura) for offshore — development depends on national-level decisions.

**Recirculating land-based pisciculture (RAS).** Closed-loop systems with mechanical waste removal, biofilter nitrification, oxygen injection. Currently used in Chile for salmon's first life stage. Increasing interest for grow-out. High CAPEX/OPEX is the binding constraint.

### Problem statement adopted by the policy

> "Productores interesados en desarrollar acuicultura sustentable, y en especial acuicultura de pequeña escala, enfrentan múltiples barreras y costos que limitan la instalación de centros sustentables en la Región a pesar que es una opción interesante para impulsar procesos equitativos de desarrollo territorial en la Región."

**General objective:** Articulate public and private actors to ensure sustainability in territories where aquaculture takes place.

### Logical-framework matrix

Four strategic axes, each with 3–4 critical variables, baseline values, and target values for years 1–4.

| # | Sub-problem | Strategic axis |
|---|---|---|
| 1 | Negative perception and low legitimacy of public sector management of aquaculture | Improve governance adequate to orient and foster sustainable aquaculture in Biobío/Ñuble |
| 2 | Weak connection between knowledge actors and the public/productive sectors, reducing their contribution to territorial development | Strengthen technology and knowledge transfer between public and private actors, especially for local communities |
| 3 | Lack of productive options in territories characterized by social vulnerability | Foster sustainable small-scale aquaculture (APE) through spatial planning and knowledge integration, especially in socially vulnerable areas |
| 4 | Conflicts over coastal-zone use that may be amplified by climate change | Foster harmonization of aquaculture with other economic, social, and commercial activities using an ecosystem and precautionary approach |

Recurring critical variables (with example baseline → year-4 targets):

- *State capacity* (Axis 1, 4): 50 → 60 → 70 → 80 → 90
- *Formal compliance with the legal framework* (Axis 1): 60 → 65 → 70 → 75 → 80
- *Decentralization / transparency* (Axes 1, 2, 3): 30 → 40 → 50 → 70 → 70
- *Citizen perception of aquaculture and public sector management* (Axes 1, 3, 4): 30 → 40 → 50 → 70 → 70
- *Local economic impact of aquaculture* (Axes 2, 4): 20 → 40 → 60 → 60 → 60
- *Biodiversity* (Axis 2): 60 → 60 → 60 → 60 → 60 (i.e., minimize negative externalities; no growth required)
- *Employment impact* (Axis 3): 20 → 40 → 60 → 60 → 60

### Governance proposal

Create a Comisión Regional de Acuicultura — a public–private commission analogous to the existing national one. Public-sector seats: Gobierno Regional, SERNAPESCA, Ministerio de Economía, Ministerio del Medio Ambiente, SEA, Dirección General del Territorio Marítimo, Marina Mercante, plus key communes. Private-sector seats: small-scale producers, pisciculture, large-scale salmon, ECMPO holders, workers, technical high schools. Supplemented by a technical advisory council of aquaculture experts.

## Contributions

- First systematic diagnosis of the aquaculture sector in Biobío and Ñuble after the regional split (Ñuble created 2018) covering ecological, socioeconomic, and governance dimensions.
- Application of the FAO Ecosystem Approach to Aquaculture (EEA) framework to a Chilean region.
- A fuzzy-logic-derived logical-framework matrix that operationalizes the policy with baseline values, year-by-year targets, and explicit critical variables — methodologically detailed in the companion Metodología pre-report.
- A concrete public–private governance scheme (Regional Aquaculture Commission) anchored in the regulatory architecture of the LGPA and FIP commission model.

## Limitations and Assumptions

Explicit limitations:

- Marine ecosystem state is "largely unknown"; biodiversity baselines are weak.
- Multidimensional poverty data and education data come from national instruments with limited resolution.
- The Biobío fishery contributes only 0.97% of regional GDP — aquaculture's relative scale is modest and conclusions cannot be extrapolated from the Los Lagos salmon experience.
- Governance literature for aquaculture in Biobío is absent; reliance on stakeholder interviews + FAO and OECD reviews.
- AAA (Áreas Aptas para la Acuicultura) overlap with AMERB and ECMPO, and the regional ordering instrument (PROT) does not explicitly recognize aquaculture in freshwater or in most coastal areas.
- Offshore aquaculture is currently not enabled by regulation, so the strategic option depends on national-level legal changes outside the scope of the regional policy.

Embedded assumptions:

- The FAO Ecosystem Approach is the correct organising framework for sustainability.
- Tacit knowledge from stakeholder interviews is a valid input on the same footing as scientific literature for policy-relevant variables.
- Fuzzy logic (Mamdani-type) appropriately handles the imprecision and incompleteness of available information.
- Target values for critical variables (e.g., "year-4 target = 90") are set by expert judgement, not derived from a model.

## What the Paper Does Not Do

- Does not estimate a counterfactual: no quantitative model of "with policy vs. without policy" outcomes.
- Does not establish a causal claim about whether ownership consolidation, regulation, or coordination yields better environmental outcomes — it proposes a governance framework, not a causal evaluation.
- Does not implement the policy; it proposes a logical-framework matrix and a governance commission.
- Does not quantify the cost of implementing the four strategic axes or the proposed Comisión Regional.
- Does not address inland (freshwater) aquaculture beyond noting that pisciculturas operate in the interior; the main analysis is the coastal zone.
- Does not provide a formal cost-benefit comparison among the three strategic options (APE / offshore / RAS).

## Key Takeaways

- Biobío's aquaculture is "incipient" — small in volume (e.g., 1,905 t pisciculture production in 2017) but with infrastructure and human-capital advantages (15 candidate APE zones identified; 4% of national smolt supply; >60% of national fish exports passing through Biobío ports).
- The binding constraints are (i) ecological — contamination, anoxia, biodiversity gaps; (ii) socioeconomic — low education, restricted credit, weak technology adoption; (iii) governance — fragmentation, weak compliance, low citizen legitimacy.
- Three viable strategic options: small-scale within AMERB/ECMPO; offshore (needs national regulatory change); recirculating land-based (needs CAPEX/OPEX-driven business models).
- Policy is operationalized as four strategic axes mapped to four sub-problems with critical variables and 4-year targets.
- The governance proposal is institutional: a Regional Aquaculture Commission with public, private, and worker representation, advised by a technical council.

## Useful Factual Details

- **Project number:** Proyecto FIC 4000116 (also referenced as FIC-R 2017).
- **Executing institution:** Centro Interdisciplinario para la Investigación Acuícola (INCAR), Universidad de Concepción.
- **Funding source:** Programa Fondo de Innovación para la Competitividad Regional, Gobierno Regional del Biobío.
- **Date of publication:** December 2019 (PDF metadata: 2019-12-16).
- **Authors:** 12 — Simon, Quiñones, Soto, Dresdner, González, Troncoso, Ceballos, León, Montes, Santis, Sanhueza, Figueroa.
- **Director:** Jeanne Simon Rodgers.
- **Page count:** 59 (PDF, letter size).
- **Companion report:** Metodología para la construcción del Modelo de Lógica Difusa, same project, 51 pp.
- **Production data 2003–2017 (Biobío, tons):** total harvest declined from 9,537 t (2003) to 91 t (2017). Algae 9,319 → 19 t; finfish 217 → 66 t; molluscs ~1 → 5 t.
- **SEIA pipeline 1997–2017:** 30 projects, USD 82.19M total investment.
- **Coastal tenure:** 138 AMERB (44,287 ha), 8 ECMPO (>238,000 ha), 88 concession requests (~1,600 ha).
- **APE candidate sites:** 15 in Biobío, total 7,093.55 ha.
- **Reference scale used in critical-variable scoring:** 0–100, year 0 baseline through year-4 target.

## Citation

```bibtex
@techreport{SimonEtAl_FIC_EstudioBase_2019,
  author      = {Simon, Jeanne and Qui\~nones, Renato and Soto, Doris and Dresdner, Jorge
                 and Gonz\'alez, Nuria and Troncoso, Lilian and Ceballos-Concha, Adams
                 and Le\'on, Jorge and Montes, Rodrigo and Santis, Oscar
                 and Sanhueza, \'Alvaro and Figueroa, Yanina},
  title       = {Estudio Base: Pol\'itica P\'ublica Regional para el Desarrollo de la
                 Acuicultura Sustentable. Sistematizaci\'on de conocimiento t\'acito y
                 expl\'icito para la promoci\'on de la acuicultura sustentable en la
                 Regi\'on del B\'io-B\'io: Una aproximaci\'on mediante la aplicaci\'on
                 de l\'ogica difusa},
  institution = {Centro Interdisciplinario para la Investigaci\'on Acu\'icola (INCAR),
                 Universidad de Concepci\'on},
  type        = {Informe t\'ecnico},
  number      = {Proyecto FIC-R 2017 (FIC 4000116)},
  address     = {Concepci\'on, Chile},
  year        = {2019},
  month       = dec,
  pages       = {59}
}
```

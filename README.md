# Air Pollution


Air pollution is a leading cause of premature death and morbidity. The 2019 Global Burden of Disease study (Murray et al., 2020) finds that deaths attributable to air pollution rank 4th globally, only behind causes such as tobacco, dietary risk, and high systolic blood pressure.
Murray et al., 2020 attributes 4.14 million deaths in 2019 to outdoor air pollution. (It further attributes 2.31 million deaths in 2019 to household air pollution.)


Fossil fuel combustion, particularly in the power sector, is a leading cause of ambient air pollution. 
Mining and combustion of fossil fuels leads to the emission of sulphur, nitrogen oxides, and (fine) particulate matter that results in illness and millions of premature deaths each year (ETC, 2023).


The air pollution to which humans are exposed is multifaceted; there are no standardized approaches to characterize pollutant mixtures, which often include hundreds of individual gaseous compounds and particles of complex physico-chemical composition (Brauer et al., 2012). 
Hence, to assess individuals’ exposure to air pollution for health risk evaluation, indicator pollutants are typically used. 
In epidemiologic cohort studies of long-term exposure, fine particulate matter exposure (i.e., PM2.5) is the most robust indicator of adverse health impacts. 
Hence, most studies on air pollution focus on the health risk posed by fine particulate matter (PM2.5) (e.g., Burnett et al., 2014; Burnett et al., 2018; van et al., 2018; Rauner et al., 2020; Rauner et al., 2020; WB, 2021; WB, 2022; Tang et al., 2022; Huang et al., 2023; Yang et al., 2023), and so do we. 
Particulate matter (PM) comprises multiple components (i.e., a mixture of solid particles and liquid droplets) and size fractions. 
Adverse health effects of fine particulate matter (PM2.5) are more severe than those of coarse particulate matter because fine particles more easily penetrate into the respiratory tract (Chen et al., 2020). 
(In the 2019 Integrated Science Assessment by the US Environmental Protection Agency (EPA), the association between PM2.5 and mortality was rated as “causal”, whereas the association between PM10 and mortality was rated as “suggestive” (EPA, 2019).


Particulate matter with an aerodynamic diameter under 2.5 µm is categorized as PM2.5, and originates mainly from fossil-fuel combustion. 
PM10 includes both fine (PM2.5) and coarse particulate matter with an aerodynamic diameter under 10 µm.


Exposure to PM2.5 from diverse combustion sources is attributed to increased mortality from six diseases: 
(1) stroke, (2) ischemic heart disease (IHD), (3) chronic obstructive pulmonary disease (COPD), (4) lung cancer (LC), (5) lower respiratory infections (LRI), and (6) type II diabetes (DM) (Lim et al., 2012; Murray et al., 2020).


The World Health Organization’s recommended PM2.5 air quality guideline (AQG) is set at 5 µg/m³ (WHO, 2021), with interim targets of 35, 25, 15, and 10 µg/m³, respectively, for the annual average. 
The global average air pollution exposure in 2019 was 43 µg/m³ (Murray et al., 2020), which far exceeds the AQG of 5 µg/m³. The global average masks significant country-level differences in PM2.5 air pollution levels. 
For instance, the average air pollution exposure in 2020 (the latest year of World Bank data) was 48 µg/m³ in India, 35 µg/m³ in China, 8 µg/m³ in the United States, 12 µg/m³ in Europe, 40 µg/m³ in the Arab World, 38 µg/m³ in Sub-Saharan Africa, and 47 µg/m³ in South Asia. (See the full list here: [World Bank Data](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)).

___
**Figure 1: PM2.5 Air Pollution Concentration (μg m3) in 2020**
![Alt text](https://github.com/panahovf/airpollution/blob/006e9fa8d767c74a10ee374eaddce8bd813eb055/images/PM2.5WorldBankLevelWorldMap.png)
___
<br>

# Air Pollution Methodology


Broadly speaking, the standard way in which reduced air pollution economic health benefits are measured is by studying how reduced fossil fuel usage brings down PM2.5 concentration levels at the (population‐weighted) grid level. 
Once the new PM2.5 concentration levels are estimated, the standard methodology developed by air pollution experts is to estimate avoided deaths by making use of “concentration‐response functions” (CRF). 
The CRF for each of the six diseases establishes what fraction of baseline deaths for that disease can be attributed to air pollution. 
To then determine the economic value of avoided mortalities because of lower air pollution, an economic value is attached to a human life. Typically, the “Value of a Statistical Life” (VSL) is used.


We will follow the standard approach to air pollution modeling throughout, as our innovation does not aim to be the air pollution modeling itself; rather, our innovation is its novel application to how gradually phasing out fossil fuels in the power sector results in air pollution economic health benefits. 
The only component of the air pollution modeling where we make a purposeful simplification is in the translation from fossil fuel reduction to reduced air pollution levels. 
The air pollution concentration of PM2.5 is typically evaluated with “transport models” (see, e.g., Krol et al., 2005). 
In essence, air pollution transport models evaluate how air pollutant emissions in one region affect the air pollution concentration in another region, taking into account the atmospheric chemistry and climatic factors at play. 
Atmospheric chemistry determines how different precursor air pollutants interact in the atmosphere to form other air pollutants, thereby determining air pollution concentrations. Van et al., 2018 created TM5‐FASST, a global reduced‐form air quality source–receptor model that has been designed to compute ambient pollutant concentrations of PM2.5. 
The TM5‐FASST model captures *linearized* emission–concentration sensitivities derived from the full chemistry–climate transport model TM5. As Van et al., 2018 show, TM5‐FASST approximates the TM5 model outcomes well, and has the benefit of reduced computational complexity. It is used in several reputable air pollution studies (such as Rauner et al., 2020 and Huang et al., 2023).
Indeed, the reason linearized air pollution tools are widely used is that running the full air pollution transport models is, for most purposes, not practical because it requires enormous computational power and calibration of many parameters. 
For these reasons, we will also take a linearized approach to air pollution modeling, grounded in the full air pollution transport model of McDuffie et al., 2021.


We are deeply grateful to Professor Michael Brauer, a leading expert in air pollution modeling and a key contributor to the Global Burden of Disease (GBD) studies on air pollution, for his careful evaluation of the methodology we adopt in this paper. 
Professor Brauer provided detailed advice through iterative discussions and proposed the linearized approach we adopt in this paper for applying the results of McDuffie et al., 2021 in a simple yet robust manner.


In what follows, we'll set out the detailed steps of our air pollution methodology for evaluating economic health benefits from phasing out fossil fuels in the power sector.


### Step 1: Projecting PM2.5 concentration levels


As a starting point, we take the current (t<sub>0</sub>=2024) PM2.5 concentration levels C<sub>y,z,t<sub>0</sub></sub> globally at 1 km x 1 km spatial resolution, where z &isin; 𝒵 (with 𝒵 being the global set of grid cells) is the unique grid cell and \(y\) specifies the country to which this grid cell belongs. 
We assume that the latest available data for 2021 remains unchanged for (t<sub>0</sub>=2024).


Next, drawing on the chemical transport model of McDuffie et al., 2021, we would like to determine the maximum (denoted with a “hat”) improvement in the PM2.5 air pollution concentration level C&#770;<sub>y,z,f</sub> at the grid level should a global shut-down of fossil fuels in the energy sector take place at once (as then we can draw on the results of McDuffie et al., 2021).
To do this, we take from McDuffie et al. their estimates of the “fractional source contribution” F<sub>z,f</sub> at grid \(z\) and for fossil fuel type (or other PM2.5 source) \(f\) level. 
The fractional source contribution F<sub>z,f</sub> captures—using a global air pollution transport model—by what percentage the current PM2.5 concentration C<sub>y,z,t<sub>0</sub></sub> in grid \(z\) would fall should fossil fuels (or other PM2.5 sources) of type \(f\) be shut down at once all over the world.
Particularly, from their fractional resource contribution database, we use “ENEcoal” (ENE = energy) and “ENEother” as the closest proxies to fossil fuel combustion from coal-fired power plants, and oil- and gas-fired power plants, respectively. 
Hence, the maximum reduction in the PM2.5 air pollution concentration level C&#770;<sub>y,z,f</sub> at grid \(z\) in country \(y\) is given by:


<div align="center">
C&#770;<sub>y,z,f</sub> = C<sub>y,z,t<sub>0</sub></sub> &times; F<sub>z,f</sub>
</div>
<br>


for globally shutting down f = [ENEcoal, ENEother], respectively. 
McDuffie et al. have only studied the fractional resource contribution at the grid level from a global shutdown of fossil fuels (or other PM2.5 sources) of type \(f\); 
they have not studied the effect of the shut down of fossil fuels of single countries on the grid-level PM2.5 concentration, nor the effect of the gradual phase out of fossil fuels in single countries or groups of countries on the grid-level PM2.5 concentration—partly because running these combinations on large air pollution models is computationally taxing.


To novelly model the air pollution benefits of a gradual phase out of fossil fuels in the power sector (in line with specific scenario pathway *s*) rather than the complete halt to global fossil fuels (as prior studies such as McDuffie et al., 2021 have done), we—based on expert advice from renowned air pollution experts—make the reasonable simplifying assumption that the current PM2.5 air pollution concentration relative to the maximum PM2.5 air pollution concentration drops linearly in the CO₂ emission reduction as fossil fuels are phased out according to scenario *s* (we take *s = s₂*: the 1.5°C 50% carbon budget consistent net zero scenario). 
We also assume that air pollution benefits are largely local within one country, so that we can use a global shutdown and phase out scenario to model the air pollution impact of country-level decarbonization.  

  
Given these reasonable simplifying assumptions, we project how the PM2.5 concentration at the grid level will fall as fossil fuels are gradually phased out in the power sector. 
The projected PM2.5 air pollution concentration *C*<sup>s</sup><sub>y, z, t</sub> at time *t* ∈ [t₀+1, T] in country *y* at grid cell *z* under decarbonization scenario *s* is estimated by the current PM2.5 concentration *C*<sub>y, z, t₀</sub> at grid *z* in country *y* minus the sum over the fossil fuel types *f* ∈ ℱ (i.e., ENECoal and ENEOther — where ENEOther groups together oil and gas) of the product of the remaining CO₂ emission share in country *y* for fossil fuel *f* (relative to a complete phase out) and the maximum reduction in the PM2.5 concentration *Ċ*<sub>y, z, f</sub> at grid *z* in country *y* for turning off fossil fuel *f*:

<div align="center">
C<sup>s</sup><sub>y, z, t</sub> = C<sub>y, z, t<sub>0</sub></sub> − ∑<sub>f ∈ ℱ</sub> S<sup>s</sup><sub>y,f,t</sub> &times; C&#770;<sub>y, z, f</sub>
</div>
<br>


where the remaining CO₂ emission share in country *y* for fossil fuel *f* (relative to a complete phase out) is given by one minus the time-*t* CO₂ emissions resulting from fossil fuel *f* in country *y* relative to the initial CO₂ emissions *E*<sub>y,f,t₀</sub> of fossil fuel *f* in country *y*:

<div align="center">
S<sup>s</sup><sub>y,f,t</sub> = 1 − ( E<sup>s</sup><sub>y,f,t</sub> / E<sub>y,f,t<sub>0</sub></sub> )
</div>
<br>


For example, this means that if the power sector phase out of fossil fuel (*f = coal*) has resulted in E<sup>s</sup><sub>y,f,t</sub> / E<sub>y,f,t<sub>0</sub></sub> = 25% of remaining CO₂ emissions relative to initial emissions E<sub>y,f,t<sub>0</sub></sub> in country *y*, and there is no phase out of oil or gas in that country, then the share is S<sup>s</sup><sub>y,f,t</sub> = 75%.  

 
So the new PM2.5 concentration is 75% of the maximum PM2.5 concentration reduction amount lower than the initial PM2.5 concentration level, i.e.,


<div align="center">
C<sup>s</sup><sub>y, z, t</sub> = C<sub>y, z, t<sub>0</sub></sub> − 0.75 &times; Ċ<sub>y, z, f</sub>
</div>
<br>


where Ċ<sub>y, z, f</sub> denotes the maximum reduction in PM2.5 concentration when fossil fuel *f* is completely shut down.


Country *y*’s (unweighted) PM2.5 air pollution concentration at time *t* is defined as the average of the projected PM2.5 concentrations of its grid cells. In other words, if the set of grid cells in country *y* is denoted by 𝒵<sub>y</sub>, then the unweighted concentration is given by:


<div align="center">
<span style="text-decoration: overline;">C</span><sup>s</sup><sub>y,t</sub> = ∑<sub>z ∈ 𝒵<sub>y</sub></sub> C<sup>s</sup><sub>y,z,t</sub>
</div>
<br>


For evaluating the economic benefits of reduced air pollution, the population‐weighted PM2.5 concentration is typically used. This is defined as:


<div align="center">
C<sup>s</sup><sub>y,t</sub> = ∑<sub>z ∈ 𝒵<sub>y</sub></sub> [ C<sup>s</sup><sub>y,z,t</sub> &times; (P<sub>y,z,t</sub> / P<sub>y,t</sub>) ]
</div>
<br>


where:
- P<sub>y,z,t</sub> is the projected population in country *y* in grid cell *z* at time *t*,
- P<sub>y,t</sub> is the projected total population in country *y* at time *t*.


Grid-level population estimates are obtained from the Global Human Settlement Layer project (latest version 2023) for the year 2020. 
Although the project provides grid-level population projections for a few dates, we take a conservative approach by assuming that the spatial distribution of the population in the future is the same as today (i.e., P<sup>t</sup><sub>y,z</sub> / P<sup>t</sup><sub>y</sub> = P<sub>y,z,t<sub>0</sub></sub> / P<sub>y,t<sub>0</sub></sub>) for all t ∈ [t<sub>0</sub>+1, T]. 
Thus, the ratio P<sub>y,z,t</sub> / P<sub>y,t</sub> serves as a weight for obtaining the population‐adjusted PM2.5 concentration from the unweighted concentration.


Global grid levels across the multiple datasets used in this study are adjusted to a common spatial resolution of 1 km × 1 km.


In the **left panel** of *Figure 2*, we show the unweighted PM2.5 concentration, <span style="text-decoration: overline;">C</span><sup>t<sub>2021</sub></sup><sub>y</sub>, 
(from the equation above) and the population‐weighted PM2.5 concentration, C<sup>t<sub>2021</sub></sup><sub>y</sub>, for each country *y* according to our data. 
In the **right panel**, we compare the population‐weighted PM2.5 concentration levels (aggregated from our 1 km × 1 km grid data) to those reported by the World Bank for 2020 (latest available) and find these are fairly consistent (i.e., they lie along the 45° line), illustrating that our data is consistent with another authoritative source.


In the **left panel** of *Figure 2*, we show the unweighted <span style="text-decoration: overline;">C</span><sup>t<sub>2021</sub></sup><sub>y</sub> and the population‐weighted C<sup>t<sub>2021</sub></sup><sub>y</sub> for each country *y*. In the **right panel**,
we compare the population‐weighted C<sup>t<sub>2021</sub></sup><sub>y</sub> estimates to those of the World Bank 2020 and find high consistency, demonstrating the reliability of our data.

___
**Figure 2: PM2.5 air pollution concentration (μg/m3) estimates**
<br>
&nbsp;
![Alt text](https://github.com/panahovf/airpollution/blob/2aba9a79593a15b05b3c08c3b36c3ca03d734bfd/images/AirPollutionComparisonWorldBank.png)
___
<br>


In *Figure 3*, we show projections of the PM2.5 concentration C<sup>s₂</sup><sub>y, z, t</sub> at the grid level (see the earlier equation for projected concentration) for 2025, 2030, and 2035, along with their population‐weighted country average, under the 1.5°C 50% carbon-budget consistent net‐zero 2050 scenario (*s = s₂*).

___
**Figure 3: Projections (for 2025, 2030, 2035) of the PM2.5 air pollution concentration (μg/m3)
estimates at the grid level and their country level (population-weighted) average for eight de-
veloping countries**
<br>
&nbsp;
![Alt text](https://github.com/panahovf/airpollution/blob/8f24f6bd2231b6c3b61c4c79fc974f765bcd033e/images/DeclineOfAirPollutionLevels.png)
___
<br>


### Step 2: Mortality impact

Having estimated PM2.5 concentration into 2050 under current policies (s = s₁) and the net‐zero 1.5°C 50% (s = s₂) scenarios, we proceed with identifying impacts on mortality rates. 
To do this, we make use of the “concentration response functions” R<sub>d</sub> which have been developed for each disease d attributable to air pollution; see *Figure 4*.

___
**Figure 4: Concentration response functions Rd for each disease d**

![Alt text](https://github.com/panahovf/airpollution/blob/882068a7241924c1aec16f0a889efea541c51a17/images/methodology%20-%20response%20functions.png)
___
<br>

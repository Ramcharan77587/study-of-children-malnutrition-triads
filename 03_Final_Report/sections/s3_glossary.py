# -*- coding: utf-8 -*-
"""
Section 3: Encyclopedic Technical Glossary & Methodological Reference Guide (Every Term Explained)
"""

def get_glossary_markdown():
    return r"""## 3. Encyclopedic Technical Glossary & Methodological Reference Guide

This exhaustive glossary provides rigorous clinical, mathematical, demographic, and policy definitions for every technical term, indicator, statistical test, machine learning method, and national scheme referenced throughout Project NIErnaya.

---

### Domain A: Pediatric Anthropometry, Clinical Nutrition & Etiology

#### 1. Stunting (Height-for-Age Z-Score < -2 SD)
* **Formal Definition:** A condition where a child under five years of age has a height (or recumbent length for infants under 24 months) that falls more than two standard deviations below the median of the World Health Organization (WHO) Child Growth Standards (2006) for that age and sex.
* **Clinical Formula:**
  $$\text{HAZ} = \frac{\text{Height}_{\text{observed}} - \text{Median}_{\text{reference}}}{\text{SD}_{\text{reference}}} < -2.0$$
* **Biological Mechanism:** Stunting reflects chronic, long-term, cumulative nutritional deprivation and repeated bouts of infection (especially diarrhea and intestinal worm infestations). It represents linear growth faltering that occurs primarily during the critical "First 1,000 Days" window (conception to two years of age). Beyond age two, the physical and neurological deficits of stunting become largely permanent and irreversible.
* **Significance in NIErnaya:** Measured as `stunting_pct` across 706 districts (Mean: $33.51\%$, Range: $13.20\% - 60.60\%$). Concentrated along the northern and eastern Gangetic plains.

#### 2. Wasting (Weight-for-Height Z-Score < -2 SD)
* **Formal Definition:** A condition where a child under five has a body weight that falls more than two standard deviations below the median weight-for-height of the WHO Child Growth Standards (2006).
* **Clinical Formula:**
  $$\text{WHZ} = \frac{\text{Weight}_{\text{observed}} - \text{Median}_{\text{reference}}}{\text{SD}_{\text{reference}}} < -2.0$$
* **Biological Mechanism:** Wasting is the primary indicator of **acute malnutrition**. It results from rapid weight loss or failure to gain weight due to acute illness (such as acute gastroenteritis or pneumonia) or sudden severe food shortages. Unlike stunting, which develops slowly over months or years, wasting can develop within days or weeks. A wasted child experiences muscle catabolism and immune depletion, suffering a 3- to 9-fold higher risk of mortality.
* **Significance in NIErnaya:** Measured as `wasting_pct` (Mean: $18.54\%$, Range: $5.00\% - 48.00\%$). Paradoxically highest in industrialized western states (Gujarat at $26.14\%$, Maharashtra at $25.80\%$).

#### 3. Underweight (Weight-for-Age Z-Score < -2 SD)
* **Formal Definition:** A condition where a child's weight falls more than two standard deviations below the median weight-for-age of the WHO reference population.
* **Clinical Formula:**
  $$\text{WAZ} = \frac{\text{Weight}_{\text{observed}} - \text{Median}_{\text{reference}}}{\text{SD}_{\text{reference}}} < -2.0$$
* **Biological Mechanism:** Underweight is a **composite indicator**. Because body weight is influenced by both skeletal height and acute muscle/fat mass, an underweight child may be stunted, wasted, or both simultaneously. While historically the primary metric monitored by UNICEF, modern epidemiology treats it as an aggregate rather than a distinct clinical pathology.
* **Significance in NIErnaya:** Measured as `underweight_pct` (Mean: $29.50\%$, Range: $7.20\% - 62.40\%$). Exhibits the highest standard deviation ($\sigma = 9.68\%$) among the triad.

#### 4. Severe Acute Malnutrition (SAM) & Moderate Acute Malnutrition (MAM)
* **Definitions & Cutoffs:**
  * **SAM:** Weight-for-Height Z-score (WHZ) $< -3.0$ SD, or Mid-Upper Arm Circumference (MUAC) $< 115\text{ mm}$, or the presence of bilateral pitting pedal edema.
  * **MAM:** WHZ between $-3.0$ SD and $-2.0$ SD, or MUAC between $115\text{ mm}$ and $125\text{ mm}$, without edema.
* **Clinical Protocol:** SAM requires immediate medical intervention via Nutritional Rehabilitation Centres (NRCs) using Therapeutic F-75/F-100 feeds or Ready-to-Use Therapeutic Food (RUTF) to prevent metabolic collapse and septic shock.

#### 5. Child Anaemia (Haemoglobin < 11.0 g/dL)
* **Formal Definition:** Blood haemoglobin (Hb) concentration below $11.0\text{ g/dL}$ in children aged 6–59 months, adjusted for altitude where applicable.
* **Clinical Categories:**
  * Mild Anaemia: $10.0 - 10.9\text{ g/dL}$
  * Moderate Anaemia: $7.0 - 9.9\text{ g/dL}$
  * Severe Anaemia: $< 7.0\text{ g/dL}$
* **Biological Mechanism:** Driven primarily by dietary iron deficiency, poor bioavailability of plant-based non-heme iron, chronic parasitic infections (hookworm), and recurrent malaria. Causes tissue hypoxia, impaired neuromuscular coordination, reduced cellular immunity, and irreversible cognitive deficits.
* **Significance in NIErnaya:** Measured as `child_anemia_pct` (Mean: $66.49\%$, Range: $28.00\% - 91.90\%$). Demonstrates a systemic national baseline exceeding $60\%$ across most districts.

#### 6. Environmental Enteropathy / Environmental Enteric Dysfunction (EED)
* **Formal Definition:** A subclinical, chronic inflammatory disorder of the small intestine prevalent among children living in unhygienic conditions characterized by open defecation and fecal contamination.
* **Pathophysiological Mechanism:** Ingestion of fecal-oral pathogens (bacteria, protozoa, helminths) triggers chronic blunting of intestinal villi, thinning of the mucosal barrier, and immune activation. Even if a child consumes sufficient calories, the atrophied gut cannot absorb nutrients. Chronic gut leakiness also allows bacterial endotoxins into the bloodstream, sustaining low-grade systemic inflammation that halts skeletal growth.
* **Significance in NIErnaya:** Explains the powerful protective correlation of improved sanitation ($r = -0.503$ with stunting): eliminating open defecation arrests environmental enteropathy.

#### 7. Linear Growth Faltering & The First 1,000 Days Window
* **Formal Definition:** The developmental window spanning from conception through a child's second birthday ($270\text{ days of pregnancy} + 365\text{ days (Year 1)} + 365\text{ days (Year 2)} = 1,000\text{ days}$).
* **Epidemiological Significance:** Up to $80\%$ of human brain growth and skeletal linear velocity occurs during this period. Nutritional or infectious insults during these 1,000 days cause irreversible damage to physical height, neural synaptic connectivity, and metabolic programming.

#### 8. Intergenerational Malnutrition Cycle
* **Mechanistic Pathway:** An undernourished, stunted young girl reaches adolescence with a small pelvis and low micronutrient reserves. If married early, she conceives before completing physical maturation. The fetus suffers intrauterine growth restriction (IUGR), resulting in a Low Birth Weight ($<2.5\text{ kg}$) infant. This child enters life with compromised growth velocity, perpetuating stunting into the next generation.
* **Significance in NIErnaya:** Validated by the strong correlation between early marriage and stunting ($r = +0.428$).

#### 9. The Child Malnutrition Triad
* **Concept:** The collective triad of anthropometric indicators tracked globally under UN SDG 2: Stunting (chronic), Wasting (acute), and Underweight (composite).

#### 10. The Stunting–Wasting Duality / Phenotypic Divergence
* **Discovery:** The spatial and statistical independence of stunting and wasting across Indian districts ($r = 0.224$, shared variance $<5\%$). Stunting concentrates in the eastern Gangetic agricultural plains; wasting concentrates in the western industrialized corridor.

---

### Domain B: Survey Methodology, Sampling & Demographic Cartography

#### 11. NFHS-5 (National Family Health Survey Round 5)
* **Definition:** A large-scale, multi-round national household survey conducted between 2019 and 2021 across all 28 States and 8 Union Territories of India.
* **Administrative Scope:** Coordinated by the Ministry of Health and Family Welfare (MoHFW) with the International Institute for Population Sciences (IIPS), Mumbai serving as the nodal technical agency.

#### 12. Stratified Two-Stage Cluster Sampling Design
* **Methodology:**
  * **Stage 1 (Primary Sampling Units - PSUs):** In rural areas, villages are selected with Probability Proportional to Size (PPS). In urban areas, Census Enumeration Blocks (CEBs) are selected with PPS.
  * **Stage 2 (Household Selection):** Complete household listing is mapped in each selected PSU; 22–30 households are randomly chosen via systematic circular sampling.
  * Anthropometric measurements (height and weight) and capillary blood hemoglobin testing are performed on all eligible children under age five within selected households using standardized digital scales, stadiometers, and HemoCue photometers.

#### 13. Factual District Records vs. Population-Weighted National Estimates
* **Distinction:**
  * **Factual District Record:** The unweighted sample mean of children surveyed within an administrative district boundary. Represents the operational health status of that geographic jurisdiction.
  * **Population-Weighted National Estimate:** Re-weights district records by child population densities.
  * **NIErnaya Mandate:** We explicitly analyze unweighted district records because our objective is administrative performance benchmarking across governance units, where each district represents an equal sovereign administrative mandate for public health resource allocation.

#### 14. Ecological Dataset & The Ecological Fallacy
* **Ecological Dataset:** Data where the unit of observation is an aggregate group or administrative area (e.g., district level) rather than an individual patient.
* **Ecological Fallacy:** The statistical error of inferring individual-level causal relationships directly from group-level correlations (e.g., assuming an individual illiterate mother's child will automatically be stunted because the district has low female literacy). Project NIErnaya explicitly avoids the ecological fallacy by presenting associations as district-level systemic risks and ecological gradients.

#### 15. District Cartographic Alignment (Census 2011 vs. NFHS-5 706 Districts)
* **Cartographic Challenge:** The 2011 Census of India established 640 administrative districts. Between 2011 and 2021, state governments carved out 66 new districts through administrative bifurcations and trifurcations (e.g., Telangana dividing 10 districts into 33).
* **NIErnaya Solution:** We maintained all 706 factual NFHS-5 districts in tabular analysis. For geospatial mapping, our automated matching pipeline links 637 districts (99.4% coverage) using normalized state-district composite keys with Census code fallback reconciliation.

#### 16. Missingness Mechanisms (MCAR, MAR, MNAR)
* **Mechanisms:**
  * Missing Completely at Random (MCAR): Missingness is unrelated to observed or unobserved data.
  * Missing at Random (MAR): Missingness depends systematically on observed covariates.
  * Missing Not at Random (MNAR): Missingness depends on the unobserved value itself.
* **Audit Result:** Our audit confirmed **0% missing values** across all 10 analytical indicators for 706 districts, eliminating the need for synthetic imputation.

---

### Domain C: Statistical & Exploratory Data Analysis Methods

#### 17. Parametric vs. Non-Parametric Statistics
* **Parametric:** Statistical methods that assume data are generated from a specific probability distribution with fixed parameters (e.g., normal distribution with mean $\mu$ and standard deviation $\sigma$). Example: Pearson correlation, OLS regression.
* **Non-Parametric:** Distribution-free methods that do not assume normality, relying instead on rank orderings or medians. Robust against extreme skewness and outliers. Example: Spearman rank correlation, Mann-Whitney U test.

#### 18. Interquartile Range (IQR) & Tukey's $1.5 \times \text{IQR}$ Outlier Rule
* **Formula:** $\text{IQR} = Q_3 - Q_1$ (difference between 75th and 25th percentiles).
* **Tukey Outlier Thresholds:**
  $$\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}, \quad \text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$$
* **Application in NIErnaya:** 92 values exceeded these bounds across 10 indicators. All 92 were retained because they represent true humanitarian crises in high-burden tribal or remote districts, not data measurement errors.

#### 19. Skewness and Kurtosis
* **Skewness:** Measure of distribution asymmetry around the mean.
  $$\gamma_1 = \frac{\sum (x_i - \bar{x})^3}{(n-1) s^3}$$
  * Stunting exhibits mild skewness ($+0.34$); Wasting exhibits substantial positive skewness ($+0.92$), reflecting an extended right tail of acute crisis districts.
* **Kurtosis:** Measure of the thickness or "heaviness" of distribution tails relative to a normal distribution.

#### 20. Pearson Product-Moment Correlation ($r$)
* **Formula:**
  $$r_{xy} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
* **Interpretation:** Measures the strength and direction of a **linear relationship** between two continuous variables on a scale from $-1.0$ to $+1.0$.

#### 21. Spearman Rank-Order Correlation ($\rho$)
* **Formula:**
  $$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$
  where $d_i = \text{rank}(x_i) - \text{rank}(y_i)$.
* **Interpretation:** Measures the strength and direction of a **monotonic relationship** based on ranked data. Robust against non-linear monotonic shifts and extreme leverage points.

#### 22. Benjamini–Hochberg False Discovery Rate (FDR) Procedure
* **Mathematical Algorithm:**
  1. Rank all $m$ calculated $p$-values in ascending order: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
  2. For a chosen False Discovery Rate $Q$ (e.g., $Q = 0.001$), find the largest rank $k$ such that:
     $$p_{(k)} \le \frac{k}{m} Q$$
  3. Reject all null hypotheses for $i = 1, \dots, k$.
* **Project Justification:** Corrects for multiple testing across 21 bivariate correlation pairs, eliminating false positives (Type I error) without the excessive conservatism of Bonferroni.

#### 23. Type I Error ($\alpha$) vs. Type II Error ($\beta$)
* **Type I Error ($\alpha$):** False positive—concluding that a driver is significantly correlated with malnutrition when no true association exists.
* **Type II Error ($\beta$):** False negative—failing to detect a genuine real-world determinant due to excessive statistical penalties.

#### 24. Multicollinearity & Variance Inflation Factor (VIF)
* **Definition:** A condition where two or more predictor variables in a statistical model are highly linearly related, inflating standard errors and rendering regression coefficients unstable.
* **Formula:**
  $$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
  where $R_j^2$ is the coefficient of determination obtained by regressing predictor $x_j$ on all other predictors.
* **Evaluation in NIErnaya:**
  * Improved Water: $\text{VIF} = 1.19$
  * Improved Sanitation: $\text{VIF} = 2.50$
  * Female Literacy: $\text{VIF} = 2.45$
  * Early Marriage: $\text{VIF} = 1.74$
  All VIFs are strictly $< 2.50$, far below the critical threshold of $5.0$, confirming the absence of harmful multicollinearity.

#### 25. The "Water Access Paradox" & Statistical Ceiling Effect
* **Paradox:** Improved drinking water access has a near-zero correlation with stunting ($r = -0.037$).
* **Two Causes:**
  1. **Ceiling Effect:** Median access is $97.00\%$ across India (IQR only $5.6\%$). When virtually all districts report $>90\%$ access, variance approaches zero, constraining mathematical correlation.
  2. **Measurement Decoupling:** NFHS defines "improved water" by infrastructure type (covered tubewell, piped supply) rather than testing water purity. Water is frequently contaminated during carriage, open storage, and cup dipping at home.

---

### Domain D: Preprocessing & Feature Engineering

#### 26. Standard Z-Score Normalization
* **Formula:**
  $$z = \frac{x - \mu}{\sigma}$$
* **Purpose:** Rescales raw variables with disparate means and units into a dimensionless standard normal distribution ($\mu = 0, \sigma = 1$), allowing equal mathematical weighting in composite indices.

#### 27. Socioeconomic Vulnerability Index (SVI)
* **Engineered Formula:**
  $$\text{SVI} = \frac{z(\text{Early Marriage}) - z(\text{Female Literacy})}{2}$$
* **Analytical Interpretation:** Integrates female disempowerment into a single standardized axis. Correlates at $r = +0.583$ with Underweight and $+0.536$ with Stunting.

#### 28. Sanitation–Water Gap Index
* **Engineered Formula:**
  $$\text{Gap}_{\text{W-S}} = \text{Improved Water \%} - \text{Improved Sanitation \%}$$
* **Analytical Interpretation:** Captures the structural divergence between access to drinking water and lack of toilet facilities. When households fetch piped water in environments surrounded by open defecation, fecal pathogens contaminate water containers, driving an $r = +0.507$ correlation with underweight.

#### 29. Maternal Care Disconnect / Gap Index
* **Engineered Formula:**
  $$\text{Gap}_{\text{M}} = \text{Institutional Births \%} - \text{ANC 4+ Visits \%}$$
* **Analytical Interpretation:** Measures healthcare system fragmentation. In many districts, institutional delivery rates exceed $90\%$ (driven by JSY cash incentives), but mothers attended fewer than four antenatal checkups ($<50\%$), missing vital fetal growth monitoring and anemia prophylaxis.

#### 30. Nutritional Burden Index (NBI)
* **Engineered Formula:**
  $$\text{NBI} = \frac{\text{Stunting \%} + \text{Wasting \%} + \text{Underweight \%}}{3}$$
* **Analytical Interpretation:** Composite benchmark of overall pediatric nutritional distress.

#### 31. Data Leakage & Target Contamination Safeguards
* **Definition:** Data leakage occurs when information from outside the training dataset (specifically the target outcome) is inadvertently incorporated into the feature engineering pipeline.
* **NIErnaya Protocol:** Because NBI directly incorporates Stunting, Wasting, and Underweight, it was **quarantined from predictive feature sets**. All z-score scalings and PCA transformations were computed strictly on the predictor matrix ($X$) without exposure to target outcomes ($y$).

---

### Domain E: Dimensionality Reduction & Principal Component Analysis (PCA)

#### 32. Principal Component Analysis (PCA)
* **Mathematical Definition:** An unsupervised orthogonal linear transformation that transforms a set of correlated continuous variables into a smaller set of linearly uncorrelated latent variables called principal components.

#### 33. Covariance & Correlation Matrix Decomposition
* **Process:** Standardizing variables transforms the covariance matrix into the sample correlation matrix:
  $$R = \frac{1}{n-1} Z^T Z$$
  We solve the characteristic eigenvalue equation:
  $$R v_k = \lambda_k v_k$$
  where $\lambda_k$ is the $k$-th eigenvalue and $v_k$ is the corresponding eigenvector.

#### 34. Eigenvalues ($\lambda$) and Eigenvectors
* **Eigenvalue ($\lambda_k$):** Represents the total amount of variance captured by the $k$-th principal component. In standardized PCA with $P$ variables, the sum of all eigenvalues equals $P$ ($\sum \lambda_k = 7.0$).
* **Eigenvector ($v_k$):** The directional unit vector that defines the linear combination weights of original variables.

#### 35. Kaiser-Guttman Criterion ($\lambda > 1.0$)
* **Decision Rule:** Retain only those principal components with eigenvalues strictly greater than $1.0$. An eigenvalue $<1.0$ contains less information than a single standardized original variable.

#### 36. Cattell's Scree Plot & Elbow Criterion
* **Definition:** A line plot of sorted eigenvalues against component index numbers. The optimal retention cutoff is the "elbow"—the point where the steep downward curve flattens out into residual rubble.
* **NIErnaya Result:** Eigenvalue curve drops sharply from $\lambda_1 = 2.75$ and $\lambda_2 = 1.64$ to $\lambda_3 = 0.81$, confirming exactly two retention components.

#### 37. Factor / Component Loadings ($a_{ij}$)
* **Definition:** The correlation between the original standardized variable $x_i$ and the extracted principal component $PC_j$:
  $$a_{ij} = v_{ij} \sqrt{\lambda_j}$$
* **Interpretation:** Values close to $+1.0$ or $-1.0$ indicate dominant contributions to that latent axis.

#### 38. Orthogonality & Subspace Independence
* **Property:** All principal components are mathematically orthogonal to one another:
  $$\text{Cov}(PC_1, PC_2) = 0$$
  This ensures that PC1 and PC2 measure completely independent systemic dimensions of district vulnerability.

#### 39. PC1: "Socioeconomic Infrastructure Axis" (39.31% Variance)
* **Characterization:** Dominated by Female Literacy ($+0.504$), Improved Sanitation ($+0.490$), Early Marriage ($-0.463$), and Child Anaemia ($-0.354$). Captures structural socio-environmental empowerment.

#### 40. PC2: "Clinical Healthcare Delivery Axis" (23.39% Variance)
* **Characterization:** Dominated by Institutional Births ($+0.613$), 4+ ANC Visits ($+0.578$), and Improved Water ($+0.449$). Captures health facility utilization.

---

### Domain F: National Policy Frameworks, Programs & Global Commitments

#### 41. UN Sustainable Development Goal 2 (SDG 2, Target 2.2)
* **Global Target:** "By 2030, end all forms of malnutrition, including achieving, by 2025, the internationally agreed targets on stunting and wasting in children under 5 years of age."

#### 42. POSHAN Abhiyaan (National Nutrition Mission) / POSHAN 2.0
* **Framework:** India's flagship program launched by the Ministry of Women and Child Development (MoWCD) to improve nutritional outcomes for children under six, adolescent girls, pregnant women, and lactating mothers through technology convergence, behavior change communication, and community mobilization.

#### 43. Swachh Bharat Mission – Gramin (SBM-G)
* **Framework:** Nationwide sanitation campaign launched by the Ministry of Jal Shakti to eliminate open defecation across rural India through toilet construction, behavior change, and solid/liquid waste management (ODF-Plus).

#### 44. Jal Jeevan Mission (JJM / Har Ghar Jal)
* **Framework:** Flagship scheme aiming to provide Functional Household Tap Connections (FHTC) with 55 liters per capita per day of potable water to every rural household.

#### 45. Pradhan Mantri Matru Vandana Yojana (PMMVY)
* **Framework:** Direct Benefit Transfer (DBT) maternity benefit scheme providing partial wage compensation to pregnant and lactating mothers for early registration and institutional delivery.

#### 46. Beti Bachao Beti Padhao (BBBP)
* **Framework:** Inter-ministerial initiative aimed at preventing gender-biased sex selection and ensuring the survival, protection, and secondary education of the girl child.

#### 47. Anemia Mukt Bharat (AMB)
* **Framework:** National strategy to reduce anemia prevalence via the 6x6x6 mechanism (6 target age groups, 6 interventions, 6 institutional mechanisms), deploying prophylactic iron-folic acid (IFA) supplementation and deworming.
"""

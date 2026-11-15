# -*- coding: utf-8 -*-
"""
Section 1: Presentation Architecture, Pacing Blueprint & Evaluation Rubric Alignment
"""

def get_intro_markdown():
    return """# Project NIErnaya — Complete Phase 2 Presentation Companion, Slide-by-Slide Explanation, Speaker Script & Encyclopedic Technical Glossary

**Document Subtitle:** Official Evaluation Defense Guide & Methodological Reference for the NFHS-5 District-Level Child Malnutrition Analytics Deck  
**Delivered Formats:** Executive PDF Reference · Print-Styled HTML · Master Markdown Documentation  
**Companion Deck:** [`NIErnaya_Phase2_Presentation_Deck.html`](file:///D:/DAV%20NIErnaya/03_Final_Report/NIErnaya_Phase2_Presentation_Deck.html) / [`NIErnaya_Phase2_Presentation_Deck.pptx`](file:///D:/DAV%20NIErnaya/03_Final_Report/NIErnaya_Phase2_Presentation_Deck.pptx)  
**Primary Analytical Corpus:** 706 Empirical Districts · 37 States & Union Territories · 10 Primary NFHS-5 Survey Indicators · Zero Synthetic Imputations  
**Target Presentation Duration:** 10–12 Minutes (+ 3–5 Minutes Evaluator Q&A Defense)  
**Author / Research Initiative:** Project NIErnaya (National Insights & Evidence-based Research for Nutritional Advocacy & Yield Analytics) — November 2026  

---

## 1. Executive Presentation Blueprint & Narrative Architecture

### 1.1 The 4-Act Analytical Narrative Arc
Project NIErnaya's 18-slide presentation is structured as a tightly cohesive four-act narrative designed to address all requirements of the Phase 2 analytics competition:

* **Act I: The National Problem & Empirical Foundation (Slides 1–7)**
  * *Objective:* Establish the humanitarian and economic urgency of child undernutrition under UN Sustainable Development Goal 2 (Target 2.2).
  * *Core Evidence:* Audit 706 district factual records with 0% missingness; delineate the three distinct clinical dimensions of the malnutrition triad (Stunting, Wasting, Underweight); and present the breakthrough cartographic finding: the **Stunting–Wasting Duality** (geographic decoupling between the eastern Gangetic stunting belt and the western wasting corridor).
* **Act II: Multi-Sectoral Associations & The Water Paradox (Slides 8–11)**
  * *Objective:* Unpack the underlying socioeconomic, environmental, and maternal drivers explaining district-level malnutrition.
  * *Core Evidence:* Dual correlation matrices (Pearson $r$ and Spearman $\rho$) with Benjamini–Hochberg False Discovery Rate (FDR) adjustments ($q < 0.001$); establish improved sanitation and female literacy as premier protective levers; identify early marriage as the leading vulnerability driver; resolve the "Water Access Paradox" via statistical ceiling effects and water quality decoupling.
* **Act III: Mathematical Preprocessing & Latent Factor Discovery (Slides 12–14)**
  * *Objective:* Demonstrate rigorous data science, feature engineering, and dimensionality reduction.
  * *Core Evidence:* Engineer four domain-grounded composite indices (Socioeconomic Vulnerability Index, Sanitation–Water Gap, Maternal Care Disconnect, Nutritional Burden Index) with strict data leakage quarantine protocols; execute Principal Component Analysis (PCA) extracting two orthogonal axes explaining **62.70% of total variance** (PC1: Socioeconomic Infrastructure vs. PC2: Clinical Healthcare Delivery).
* **Act IV: Actionable Policy Imperatives & Submission Provenance (Slides 15–18)**
  * *Objective:* Translate empirical coefficients into five concrete, non-linear policy recommendations for POSHAN Abhiyaan and allied ministries; summarize reproducible project artifacts; execute defense Q&A.

---

### 1.2 Presentation Timing & Pacing Blueprint (10–12 Minute Master Schedule)

| Slide | Category / Title | Focus & Core Deliverable | Target Timestamp | Allotted Time |
| :--- | :--- | :--- | :---: | :---: |
| **01** | **Title Slide** | Project identity, scope, 706 factual districts | 0:00 – 0:40 | 40s |
| **02** | **The Problem: Why This Matters** | Clinical triad definitions, SDG 2.2, national scale | 0:40 – 1:30 | 50s |
| **03** | **Dataset Overview & Audit** | Provenance, 0% missingness, 92 retained outliers | 1:30 – 2:20 | 50s |
| **04** | *Section I Divider* | Exploratory Data Analysis transition | 2:20 – 2:30 | 10s |
| **05** | **Malnutrition Triad Distributions** | Univariate distributions, boxplots, normality checks | 2:30 – 3:30 | 60s |
| **06** | **State-Level Disparities** | State rankings, stunting vs wasting divergence | 3:30 – 4:30 | 60s |
| **07** | **Geographic Hotspots & Duality** | National choropleths, spatial cluster decoupling | 4:30 – 5:30 | 60s |
| **08** | *Section II Divider* | Correlation & Relationships transition | 5:30 – 5:40 | 10s |
| **09** | **Pearson & Spearman Heatmaps** | Correlation matrices, FDR adjustments, triad links | 5:40 – 6:30 | 50s |
| **10** | **Strongest Multi-Sectoral Drivers** | Top protective levers, early marriage, Water Paradox | 6:30 – 7:30 | 60s |
| **11** | **Bivariate Scatter Evidence** | 706-district scatter plots with OLS regression lines | 7:30 – 8:20 | 50s |
| **12** | *Section III Divider* | Preprocessing & Feature Engineering transition | 8:20 – 8:30 | 10s |
| **13** | **Engineered Composite Features** | SVI, Sanitation-Water Gap, Leakage Quarantine | 8:30 – 9:30 | 60s |
| **14** | **Principal Component Analysis** | Scree plot, Kaiser criterion, PC1 & PC2 axes | 9:30 – 10:30 | 60s |
| **15** | *Section IV Divider* | Key Insights & Conclusions transition | 10:30 – 10:40 | 10s |
| **16** | **Five Evidence-Based Insights** | Actionable policy recommendations for POSHAN | 10:40 – 11:30 | 50s |
| **17** | **Deliverables & Methodology** | Code repository, report, WebP atlas, Streamlit app | 11:30 – 12:00 | 30s |
| **18** | **Thank You / Q&A Defense** | Formal close, evaluator defense readiness | 12:00 + | Q&A |

---

### 1.3 Evaluation Rubric Alignment Matrix

| Evaluation Dimension | Weight | Project NIErnaya Evidence & Presentation Anchor |
| :--- | :---: | :--- |
| **1. Dataset Understanding & Exploratory Analysis** | 25% | **Slides 2, 3, 5, 6, 7:** Deep coverage of 706 factual districts; parametric/non-parametric distribution properties; boxplot outlier audits; state-level disparities; spatial duality discovery. |
| **2. Data Preprocessing & Cleaning** | 20% | **Slides 3, 12, 13:** Transparent audit trail; 0% synthetic imputation; preservation of 65 newly formed districts; ethical retention of 92 extreme epidemiologic outliers; strict range enforcement $[0, 100]$. |
| **3. Correlation Analysis & Feature Relationships** | 20% | **Slides 9, 10, 11:** Parametric Pearson vs. non-parametric Spearman rank correlation; Benjamini–Hochberg FDR adjustments; identification of protective vs. risk factors; resolution of the Water Access Paradox; VIF multicollinearity screening. |
| **4. Feature Engineering & PCA** | 20% | **Slides 13, 14:** Creation of 4 domain-driven composite indices; mathematical z-score normalization; explicit data leakage quarantine protocol; PCA eigen-decomposition yielding 62.70% variance across 2 orthogonal axes. |
| **5. Actionable Insights & Professional Delivery** | 15% | **Slides 16, 17, 18:** 5 multi-sectoral policy recommendations tailored to POSHAN 2.0; production-grade deliverables (PDF report, 468-chart WebP atlas, PPTX, interactive Streamlit GIS dashboard). |

---

### 1.4 Non-Verbal Presenter Strategy & Stage Presence
1. **Pacing and Vocal Modulation:** Speak at an unhurried, measured pace (~130 words per minute). Slow down when introducing critical statistical metrics (e.g., "$r = -0.583$", "62.70% variance").
2. **Visual Pointers:** Never let an audience read a slide unguided. Always direct attention explicitly: *"If you look at the top-right quadrant of Slide 7...", "Notice the blue line in Figure 3..."*
3. **Physical Gestures for Duality (Slide 7):** When describing the Stunting–Wasting Duality, use two hands to gesture geographically—left hand towards the eastern Gangetic plain for chronic stunting, right hand towards the western corridor (Gujarat/Maharashtra) for acute wasting.
4. **Transition Continuity:** Never end a slide with silence. Always use the provided verbal transition hooks to seamlessly lead into the next conceptual block.
"""

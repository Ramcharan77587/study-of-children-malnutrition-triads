# Project NIErnaya: National Insights & Evidence-Based Research for Nutritional Advocacy & Yield Analytics

**Target Sustainable Development Goal:** UN SDG 2 (Zero Hunger) — Target 2.2 (End all forms of malnutrition by 2030)  
**Primary Focus:** District-Level Precision Analytics of the Child Malnutrition Triad (Stunting, Wasting, Underweight)  
**Survey Dataset:** Fifth National Family Health Survey (NFHS-5, 2019–2021) — Ministry of Health & Family Welfare (MoHFW) / International Institute for Population Sciences (IIPS)  
**Geospatial Boundaries:** Census of India 2011 District Hierarchy  

---

## 📁 Repository & Folder Architecture

```text
D:\DAV NIErnaya
├── 01_Visual_Atlas/             # 468 publication-grade WebP visual analytics charts
│   ├── 01_Main_NFHS5/           # 41 core plots (distributions, boxplots, correlations, PCA)
│   ├── 02_Supplementary_India/  # 212 indicator profile charts from India.csv
│   ├── 03_Supplementary_India_Change/ # 212 longitudinal comparison charts from India_Change.csv
│   └── 04_Geographical_Maps/    # 3 pan-India state-level malnutrition choropleth maps
│
├── 02_Analysis_Outputs/         # Audit reports, statistical tables, and engineered data
│   ├── 01_Audit/                # Data-quality checks, missingness, 1.5x IQR outlier screenings
│   ├── 02_Main_EDA/             # Pearson & Spearman matrices (FDR adjusted), state rankings
│   ├── 03_Supplementary_India/  # Indicator-level survey comparison summaries
│   ├── 04_Supplementary_Change/ # Change column formula validation audits
│   ├── 05_Feature_Engineering_PCA/ # PCA scree plots, component loadings, variance ratios
│   ├── 06_Final_Data/           # Clean conservative CSV & engineered dataset (18 columns)
│   └── 07_Indicator_Inventory/  # Domain classification and candidate prioritization
│
├── 03_Final_Report/             # Phase 2 submission deliverables & presentation suite
│   ├── NIErnaya_Phase2_Final_Technical_Report.pdf   # 14-page formal peer-grade technical report
│   ├── NIErnaya_Phase2_Presentation_Guide_and_Speaker_Notes.pdf # 39-page master presentation guide & encyclopedic glossary
│   ├── NIErnaya_Phase2_Presentation_Deck.pptx       # 18-slide 16:9 widescreen PowerPoint deck
│   ├── NIErnaya_Phase2_Presentation_Deck.html       # Standalone interactive browser slide deck
│   └── NIErnaya_Phase2_Presentation_Speaker_Notes.md # Slide-by-slide 10–12 min script & jury Q&A
│
├── dashboard/                   # Interactive Streamlit Health Intelligence Application
│   ├── app.py                   # Multi-page dashboard with auto-preloaded district microdata
│   ├── README.md                # Local setup instructions
│   └── requirements.txt         # Lightweight dashboard dependencies
│
├── data/                        # Raw, processed, and geospatial inputs
│   ├── raw/                     # Original NFHS-5 factsheet datasets (India.csv, India_Change.csv)
│   ├── processed/               # Cleaned factual dataset (706 districts) & metadata codebook
│   └── geo/                     # Census 2011 district boundary GeoJSON polygons
│
├── notebooks/                   # Interactive Jupyter research and exploration notebooks
│   ├── 01_EDA_Main_Malnutrition_Dataset.ipynb  # Primary NFHS-5 EDA, outliers, and PCA
│   ├── 02_Supplementary_India_Survey_Audit.ipynb # Supplementary India.csv audit
│   └── 03_Supplementary_Change_Analysis.ipynb  # Longitudinal NFHS-4 vs NFHS-5 change audit
│
├── scripts/                     # Reproducible automation and pipeline scripts
│   ├── process_factual_data.py         # Phase 1 extraction, cleaning, and codebook generator
│   ├── NIErnaya_Phase2_Master_Pipeline.py # Phase 2 end-to-end audit, EDA, PCA, and export pipeline
│   ├── generate_presentation.py       # Rebuilds the self-contained HTML slide deck
│   └── generate_pptx.py               # Rebuilds the 18-slide PowerPoint deck
│
├── submission/                  # Archived Phase 1 submission bundles & verification packages
└── README_SUBMISSION.txt        # Phase 2 submission manifest and methodological constraints
```

---

## ⚡ Quickstart Guide

### 1. Launch the Interactive Web Dashboard
```powershell
cd dashboard
streamlit run app.py
```
*The app automatically preloads the local 706-district dataset, metadata dictionary, and geospatial boundaries.*

### 2. View the Presentation Deck & Defense Guide
- **Master Presentation Guide & Encyclopedic Glossary (PDF)**: Open [`03_Final_Report/NIErnaya_Phase2_Presentation_Guide_and_Speaker_Notes.pdf`](file:///D:/DAV%20NIErnaya/03_Final_Report/NIErnaya_Phase2_Presentation_Guide_and_Speaker_Notes.pdf) for the comprehensive 39-page slide-by-slide script, timing, cues, defense playbook, and 47-term lexicon.
- **PowerPoint**: Open [`03_Final_Report/NIErnaya_Phase2_Presentation_Deck.pptx`](file:///D:/DAV%20NIErnaya/03_Final_Report/NIErnaya_Phase2_Presentation_Deck.pptx) in Microsoft PowerPoint, Google Slides, or Office 365.
- **Browser**: Open [`03_Final_Report/NIErnaya_Phase2_Presentation_Deck.html`](file:///D:/DAV%20NIErnaya/03_Final_Report/NIErnaya_Phase2_Presentation_Deck.html) in any browser (Press `F` for Fullscreen).
- **Speaker Notes**: Refer to [`03_Final_Report/NIErnaya_Phase2_Presentation_Speaker_Notes.md`](file:///D:/DAV%20NIErnaya/03_Final_Report/NIErnaya_Phase2_Presentation_Speaker_Notes.md) for defense delivery.

### 3. Re-run the Complete Analysis Pipeline
```powershell
python scripts/NIErnaya_Phase2_Master_Pipeline.py
```

### 4. Open Exploratory Jupyter Notebooks
```powershell
jupyter lab notebooks/
```

### 5. Deploy to Vercel (1-Click Static Web Portal & Presentation Suite)
This repository includes a pre-configured `vercel.json` and root `index.html`:
1. Push your changes to GitHub (already synced to `main`).
2. Go to [vercel.com](https://vercel.com) and log in with GitHub.
3. Click **Add New...** → **Project**, select `study-of-children-malnutrition-triads`.
4. Leave all build settings at their defaults (Framework Preset: **Other**; Root Directory: `./`).
5. Click **Deploy**!
*Your live Vercel URL will immediately serve the Executive Portal, the 18-slide interactive presentation deck (`/deck`), the 39-page master defense guide (`/guide`), technical report (`/report`), and the WebAssembly dashboard (`/app`).*

### 6. Deploy to Streamlit Community Cloud (Native Python Server)
For full native Python server hosting with live Plotly map rendering:
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
2. Click **New app**, select `Ramcharan77587/study-of-children-malnutrition-triads`, branch `main`.
3. Set **Main file path** to `dashboard/app.py`.
4. Click **Deploy**!

---

## 📊 Core Analytical Findings Summary

| Outcome / Indicator | District Mean (μ) | Median | Std. Dev. (σ) | Observed Range | Strongest Correlate (Pearson $r$) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Stunting (HAZ < -2)** | **33.51%** | 32.80% | 8.47% | 13.20% – 60.60% | Female Literacy ($r = -0.539$), Sanitation ($r = -0.503$) |
| **Wasting (WHZ < -2)** | **18.54%** | 18.10% | 6.48% | 4.50% – 48.00% | Socioeconomic Vulnerability ($r = +0.306$) |
| **Underweight (WAZ < -2)**| **29.50%** | 29.35% | 9.68% | 7.20% – 62.40% | Improved Sanitation ($r = -0.583$), Literacy ($r = -0.545$) |
| **Early Marriage (<18 yrs)**| **20.67%** | 18.35% | 12.79% | 0.00% – 80.90% | Strongest Risk Factor ($r = +0.481$ with Underweight) |
| **PCA Dimensionality** | **PC1: 39.31%** | **PC2: 23.39%** | **62.70%** Cumulative | First 2 components capture structural developmental axis |

---

## 🛡️ Data Governance & Integrity Guarantees
- **Zero Synthetic Values:** 100% empirical fact-sheet numbers from MoHFW / IIPS official publications.
- **Missingness Integrity:** 0% missing analytical percentage cells across all 706 factual districts.
- **Leakage Guards:** The composite `nutritional_burden_index` is strictly quarantined for descriptive profiling and never exposed to predictive models.
- **Outlier Preservation:** 92 IQR outlier flags audited and preserved to represent genuine public-health hotspots.

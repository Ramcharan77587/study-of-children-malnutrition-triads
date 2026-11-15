 NATIONAL INSIGHTS & EVIDENCE-BASED RESEARCH FOR
                 NUTRITIONAL ADVOCACY & YIELD ANALYTICS
PHASE 1: FACTUAL DISTRICT-LEVEL BASELINE & GEOSPATIAL GROUNDING

1. PROBLEM FORMULATION & SCOPE:
--------------------------------------------------------------------------------
Malnutrition remains a leading contributor to child morbidity and mortality in India.
Sustainable Development Goal 2 (Zero Hunger), Target 2.2, establishes an explicit mandate
to eliminate all forms of malnutrition by 2030, targeting:
  - Stunting (chronic height-for-age deficit: HAZ < -2 SD)
  - Wasting (acute weight-for-height deficit: WHZ < -2 SD)
  - Underweight (composite weight-for-age deficit: WAZ < -2 SD)

Project  constructs an empirical, district-level evidentiary foundation
grounded in official survey data from the Fifth National Family Health Survey (NFHS-5, 
2019-2021). The primary goal of Phase 1 is to assemble 100% authentic, factual
district-level indicators across Indian administrative units, bridging anthropometric
deficits with multi-sectoral drivers (maternal health, WASH infrastructure, female
literacy, early marriage, child anaemia, and healthcare access).

ZERO SYNTHETIC VALUES: All data points in this dataset originate directly from official
Ministry of Health and Family Welfare (MoHFW) / International Institute for Population
Sciences (IIPS) district factsheet tabulations. No generative or synthetic figures are used.


2. DATA PROVENANCE & OFFICIAL CITATIONS:
--------------------------------------------------------------------------------
Primary Survey Source:
  - Survey: National Family Health Survey 5 (NFHS-5), 2019-2021
  - Nodal Agency: International Institute for Population Sciences (IIPS), Mumbai
  - Sponsoring Ministry: Ministry of Health and Family Welfare (MoHFW), Government of India
  - Technical Assistance: ICF International, USA & USAID
  - Citation:
      International Institute for Population Sciences (IIPS) and ICF. 2021.
      National Family Health Survey (NFHS-5), India, 2019-21: District Fact Sheets.
      Mumbai: IIPS. Available at: http://rchiips.org/nfhs/factsheet_NFHS-5.shtml

Geospatial Boundary Provenance:
  - Format: GeoJSON District Boundary Polygons (Census of India 2011 Hierarchy)
  - Source: Datameet / Geohacker India Spatial Repository
  - Linkage: Aligned via Census 2011 State & District Identification Codes (`state_code`, `district_code`)


3. DATASET CHARACTERISTICS & VALIDATION METRICS:
--------------------------------------------------------------------------------
- Total Administrative Units Analyzed: 706 Factual Districts
- States / Union Territories Represented: 37 States and UTs
- Total Feature Columns: 14
  * 4 Spatial & Primary Key Identifiers (`district_name`, `state_name`, `district_code`, `state_code`)
  * 3 Anthropometric Dependent Variables (`stunting_pct`, `wasting_pct`, `underweight_pct`)
  * 7 Multi-Sectoral Predictors (`female_literacy_pct`, `improved_sanitation_pct`,
                                 `improved_water_pct`, `anc_4plus_pct`, `child_anemia_pct`,
                                 `early_marriage_pct`, `institutional_births_pct`)
- Completeness Rate: 100.00% complete for all 10 survey indicators across all 706 districts.
- Range Validation Checks: All percentage variables bounded strictly within realistic [0.0%, 100.0%] domain.
- Synthetic Check: Zero synthetic / random numbers; verified against published IIPS district fact sheets.


4. KEY DESCRIPTIVE STATISTICS (N = 706 Districts):
--------------------------------------------------------------------------------
Indicator                           Mean      Std Dev      Min       50% (Med)     Max
--------------------------------------------------------------------------------
Stunting (% HAZ < -2 SD)            33.51%      8.47%    13.20%     32.80%     60.60%
Wasting (% WHZ < -2 SD)             18.54%      6.48%     4.50%     18.10%     48.00%
Underweight (% WAZ < -2 SD)         29.50%      9.68%     7.20%     29.35%     62.40%
Improved Sanitation Facility (%)    71.95%     14.30%    29.20%     73.75%     99.90%
Improved Drinking Water (%)         93.78%      8.66%    41.20%     97.00%     100.00%
Female Literacy (15-49 yrs) (%)     73.09%     12.72%    37.10%     73.80%     99.70%
Child Anaemia (6-59 months) (%)     65.81%     12.07%    24.90%     67.70%     95.50%
--------------------------------------------------------------------------------


5. SUBMISSION ARCHIVE INVENTORY:
--------------------------------------------------------------------------------
The archive 'submission_phase1_factual_data.zip' contains:
  1. nfhs5_india_district_child_malnutrition_factual.csv
     - Fully cleaned, standardized, factual district dataset with primary keys,
       anthropometric triad (SDG 2.2), and multi-sectoral drivers.
  2. dataset_metadata_dictionary.csv
     - Variable-by-variable codebook detailing indicator descriptions, units,
       data types, official NFHS-5 indicator mapping, and UN SDG target alignment.
  3. india_district_boundary.geojson
     - Spatial polygons of Indian district boundaries compatible with Census 2011.
  4. README_NIErnaya_Phase1_Documentation.txt
     - Complete documentation of methodology, provenance citations, validation
       metrics, and descriptive analysis.

================================================================================

================================================================================

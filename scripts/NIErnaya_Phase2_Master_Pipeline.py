"""
NIErnaya 2026 – Phase 2 master analysis pipeline
------------------------------------------------
Run from Jupyter/VS Code after placing the three CSV files in the same folder,
or update the three paths in CONFIG below.

This pipeline:
1. Audits the main NFHS-5 district malnutrition dataset.
2. Performs core EDA, correlations, outlier screening, feature engineering and PCA.
3. Audits both supplementary NFHS datasets without unsafe district-level merging.
4. Creates an indicator inventory with a rule-based relevance suggestion for manual review.
5. Compares NFHS-4 and NFHS-5 only where both values are available and records validation checks.
6. Exports clean copies, reports, tables and plots into one output folder.
7. Uses NumPy for PCA; scikit-learn is not required.

IMPORTANT:
- It does NOT impute district identifiers.
- It does NOT automatically delete statistical outliers.
- It does NOT assume every zero means missing.
- It does NOT merge supplementary data into the main dataset.
- Rule-based indicator classifications are suggestions and must be reviewed.
- `Change` is audited against NFHS5-NFHS4 but is not overwritten.
"""

from pathlib import Path
import re
import warnings
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr, spearmanr

warnings.filterwarnings("ignore", category=FutureWarning)

# ----------------------------- CONFIG ---------------------------------
ROOT_DIR = Path(__file__).resolve().parent
if ROOT_DIR.name == "scripts":
    ROOT_DIR = ROOT_DIR.parent
BASE_DIR = ROOT_DIR

def find_file(candidates):
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]

MAIN_FILE = find_file([
    BASE_DIR / "data" / "processed" / "nfhs5_india_district_child_malnutrition_factual.csv",
    BASE_DIR / "nfhs5_india_district_child_malnutrition_factual.csv",
    BASE_DIR / "submission" / "submission_phase1_factual_data" / "nfhs5_india_district_child_malnutrition_factual.csv"
])

INDIA_FILE = find_file([
    BASE_DIR / "data" / "raw" / "India.csv",
    BASE_DIR / "India.csv",
    BASE_DIR / "submission" / "submission_phase1_factual_data" / "India.csv"
])

CHANGE_FILE = find_file([
    BASE_DIR / "data" / "raw" / "India_Change.csv",
    BASE_DIR / "India_Change.csv",
    BASE_DIR / "submission" / "submission_phase1_factual_data" / "India_Change.csv"
])

OUT_DIR = BASE_DIR / "02_Analysis_Outputs"

MAIN_OUTCOMES = ["stunting_pct", "wasting_pct", "underweight_pct"]
MAIN_PREDICTORS = [
    "female_literacy_pct", "improved_sanitation_pct", "improved_water_pct",
    "anc_4plus_pct", "child_anemia_pct", "early_marriage_pct",
    "institutional_births_pct"
]
PERCENT_SUFFIX = "_pct"
RANDOM_STATE = 42

# -------------------------- GENERAL HELPERS ---------------------------
def make_dirs():
    for folder in ["01_Audit", "02_Main_EDA", "03_Supplementary_India",
                   "04_Supplementary_Change", "05_Feature_Engineering_PCA",
                   "06_Final_Data", "07_Indicator_Inventory"]:
        (OUT_DIR / folder).mkdir(parents=True, exist_ok=True)

def save_csv(df, relative_path):
    path = OUT_DIR / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path

def save_plot(path):
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()

def normalise_text(series):
    return (series.astype("string").str.strip()
            .str.replace(r"\s+", " ", regex=True))

def safe_numeric(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def audit_frame(df, name):
    result = {
        "dataset": name,
        "rows": len(df),
        "columns": len(df.columns),
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "total_missing_cells": int(df.isna().sum().sum()),
    }
    missing = df.isna().sum().rename("missing_count").to_frame()
    missing["missing_pct"] = (missing["missing_count"] / max(len(df), 1) * 100).round(2)
    missing.to_csv(OUT_DIR / "01_Audit" / f"{name}_missingness.csv")
    return result

def iqr_outlier_summary(df, columns):
    rows = []
    for col in columns:
        x = pd.to_numeric(df[col], errors="coerce").dropna()
        if x.empty:
            continue
        q1, q3 = x.quantile([.25, .75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        flagged = ((x < low) | (x > high))
        rows.append({
            "variable": col, "Q1": q1, "Q3": q3, "IQR": iqr,
            "lower_fence": low, "upper_fence": high,
            "outlier_flags": int(flagged.sum()),
            "outlier_flag_pct": round(float(flagged.mean() * 100), 2),
            "min": x.min(), "max": x.max()
        })
    return pd.DataFrame(rows)

def fdr_bh(p_values):
    """Benjamini-Hochberg adjusted p-values."""
    p = np.asarray(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    adjusted = ranked * n / np.arange(1, n + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.clip(adjusted, 0, 1)
    return out

# ----------------------- MAIN DATASET PIPELINE ------------------------
def run_main_dataset():
    print("\n[1/3] Processing main NFHS-5 dataset...")
    df = pd.read_csv(MAIN_FILE)
    audit = audit_frame(df, "main_nfhs5")
    df["state_name"] = normalise_text(df["state_name"])
    df["district_name"] = normalise_text(df["district_name"])

    numeric_cols = MAIN_OUTCOMES + MAIN_PREDICTORS
    df = safe_numeric(df, numeric_cols)

    # Data-quality checks
    range_rows = []
    for c in numeric_cols:
        range_rows.append({
            "variable": c,
            "missing": int(df[c].isna().sum()),
            "min": df[c].min(),
            "max": df[c].max(),
            "outside_0_100": int(((df[c] < 0) | (df[c] > 100)).sum())
        })
    save_csv(pd.DataFrame(range_rows), "01_Audit/main_numeric_range_checks.csv")

    key_dupes = int(df.duplicated(["state_name", "district_name"]).sum())
    audit["duplicate_state_district_keys"] = key_dupes
    audit["missing_district_code"] = int(df["district_code"].isna().sum())
    save_csv(pd.DataFrame([audit]), "01_Audit/master_audit_summary.csv")

    # Descriptive statistics
    desc = df[numeric_cols].describe().T
    desc["skewness"] = df[numeric_cols].skew()
    desc["kurtosis"] = df[numeric_cols].kurtosis()
    save_csv(desc.reset_index(names="variable"), "02_Main_EDA/descriptive_statistics.csv")

    # Distributions and boxplots
    for c in numeric_cols:
        plt.figure(figsize=(7, 4))
        plt.hist(df[c].dropna(), bins=25, edgecolor="black")
        plt.title(f"Distribution: {c}")
        plt.xlabel(c); plt.ylabel("District count")
        save_plot(OUT_DIR / "02_Main_EDA" / f"hist_{c}.png")

        plt.figure(figsize=(7, 3))
        plt.boxplot(df[c].dropna(), vert=False)
        plt.title(f"Boxplot: {c}")
        plt.xlabel(c)
        save_plot(OUT_DIR / "02_Main_EDA" / f"box_{c}.png")

    # Outlier screening only; no automatic deletion
    outliers = iqr_outlier_summary(df, numeric_cols)
    save_csv(outliers, "01_Audit/main_iqr_outlier_screening.csv")

    # Correlation matrices and predictor-outcome tests
    pearson = df[numeric_cols].corr(method="pearson")
    spearman = df[numeric_cols].corr(method="spearman")
    pearson.to_csv(OUT_DIR / "02_Main_EDA" / "pearson_correlation_matrix.csv")
    spearman.to_csv(OUT_DIR / "02_Main_EDA" / "spearman_correlation_matrix.csv")

    test_rows = []
    for predictor in MAIN_PREDICTORS:
        for outcome in MAIN_OUTCOMES:
            pair = df[[predictor, outcome]].dropna()
            if len(pair) >= 3 and pair[predictor].nunique() > 1 and pair[outcome].nunique() > 1:
                pr, pp = pearsonr(pair[predictor], pair[outcome])
                sr, sp = spearmanr(pair[predictor], pair[outcome])
            else:
                pr = pp = sr = sp = np.nan
            test_rows.append({
                "predictor": predictor, "outcome": outcome, "n": len(pair),
                "pearson_r": pr, "pearson_p": pp,
                "spearman_rho": sr, "spearman_p": sp
            })
    tests = pd.DataFrame(test_rows)
    tests["pearson_p_BH"] = fdr_bh(tests["pearson_p"].fillna(1))
    tests["spearman_p_BH"] = fdr_bh(tests["spearman_p"].fillna(1))
    save_csv(tests, "02_Main_EDA/predictor_outcome_correlations.csv")

    # Correlation heatmap using matplotlib only
    fig, ax = plt.subplots(figsize=(12, 9))
    im = ax.imshow(pearson.values, vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(numeric_cols)), numeric_cols, rotation=90)
    ax.set_yticks(range(len(numeric_cols)), numeric_cols)
    ax.set_title("Main dataset Pearson correlation matrix")
    fig.colorbar(im, ax=ax, label="Pearson correlation")
    save_plot(OUT_DIR / "02_Main_EDA" / "correlation_heatmap.png")

    # Scatter plots for all predictor-outcome pairs
    for predictor in MAIN_PREDICTORS:
        for outcome in MAIN_OUTCOMES:
            plt.figure(figsize=(6, 4))
            plt.scatter(df[predictor], df[outcome], alpha=.65)
            plt.xlabel(predictor); plt.ylabel(outcome)
            plt.title(f"{predictor} vs {outcome}")
            save_plot(OUT_DIR / "02_Main_EDA" / f"scatter_{predictor}_vs_{outcome}.png")

    # State-level district averages; explicitly unweighted
    state_means = df.groupby("state_name")[MAIN_OUTCOMES].mean().reset_index()
    state_counts = df.groupby("state_name").size().rename("district_count").reset_index()
    state_means = state_means.merge(state_counts, on="state_name")
    state_means["aggregation_note"] = "Unweighted mean of district percentages; not population-weighted prevalence"
    save_csv(state_means, "02_Main_EDA/state_unweighted_district_means.csv")

    for outcome in MAIN_OUTCOMES:
        ranked = state_means.sort_values(outcome, ascending=False)
        plt.figure(figsize=(10, max(6, len(ranked) * .22)))
        plt.barh(ranked["state_name"], ranked[outcome])
        plt.gca().invert_yaxis()
        plt.xlabel("Unweighted mean of district percentages")
        plt.title(f"State-wise district-average {outcome}")
        save_plot(OUT_DIR / "02_Main_EDA" / f"state_rank_{outcome}.png")

    # Feature engineering: preserve originals and add documented exploratory features
    engineered = df.copy()
    engineered["sanitation_water_gap"] = engineered["improved_water_pct"] - engineered["improved_sanitation_pct"]
    engineered["maternal_care_gap"] = engineered["institutional_births_pct"] - engineered["anc_4plus_pct"]
    lit_z = (engineered["female_literacy_pct"] - engineered["female_literacy_pct"].mean()) / engineered["female_literacy_pct"].std(ddof=0)
    marriage_z = (engineered["early_marriage_pct"] - engineered["early_marriage_pct"].mean()) / engineered["early_marriage_pct"].std(ddof=0)
    engineered["socioeconomic_vulnerability_index"] = (marriage_z - lit_z) / 2
    engineered["nutritional_burden_index_descriptive_only"] = engineered[MAIN_OUTCOMES].mean(axis=1)

    engineered_corr = engineered[
        ["sanitation_water_gap", "maternal_care_gap", "socioeconomic_vulnerability_index"] + MAIN_OUTCOMES
    ].corr()
    engineered_corr.to_csv(OUT_DIR / "05_Feature_Engineering_PCA/engineered_feature_correlations.csv")
    save_csv(engineered, "06_Final_Data/main_nfhs5_engineered.csv")

    # PCA on the seven predictors using NumPy only (no scikit-learn DLLs required).
    # Complete-case PCA: rows with missing predictor values are excluded only from PCA,
    # not from the saved main dataset. Standardisation uses population SD (ddof=0).
    pca_data = df[MAIN_PREDICTORS].copy()
    pca_complete = pca_data.dropna()
    if len(pca_complete) >= 3:
        X = pca_complete.to_numpy(dtype=float)
        means = X.mean(axis=0)
        stds = X.std(axis=0, ddof=0)
        if np.any(stds == 0):
            raise ValueError("PCA cannot run: at least one predictor has zero variance.")
        X_scaled = (X - means) / stds

        # Eigen-decomposition of the sample covariance matrix.
        covariance = np.cov(X_scaled, rowvar=False, ddof=1)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance)
        order = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[order]
        components = eigenvectors[:, order]
        explained_ratio = eigenvalues / eigenvalues.sum()
        scores = X_scaled @ components

        pca_table = pd.DataFrame({
            "component": [f"PC{i+1}" for i in range(len(MAIN_PREDICTORS))],
            "eigenvalue": eigenvalues,
            "explained_variance_ratio": explained_ratio,
            "cumulative_explained_variance": np.cumsum(explained_ratio)
        })
        loadings = pd.DataFrame(
            components,
            index=MAIN_PREDICTORS,
            columns=[f"PC{i+1}" for i in range(len(MAIN_PREDICTORS))]
        )
        save_csv(pca_table, "05_Feature_Engineering_PCA/pca_explained_variance.csv")
        loadings.to_csv(OUT_DIR / "05_Feature_Engineering_PCA" / "pca_loadings.csv")
        scores_df = pd.DataFrame(scores, columns=[f"PC{i+1}" for i in range(scores.shape[1])])
        scores_df.to_csv(OUT_DIR / "05_Feature_Engineering_PCA" / "pca_scores_complete_cases.csv", index=False)
        pd.DataFrame({"predictor": MAIN_PREDICTORS, "mean_used_for_standardisation": means,
                      "population_sd_used_for_standardisation": stds}).to_csv(
            OUT_DIR / "05_Feature_Engineering_PCA" / "pca_standardisation_parameters.csv", index=False)

        plt.figure(figsize=(7, 4))
        plt.plot(range(1, len(pca_table)+1), pca_table["explained_variance_ratio"]*100, marker="o")
        plt.xticks(range(1, len(pca_table)+1))
        plt.xlabel("Principal component"); plt.ylabel("Explained variance (%)")
        plt.title("PCA scree plot")
        save_plot(OUT_DIR / "05_Feature_Engineering_PCA" / "pca_scree_plot.png")

    # Clean copy: only safe text normalisation and numeric parsing; no imputation/deletion
    save_csv(df, "06_Final_Data/main_nfhs5_cleaned_conservative.csv")
    print("Main dataset completed.")
    return df

# ---------------- SUPPLEMENTARY INDICATOR CLASSIFICATION -------------
def classify_indicator(indicator):
    """Rule-based suggestion only. Review every indicator before final use."""
    s = re.sub(r"\s+", " ", str(indicator).lower()).strip()

    direct_terms = [
        "stunted", "wasted", "underweight", "severely wasted", "overweight",
        "exclusively breastfed", "breastfed within one hour",
        "solid or semisolid food", "adequate diet", "children age 6-59 months who are anaemic",
        "children under age 5"
    ]
    if any(term in s for term in direct_terms):
        return "A", "Direct child nutrition / feeding / nutritional outcome", "Core candidate"

    strong_terms = [
        "antenatal", "antenatal care", "iron folic acid", "postnatal",
        "vaccin", "immuniz", "immunis", "vitamin a", "diarrhoea",
        "diarrhea", "acute respiratory", "ors", "zinc", "institutional births",
        "skilled health personnel", "births delivered", "improved sanitation",
        "improved drinking", "clean fuel", "iodized salt", "health insurance",
        "women who are literate", "10 or more years of schooling",
        "married before age 18", "already mothers or pregnant",
        "women whose bmi is below normal", "low bmi"
    ]
    if any(term in s for term in strong_terms):
        return "B", "Maternal / child health / household / socioeconomic context", "Supporting candidate"

    secondary_terms = [
        "family planning", "unmet need", "caesarean", "cesarean",
        "out-of-pocket", "preprimary", "electricity", "population below age 15",
        "tobacco", "alcohol", "overweight", "obesity"
    ]
    if any(term in s for term in secondary_terms):
        return "C", "Indirect demographic / health / socioeconomic context", "Secondary or exclude from core"

    return "C", "Indirect or unclear relevance; inspect source definition", "Manual review required"

def prepare_supplementary(df, dataset_name, district_col):
    df = df.copy()
    # Keep raw labels in original columns; add normalised helper columns.
    for c in ["State", district_col, "Category", "Indicator"]:
        if c in df.columns:
            df[c + "_clean"] = normalise_text(df[c])

    # Parse survey and change values numerically; preserve original data separately in memory.
    for c in ["NFHS 5", "NFHS 4", "Change"]:
        if c in df.columns:
            df[c + "_numeric"] = pd.to_numeric(df[c], errors="coerce")

    # Exact duplicate count and key collision audit (do not auto-drop key collisions).
    exact_dupes = int(df.duplicated().sum())
    key_cols = ["State_clean", district_col + "_clean", "Indicator_clean"]
    key_dupes = int(df.duplicated(key_cols, keep=False).sum()) if all(c in df.columns for c in key_cols) else None

    summary = {
        "dataset": dataset_name, "rows": len(df), "columns": len(df.columns),
        "exact_duplicate_rows": exact_dupes,
        "duplicate_state_district_indicator_rows": key_dupes,
        "missing_state": int(df["State"].isna().sum()),
        "missing_district_name": int(df[district_col].isna().sum()),
        "missing_district_code": int(df["DT_CEN_CD"].isna().sum()),
        "unique_indicators": int(df["Indicator_clean"].nunique()),
        "unique_categories": int(df["Category_clean"].nunique())
    }
    save_csv(pd.DataFrame([summary]), f"01_Audit/{dataset_name}_audit_summary.csv")

    # Normalise whitespace in labels; do not alter district codes or infer missing codes.
    for c in ["State", district_col, "Category", "Indicator"]:
        if c in df.columns:
            df[c] = normalise_text(df[c])

    # Duplicate report. Preserve records in cleaned output pending source review.
    dupes = df[df.duplicated(keep=False)].sort_values(["State", district_col, "Indicator"])
    save_csv(dupes, f"01_Audit/{dataset_name}_exact_duplicates_for_review.csv")

    # Range profile: do not apply 0-100 rule globally because some indicators use other units.
    numeric_cols = [c for c in ["NFHS 5_numeric", "NFHS 4_numeric", "Change_numeric"] if c in df.columns]
    range_profile = df.groupby(["Category", "Indicator"], dropna=False)[numeric_cols].agg(["count", "min", "max", "mean"])
    range_profile.to_csv(OUT_DIR / "01_Audit" / f"{dataset_name}_indicator_numeric_profile.csv")

    # Availability and zero counts by indicator
    rows = []
    for indicator, grp in df.groupby("Indicator", dropna=False):
        row = {"Indicator": indicator, "rows": len(grp)}
        for c in ["NFHS 4_numeric", "NFHS 5_numeric", "Change_numeric"]:
            if c in grp.columns:
                x = grp[c]
                row[f"{c}_nonmissing"] = int(x.notna().sum())
                row[f"{c}_zero_count"] = int((x == 0).sum())
                row[f"{c}_min"] = x.min()
                row[f"{c}_max"] = x.max()
        row["Category"] = grp["Category"].dropna().iloc[0] if grp["Category"].notna().any() else None
        rows.append(row)
    availability = pd.DataFrame(rows)
    save_csv(availability, f"01_Audit/{dataset_name}_indicator_availability_and_zeros.csv")

    # Rule-based relevance inventory; manual review is required.
    inventory_rows = []
    for (category, indicator), grp in df.groupby(["Category", "Indicator"], dropna=False):
        priority, relevance, decision = classify_indicator(indicator)
        inventory_rows.append({
            "Category": category, "Indicator": indicator, "Priority_suggestion": priority,
            "Relevance_suggestion": relevance, "Suggested_decision": decision,
            "Rows": len(grp),
            "NFHS4_nonmissing": int(grp["NFHS 4_numeric"].notna().sum()) if "NFHS 4_numeric" in grp else np.nan,
            "NFHS5_nonmissing": int(grp["NFHS 5_numeric"].notna().sum()) if "NFHS 5_numeric" in grp else np.nan,
        })
    inventory = pd.DataFrame(inventory_rows)
    save_csv(inventory, f"07_Indicator_Inventory/{dataset_name}_indicator_classification_REVIEW_REQUIRED.csv")

    # Survey comparison by indicator: district-row means, explicitly unweighted.
    if {"NFHS 4_numeric", "NFHS 5_numeric"}.issubset(df.columns):
        compare_rows = []
        for indicator, grp in df.groupby("Indicator", dropna=False):
            a = grp["NFHS 4_numeric"]
            b = grp["NFHS 5_numeric"]
            paired = grp[["NFHS 4_numeric", "NFHS 5_numeric"]].dropna()
            compare_rows.append({
                "Indicator": indicator,
                "NFHS4_mean_available_rows": a.mean(),
                "NFHS5_mean_available_rows": b.mean(),
                "paired_rows": len(paired),
                "paired_NFHS4_mean": paired["NFHS 4_numeric"].mean() if len(paired) else np.nan,
                "paired_NFHS5_mean": paired["NFHS 5_numeric"].mean() if len(paired) else np.nan,
                "paired_mean_difference_5_minus_4": (
                    paired["NFHS 5_numeric"] - paired["NFHS 4_numeric"]
                ).mean() if len(paired) else np.nan,
                "note": "Unweighted row-level summary; check indicator definitions, district coverage and units."
            })
        comp = pd.DataFrame(compare_rows)
        save_csv(comp, f"{'03_Supplementary_India' if dataset_name=='india' else '04_Supplementary_Change'}/{dataset_name}_indicator_survey_comparison.csv")

    # Clean conservative output: trim label whitespace, parse numeric values, preserve all rows.
    save_csv(df, f"06_Final_Data/{dataset_name}_cleaned_conservative.csv")
    return df

def run_change_audit(change_df):
    if not {"NFHS 4_numeric", "NFHS 5_numeric", "Change_numeric"}.issubset(change_df.columns):
        return
    valid = change_df[["NFHS 4_numeric", "NFHS 5_numeric", "Change_numeric"]].dropna()
    valid = valid.copy()
    valid["computed_difference"] = valid["NFHS 5_numeric"] - valid["NFHS 4_numeric"]
    valid["absolute_error"] = (valid["Change_numeric"] - valid["computed_difference"]).abs()
    audit = pd.DataFrame([{
        "rows_with_all_three_values": len(valid),
        "matches_difference_within_0_11": int((valid["absolute_error"] <= 0.11).sum()),
        "match_rate_pct_within_0_11": round(float((valid["absolute_error"] <= 0.11).mean()*100), 2) if len(valid) else np.nan,
        "median_absolute_difference": valid["absolute_error"].median() if len(valid) else np.nan,
        "note": "Audit only. Change may use indicator-specific formulas, denominator changes or source conventions."
    }])
    save_csv(audit, "01_Audit/change_column_formula_audit.csv")
    save_csv(valid.sort_values("absolute_error", ascending=False).head(100),
             "01_Audit/change_column_largest_formula_mismatches.csv")

# ------------------------------- RUN ----------------------------------
def main():
    make_dirs()
    for p in [MAIN_FILE, INDIA_FILE, CHANGE_FILE]:
        if not p.exists():
            raise FileNotFoundError(
                f"Cannot find {p}. Put the CSV in {BASE_DIR.resolve()} or update CONFIG."
            )

    main_df = run_main_dataset()

    print("\n[2/3] Processing supplementary India.csv...")
    india = pd.read_csv(INDIA_FILE, dtype={"DT_CEN_CD": "string"}, low_memory=False)
    india = prepare_supplementary(india, "india", "District")

    print("\n[3/3] Processing supplementary India_Change.csv...")
    change = pd.read_csv(CHANGE_FILE, dtype={"DT_CEN_CD": "string"}, low_memory=False)
    change = prepare_supplementary(change, "india_change", "District Name")
    run_change_audit(change)

    # One compact run manifest
    manifest = {
        "main_dataset_rows": len(main_df),
        "india_rows": len(india),
        "india_change_rows": len(change),
        "outputs_directory": str(OUT_DIR.resolve()),
        "important_cautions": [
            "No automatic imputation of district codes.",
            "No automatic outlier removal.",
            "No automatic treatment of zero as missing.",
            "No district-level merging across datasets.",
            "Indicator classification is rule-based and requires manual review.",
            "State averages are unweighted unless population weights are supplied."
        ]
    }
    with open(OUT_DIR / "RUN_MANIFEST.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\nPIPELINE FINISHED.")
    print(f"All outputs saved in: {OUT_DIR.resolve()}")
    print("Review the files ending in REVIEW_REQUIRED and all audit reports before using the cleaned data.")

if __name__ == "__main__":
    main()

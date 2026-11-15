# NIErnaya 2026 — NFHS-5 Child Nutrition Intelligence Dashboard
# Run: streamlit run app.py
# Upload the primary NFHS-5 CSV and (for maps) the validated district GeoJSON in the sidebar.

import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore", category=FutureWarning)

st.set_page_config(
    page_title="NIErnaya | Child Nutrition Intelligence",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Theme -----------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #08111f; color: #e8eef7; }
[data-testid="stSidebar"] { background: #0d1929; border-right: 1px solid #23344b; }
[data-testid="stHeader"] { background: rgba(8,17,31,0.9); }
h1,h2,h3 { font-family: 'Manrope', sans-serif !important; color: #f4f7fb; }
p, label, span { color: #d7e0ed; }
div[data-testid="stMetric"] {
  background: linear-gradient(145deg,#12243a,#0d1b2d);
  border: 1px solid #263d58; padding: 16px; border-radius: 14px;
}
div[data-testid="stMetricLabel"] { color: #9fb2c9; }
div[data-testid="stMetricValue"] { color: #f5f8fc; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; }
hr { border-color: #263d58; }
.small-muted { color:#9fb2c9; font-size:0.88rem; }
.insight {
  background:#10243a; border:1px solid #29435f; border-left:4px solid #46b3a4;
  padding:14px 16px; border-radius:10px; margin:8px 0 14px 0;
}
.warning {
  background:#302719; border:1px solid #70552b; border-left:4px solid #e4ad52;
  padding:12px 15px; border-radius:10px; margin:8px 0;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------- Constants -------------------------------------
OUTCOMES = ["stunting_pct", "wasting_pct", "underweight_pct"]
PREDICTORS = [
    "female_literacy_pct", "improved_sanitation_pct", "improved_water_pct",
    "anc_4plus_pct", "child_anemia_pct", "early_marriage_pct",
    "institutional_births_pct",
]
INDICATORS = OUTCOMES + PREDICTORS
LABELS = {
    "stunting_pct": "Stunting",
    "wasting_pct": "Wasting",
    "underweight_pct": "Underweight",
    "female_literacy_pct": "Female literacy",
    "improved_sanitation_pct": "Improved sanitation",
    "improved_water_pct": "Improved drinking water",
    "anc_4plus_pct": "4+ ANC visits",
    "child_anemia_pct": "Child anaemia",
    "early_marriage_pct": "Early marriage",
    "institutional_births_pct": "Institutional births",
}
DESCRIPTIONS = {
    "stunting_pct": "Children under 5 who are stunted (low height-for-age).",
    "wasting_pct": "Children under 5 who are wasted (low weight-for-height).",
    "underweight_pct": "Children under 5 who are underweight (low weight-for-age).",
    "female_literacy_pct": "Female literacy indicator in the district dataset.",
    "improved_sanitation_pct": "Households/population with improved sanitation, as defined by the source.",
    "improved_water_pct": "Access to improved drinking water, as defined by the source.",
    "anc_4plus_pct": "Mothers receiving at least four antenatal care visits.",
    "child_anemia_pct": "Children with anaemia.",
    "early_marriage_pct": "Early marriage indicator in the district dataset.",
    "institutional_births_pct": "Births delivered in a health facility.",
}
EXPECTED_COLS = ["district_name", "state_name", "district_code", "state_code"] + INDICATORS

# ----------------------------- Helpers ---------------------------------------
def norm(value):
    if pd.isna(value):
        return ""
    s = str(value).strip().lower()
    s = re.sub(r"\b(district|dist)\b", "", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s

def safe_numeric(df):
    out = df.copy()
    for c in INDICATORS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out

def read_csv_upload(upload):
    if upload is None:
        return None
    try:
        upload.seek(0)
        return pd.read_csv(upload)
    except UnicodeDecodeError:
        upload.seek(0)
        return pd.read_csv(upload, encoding="latin-1")

def get_geojson(upload):
    if upload is None:
        return None
    try:
        upload.seek(0)
        obj = json.load(upload)
        if obj.get("type") == "FeatureCollection":
            return obj
    except Exception as e:
        st.error(f"Could not read GeoJSON: {e}")
    return None

def add_composite_keys(df, district_col, state_col):
    x = df.copy()
    x["_join_key"] = (
        x[state_col].map(norm).astype(str) + "|" +
        x[district_col].map(norm).astype(str)
    )
    x.loc[(x[district_col].isna()) | (x[state_col].isna()), "_join_key"] = ""
    return x

def norm_code(sc, dc):
    try:
        if pd.isna(sc) or pd.isna(dc) or sc == "" or dc == "":
            return ""
        return f"{int(float(sc))}|{int(float(dc))}"
    except (ValueError, TypeError):
        return ""

def pick_default_prop(props, preferred):
    for p in preferred:
        if p in props:
            return props.index(p)
    return 0

def make_geo_frame(geo, district_prop, state_prop):
    feats = geo.get("features", [])
    rows = []
    for i, f in enumerate(feats):
        props = f.get("properties", {}) or {}
        sc = props.get("ST_CEN_CD") or props.get("state_code")
        dc = props.get("DT_CEN_CD") or props.get("district_code")
        rows.append({
            "_feature_index": i,
            "_district": props.get(district_prop),
            "_state": props.get(state_prop),
            "_join_key": norm(props.get(state_prop)) + "|" + norm(props.get(district_prop)),
            "_code_key": norm_code(sc, dc),
            "_geometry": f.get("geometry"),
        })
    return pd.DataFrame(rows)

def fmt_pct(x):
    return "—" if pd.isna(x) else f"{x:.1f}%"

def metric_summary(df, col):
    s = pd.to_numeric(df[col], errors="coerce").dropna()
    if len(s) == 0:
        return None
    return {
        "n": int(s.size), "mean": float(s.mean()), "median": float(s.median()),
        "min": float(s.min()), "max": float(s.max()), "std": float(s.std()),
    }

def chart_theme(fig, height=None):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#dce6f2"),
        margin=dict(l=10, r=10, t=55, b=10),
        legend_title_text="", title_font=dict(size=17),
    )
    if height:
        fig.update_layout(height=height)
    return fig

def make_choropleth(geo, geo_district, geo_state, data, indicator):
    geo_df = make_geo_frame(geo, geo_district, geo_state)
    data2 = add_composite_keys(data, "district_name", "state_name")
    
    # Generate Census codes key for robust fallback matching
    if "state_code" in data2.columns and "district_code" in data2.columns:
        data2["_code_key"] = [
            norm_code(s, d) for s, d in zip(data2["state_code"], data2["district_code"])
        ]
    else:
        data2["_code_key"] = ""
        
    valid_name_data = data2[data2["_join_key"] != ""]
    dup_data = int(valid_name_data["_join_key"].duplicated(keep=False).sum())
    dup_geo = int(geo_df[geo_df["_join_key"] != ""]["_join_key"].duplicated(keep=False).sum())
    
    # 1. Primary match: normalized state + district name
    name_map = dict(zip(valid_name_data["_join_key"], valid_name_data[indicator]))
    
    # 2. Secondary match fallback: Census state_code | district_code
    valid_code_data = data2[(data2["_code_key"] != "") & (data2[indicator].notna())]
    code_map = dict(zip(valid_code_data["_code_key"], valid_code_data[indicator]))
    
    merged = geo_df.copy()
    vals = []
    match_sources = []
    for _, r in merged.iterrows():
        v = name_map.get(r["_join_key"])
        if v is not None and not pd.isna(v):
            vals.append(v)
            match_sources.append("name")
        elif r["_code_key"] and r["_code_key"] in code_map:
            v = code_map[r["_code_key"]]
            vals.append(v)
            match_sources.append("census_code")
        else:
            vals.append(np.nan)
            match_sources.append("unmatched")
            
    merged[indicator] = vals
    merged["_match_source"] = match_sources
    matched = int(merged[indicator].notna().sum())
    
    geo_features = []
    for _, row in merged.iterrows():
        geom = row["_geometry"]
        if not geom:
            continue
        props = {
            "_join_key": row["_join_key"],
            "district": str(row["_district"]),
            "state": str(row["_state"]),
            "value": None if pd.isna(row[indicator]) else float(row[indicator]),
        }
        geo_features.append({"type": "Feature", "geometry": geom, "properties": props})
    geo_out = {"type": "FeatureCollection", "features": geo_features}
    return geo_out, merged, dup_data, dup_geo, matched

def show_map(geo, data, indicator, geo_district, geo_state, key, basemap_style="open-street-map"):
    geo_out, merged, dup_data, dup_geo, matched = make_choropleth(
        geo, geo_district, geo_state, data, indicator
    )
    total = len(merged)
    name_matches = int((merged["_match_source"] == "name").sum())
    code_matches = int((merged["_match_source"] == "census_code").sum())
    pct_matched = (matched / total * 100) if total else 0
    
    st.caption(
        f"Geographic match: **{matched:,}/{total:,} ({pct_matched:.1f}%)** GeoJSON features mapped "
        f"({name_matches:,} direct name, {code_matches:,} census code fallback) · "
        f"CSV duplicates: {dup_data:,} · GeoJSON duplicates: {dup_geo:,}"
    )
    if dup_data or dup_geo:
        st.warning("Duplicate composite keys detected. Review the join before interpreting this map.")
    if matched == 0:
        st.error("No districts matched. Check the selected GeoJSON district/state properties and spelling conventions.")
        return
    if matched < total * 0.7:
        st.warning("Less than 70% of GeoJSON features matched. Treat this map as provisional.")
        
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geo_out, locations=merged["_join_key"], z=merged[indicator],
        featureidkey="properties._join_key", colorscale="YlOrRd",
        marker_opacity=0.82, marker_line_width=0.35, marker_line_color="#1e293b",
        colorbar=dict(title=LABELS.get(indicator, indicator) + " (%)"),
        customdata=np.stack([
            merged["_district"].fillna("").astype(str),
            merged["_state"].fillna("").astype(str)
        ], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>" +
                      LABELS.get(indicator, indicator) + ": %{z:.1f}%<extra></extra>",
    ))
    
    # Basemap style options: 'open-street-map' or 'white-bg' (100% free, 0 API key required)
    fig.update_layout(
        mapbox_style=basemap_style,
        mapbox_zoom=3.2, mapbox_center={"lat": 22.5, "lon": 82.0},
        height=580, margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#dce6f2"),
    )
    st.plotly_chart(fig, use_container_width=True, key=key)
    unmatched = merged[merged[indicator].isna()][["_district", "_state"]]
    if len(unmatched) > 0:
        with st.expander(f"View unmatched GeoJSON features ({len(unmatched)})"):
            st.dataframe(unmatched.rename(columns={"_district":"GeoJSON district","_state":"GeoJSON state"}),
                         use_container_width=True, hide_index=True)

def data_quality(df):
    report = []
    for c in EXPECTED_COLS:
        if c in df.columns:
            report.append({"Column": c, "Missing": int(df[c].isna().sum()),
                           "Missing %": round(df[c].isna().mean()*100, 2),
                           "Unique values": int(df[c].nunique(dropna=True))})
    return pd.DataFrame(report)

def state_means(df, indicators):
    return df.groupby("state_name", dropna=False)[indicators].mean(numeric_only=True).reset_index()

def top_bottom(df, indicator, n=10):
    cols = ["district_name", "state_name", indicator]
    x = df[cols].dropna(subset=[indicator]).copy()
    return x.nlargest(n, indicator), x.nsmallest(n, indicator)

# ----------------------------- Sidebar ---------------------------------------
st.sidebar.markdown("## NIErnaya 2026")
st.sidebar.caption("NFHS-5 District Child Nutrition Intelligence")
st.sidebar.markdown("---")
st.sidebar.markdown("### Active Data Corpus")

# ----------------------------- Load data -------------------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

def resolve_local(rel_paths):
    for r in rel_paths:
        p1 = PROJECT_ROOT / r
        if p1.exists():
            return p1
        p2 = APP_DIR / r
        if p2.exists():
            return p2
        p3 = Path(r)
        if p3.exists():
            return p3
    return None

# 1. Primary Dataset (Default: 706 factual districts)
def_primary = resolve_local([
    "data/processed/nfhs5_india_district_child_malnutrition_factual.csv",
    "data/processed/main_nfhs5_cleaned_conservative.csv",
    "02_Analysis_Outputs/06_Final_Data/main_nfhs5_cleaned_conservative.csv"
])
if def_primary and def_primary.exists():
    raw_df = pd.read_csv(def_primary)
    st.sidebar.success("✔ 706 Districts Microdata (NFHS-5)")
else:
    st.title("NIErnaya | National Child Nutrition Intelligence")
    st.markdown("### A district-level view of child nutrition in India")
    st.error("Default primary dataset (`nfhs5_india_district_child_malnutrition_factual.csv`) not found.")
    st.stop()

df = safe_numeric(raw_df)
missing_cols = [c for c in EXPECTED_COLS if c not in df.columns]
if missing_cols:
    st.error("Your dataset is missing expected columns: " + ", ".join(missing_cols))
    st.write("Columns found:", list(df.columns))
    st.stop()

available_indicators = [c for c in INDICATORS if c in df.columns]

# 2. Boundary GeoJSON (Default: 641 Census district polygons)
def_geo = resolve_local(["data/geo/Districts.geojson", "data/geo/india_district_boundary.geojson"])
geo = None
if def_geo and def_geo.exists():
    try:
        with open(def_geo, "r", encoding="utf-8") as f:
            geo = json.load(f)
        st.sidebar.success("✔ Census District GeoJSON (641 Polygons)")
    except Exception:
        geo = None

# 3. Metadata Dictionary (Default)
def_meta = resolve_local(["data/processed/dataset_metadata_dictionary.csv"])
metadata = pd.read_csv(def_meta) if (def_meta and def_meta.exists()) else None
if metadata is not None:
    st.sidebar.info("✔ Indicator Metadata Dictionary")

# 4. Supplementary Datasets (Default)
def_india = resolve_local(["data/raw/India.csv", "02_Analysis_Outputs/06_Final_Data/india_cleaned_conservative.csv"])
india_df = pd.read_csv(def_india, low_memory=False) if (def_india and def_india.exists()) else None

def_change = resolve_local(["data/raw/India_Change.csv", "02_Analysis_Outputs/06_Final_Data/india_change_cleaned_conservative.csv"])
change_df = pd.read_csv(def_change, low_memory=False) if (def_change and def_change.exists()) else None

st.sidebar.caption("Factual district microdata loaded by default. Zero manual upload required.")
st.sidebar.markdown("---")

# ----------------------------- Navigation ------------------------------------
pages = [
    "National Findings Overview", "Dataset Explorer", "EDA Studio",
    "PCA Lab", "Supplementary Data", "Geospatial Intelligence",
    "Methods & Provenance",
]
page = st.sidebar.radio("Navigate", pages, index=0)

# ----------------------------- Header ----------------------------------------
st.markdown("# NIErnaya")
st.markdown("### National Insights & Evidence-Based Research for Nutritional Advocacy & Yield Analytics")
st.caption("NFHS-5 · 2019–21 · District-level exploratory analysis")
st.markdown("---")

# ============================= OVERVIEW ======================================
if page == "National Findings Overview":
    st.title("National Findings Overview")
    st.markdown("A consolidated view of nutrition outcomes, associated district indicators, geography and statistical evidence.")
    valid_districts = int(df[["district_name","state_name"]].dropna().drop_duplicates().shape[0])
    state_count = int(df["state_name"].nunique(dropna=True))
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("District records", f"{len(df):,}")
    col2.metric("Distinct district–state pairs", f"{valid_districts:,}")
    col3.metric("States / UTs", f"{state_count:,}")
    col4.metric("Indicators available", f"{len(available_indicators)}")

    st.markdown("## 1 · Child nutrition outcomes")
    cards = st.columns(3)
    for c, ind in zip(cards, OUTCOMES):
        s = metric_summary(df, ind)
        with c:
            if s:
                st.metric(LABELS[ind] + " · district mean", fmt_pct(s["mean"]))
                st.caption(f"Median {fmt_pct(s['median'])} · range {s['min']:.1f}–{s['max']:.1f}% · n={s['n']}")
    st.caption("These are unweighted averages across district records, not population-weighted national prevalence estimates.")
    outcome_long = df[["district_name","state_name"] + OUTCOMES].melt(
        id_vars=["district_name","state_name"], var_name="Indicator", value_name="Percent"
    ).dropna()
    if not outcome_long.empty:
        outcome_long["Indicator"] = outcome_long["Indicator"].map(LABELS)
        fig = px.box(outcome_long, x="Indicator", y="Percent", color="Indicator",
                     points="outliers", title="Distribution of district-level nutrition outcomes")
        st.plotly_chart(chart_theme(fig, 390), use_container_width=True)

    st.markdown("## 2 · National district map gallery")
    if geo:
        features = geo.get("features", [])
        property_names = sorted({k for f in features for k in (f.get("properties", {}) or {}).keys()})
        default_d = pick_default_prop(property_names, ["Dist_name", "district_name", "NAME_2", "district", "DISTRICT"])
        default_s = pick_default_prop(property_names, ["ST_NM", "state_name", "NAME_1", "state", "STNAME"])
        g1, g2, g3 = st.columns([1, 1, 1.2])
        with g1:
            geo_district = st.selectbox("GeoJSON district property", property_names, index=default_d, key="overview_geo_d")
        with g2:
            geo_state = st.selectbox("GeoJSON state property", property_names, index=default_s, key="overview_geo_s")
        with g3:
            ov_style_choice = st.selectbox(
                "Basemap style (No API Key Required)",
                ["OpenStreetMap (Standard Tiles)", "Clean Dark Canvas (Polygons Only / Fast)"],
                index=0,
                key="overview_map_style"
            )
            ov_bstyle = "open-street-map" if "OpenStreetMap" in ov_style_choice else "white-bg"
        for start in range(0, len(OUTCOMES), 2):
            cols = st.columns(2)
            for col, ind in zip(cols, OUTCOMES[start:start+2]):
                with col:
                    st.markdown(f"#### {LABELS[ind]}")
                    show_map(geo, df, ind, geo_district, geo_state, f"overview_{ind}", basemap_style=ov_bstyle)
    else:
        st.info("District boundary GeoJSON not found in data/geo/ directory.")

    st.markdown("## 3 · Contributing and contextual indicators")
    pred_cols = st.columns(2)
    for i, ind in enumerate(PREDICTORS):
        if ind not in df.columns: continue
        s = metric_summary(df, ind)
        with pred_cols[i % 2]:
            if s:
                st.markdown(f"**{LABELS[ind]}**")
                st.caption(f"District mean: {s['mean']:.1f}% · median: {s['median']:.1f}% · range: {s['min']:.1f}–{s['max']:.1f}%")
    pred_long = df[PREDICTORS].melt(var_name="Indicator", value_name="Percent").dropna()
    if not pred_long.empty:
        pred_long["Indicator"] = pred_long["Indicator"].map(LABELS)
        fig = px.box(pred_long, x="Indicator", y="Percent", color="Indicator",
                     title="District-level distribution of contextual indicators")
        fig.update_xaxes(tickangle=-25)
        st.plotly_chart(chart_theme(fig, 430), use_container_width=True)

    st.markdown("## 4 · Statistical relationships")
    corr_cols = [c for c in available_indicators if df[c].notna().sum() >= 3]
    if len(corr_cols) >= 2:
        corr = df[corr_cols].corr(method="spearman", min_periods=3)
        corr.index = [LABELS.get(x,x) for x in corr.index]
        corr.columns = [LABELS.get(x,x) for x in corr.columns]
        fig = px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu_r",
                        title="Spearman correlation across district indicators")
        st.plotly_chart(chart_theme(fig, 620), use_container_width=True)
        st.caption("Correlation describes association, not causation. Pairwise sample sizes may differ because of missing values.")
        rel = []
        for outcome in OUTCOMES:
            for predictor in PREDICTORS:
                if outcome in df and predictor in df:
                    pair = df[[outcome,predictor]].dropna()
                    if len(pair) >= 3 and pair[outcome].nunique()>1 and pair[predictor].nunique()>1:
                        r = pair.corr(method="spearman").iloc[0,1]
                        rel.append({"Nutrition outcome":LABELS[outcome],"Indicator":LABELS[predictor],
                                    "Spearman rho":r,"Pairwise districts":len(pair)})
        if rel:
            rel_df = pd.DataFrame(rel).sort_values("Spearman rho", key=lambda x: x.abs(), ascending=False)
            st.markdown("#### Strongest observed associations")
            st.dataframe(rel_df.head(12).style.format({"Spearman rho":"{:.3f}"}),
                         use_container_width=True, hide_index=True)
    else:
        st.info("At least two usable numeric indicators are needed for correlation analysis.")

    st.markdown("## 5 · Districts at the high end of each nutrition outcome")
    st.caption("These are the highest observed district percentages in the uploaded dataset; they are not causal rankings or policy scores.")
    for ind in OUTCOMES:
        with st.expander(f"Highest 10 districts · {LABELS[ind]}", expanded=(ind=="stunting_pct")):
            hi, lo = top_bottom(df, ind, 10)
            st.dataframe(hi.rename(columns={ind:LABELS[ind]}).style.format({LABELS[ind]:"{:.1f}%"}),
                         use_container_width=True, hide_index=True)

    st.markdown("## 6 · Data quality snapshot")
    q1,q2,q3 = st.columns(3)
    q1.metric("Missing district codes", f"{df['district_code'].isna().sum():,}")
    q2.metric("Repeated district codes", f"{df['district_code'].duplicated(keep=False).sum():,}")
    q3.metric("Rows with any missing indicator", f"{df[available_indicators].isna().any(axis=1).sum():,}")
    st.markdown("""
    <div class="warning"><b>Interpretation note:</b> District-level averages are unweighted unless valid population weights are supplied. Do not interpret correlations as causal effects. Geographic comparisons should be interpreted only after reviewing the match coverage and unmatched districts.</div>
    """, unsafe_allow_html=True)

# ============================= DATA EXPLORER ================================
elif page == "Dataset Explorer":
    st.title("Dataset Explorer")
    st.write("Inspect the primary NFHS-5 district dataset and its completeness.")
    st.metric("Rows × columns", f"{df.shape[0]:,} × {df.shape[1]:,}")
    st.dataframe(df, use_container_width=True, height=520)
    st.markdown("### Missingness and uniqueness")
    st.dataframe(data_quality(df), use_container_width=True, hide_index=True)
    st.download_button("Download current primary dataset", df.to_csv(index=False).encode("utf-8"),
                       "nfhs5_primary_dataset.csv", "text/csv")

# ============================= EDA STUDIO ===================================
elif page == "EDA Studio":
    st.title("EDA Studio")
    indicator = st.selectbox("Choose an indicator", available_indicators,
                             format_func=lambda x: LABELS.get(x,x))
    s = metric_summary(df, indicator)
    if s:
        a,b,c,d = st.columns(4)
        a.metric("District mean", fmt_pct(s["mean"]))
        b.metric("Median", fmt_pct(s["median"]))
        c.metric("Minimum", fmt_pct(s["min"]))
        d.metric("Maximum", fmt_pct(s["max"]))
    x = df[indicator].dropna()
    c1,c2 = st.columns(2)
    with c1:
        fig = px.histogram(x, nbins=25, title=f"Distribution · {LABELS[indicator]}", labels={"value":"Percent"})
        st.plotly_chart(chart_theme(fig,390), use_container_width=True)
    with c2:
        fig = px.box(x, points="outliers", title=f"Spread and potential extremes · {LABELS[indicator]}")
        st.plotly_chart(chart_theme(fig,390), use_container_width=True)
    st.markdown("### Districts with highest and lowest values")
    hi,lo = top_bottom(df,indicator,10)
    a,b=st.columns(2)
    with a:
        st.markdown("**Highest 10**")
        st.dataframe(hi, use_container_width=True, hide_index=True)
    with b:
        st.markdown("**Lowest 10**")
        st.dataframe(lo, use_container_width=True, hide_index=True)
    st.markdown("### State-wise unweighted district means")
    sm = state_means(df,[indicator]).sort_values(indicator,ascending=False)
    fig=px.bar(sm,x="state_name",y=indicator,title=f"State comparison · mean district {LABELS[indicator]}")
    fig.update_xaxes(tickangle=-60)
    st.plotly_chart(chart_theme(fig,500),use_container_width=True)
    st.caption("Each state value is the unweighted mean of available district observations in that state.")

# ============================= PCA LAB ======================================
elif page == "PCA Lab":
    st.title("PCA Lab")
    st.caption("Exploratory dimensionality reduction. PCA is not used to predict or rank districts.")
    try:
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        pca_cols = st.multiselect("Variables for PCA", available_indicators,
                                  default=[c for c in INDICATORS if c in df.columns][:6])
        if len(pca_cols) < 2:
            st.info("Select at least two numeric indicators.")
        else:
            pca_data = df[pca_cols].dropna()
            if len(pca_data) < 3:
                st.warning("Not enough complete rows for PCA.")
            else:
                scaled = StandardScaler().fit_transform(pca_data)
                model = PCA()
                scores = model.fit_transform(scaled)
                exp = model.explained_variance_ratio_
                fig=px.bar(x=[f"PC{i+1}" for i in range(len(exp))],y=exp*100,
                           labels={"x":"Principal component","y":"Explained variance (%)"},
                           title="Explained variance by principal component")
                st.plotly_chart(chart_theme(fig,350),use_container_width=True)
                if scores.shape[1]>=2:
                    score_df=pd.DataFrame({"PC1":scores[:,0],"PC2":scores[:,1]})
                    fig=px.scatter(score_df,x="PC1",y="PC2",title="District observations in PC1–PC2 space")
                    st.plotly_chart(chart_theme(fig,430),use_container_width=True)
                loadings=pd.DataFrame(model.components_.T,index=pca_cols,
                                       columns=[f"PC{i+1}" for i in range(len(pca_cols))])
                st.markdown("### Component loadings")
                st.dataframe(loadings.style.format("{:.3f}"),use_container_width=True)
                st.caption(f"PCA used {len(pca_data):,} complete district rows. Variables were standardized before PCA.")
    except Exception as e:
        st.error(f"PCA could not be run in this environment: {e}")
        st.info("Install scikit-learn with: python -m pip install scikit-learn")

# ============================= SUPPLEMENTARY ================================
elif page == "Supplementary Data":
    st.title("Supplementary Data")
    st.caption("Optional comparison datasets are kept separate from the primary district-level NFHS-5 analysis.")
    if india_df is not None:
        st.markdown("### India.csv")
        st.write(f"{len(india_df):,} rows × {len(india_df.columns):,} columns")
        st.dataframe(india_df.head(100),use_container_width=True)
    else:
        st.info("India.csv dataset not found in data/raw/ directory.")
    if change_df is not None:
        st.markdown("### India_Change.csv")
        st.write(f"{len(change_df):,} rows × {len(change_df.columns):,} columns")
        st.dataframe(change_df.head(100),use_container_width=True)
    else:
        st.info("India_Change.csv dataset not found in data/raw/ directory.")
    if metadata is not None:
        st.markdown("### Indicator metadata dictionary")
        st.dataframe(metadata,use_container_width=True)
    else:
        st.info("Metadata dictionary not found in data/processed/ directory.")

# ============================= GEOSPATIAL ===================================
elif page == "Geospatial Intelligence":
    st.title("Geospatial Intelligence")
    if not geo:
        st.warning("District boundary GeoJSON not found in data/geo/ directory.")
        st.stop()
    features = geo.get("features", [])
    props = sorted({k for f in features for k in (f.get("properties", {}) or {}).keys()})
    if not props:
        st.error("No feature properties found in GeoJSON.")
        st.stop()
    d_default = pick_default_prop(props, ["Dist_name", "district_name", "NAME_2", "district", "DISTRICT"])
    s_default = pick_default_prop(props, ["ST_NM", "state_name", "NAME_1", "state", "STNAME"])
    
    col_d, col_s, col_map = st.columns([1, 1, 1.2])
    with col_d:
        gd = st.selectbox("GeoJSON district property", props, index=d_default, key="geo_d")
    with col_s:
        gs = st.selectbox("GeoJSON state property", props, index=s_default, key="geo_s")
    with col_map:
        map_choice = st.selectbox(
            "Basemap style (No API Key Required)",
            ["OpenStreetMap (Standard Tiles)", "Clean Dark Canvas (Polygons Only / Fast)"],
            index=0,
            key="geo_map_style"
        )
        bstyle = "open-street-map" if "OpenStreetMap" in map_choice else "white-bg"

    indicator = st.selectbox("Map indicator", available_indicators, format_func=lambda x: LABELS.get(x, x))
    st.markdown(f"### {LABELS[indicator]} across Indian districts")
    show_map(geo, df, indicator, gd, gs, "single_geo_map", basemap_style=bstyle)
    
    st.markdown("### Matching diagnostics")
    _, merged_diag, dup_data, dup_geo, matched_cnt = make_choropleth(geo, gd, gs, df, indicator)
    name_matches = int((merged_diag["_match_source"] == "name").sum())
    code_matches = int((merged_diag["_match_source"] == "census_code").sum())
    total_feats = len(merged_diag)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("GeoJSON features", f"{total_feats:,}")
    m2.metric("Direct name matches", f"{name_matches:,}")
    m3.metric("Census code fallback", f"{code_matches:,}")
    m4.metric("Total mapped coverage", f"{matched_cnt}/{total_feats} ({matched_cnt/total_feats*100:.1f}%)" if total_feats else "0%")
    
    unmatched_geo = merged_diag[merged_diag["_match_source"] == "unmatched"][["_district", "_state"]]
    
    ddf = add_composite_keys(df, "district_name", "state_name")
    geo_names = set(merged_diag["_join_key"])
    unmatched_csv = ddf[~ddf["_join_key"].isin(geo_names)][["district_name", "state_name"]]
    
    x, y = st.columns(2)
    with x:
        st.markdown(f"**Unmatched GeoJSON features ({len(unmatched_geo)})**")
        st.dataframe(unmatched_geo.rename(columns={"_district": "GeoJSON district", "_state": "GeoJSON state"}),
                     use_container_width=True, hide_index=True)
    with y:
        st.markdown(f"**Unmatched CSV records ({len(unmatched_csv)})**")
        st.dataframe(unmatched_csv.head(100), use_container_width=True, hide_index=True)

# ============================= METHODS =======================================
elif page == "Methods & Provenance":
    st.title("Methods & Provenance")
    st.markdown("### Primary analytical source")
    st.write("NFHS-5 district-level factual dataset uploaded by the user. The metadata dictionary should be used to verify indicator definitions and denominators.")
    st.markdown("### Analytical principles")
    st.markdown("""
    - The primary CSV is the source for district-level numerical analysis.
    - GeoJSON is used only after district–state composite-name matching is inspected.
    - District codes are not assumed to be globally unique or complete.
    - Missing values are not silently imputed.
    - Zero values are not automatically treated as missing.
    - Outliers are inspected, not automatically deleted.
    - State summaries are unweighted means of district observations unless valid weights are provided.
    - District averages must not be described as population-weighted national prevalence.
    - Correlation and other associations do not establish causation.
    - Unmatched geographic features are shown as unmatched, not converted to zero.
    """)
    st.markdown("### Current dataset audit")
    st.dataframe(data_quality(df),use_container_width=True,hide_index=True)
    st.markdown("### Geographic matching")
    st.write("The map join uses normalized `state_name + district_name` in the CSV and the selected state and district properties in GeoJSON. Always inspect match counts and unmatched examples before interpreting maps.")
    st.markdown("### Interpretation")
    st.write("The dashboard is an exploratory evidence interface. It does not provide clinical diagnoses, causal estimates, or population-weighted prevalence unless appropriate survey weights and methodology are explicitly incorporated.")

st.markdown("---")
st.caption("NIErnaya 2026 · Exploratory analysis interface · Verify all source definitions and geographic matches before presentation.")

"""
NIErnaya Phase 2 — Presentation Deck Generator
Generates a self-contained HTML slide deck with embedded chart images.
"""
import base64
import os

# ─────────────────────────────── Image Loader ────────────────────────────────
def b64img(path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    ext = path.rsplit('.', 1)[-1]
    mime = 'image/webp' if ext == 'webp' else f'image/{ext}'
    return f'data:{mime};base64,{data}'

imgs = {
    'pearson':     b64img('01_Visual_Atlas/01_Main_NFHS5/pearson_correlation.webp'),
    'spearman':    b64img('01_Visual_Atlas/01_Main_NFHS5/spearman_correlation.webp'),
    'box_out':     b64img('01_Visual_Atlas/01_Main_NFHS5/boxplot_outcomes.webp'),
    'box_pred':    b64img('01_Visual_Atlas/01_Main_NFHS5/boxplot_predictors.webp'),
    'h_stunt':     b64img('01_Visual_Atlas/01_Main_NFHS5/hist_stunting_pct.webp'),
    'h_waste':     b64img('01_Visual_Atlas/01_Main_NFHS5/hist_wasting_pct.webp'),
    'h_under':     b64img('01_Visual_Atlas/01_Main_NFHS5/hist_underweight_pct.webp'),
    'pca_scree':   b64img('01_Visual_Atlas/01_Main_NFHS5/pca_scree.webp'),
    'pca_load':    b64img('01_Visual_Atlas/01_Main_NFHS5/pca_loadings.webp'),
    'sc_san_st':   b64img('01_Visual_Atlas/01_Main_NFHS5/scatter_improved_sanitation_pct_vs_stunting_pct.webp'),
    'sc_lit_uw':   b64img('01_Visual_Atlas/01_Main_NFHS5/scatter_female_literacy_pct_vs_underweight_pct.webp'),
    'sc_em_st':    b64img('01_Visual_Atlas/01_Main_NFHS5/scatter_early_marriage_pct_vs_stunting_pct.webp'),
    'sc_an_uw':    b64img('01_Visual_Atlas/01_Main_NFHS5/scatter_child_anemia_pct_vs_underweight_pct.webp'),
    'sw_stunt':    b64img('01_Visual_Atlas/01_Main_NFHS5/statewise_stunting_pct.webp'),
    'sw_waste':    b64img('01_Visual_Atlas/01_Main_NFHS5/statewise_wasting_pct.webp'),
    'map_stunt':   b64img('01_Visual_Atlas/04_Geographical_Maps/MAIN_STATE_MAP_stunting_pct.webp'),
    'map_waste':   b64img('01_Visual_Atlas/04_Geographical_Maps/MAIN_STATE_MAP_wasting_pct.webp'),
}

# ─────────────────────────────── HTML Template ───────────────────────────────
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NIErnaya Phase 2 — Presentation Deck</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {{
    --bg-primary: #0a0f1a;
    --bg-slide: #111827;
    --bg-card: #1e293b;
    --accent: #f59e0b;
    --accent2: #06b6d4;
    --accent3: #8b5cf6;
    --accent4: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #334155;
    --success: #22c55e;
    --danger: #ef4444;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  html, body {{
    width: 100%; height: 100%;
    background: var(--bg-primary);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: var(--text-primary);
    overflow: hidden;
  }}

  /* ── Slide Container ── */
  .deck {{ position: relative; width: 100%; height: 100%; }}

  .slide {{
    position: absolute; inset: 0;
    display: none; flex-direction: column;
    padding: 40px 60px;
    opacity: 0;
    transition: opacity 0.4s ease;
  }}
  .slide.active {{ display: flex; opacity: 1; }}

  /* ── Title Slide ── */
  .slide.title-slide {{
    justify-content: center; align-items: center; text-align: center;
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
  }}
  .slide.title-slide::before {{
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 30% 40%, rgba(245,158,11,0.08) 0%, transparent 50%),
                radial-gradient(circle at 70% 60%, rgba(6,182,212,0.08) 0%, transparent 50%);
  }}
  .title-slide .project-badge {{
    display: inline-block; padding: 8px 24px; border-radius: 50px;
    background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3);
    color: var(--accent); font-size: 14px; font-weight: 600;
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 24px;
    position: relative; z-index: 1;
  }}
  .title-slide h1 {{
    font-size: clamp(36px, 4.5vw, 64px); font-weight: 900;
    line-height: 1.1; margin-bottom: 16px; position: relative; z-index: 1;
    background: linear-gradient(135deg, #f59e0b, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .title-slide .subtitle {{
    font-size: clamp(16px, 2vw, 24px); color: var(--text-secondary);
    font-weight: 300; max-width: 800px; line-height: 1.5;
    position: relative; z-index: 1; margin-bottom: 32px;
  }}
  .title-slide .meta {{
    font-size: 14px; color: var(--text-muted); position: relative; z-index: 1;
  }}
  .title-slide .meta span {{ color: var(--accent2); font-weight: 600; }}

  /* ── Section Divider ── */
  .slide.section-slide {{
    justify-content: center; align-items: center; text-align: center;
    background: linear-gradient(135deg, #0f172a 0%, #1a1a2e 100%);
  }}
  .section-num {{
    font-size: 80px; font-weight: 900; color: rgba(245,158,11,0.15);
    font-family: 'JetBrains Mono', monospace; line-height: 1;
  }}
  .section-title {{
    font-size: clamp(28px, 3.5vw, 48px); font-weight: 800; margin-top: 8px;
    color: var(--text-primary);
  }}
  .section-subtitle {{
    font-size: 18px; color: var(--text-secondary); margin-top: 12px; font-weight: 300;
  }}

  /* ── Content Slides ── */
  .slide-header {{
    display: flex; align-items: center; gap: 16px; margin-bottom: 28px;
    border-bottom: 1px solid var(--border); padding-bottom: 16px;
    flex-shrink: 0;
  }}
  .slide-header .num {{
    font-family: 'JetBrains Mono', monospace; font-size: 13px;
    color: var(--accent); background: rgba(245,158,11,0.12);
    padding: 4px 12px; border-radius: 6px; font-weight: 600;
  }}
  .slide-header h2 {{
    font-size: clamp(22px, 2.5vw, 32px); font-weight: 700;
  }}

  .slide-body {{ flex: 1; display: flex; gap: 32px; min-height: 0; overflow: hidden; }}
  .slide-body.col-1 {{ flex-direction: column; }}
  .slide-body.col-2 > * {{ flex: 1; min-width: 0; }}

  /* ── Cards ── */
  .card {{
    background: var(--bg-card); border-radius: 12px; padding: 24px;
    border: 1px solid var(--border);
  }}
  .card h3 {{
    font-size: 16px; font-weight: 600; margin-bottom: 12px;
    color: var(--accent2);
  }}

  /* ── Stat Grid ── */
  .stat-grid {{
    display: grid; gap: 16px;
  }}
  .stat-grid.g3 {{ grid-template-columns: repeat(3, 1fr); }}
  .stat-grid.g4 {{ grid-template-columns: repeat(4, 1fr); }}
  .stat-grid.g5 {{ grid-template-columns: repeat(5, 1fr); }}

  .stat-box {{
    background: var(--bg-card); border-radius: 12px; padding: 20px;
    border: 1px solid var(--border); text-align: center;
  }}
  .stat-box .label {{
    font-size: 11px; color: var(--text-muted); text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600; margin-bottom: 8px;
  }}
  .stat-box .value {{
    font-size: clamp(28px, 3vw, 42px); font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
  }}
  .stat-box .sub {{
    font-size: 12px; color: var(--text-secondary); margin-top: 4px;
  }}
  .stat-box.amber .value {{ color: var(--accent); }}
  .stat-box.cyan .value {{ color: var(--accent2); }}
  .stat-box.purple .value {{ color: var(--accent3); }}
  .stat-box.red .value {{ color: var(--accent4); }}
  .stat-box.green .value {{ color: var(--success); }}

  /* ── Image ── */
  .chart-container {{
    flex: 1; display: flex; justify-content: center; align-items: center;
    min-height: 0; overflow: hidden;
  }}
  .chart-container img {{
    max-width: 100%; max-height: 100%; object-fit: contain;
    border-radius: 8px;
  }}
  .two-charts {{
    display: flex; gap: 16px; flex: 1; min-height: 0;
  }}
  .two-charts .chart-container {{ flex: 1; }}

  /* ── Table ── */
  .data-table {{
    width: 100%; border-collapse: collapse; font-size: 14px;
  }}
  .data-table th {{
    text-align: left; padding: 10px 14px; border-bottom: 2px solid var(--accent);
    font-weight: 600; color: var(--accent); font-size: 12px;
    text-transform: uppercase; letter-spacing: 1px;
  }}
  .data-table td {{
    padding: 8px 14px; border-bottom: 1px solid var(--border);
    color: var(--text-secondary);
  }}
  .data-table tr:hover td {{ background: rgba(245,158,11,0.05); }}
  .data-table .val {{ font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--text-primary); }}
  .data-table .neg {{ color: var(--success); }}
  .data-table .pos {{ color: var(--danger); }}

  /* ── Bullet List ── */
  .insight-list {{
    list-style: none; padding: 0; display: flex; flex-direction: column; gap: 14px;
  }}
  .insight-list li {{
    display: flex; gap: 12px; align-items: flex-start;
    font-size: 15px; line-height: 1.55; color: var(--text-secondary);
  }}
  .insight-list .bullet {{
    flex-shrink: 0; width: 8px; height: 8px; border-radius: 50%;
    margin-top: 7px;
  }}
  .insight-list .bullet.amber {{ background: var(--accent); }}
  .insight-list .bullet.cyan {{ background: var(--accent2); }}
  .insight-list .bullet.purple {{ background: var(--accent3); }}
  .insight-list .bullet.red {{ background: var(--accent4); }}
  .insight-list .bullet.green {{ background: var(--success); }}
  .insight-list strong {{ color: var(--text-primary); }}

  /* ── Footer ── */
  .slide-footer {{
    flex-shrink: 0; display: flex; justify-content: space-between;
    align-items: center; padding-top: 12px; margin-top: 12px;
    border-top: 1px solid rgba(51,65,85,0.5);
    font-size: 11px; color: var(--text-muted);
  }}

  /* ── Navigation ── */
  .nav-bar {{
    position: fixed; bottom: 0; left: 0; right: 0;
    display: flex; align-items: center; justify-content: center; gap: 16px;
    padding: 12px 24px; background: rgba(10,15,26,0.9);
    backdrop-filter: blur(8px); border-top: 1px solid var(--border);
    z-index: 1000;
  }}
  .nav-btn {{
    background: var(--bg-card); border: 1px solid var(--border);
    color: var(--text-primary); padding: 8px 20px; border-radius: 8px;
    cursor: pointer; font-size: 14px; font-family: 'Inter', sans-serif;
    font-weight: 500; transition: all 0.2s;
  }}
  .nav-btn:hover {{ background: var(--accent); color: #000; border-color: var(--accent); }}
  .nav-counter {{
    font-family: 'JetBrains Mono', monospace; font-size: 14px;
    color: var(--text-secondary); min-width: 60px; text-align: center;
  }}
  .progress-bar {{
    position: fixed; top: 0; left: 0; height: 3px; z-index: 1001;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.3s ease;
  }}

  /* ── Tag ── */
  .tag {{
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.5px;
  }}
  .tag.amber {{ background: rgba(245,158,11,0.15); color: var(--accent); }}
  .tag.cyan {{ background: rgba(6,182,212,0.15); color: var(--accent2); }}
  .tag.green {{ background: rgba(34,197,94,0.15); color: var(--success); }}
  .tag.red {{ background: rgba(239,68,68,0.15); color: var(--danger); }}

  .highlight-box {{
    background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25);
    border-radius: 10px; padding: 16px 20px; margin-top: 12px;
  }}
  .highlight-box p {{ font-size: 14px; color: var(--text-secondary); line-height: 1.6; }}
  .highlight-box strong {{ color: var(--accent); }}

  .flex-row {{ display: flex; gap: 16px; }}
  .flex-col {{ display: flex; flex-direction: column; gap: 16px; }}
  .f1 {{ flex: 1; min-width: 0; }}
  .f2 {{ flex: 2; min-width: 0; }}
</style>
</head>
<body>

<div class="progress-bar" id="progressBar"></div>

<div class="deck" id="deck">

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 1: TITLE                                          ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide title-slide active">
  <div class="project-badge">NIErnaya 2026</div>
  <h1>Decoding India's<br>Child Malnutrition Crisis</h1>
  <p class="subtitle">
    District-Level Exploratory Data Analysis of the<br>
    NFHS-5 Child Malnutrition Triad — SDG 2 (Zero Hunger, Target 2.2)
  </p>
  <p class="meta">
    <span>706 Districts</span> · <span>37 States & UTs</span> · <span>10 Survey Indicators</span> · <span>468 Visualizations</span>
  </p>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 2: PROBLEM CONTEXT                                ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">01</span>
    <h2>The Problem: Why This Matters</h2>
  </div>
  <div class="slide-body col-1">
    <div class="stat-grid g3">
      <div class="stat-box amber">
        <div class="label">Stunted Children</div>
        <div class="value">33.5%</div>
        <div class="sub">National district average</div>
      </div>
      <div class="stat-box red">
        <div class="label">Wasted Children</div>
        <div class="value">18.5%</div>
        <div class="sub">Acute malnutrition</div>
      </div>
      <div class="stat-box purple">
        <div class="label">Underweight Children</div>
        <div class="value">29.5%</div>
        <div class="sub">Composite burden</div>
      </div>
    </div>
    <div class="flex-row" style="flex:1; min-height:0;">
      <div class="f1 flex-col">
        <div class="card" style="flex:1;">
          <h3>🎯 SDG 2 — Zero Hunger, Target 2.2</h3>
          <ul class="insight-list">
            <li><span class="bullet amber"></span><span><strong>Stunting</strong> (HAZ &lt; −2 SD) — chronic, irreversible growth faltering caused by prolonged nutritional deprivation and repeated infections</span></li>
            <li><span class="bullet red"></span><span><strong>Wasting</strong> (WHZ &lt; −2 SD) — acute weight loss from recent illness or food crises; highest mortality risk</span></li>
            <li><span class="bullet purple"></span><span><strong>Underweight</strong> (WAZ &lt; −2 SD) — composite indicator capturing both chronic and acute components</span></li>
            <li><span class="bullet cyan"></span><span>India holds the world's <strong>largest absolute burden</strong> of child malnutrition — over 40 million stunted children</span></li>
          </ul>
        </div>
      </div>
      <div class="f1">
        <div class="card" style="height:100%;">
          <h3>📊 Our Analytical Framework</h3>
          <ul class="insight-list">
            <li><span class="bullet green"></span><span><strong>3 anthropometric outcomes</strong> as dependent variables (SDG 2.2 indicators)</span></li>
            <li><span class="bullet green"></span><span><strong>7 multi-sectoral predictors</strong>: female literacy, sanitation, water, ANC coverage, child anaemia, early marriage, institutional births</span></li>
            <li><span class="bullet green"></span><span><strong>706 factual districts</strong> from NFHS-5 (2019–21) — zero synthetic data points</span></li>
          </ul>
          <div class="highlight-box" style="margin-top:auto;">
            <p><strong>Research Question:</strong> Which structural drivers explain the greatest spatial variation in district-level child malnutrition across India?</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Source: NFHS-5 (IIPS & MoHFW, Govt. of India, 2019–21)</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 3: DATASET OVERVIEW                               ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">02</span>
    <h2>Dataset Overview & Quality Audit</h2>
  </div>
  <div class="slide-body col-1">
    <div class="stat-grid g5">
      <div class="stat-box cyan">
        <div class="label">Districts</div>
        <div class="value">706</div>
        <div class="sub">Factual records</div>
      </div>
      <div class="stat-box amber">
        <div class="label">States / UTs</div>
        <div class="value">37</div>
        <div class="sub">Administrative units</div>
      </div>
      <div class="stat-box green">
        <div class="label">Missing Values</div>
        <div class="value">0%</div>
        <div class="sub">All 10 indicators</div>
      </div>
      <div class="stat-box green">
        <div class="label">Duplicate Rows</div>
        <div class="value">0</div>
        <div class="sub">Clean primary keys</div>
      </div>
      <div class="stat-box purple">
        <div class="label">Features</div>
        <div class="value">14</div>
        <div class="sub">4 keys + 10 indicators</div>
      </div>
    </div>
    <div class="flex-row" style="flex:1; min-height:0;">
      <div class="f1 card">
        <h3>Variable Architecture</h3>
        <table class="data-table">
          <tr><th>Role</th><th>Variables</th><th>Count</th></tr>
          <tr><td>Primary Keys</td><td class="val">district_name, state_name, district_code, state_code</td><td class="val">4</td></tr>
          <tr><td>Dependent (SDG 2.2)</td><td class="val">stunting_pct, wasting_pct, underweight_pct</td><td class="val">3</td></tr>
          <tr><td>Predictors (WASH)</td><td class="val">improved_sanitation_pct, improved_water_pct</td><td class="val">2</td></tr>
          <tr><td>Predictors (Social)</td><td class="val">female_literacy_pct, early_marriage_pct</td><td class="val">2</td></tr>
          <tr><td>Predictors (Health)</td><td class="val">anc_4plus_pct, child_anemia_pct, institutional_births_pct</td><td class="val">3</td></tr>
        </table>
      </div>
      <div class="f1 card">
        <h3>Data Quality Checks Performed</h3>
        <ul class="insight-list">
          <li><span class="bullet green"></span><span><strong>Range validation:</strong> All % columns bounded within [0%, 100%] ✓</span></li>
          <li><span class="bullet green"></span><span><strong>Missingness audit:</strong> Zero missing values across all 10 analytical indicators ✓</span></li>
          <li><span class="bullet green"></span><span><strong>Duplicate screening:</strong> Zero duplicate (State, District) pairs ✓</span></li>
          <li><span class="bullet amber"></span><span><strong>IQR outlier screening:</strong> Flagged 92 values; all retained as authentic survey observations</span></li>
          <li><span class="bullet green"></span><span><strong>Synthetic data check:</strong> 100% provenance from IIPS official fact sheets ✓</span></li>
          <li><span class="bullet cyan"></span><span><strong>Census code linkage:</strong> 641/706 districts matched to Census 2011 codes; 65 post-2011 districts</span></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Source: NFHS-5, IIPS (2019–21) | Census of India 2011 Boundary Codes</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 4: SECTION — EDA                                  ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide section-slide">
  <div class="section-num">I</div>
  <div class="section-title">Exploratory Data Analysis</div>
  <div class="section-subtitle">Distributions · Outliers · State-Level Disparities</div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 5: DISTRIBUTIONS                                  ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">03</span>
    <h2>Malnutrition Triad — Distribution Analysis</h2>
  </div>
  <div class="slide-body col-1">
    <div class="stat-grid g3" style="margin-bottom:8px;">
      <div class="stat-box amber">
        <div class="label">Stunting Range</div>
        <div class="value">13.2 – 60.6%</div>
        <div class="sub">μ = 33.5%, σ = 8.5%</div>
      </div>
      <div class="stat-box red">
        <div class="label">Wasting Range</div>
        <div class="value">4.5 – 48.0%</div>
        <div class="sub">μ = 18.5%, σ = 6.5%</div>
      </div>
      <div class="stat-box purple">
        <div class="label">Underweight Range</div>
        <div class="value">7.2 – 62.4%</div>
        <div class="sub">μ = 29.5%, σ = 9.7%</div>
      </div>
    </div>
    <div class="two-charts">
      <div class="chart-container">
        <img src="{imgs['box_out']}" alt="Boxplot of malnutrition outcomes">
      </div>
      <div class="chart-container">
        <img src="{imgs['h_stunt']}" alt="Stunting distribution">
      </div>
      <div class="chart-container">
        <img src="{imgs['h_waste']}" alt="Wasting distribution">
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>N = 706 districts | Histograms show district-level frequency distributions</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 6: STATE RANKINGS                                 ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">04</span>
    <h2>State-Level Disparities — Stunting vs Wasting</h2>
  </div>
  <div class="slide-body col-2">
    <div class="chart-container">
      <img src="{imgs['sw_stunt']}" alt="State-wise stunting">
    </div>
    <div class="chart-container">
      <img src="{imgs['sw_waste']}" alt="State-wise wasting">
    </div>
  </div>
  <div class="slide-footer">
    <span>Unweighted mean of district percentages per state | Bars ranked descending</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 7: GEOGRAPHIC MAPS                                ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">05</span>
    <h2>Geographic Hotspots — The Stunting–Wasting Duality</h2>
  </div>
  <div class="slide-body col-2">
    <div class="flex-col f1">
      <div class="chart-container" style="flex:1;">
        <img src="{imgs['map_stunt']}" alt="Map stunting">
      </div>
      <div class="tag amber" style="text-align:center;">Stunting Concentration: North & East</div>
    </div>
    <div class="flex-col f1">
      <div class="chart-container" style="flex:1;">
        <img src="{imgs['map_waste']}" alt="Map wasting">
      </div>
      <div class="tag red" style="text-align:center;">Wasting Concentration: West & Central</div>
    </div>
  </div>
  <div class="highlight-box">
    <p><strong>Key Finding:</strong> Stunting and wasting follow <strong>distinct spatial patterns</strong>. Bihar/UP/Jharkhand/Meghalaya dominate stunting, while Gujarat/Maharashtra drive wasting. They require <strong>different policy interventions</strong>.</p>
  </div>
  <div class="slide-footer">
    <span>Choropleth based on unweighted state means | Census 2011 boundaries</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 8: SECTION — CORRELATION                          ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide section-slide">
  <div class="section-num">II</div>
  <div class="section-title">Correlation & Relationships</div>
  <div class="section-subtitle">Pearson · Spearman · FDR-Adjusted · Multi-Sectoral Drivers</div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 9: CORRELATION MATRIX                             ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">06</span>
    <h2>Correlation Heatmaps — Pearson & Spearman</h2>
  </div>
  <div class="slide-body col-2">
    <div class="chart-container">
      <img src="{imgs['pearson']}" alt="Pearson correlation matrix">
    </div>
    <div class="chart-container">
      <img src="{imgs['spearman']}" alt="Spearman correlation matrix">
    </div>
  </div>
  <div class="slide-footer">
    <span>Both methods yield consistent rankings | Benjamini–Hochberg FDR correction applied</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 10: TOP CORRELATES TABLE                          ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">07</span>
    <h2>Strongest Multi-Sectoral Associations</h2>
  </div>
  <div class="slide-body col-1">
    <div class="card" style="flex:1; overflow:auto;">
      <table class="data-table">
        <tr><th>Predictor</th><th>Outcome</th><th>Pearson r</th><th>Spearman ρ</th><th>Direction</th><th>Interpretation</th></tr>
        <tr><td>Improved Sanitation</td><td>Underweight</td><td class="val neg">−0.583</td><td class="val neg">−0.585</td><td><span class="tag green">Protective ▼</span></td><td>Strongest single predictor</td></tr>
        <tr><td>Female Literacy</td><td>Underweight</td><td class="val neg">−0.545</td><td class="val neg">−0.549</td><td><span class="tag green">Protective ▼</span></td><td>Women's agency strongly matters</td></tr>
        <tr><td>Female Literacy</td><td>Stunting</td><td class="val neg">−0.539</td><td class="val neg">−0.520</td><td><span class="tag green">Protective ▼</span></td><td>Education prevents chronic malnutrition</td></tr>
        <tr><td>Improved Sanitation</td><td>Stunting</td><td class="val neg">−0.503</td><td class="val neg">−0.495</td><td><span class="tag green">Protective ▼</span></td><td>WASH prevents growth faltering</td></tr>
        <tr><td>Early Marriage</td><td>Underweight</td><td class="val pos">+0.481</td><td class="val pos">+0.511</td><td><span class="tag red">Risk ▲</span></td><td>Social practice increases vulnerability</td></tr>
        <tr><td>Early Marriage</td><td>Stunting</td><td class="val pos">+0.428</td><td class="val pos">+0.457</td><td><span class="tag red">Risk ▲</span></td><td>Teenage motherhood impairs child growth</td></tr>
        <tr><td>Child Anaemia</td><td>Underweight</td><td class="val pos">+0.403</td><td class="val pos">+0.386</td><td><span class="tag red">Risk ▲</span></td><td>Comorbid nutritional deficit</td></tr>
        <tr><td>ANC 4+ Visits</td><td>Stunting</td><td class="val neg">−0.361</td><td class="val neg">−0.355</td><td><span class="tag green">Protective ▼</span></td><td>Maternal contact reduces chronic undernutrition</td></tr>
        <tr><td>Improved Water</td><td>Stunting</td><td class="val" style="color:var(--text-muted)">−0.037</td><td class="val" style="color:var(--text-muted)">−0.037</td><td><span class="tag amber">Negligible</span></td><td>Ceiling effect (median = 97%)</td></tr>
      </table>
    </div>
    <div class="highlight-box">
      <p><strong>Takeaway:</strong> <strong>Sanitation</strong> and <strong>female literacy</strong> are the two strongest protective factors, while <strong>early marriage</strong> is the strongest risk factor. Water access shows negligible correlation due to near-universal coverage (97% median).</p>
    </div>
  </div>
  <div class="slide-footer">
    <span>All p-values &lt; 0.001 after BH-FDR correction (except improved water) | VIF range: 1.19–2.50</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 11: SCATTER PLOTS                                 ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">08</span>
    <h2>Key Bivariate Relationships — Scatter Evidence</h2>
  </div>
  <div class="slide-body col-1">
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; flex:1; min-height:0;">
      <div class="chart-container">
        <img src="{imgs['sc_san_st']}" alt="Sanitation vs Stunting">
      </div>
      <div class="chart-container">
        <img src="{imgs['sc_lit_uw']}" alt="Literacy vs Underweight">
      </div>
      <div class="chart-container">
        <img src="{imgs['sc_em_st']}" alt="Early Marriage vs Stunting">
      </div>
      <div class="chart-container">
        <img src="{imgs['sc_an_uw']}" alt="Anaemia vs Underweight">
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Each dot = 1 district (N = 706) | OLS regression line with 95% CI band</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 12: SECTION — PREPROCESSING & FEATURE ENGINEERING ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide section-slide">
  <div class="section-num">III</div>
  <div class="section-title">Preprocessing & Feature Engineering</div>
  <div class="section-subtitle">Composite Indices · Z-Score Normalization · Data Leakage Safeguards</div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 13: FEATURE ENGINEERING                           ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">09</span>
    <h2>Engineered Composite Features</h2>
  </div>
  <div class="slide-body col-1">
    <div class="stat-grid g4">
      <div class="stat-box amber">
        <div class="label">Socioeconomic Vulnerability Index</div>
        <div class="value" style="font-size:18px;">z(early_marriage) − z(literacy) ÷ 2</div>
        <div class="sub">r = +0.583 with underweight</div>
      </div>
      <div class="stat-box cyan">
        <div class="label">Sanitation–Water Gap</div>
        <div class="value" style="font-size:18px;">water% − sanitation%</div>
        <div class="sub">r = +0.507 with underweight</div>
      </div>
      <div class="stat-box purple">
        <div class="label">Maternal Care Gap</div>
        <div class="value" style="font-size:18px;">inst_births% − anc_4plus%</div>
        <div class="sub">r = +0.147 with underweight</div>
      </div>
      <div class="stat-box red">
        <div class="label">Nutritional Burden Index</div>
        <div class="value" style="font-size:18px;">(stunt + waste + underw) ÷ 3</div>
        <div class="sub">⚠ Descriptive only</div>
      </div>
    </div>
    <div class="flex-row" style="flex:1; min-height:0;">
      <div class="f1 card">
        <h3>Rationale & Design Decisions</h3>
        <ul class="insight-list">
          <li><span class="bullet amber"></span><span><strong>Socioeconomic Vulnerability Index</strong> captures the gap between harmful social norms (child marriage) and women's empowerment (literacy) using z-score normalization for comparable scaling</span></li>
          <li><span class="bullet cyan"></span><span><strong>Sanitation–Water Gap</strong> quantifies WASH infrastructure imbalance — districts where water coverage far exceeds sanitation suggest open defecation persists despite piped water access</span></li>
          <li><span class="bullet purple"></span><span><strong>Maternal Care Gap</strong> identifies districts where women deliver in facilities but miss the antenatal care window — a service quality indicator</span></li>
          <li><span class="bullet red"></span><span><strong>Nutritional Burden Index</strong> is quarantined from modeling pipelines (data leakage guard) but used for descriptive district ranking and geographic profiling</span></li>
        </ul>
      </div>
      <div class="f1 card">
        <h3>Preprocessing Pipeline Summary</h3>
        <ul class="insight-list">
          <li><span class="bullet green"></span><span><strong>Missing values:</strong> No imputation needed (0% missingness across all analytical columns)</span></li>
          <li><span class="bullet green"></span><span><strong>Outlier handling:</strong> IQR-flagged values retained — verified as authentic survey data from extreme-burden districts</span></li>
          <li><span class="bullet green"></span><span><strong>Type coercion:</strong> All percentage strings converted to float64; Census codes parsed to nullable integers</span></li>
          <li><span class="bullet green"></span><span><strong>Placeholder removal:</strong> "Data Not Available" dummy district excluded (J&K administrative gap)</span></li>
          <li><span class="bullet green"></span><span><strong>VIF screening:</strong> All predictor VIFs in [1.19, 2.50] — no harmful multicollinearity</span></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Output: main_nfhs5_engineered.csv (706 × 18) | All transformations documented in metadata codebook</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 14: PCA                                           ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">10</span>
    <h2>Principal Component Analysis — Dimensionality Reduction</h2>
  </div>
  <div class="slide-body col-2">
    <div class="flex-col f1">
      <div class="chart-container" style="flex:1;">
        <img src="{imgs['pca_scree']}" alt="PCA Scree Plot">
      </div>
      <div class="stat-grid g3">
        <div class="stat-box amber">
          <div class="label">PC1 Variance</div>
          <div class="value">39.3%</div>
        </div>
        <div class="stat-box cyan">
          <div class="label">PC2 Variance</div>
          <div class="value">23.4%</div>
        </div>
        <div class="stat-box green">
          <div class="label">Cumulative (2 PCs)</div>
          <div class="value">62.7%</div>
        </div>
      </div>
    </div>
    <div class="flex-col f1">
      <div class="chart-container" style="flex:1;">
        <img src="{imgs['pca_load']}" alt="PCA Loadings">
      </div>
      <div class="card">
        <h3>Component Interpretation</h3>
        <ul class="insight-list">
          <li><span class="bullet amber"></span><span><strong>PC1 — "Socioeconomic Infrastructure"</strong>: Literacy ↑, Sanitation ↑, Early Marriage ↓</span></li>
          <li><span class="bullet cyan"></span><span><strong>PC2 — "Healthcare Contact"</strong>: Institutional Births ↑, ANC ↑, Child Anaemia ↓</span></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Kaiser criterion: 2 components retained (eigenvalue &gt; 1.0) | 7 standardized predictors</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 15: SECTION — INSIGHTS                            ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide section-slide">
  <div class="section-num">IV</div>
  <div class="section-title">Key Insights & Conclusions</div>
  <div class="section-subtitle">Evidence-Backed Policy Implications</div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 16: INSIGHTS                                      ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">11</span>
    <h2>Five Evidence-Based Insights</h2>
  </div>
  <div class="slide-body col-1">
    <div class="flex-col" style="flex:1; gap:14px;">
      <div class="card" style="border-left: 3px solid var(--accent);">
        <h3 style="color:var(--accent);">1 — Sanitation Is the Strongest Single Lever</h3>
        <p style="font-size:14px; color:var(--text-secondary); line-height:1.6;">Improved sanitation shows the strongest negative correlation with underweight (r = −0.583) and stunting (r = −0.503). Districts with &lt;50% sanitation coverage average <strong>39.8% stunting</strong> vs. 29.1% in districts with &gt;80% coverage. This aligns with the environmental enteropathy pathway — open defecation causes subclinical gut inflammation that blocks nutrient absorption.</p>
      </div>
      <div class="card" style="border-left: 3px solid var(--accent2);">
        <h3 style="color:var(--accent2);">2 — Female Literacy Is Equally Decisive</h3>
        <p style="font-size:14px; color:var(--text-secondary); line-height:1.6;">Female literacy (r = −0.545 with underweight, r = −0.539 with stunting) operates through improved care-seeking behavior, dietary diversity, and delayed marriage. Districts where literacy exceeds 85% show median stunting of <strong>27.3%</strong> — nearly 10 percentage points below the national mean.</p>
      </div>
      <div class="card" style="border-left: 3px solid var(--danger);">
        <h3 style="color:var(--danger);">3 — Early Marriage Is the Strongest Risk Factor</h3>
        <p style="font-size:14px; color:var(--text-secondary); line-height:1.6;">Child marriage (before 18) shows the strongest positive correlation with underweight (+0.481) and stunting (+0.428). Adolescent mothers are themselves nutritionally depleted, leading to intergenerational transmission of growth deficits.</p>
      </div>
      <div class="card" style="border-left: 3px solid var(--accent3);">
        <h3 style="color:var(--accent3);">4 — The Stunting–Wasting Duality Demands Distinct Strategies</h3>
        <p style="font-size:14px; color:var(--text-secondary); line-height:1.6;">Bihar and UP dominate stunting (chronic, developmental); Gujarat and Maharashtra dominate wasting (acute, emergency). Treating them interchangeably in policy is a <strong>resource misallocation error</strong>.</p>
      </div>
      <div class="card" style="border-left: 3px solid var(--text-muted);">
        <h3 style="color:var(--text-secondary);">5 — Water Access ≠ Water Safety</h3>
        <p style="font-size:14px; color:var(--text-secondary); line-height:1.6;">Near-universal "improved water source" coverage (median 97%) produces negligible correlation with malnutrition (r = −0.037). The indicator measures infrastructure type, not biological water safety or faecal contamination at the point of use.</p>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Correlation ≠ Causation — all findings are associational</span>
    <span>NIErnaya Phase 2</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 17: DELIVERABLES                                  ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide">
  <div class="slide-header">
    <span class="num">12</span>
    <h2>Deliverables & Methodology Summary</h2>
  </div>
  <div class="slide-body col-2">
    <div class="flex-col f1">
      <div class="card" style="flex:1;">
        <h3>📦 Output Inventory</h3>
        <table class="data-table">
          <tr><th>Artifact</th><th>Detail</th></tr>
          <tr><td class="val">Cleaned Dataset</td><td>706 × 14 factual CSV (53 KB)</td></tr>
          <tr><td class="val">Engineered Dataset</td><td>706 × 18 with composites (101 KB)</td></tr>
          <tr><td class="val">Metadata Codebook</td><td>14 variables, SDG-mapped (4.3 KB)</td></tr>
          <tr><td class="val">Visual Atlas</td><td>468 charts across 4 categories</td></tr>
          <tr><td class="val">Audit Reports</td><td>14 quality-assurance CSVs</td></tr>
          <tr><td class="val">PCA Outputs</td><td>Loadings, scores, scree, variance</td></tr>
          <tr><td class="val">GeoJSON Boundaries</td><td>Census 2011 district polygons</td></tr>
          <tr><td class="val">Technical Report</td><td>Comprehensive PDF (14 pages)</td></tr>
        </table>
      </div>
    </div>
    <div class="flex-col f1">
      <div class="card">
        <h3>🔧 Tools & Technologies Used</h3>
        <ul class="insight-list">
          <li><span class="bullet cyan"></span><span><strong>Python 3.13</strong> — Primary analytical language</span></li>
          <li><span class="bullet cyan"></span><span><strong>pandas 2.3</strong> — Data wrangling and pivot operations</span></li>
          <li><span class="bullet cyan"></span><span><strong>NumPy + SciPy</strong> — Statistical computation, z-scores, FDR correction</span></li>
          <li><span class="bullet cyan"></span><span><strong>scikit-learn 1.7</strong> — PCA, StandardScaler</span></li>
          <li><span class="bullet cyan"></span><span><strong>Matplotlib + Seaborn</strong> — 468 publication-grade charts</span></li>
          <li><span class="bullet cyan"></span><span><strong>GeoJSON / Census 2011</strong> — Spatial boundary alignment</span></li>
        </ul>
      </div>
      <div class="card">
        <h3>📋 Data Provenance</h3>
        <ul class="insight-list">
          <li><span class="bullet amber"></span><span><strong>NFHS-5 (2019–2021)</strong> — International Institute for Population Sciences (IIPS) & MoHFW, Govt. of India</span></li>
          <li><span class="bullet amber"></span><span><strong>Census of India 2011</strong> — District boundary codes and geospatial linkage</span></li>
          <li><span class="bullet green"></span><span><strong>Zero synthetic data</strong> — 100% authentic survey observations</span></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="slide-footer">
    <span>Project NIErnaya — Phase 2 Complete Submission</span>
    <span>NIErnaya 2026</span>
  </div>
</div>

<!-- ╔════════════════════════════════════════════════════════════╗ -->
<!-- ║  SLIDE 18: THANK YOU                                     ║ -->
<!-- ╚════════════════════════════════════════════════════════════╝ -->
<div class="slide title-slide">
  <div class="project-badge">NIErnaya 2026</div>
  <h1>Thank You</h1>
  <p class="subtitle">
    SDG 2 · Zero Hunger · Target 2.2<br>
    District-Level EDA, Preprocessing & Feature Engineering
  </p>
  <p class="meta" style="margin-top: 16px;">
    <span>706 Districts</span> · <span>468 Visualizations</span> · <span>100% Authentic NFHS-5 Data</span>
  </p>
</div>

</div><!-- /deck -->

<!-- ── NAVIGATION ── -->
<div class="nav-bar">
  <button class="nav-btn" onclick="navigate(-1)">◀ Previous</button>
  <span class="nav-counter" id="counter">1 / 18</span>
  <button class="nav-btn" onclick="navigate(1)">Next ▶</button>
</div>

<script>
let current = 0;
const slides = document.querySelectorAll('.slide');
const total = slides.length;
const counter = document.getElementById('counter');
const bar = document.getElementById('progressBar');

function showSlide(n) {{
  slides.forEach(s => s.classList.remove('active'));
  current = ((n % total) + total) % total;
  slides[current].classList.add('active');
  counter.textContent = (current + 1) + ' / ' + total;
  bar.style.width = ((current + 1) / total * 100) + '%';
}}

function navigate(dir) {{ showSlide(current + dir); }}

document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {{ navigate(1); e.preventDefault(); }}
  if (e.key === 'ArrowLeft' || e.key === 'Backspace') {{ navigate(-1); e.preventDefault(); }}
  if (e.key === 'Home') {{ showSlide(0); e.preventDefault(); }}
  if (e.key === 'End') {{ showSlide(total - 1); e.preventDefault(); }}
  if (e.key === 'f' || e.key === 'F') {{
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }}
}});

// Touch/swipe support
let touchStart = 0;
document.addEventListener('touchstart', e => {{ touchStart = e.changedTouches[0].screenX; }});
document.addEventListener('touchend', e => {{
  const diff = e.changedTouches[0].screenX - touchStart;
  if (Math.abs(diff) > 50) navigate(diff < 0 ? 1 : -1);
}});

showSlide(0);
</script>

</body>
</html>'''

out_path = os.path.join('03_Final_Report', 'NIErnaya_Phase2_Presentation_Deck.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

import re
total_slides = len(re.findall(r'<div class="slide[ "]', html))
print(f'[+] Presentation deck saved to: {os.path.abspath(out_path)}')
print(f'    File size: {os.path.getsize(out_path) / 1024:.1f} KB')
print(f'    Total slides: {total_slides}')



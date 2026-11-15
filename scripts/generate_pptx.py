#!/usr/bin/env python3
"""
NIErnaya Phase 2 — PowerPoint (.pptx) Presentation Deck Generator
Generates an 18-slide, 16:9 widescreen presentation deck with embedded charts,
metric callouts, styled tables, and formatted cards.
"""

import os
import io
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# ──────────────────────────────── Colors ─────────────────────────────────────
C_BG = RGBColor(15, 23, 42)          # Deep Navy Slate (#0F172A)
C_CARD = RGBColor(30, 41, 59)        # Card Slate (#1E293B)
C_BORDER = RGBColor(51, 65, 85)      # Border (#334155)
C_AMBER = RGBColor(245, 158, 11)     # Amber Accent (#F59E0B)
C_CYAN = RGBColor(6, 182, 212)       # Cyan Accent (#06B6D4)
C_PURPLE = RGBColor(139, 92, 246)    # Purple Accent (#8B5CF6)
C_RED = RGBColor(239, 68, 68)        # Coral Red (#EF4444)
C_GREEN = RGBColor(34, 197, 94)      # Emerald Green (#22C55E)
C_WHITE = RGBColor(241, 245, 249)    # Off-White Text (#F1F5F9)
C_MUTED = RGBColor(148, 163, 184)    # Slate Text (#94A3B8)
C_DARKMUTED = RGBColor(100, 116, 139) # Dark Muted (#64748B)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"


def img_to_bytes(path):
    """Convert WebP/PNG image to in-memory PNG bytes for python-pptx."""
    img = Image.open(path)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def set_bg(slide, color=C_BG):
    """Set slide solid background color."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, num_str, title_text, category_str=None):
    """Add modern standard header to content slide."""
    # Top badge/category
    if category_str:
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.3))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category_str.upper()
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_AMBER

    # Slide number + Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(0.6))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    
    # Number prefix
    r_num = p.add_run()
    r_num.text = f"{num_str}  |  "
    r_num.font.name = FONT_MONO
    r_num.font.size = Pt(20)
    r_num.font.bold = True
    r_num.font.color.rgb = C_AMBER
    
    # Title
    r_title = p.add_run()
    r_title.text = title_text
    r_title.font.name = FONT_HEADING
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = C_WHITE

    # Bottom line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER
    line.line.color.rgb = C_BORDER


def add_footer(slide, text_left="Source: NFHS-5 (IIPS & MoHFW, Govt. of India)", text_right="Project NIErnaya — Phase 2"):
    """Add minimal footer."""
    fb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(6.0), Inches(0.3))
    tf = fb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text_left
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = C_DARKMUTED

    fb2 = slide.shapes.add_textbox(Inches(6.8), Inches(7.05), Inches(5.733), Inches(0.3))
    tf2 = fb2.text_frame
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.RIGHT
    p2.text = text_right
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.color.rgb = C_DARKMUTED


def add_card(slide, left, top, width, height, bg_color=C_CARD, border_color=C_BORDER):
    """Add a container card shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape


def add_stat_box(slide, left, top, width, height, label, value, sub, accent_color=C_AMBER):
    """Add a KPI stat callout box."""
    add_card(slide, left, top, width, height)
    
    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Label
    p0 = tf.paragraphs[0]
    p0.text = label.upper()
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = C_MUTED
    p0.alignment = PP_ALIGN.CENTER

    # Value
    p1 = tf.add_paragraph()
    p1.text = str(value)
    p1.font.name = FONT_MONO
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = accent_color
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(2)
    p1.space_after = Pt(2)

    # Subtext
    if sub:
        p2 = tf.add_paragraph()
        p2.text = str(sub)
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_DARKMUTED
        p2.alignment = PP_ALIGN.CENTER


def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    print("[*] Generating 18 widescreen slides...")

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: Title Slide
    # ═════════════════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, RGBColor(10, 15, 26))

    # Decorative accent card in center
    add_card(s1, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), bg_color=RGBColor(17, 24, 39), border_color=C_BORDER)

    # Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.9), Inches(1.6), Inches(3.5), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(245, 158, 11)
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "PROJECT NIERNAYA 2026  ·  PHASE 2"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = PP_ALIGN.CENTER

    # Main Title
    tb = s1.shapes.add_textbox(Inches(2.0), Inches(2.3), Inches(9.333), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Decoding India's Child Malnutrition Crisis"
    p.font.name = FONT_HEADING
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = "District-Level Exploratory Data Analysis & Feature Engineering of the NFHS-5 Child Malnutrition Triad (SDG 2.2)"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_CYAN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    # Key metadata tags
    tb_meta = s1.shapes.add_textbox(Inches(2.0), Inches(4.3), Inches(9.333), Inches(0.6))
    tf_m = tb_meta.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "706 Factual Districts   ·   37 States & UTs   ·   10 Survey Indicators   ·   468 Visualizations"
    p_m.font.name = FONT_MONO
    p_m.font.size = Pt(13)
    p_m.font.bold = True
    p_m.font.color.rgb = C_AMBER
    p_m.alignment = PP_ALIGN.CENTER

    # Footer note
    tb_auth = s1.shapes.add_textbox(Inches(2.0), Inches(5.2), Inches(9.333), Inches(0.5))
    tf_a = tb_auth.text_frame
    p_a = tf_a.paragraphs[0]
    p_a.text = "Deliverable: Phase 2 Final Presentation  |  100% Authentic NFHS-5 Microdata (IIPS & MoHFW, Govt. of India)"
    p_a.font.name = FONT_BODY
    p_a.font.size = Pt(11)
    p_a.font.color.rgb = C_MUTED
    p_a.alignment = PP_ALIGN.CENTER

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: Problem Context & SDG 2.2
    # ═════════════════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "01", "The Problem Context: Target 2.2 Child Malnutrition Triad", "Problem Formulation")
    add_footer(s2)

    # 3 Stat Boxes across top
    add_stat_box(s2, Inches(0.8), Inches(1.45), Inches(3.64), Inches(1.3), "Stunted Children (HAZ < -2)", "33.5%", "National district average (chronic)", C_AMBER)
    add_stat_box(s2, Inches(4.84), Inches(1.45), Inches(3.64), Inches(1.3), "Wasted Children (WHZ < -2)", "18.5%", "Acute undernutrition (emergency)", C_RED)
    add_stat_box(s2, Inches(8.88), Inches(1.45), Inches(3.64), Inches(1.3), "Underweight (WAZ < -2)", "29.5%", "Composite growth deficit", C_PURPLE)

    # Left Narrative Card
    add_card(s2, Inches(0.8), Inches(2.95), Inches(5.67), Inches(3.85))
    tb_l = s2.shapes.add_textbox(Inches(1.05), Inches(3.1), Inches(5.17), Inches(3.55))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "🎯 UN SDG 2 (Zero Hunger) — Target 2.2 Mandate"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    points_l = [
        ("Stunting (Height-for-Age): ", "Chronic, irreversible growth & cognitive impairment from prolonged dietary deficit and enteric infections."),
        ("Wasting (Weight-for-Height): ", "Acute nutritional loss carrying 9x-12x higher immediate mortality risk; requires clinical intervention."),
        ("Underweight (Weight-for-Age): ", "Composite marker of both acute and chronic deprivation."),
        ("Global Burden: ", "India is home to >40 million stunted children — the largest absolute population of any country in the world.")
    ]
    for title, desc in points_l:
        p = tf_l.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + title
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r1.font.size = Pt(11)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(11)

    # Right Analytical Framework Card
    add_card(s2, Inches(6.87), Inches(2.95), Inches(5.67), Inches(3.85))
    tb_r = s2.shapes.add_textbox(Inches(7.12), Inches(3.1), Inches(5.17), Inches(3.55))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "📊 Our District-Level Empirical Framework"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    points_r = [
        ("Unit of Analysis: ", "706 administrative districts — the fundamental operational tier for Indian health administration."),
        ("Three Dependent Outcomes: ", "Stunting (%), Wasting (%), Underweight (%)."),
        ("Seven Multi-Sectoral Predictors: ", "Female literacy, improved sanitation, drinking water, 4+ ANC visits, child anaemia, child marriage, institutional births."),
        ("Zero Synthetic Values: ", "100% empirical fact-sheet records from NFHS-5 (2019–2021). No simulated data.")
    ]
    for title, desc in points_r:
        p = tf_r.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + title
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r1.font.size = Pt(11)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(11)

    # Highlight banner inside right card
    p_box = tf_r.add_paragraph()
    p_box.space_before = Pt(12)
    r = p_box.add_run()
    r.text = "Core Inquiry: Which structural interventions generate the highest marginal reduction in child malnutrition across India's districts?"
    r.font.bold = True
    r.font.color.rgb = C_AMBER
    r.font.size = Pt(10.5)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: Dataset Architecture & Quality Audit
    # ═════════════════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "02", "Dataset Architecture & Pre-Flight Quality Audit", "Data Governance")
    add_footer(s3)

    # 5 KPI cards across top
    add_stat_box(s3, Inches(0.8), Inches(1.45), Inches(2.18), Inches(1.2), "Districts", "706", "Factual units", C_CYAN)
    add_stat_box(s3, Inches(3.18), Inches(1.45), Inches(2.18), Inches(1.2), "States / UTs", "37", "Pan-India", C_AMBER)
    add_stat_box(s3, Inches(5.56), Inches(1.45), Inches(2.18), Inches(1.2), "Missing Values", "0%", "Analytical cells", C_GREEN)
    add_stat_box(s3, Inches(7.94), Inches(1.45), Inches(2.18), Inches(1.2), "Duplicates", "0", "Primary keys", C_GREEN)
    add_stat_box(s3, Inches(10.32), Inches(1.45), Inches(2.18), Inches(1.2), "Variables", "14", "4 IDs + 10 metrics", C_PURPLE)

    # Left: Variable Architecture Table
    add_card(s3, Inches(0.8), Inches(2.85), Inches(6.0), Inches(3.95))
    tb_t = s3.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(5.6), Inches(0.4))
    p = tb_t.text_frame.paragraphs[0]
    p.text = "VARIABLE ARCHITECTURE (14 COLUMNS)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    # Table
    table_shape = s3.shapes.add_table(5, 3, Inches(1.0), Inches(3.45), Inches(5.6), Inches(3.1))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.6)
    tbl.columns[1].width = Inches(3.3)
    tbl.columns[2].width = Inches(0.7)

    headers = ["Role", "Variables", "Count"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(40, 53, 73)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_AMBER

    rows_data = [
        ("Primary Keys", "district_name, state_name, district_code, state_code", "4"),
        ("Outcomes (SDG 2.2)", "stunting_pct, wasting_pct, underweight_pct", "3"),
        ("WASH Predictors", "improved_sanitation_pct, improved_water_pct", "2"),
        ("Health & Social", "female_literacy, anc_4plus, anemia, child_marriage, inst_births", "5")
    ]
    for r_idx, (role, vars_str, cnt) in enumerate(rows_data, start=1):
        tbl.cell(r_idx, 0).text = role
        tbl.cell(r_idx, 1).text = vars_str
        tbl.cell(r_idx, 2).text = cnt
        for c_idx in range(3):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_WHITE if c_idx == 0 else C_MUTED

    # Right: Quality Audit Checklist
    add_card(s3, Inches(7.1), Inches(2.85), Inches(5.433), Inches(3.95))
    tb_q = s3.shapes.add_textbox(Inches(7.3), Inches(3.0), Inches(5.0), Inches(3.6))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True
    p = tf_q.paragraphs[0]
    p.text = "DATA QUALITY VERIFICATION RESULTS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    checks = [
        ("Range Validation: ", "100% of percentage values fall strictly within [0.0%, 100.0%]. Passed.", C_GREEN),
        ("Missingness Audit: ", "0 missing values across all 10 analytical indicators across 706 districts.", C_GREEN),
        ("Duplicate Screening: ", "Zero duplicate rows and zero duplicate (State, District) keys detected.", C_GREEN),
        ("IQR Outlier Screening: ", "92 values flagged by 1.5x IQR. All retained — extreme values represent authentic high-burden districts (e.g., Karimganj 48% wasting).", C_AMBER),
        ("Census 2011 Linkage: ", "641/706 districts mapped to Census 2011 codes. 65 post-2011 districts retained without imputation to preserve boundary integrity.", C_CYAN),
        ("Data Provenance: ", "Direct extraction from official IIPS district fact sheets. Zero synthetic numbers.", C_GREEN)
    ]
    for title, desc, col in checks:
        p = tf_q.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + title
        r1.font.bold = True
        r1.font.color.rgb = col
        r1.font.size = Pt(10)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(9.5)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: Section I Divider — Exploratory Data Analysis
    # ═════════════════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, RGBColor(10, 15, 26))
    add_card(s4, Inches(2.0), Inches(2.0), Inches(9.333), Inches(3.5), bg_color=C_CARD, border_color=C_BORDER)

    tb = s4.shapes.add_textbox(Inches(2.5), Inches(2.5), Inches(8.333), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SECTION I"
    p.font.name = FONT_MONO
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Exploratory Data Analysis"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(38)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Distribution Dynamics  ·  State-Level Disparities  ·  Spatial Hotspots"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(15)
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 5: Outcome Distribution Analysis
    # ═════════════════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "03", "Malnutrition Triad: Distribution & Spread Across 706 Districts", "Exploratory Analysis")
    add_footer(s5)

    # Top Stat summary
    add_stat_box(s5, Inches(0.8), Inches(1.45), Inches(3.64), Inches(1.15), "Stunting (HAZ < -2)", "μ = 33.51%", "Range: 13.2% - 60.6% | σ = 8.47%", C_AMBER)
    add_stat_box(s5, Inches(4.84), Inches(1.45), Inches(3.64), Inches(1.15), "Wasting (WHZ < -2)", "μ = 18.54%", "Range: 4.5% - 48.0% | σ = 6.48%", C_RED)
    add_stat_box(s5, Inches(8.88), Inches(1.45), Inches(3.64), Inches(1.15), "Underweight (WAZ < -2)", "μ = 29.50%", "Range: 7.2% - 62.4% | σ = 9.68%", C_PURPLE)

    # 3 Charts across bottom
    s5.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/boxplot_outcomes.webp"), Inches(0.8), Inches(2.75), Inches(3.7), Inches(4.0))
    s5.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/hist_stunting_pct.webp"), Inches(4.8), Inches(2.75), Inches(3.7), Inches(4.0))
    s5.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/hist_wasting_pct.webp"), Inches(8.8), Inches(2.75), Inches(3.7), Inches(4.0))

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 6: State Rankings — Stunting vs Wasting
    # ═════════════════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "04", "State-Level Disparities: Ranked District Averages", "Comparative Analysis")
    add_footer(s6, "State summaries are unweighted means of district values across 706 districts")

    # Left chart: Stunting
    s6.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/statewise_stunting_pct.webp"), Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.3))

    # Right chart: Wasting
    s6.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/statewise_wasting_pct.webp"), Inches(6.9), Inches(1.45), Inches(5.6), Inches(5.3))

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 7: Geographic Maps & The Duality Finding
    # ═════════════════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "05", "Geographic Hotspots: The Stunting–Wasting Spatial Duality", "Geographic Patterns")
    add_footer(s7, "State-level choropleths based on Census 2011 boundaries")

    # Two map images side by side
    s7.shapes.add_picture(img_to_bytes("01_Visual_Atlas/04_Geographical_Maps/MAIN_STATE_MAP_stunting_pct.webp"), Inches(0.8), Inches(1.45), Inches(5.6), Inches(4.2))
    s7.shapes.add_picture(img_to_bytes("01_Visual_Atlas/04_Geographical_Maps/MAIN_STATE_MAP_wasting_pct.webp"), Inches(6.9), Inches(1.45), Inches(5.6), Inches(4.2))

    # Bottom Callout Card
    add_card(s7, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.15), bg_color=C_CARD, border_color=C_AMBER)
    tb_c = s7.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(11.333), Inches(0.95))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "CORE POLICY INSIGHT: THE STUNTING–WASTING PHENOTYPIC DUALITY"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    p2 = tf_c.add_paragraph()
    p2.text = "• Chronic Stunting concentrates in the northern & eastern Gangetic belt (Meghalaya 43.0%, Bihar 42.6%, Jharkhand 40.2%, UP 39.6%).\n• Acute Wasting concentrates in western & central states (Gujarat 26.1%, Maharashtra 25.8%, Bihar 24.2%).\n• Programmatic Impact: Treating stunting and wasting interchangeably in scheme allocations leads to strategic misallocation. Wasting requires emergency therapeutic nutrition, while stunting requires multi-year WASH and girl-child investments."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 8: Section II Divider — Correlation & Statistical Analysis
    # ═════════════════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, RGBColor(10, 15, 26))
    add_card(s8, Inches(2.0), Inches(2.0), Inches(9.333), Inches(3.5), bg_color=C_CARD, border_color=C_BORDER)

    tb = s8.shapes.add_textbox(Inches(2.5), Inches(2.5), Inches(8.333), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SECTION II"
    p.font.name = FONT_MONO
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Correlation & Statistical Inference"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(38)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Pearson & Spearman Matrices  ·  FDR Significance  ·  Multi-Sectoral Levers"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(15)
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 9: Correlation Heatmaps
    # ═════════════════════════════════════════════════════════════════════════
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "06", "Correlation Matrices: Pearson (Linear) & Spearman (Monotonic)", "Statistical Analysis")
    add_footer(s9, "All 21 predictor-outcome correlations adjusted for False Discovery Rate (Benjamini-Hochberg)")

    # Left: Pearson Heatmap
    s9.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/pearson_correlation.webp"), Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.3))

    # Right: Spearman Heatmap
    s9.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/spearman_correlation.webp"), Inches(6.9), Inches(1.45), Inches(5.6), Inches(5.3))

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 10: Top Correlates Table & Interpretation
    # ═════════════════════════════════════════════════════════════════════════
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "07", "Multi-Sectoral Associations: The Strongest Levers", "Driver Quantification")
    add_footer(s10, "p < 0.001 for all entries except improved water | VIF across all 7 predictors in [1.19, 2.50]")

    # League Table
    add_card(s10, Inches(0.8), Inches(1.45), Inches(11.733), Inches(4.0))
    table_shape = s10.shapes.add_table(10, 5, Inches(1.0), Inches(1.6), Inches(11.333), Inches(3.6))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.8)
    tbl.columns[1].width = Inches(2.0)
    tbl.columns[2].width = Inches(1.4)
    tbl.columns[3].width = Inches(1.4)
    tbl.columns[4].width = Inches(3.733)

    t_headers = ["Predictor Indicator", "Malnutrition Outcome", "Pearson r", "Spearman ρ", "Policy Interpretation"]
    for i, h in enumerate(t_headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(40, 53, 73)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_AMBER

    corr_rows = [
        ("Improved Sanitation", "Underweight", "-0.583", "-0.585", "Strongest single protective association; environmental enteropathy barrier"),
        ("Female Literacy (15-49 yrs)", "Underweight", "-0.545", "-0.549", "Maternal agency & dietary literacy strongly protective"),
        ("Female Literacy (15-49 yrs)", "Stunting", "-0.539", "-0.520", "Key chronic protection; delays marriage, empowers nutrition choices"),
        ("Improved Sanitation", "Stunting", "-0.503", "-0.495", "Eliminating open defecation directly curtails chronic linear stunting"),
        ("Early Marriage (<18 yrs)", "Underweight", "+0.481", "+0.511", "Strongest vulnerability driver; adolescent pregnancy depletes infant"),
        ("Early Marriage (<18 yrs)", "Stunting", "+0.428", "+0.457", "Intergenerational transmission of maternal malnutrition"),
        ("Child Anaemia (6-59 mos)", "Underweight", "+0.403", "+0.386", "Severe comorbid nutritional & micronutrient deficit"),
        ("Antenatal Care (4+ ANC)", "Stunting", "-0.361", "-0.355", "Clinical maternal care provides vital micronutrient & fetal protection"),
        ("Improved Drinking Water", "Stunting", "-0.037", "-0.037", "Negligible correlation: ceiling effect (97% median) & unmeasured water quality")
    ]
    for r_idx, (p_name, o_name, pr, sr, interp) in enumerate(corr_rows, start=1):
        tbl.cell(r_idx, 0).text = p_name
        tbl.cell(r_idx, 1).text = o_name
        tbl.cell(r_idx, 2).text = pr
        tbl.cell(r_idx, 3).text = sr
        tbl.cell(r_idx, 4).text = interp
        
        # Color coding
        for c_idx in range(5):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if c_idx == 2 or c_idx == 3:
                p.font.name = FONT_MONO
                p.font.bold = True
                p.font.color.rgb = C_GREEN if "-" in pr else (C_RED if "+" in pr else C_MUTED)
            elif c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
            else:
                p.font.color.rgb = C_MUTED

    # Bottom Highlight Note
    add_card(s10, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.2), bg_color=C_CARD, border_color=C_AMBER)
    tb_b = s10.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.333), Inches(1.0))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "💡 WHY IS WATER ACCESS UNCORRELATED (r = -0.037)?"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = tf_b.add_paragraph()
    p2.text = "1. Statistical Ceiling Effect: Piped/tubewell infrastructure coverage has reached a median of 97.0% across districts, leaving minimal variance to correlate.\n2. Quantity vs. Quality: NFHS-5 tracks proximity to improved source, NOT bacteriological safety or point-of-use fecal contamination."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 11: Bivariate Scatter Evidence
    # ═════════════════════════════════════════════════════════════════════════
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "08", "Bivariate Evidence: District-Level Scatter Gradients (N = 706)", "Empirical Verification")
    add_footer(s11, "Each circle represents one district | Red OLS line with 95% confidence interval")

    # 2x2 grid of scatter plots
    s11.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/scatter_improved_sanitation_pct_vs_stunting_pct.webp"), Inches(0.8), Inches(1.45), Inches(5.6), Inches(2.65))
    s11.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/scatter_female_literacy_pct_vs_underweight_pct.webp"), Inches(6.9), Inches(1.45), Inches(5.6), Inches(2.65))
    s11.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/scatter_early_marriage_pct_vs_stunting_pct.webp"), Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.65))
    s11.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/scatter_child_anemia_pct_vs_underweight_pct.webp"), Inches(6.9), Inches(4.25), Inches(5.6), Inches(2.65))

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 12: Section III Divider — Preprocessing & Feature Engineering
    # ═════════════════════════════════════════════════════════════════════════
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12, RGBColor(10, 15, 26))
    add_card(s12, Inches(2.0), Inches(2.0), Inches(9.333), Inches(3.5), bg_color=C_CARD, border_color=C_BORDER)

    tb = s12.shapes.add_textbox(Inches(2.5), Inches(2.5), Inches(8.333), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SECTION III"
    p.font.name = FONT_MONO
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Preprocessing & Feature Engineering"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(38)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Composite Indicators  ·  PCA Dimensionality  ·  Target Leakage Guards"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(15)
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 13: Engineered Composite Features
    # ═════════════════════════════════════════════════════════════════════════
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, "09", "Engineered Domain Features & Analytical Formulations", "Feature Engineering")
    add_footer(s13, "Engineered dataset saved: main_nfhs5_engineered.csv (706 rows x 18 columns)")

    # 4 Stat Boxes for features
    add_stat_box(s13, Inches(0.8), Inches(1.45), Inches(2.68), Inches(1.3), "Socioeconomic Vulnerability", "r = +0.583", "(z(marriage) - z(lit)) / 2", C_AMBER)
    add_stat_box(s13, Inches(3.81), Inches(1.45), Inches(2.68), Inches(1.3), "Sanitation-Water Gap", "r = +0.507", "Water% - Sanitation%", C_CYAN)
    add_stat_box(s13, Inches(6.82), Inches(1.45), Inches(2.68), Inches(1.3), "Maternal Care Gap", "r = +0.147", "Inst. Births% - ANC 4+%", C_PURPLE)
    add_stat_box(s13, Inches(9.83), Inches(1.45), Inches(2.68), Inches(1.3), "Nutritional Burden Index", "DESCRIPTIVE", "Mean(Stunt, Waste, Underw)", C_RED)

    # Left Card: Detailed Logic
    add_card(s13, Inches(0.8), Inches(2.95), Inches(6.0), Inches(3.85))
    tb_el = s13.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(5.6), Inches(3.55))
    tf_el = tb_el.text_frame
    tf_el.word_wrap = True
    p = tf_el.paragraphs[0]
    p.text = "ENGINEERED FEATURE MECHANISMS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    feat_desc = [
        ("Socioeconomic Vulnerability Index (r = +0.58): ", "Combines normalized child marriage risk with educational deficit. Directly accounts for patriarchal norms and girl-child marginalization."),
        ("Sanitation-Water Gap (r = +0.51): ", "Quantifies WASH imbalance where piped water access exists without corresponding toilet facilities, driving severe bacterial runoff into groundwater."),
        ("Maternal Care Gap (r = +0.15): ", "Identifies districts where mothers utilize clinics for emergency delivery but lacked preventive care throughout gestation.")
    ]
    for title, desc in feat_desc:
        p = tf_el.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + title
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r1.font.size = Pt(10.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(10)

    # Right Card: Leakage Guard
    add_card(s13, Inches(7.1), Inches(2.95), Inches(5.433), Inches(3.85))
    tb_er = s13.shapes.add_textbox(Inches(7.3), Inches(3.1), Inches(5.0), Inches(3.55))
    tf_er = tb_er.text_frame
    tf_er.word_wrap = True
    p = tf_er.paragraphs[0]
    p.text = "🛡️ CRITICAL DATA LEAKAGE SAFEGUARD"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_RED

    leak_points = [
        ("Target Leakage Quarantine: ", "The Nutritional Burden Index is constructed from Stunting, Wasting, and Underweight. It is strictly quarantined for descriptive district profiling and NEVER used as an input feature for regression modeling."),
        ("Standardization Integrity: ", "All z-score scaling and PCA transformations are computed strictly on the predictor matrix, completely isolated from target outcomes."),
        ("Conservative Code Imputation: ", "65 newly formed districts (post-Census 2011) have null census codes. These are left as null rather than using synthetic KNN imputation to prevent geographic distortion.")
    ]
    for title, desc in leak_points:
        p = tf_er.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + title
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r1.font.size = Pt(10.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(10)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 14: PCA Dimensionality Reduction
    # ═════════════════════════════════════════════════════════════════════════
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "10", "Principal Component Analysis (PCA): Latent Structural Axes", "Dimensionality Reduction")
    add_footer(s14, "PCA performed on 7 standardized predictors across 706 districts | Kaiser Criterion: Eigenvalue > 1.0")

    # Scree Plot
    s14.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/pca_scree.webp"), Inches(0.8), Inches(1.45), Inches(5.6), Inches(4.0))

    # Loadings Chart
    s14.shapes.add_picture(img_to_bytes("01_Visual_Atlas/01_Main_NFHS5/pca_loadings.webp"), Inches(6.9), Inches(1.45), Inches(5.6), Inches(4.0))

    # Bottom Variance Card
    add_card(s14, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.35), bg_color=C_CARD, border_color=C_CYAN)
    tb_p = s14.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.333), Inches(1.15))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "PCA INTERPRETATION: TWO ORTHOGONAL FORCES EXPLAIN 62.70% OF PREDICTOR VARIANCE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    p2 = tf_p.add_paragraph()
    p2.text = "• PC1 (39.31% Variance | Eigenvalue 2.76) — 'Socioeconomic Infrastructure Axis': Loads heavily on female literacy (-0.52) and improved sanitation (-0.48); opposing child marriage (+0.44) and anemia (+0.28). Represents foundational developmental capacity.\n• PC2 (23.39% Variance | Eigenvalue 1.64) — 'Healthcare Contact Axis': Loads on institutional births (-0.56), child anemia (-0.50), improved water (-0.45), and ANC 4+ (-0.40). Reflects institutional medical engagement."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 15: Section IV Divider — Policy Insights & Conclusion
    # ═════════════════════════════════════════════════════════════════════════
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15, RGBColor(10, 15, 26))
    add_card(s15, Inches(2.0), Inches(2.0), Inches(9.333), Inches(3.5), bg_color=C_CARD, border_color=C_BORDER)

    tb = s15.shapes.add_textbox(Inches(2.5), Inches(2.5), Inches(8.333), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SECTION IV"
    p.font.name = FONT_MONO
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Evidence-Based Policy Insights"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(38)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Actionable Recommendations  ·  Schematic Realignment  ·  Phase 2 Conclusion"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(15)
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 16: Five Core Policy Insights
    # ═════════════════════════════════════════════════════════════════════════
    s16 = prs.slides.add_slide(blank_layout)
    set_bg(s16)
    add_header(s16, "11", "Five Evidence-Based Insights for National Malnutrition Policy", "Policy Strategy")
    add_footer(s16, "Aligned with POSHAN Abhiyaan 2.0, Swachh Bharat Mission, and Jal Jeevan Mission")

    insights = [
        ("1. Sanitation is a Direct Nutrition Intervention", "Improved sanitation (r = -0.58) acts through the environmental enteropathy pathway. Without functional latrines, chronic subclinical gut inflammation prevents nutrient absorption regardless of food intake. SBM must be integrated directly into POSHAN 2.0.", C_AMBER),
        ("2. Girls' Secondary Education is Nutritional Insurance", "Female literacy (r = -0.55) empowers maternal feeding autonomy, delayed childbearing, and care-seeking behavior. Districts with >85% literacy display 10% lower stunting on average.", C_CYAN),
        ("3. Eradicate Early Child Marriage to Break Intergenerational Deficits", "Child marriage (r = +0.48) is the primary driver of adolescent pregnancy, low birth weight, and poor maternal lactation reserve. Enforcing marriage laws is fundamental to child health.", C_RED),
        ("4. Realign Programmatic Targets to the Stunting-Wasting Duality", "Northern/Eastern states (Bihar, UP, Meghalaya) require long-term linear stunting programs (WASH, school meals); Western states (Gujarat, Maharashtra) need acute emergency wasting protocols (SAM centers, therapeutic feeding).", C_PURPLE),
        ("5. Shift Water Policy from Coverage Quantity to Point-of-Use Biological Safety", "Near-universal coverage of improved water infrastructure (median 97%) yields r = -0.037 with malnutrition. Testing for E. coli at the kitchen tap is the missing link.", C_GREEN)
    ]

    card_h = Inches(0.95)
    start_y = Inches(1.45)
    gap = Inches(0.12)

    for idx, (title, desc, acc_col) in enumerate(insights):
        y_pos = start_y + idx * (card_h + gap)
        add_card(s16, Inches(0.8), y_pos, Inches(11.733), card_h)
        
        # Accent strip on left of card
        strip = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos, Inches(0.1), card_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = acc_col
        strip.line.fill.background()

        tb_i = s16.shapes.add_textbox(Inches(1.05), y_pos + Inches(0.08), Inches(11.3), card_h - Inches(0.16))
        tf_i = tb_i.text_frame
        tf_i.word_wrap = True
        
        p = tf_i.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = acc_col

        p2 = tf_i.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_WHITE
        p2.space_before = Pt(2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 17: Deliverables & Tech Stack
    # ═════════════════════════════════════════════════════════════════════════
    s17 = prs.slides.add_slide(blank_layout)
    set_bg(s17)
    add_header(s17, "12", "Deliverables Manifest & Technology Stack", "Project Governance")
    add_footer(s17)

    # Left: Output Inventory Table
    add_card(s17, Inches(0.8), Inches(1.45), Inches(5.67), Inches(5.3))
    tb_del = s17.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.27), Inches(0.35))
    p = tb_del.text_frame.paragraphs[0]
    p.text = "PHASE 2 DELIVERABLES MANIFEST"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    table_del = s17.shapes.add_table(8, 2, Inches(1.0), Inches(2.05), Inches(5.27), Inches(4.4))
    tbl_d = table_del.table
    tbl_d.columns[0].width = Inches(2.4)
    tbl_d.columns[1].width = Inches(2.87)

    d_headers = ["Artifact", "Specification"]
    for i, h in enumerate(d_headers):
        cell = tbl_d.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(40, 53, 73)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_AMBER

    del_rows = [
        ("Cleaned Factual CSV", "706 districts x 14 columns (53 KB)"),
        ("Engineered CSV", "706 districts x 18 features (101 KB)"),
        ("Metadata Codebook", "Detailed dictionary mapped to SDG targets"),
        ("Visual Atlas", "468 WebP charts across 4 directories"),
        ("Audit Reports", "14 quality assurance CSVs in 01_Audit"),
        ("PCA Outputs", "Loadings, scores, scree, variance tables"),
        ("Final Technical Report", "14-page PDF document in 03_Final_Report")
    ]
    for r_idx, (art, spec) in enumerate(del_rows, start=1):
        tbl_d.cell(r_idx, 0).text = art
        tbl_d.cell(r_idx, 1).text = spec
        for c_idx in range(2):
            cell = tbl_d.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_WHITE if c_idx == 0 else C_MUTED

    # Right: Tech Stack & Provenance Cards
    add_card(s17, Inches(6.87), Inches(1.45), Inches(5.67), Inches(2.55))
    tb_ts = s17.shapes.add_textbox(Inches(7.1), Inches(1.6), Inches(5.2), Inches(2.25))
    tf_ts = tb_ts.text_frame
    tf_ts.word_wrap = True
    p = tf_ts.paragraphs[0]
    p.text = "🛠️ TOOLS & TECHNOLOGIES USED"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    tools = [
        ("Python 3.13: ", "Core programming language for end-to-end data pipeline"),
        ("pandas 2.3 + NumPy: ", "Data pivoting, array operations, missingness audits"),
        ("SciPy + Statsmodels: ", "Spearman rank, Benjamini-Hochberg FDR correction, VIF"),
        ("scikit-learn 1.7: ", "StandardScaler, Principal Component Analysis (PCA)"),
        ("Matplotlib + Seaborn: ", "468 publication-grade visualization charts")
    ]
    for name, desc in tools:
        p = tf_ts.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + name
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r1.font.size = Pt(9.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(9.5)

    add_card(s17, Inches(6.87), Inches(4.2), Inches(5.67), Inches(2.55))
    tb_pr = s17.shapes.add_textbox(Inches(7.1), Inches(4.35), Inches(5.2), Inches(2.25))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True
    p = tf_pr.paragraphs[0]
    p.text = "🏛️ DATA PROVENANCE & REPRODUCIBILITY"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    provs = [
        ("Primary Source: ", "Fifth National Family Health Survey (NFHS-5, 2019-2021)"),
        ("Nodal Agencies: ", "IIPS Mumbai & MoHFW, Government of India"),
        ("Spatial Boundaries: ", "Census of India 2011 district polygons (Geohacker)"),
        ("Zero Synthetic Values: ", "All observations strictly verified from published survey data"),
        ("Reproducibility: ", "Single-command execution scripts for audit, EDA, PCA, and reporting")
    ]
    for name, desc in provs:
        p = tf_pr.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + name
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r1.font.size = Pt(9.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = C_MUTED
        r2.font.size = Pt(9.5)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 18: Conclusion & Thank You
    # ═════════════════════════════════════════════════════════════════════════
    s18 = prs.slides.add_slide(blank_layout)
    set_bg(s18, RGBColor(10, 15, 26))

    add_card(s18, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), bg_color=RGBColor(17, 24, 39), border_color=C_BORDER)

    badge = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.9), Inches(1.7), Inches(3.5), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(245, 158, 11)
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "PROJECT NIERNAYA 2026"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = PP_ALIGN.CENTER

    tb = s18.shapes.add_textbox(Inches(2.0), Inches(2.4), Inches(9.333), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Thank You"
    p.font.name = FONT_HEADING
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Targeting Zero Hunger (SDG 2.2) Through District-Level Precision Analytics"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(17)
    p2.font.color.rgb = C_CYAN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(8)

    tb_s = s18.shapes.add_textbox(Inches(2.0), Inches(4.2), Inches(9.333), Inches(0.6))
    tf_s = tb_s.text_frame
    p_s = tf_s.paragraphs[0]
    p_s.text = "706 Factual Districts  ·  468 Charts  ·  7 Multi-Sectoral Predictors  ·  62.7% PCA Variance"
    p_s.font.name = FONT_MONO
    p_s.font.size = Pt(13)
    p_s.font.bold = True
    p_s.font.color.rgb = C_AMBER
    p_s.alignment = PP_ALIGN.CENTER

    tb_q = s18.shapes.add_textbox(Inches(2.0), Inches(5.1), Inches(9.333), Inches(0.6))
    tf_q = tb_q.text_frame
    p_q = tf_q.paragraphs[0]
    p_q.text = "We welcome questions, discussion, and feedback from the evaluators."
    p_q.font.name = FONT_BODY
    p_q.font.size = Pt(13)
    p_q.font.color.rgb = C_MUTED
    p_q.alignment = PP_ALIGN.CENTER

    # Save
    out_pptx = os.path.join("03_Final_Report", "NIErnaya_Phase2_Presentation_Deck.pptx")
    prs.save(out_pptx)
    print(f"[+] PowerPoint presentation successfully created: {os.path.abspath(out_pptx)}")
    print(f"    File size: {os.path.getsize(out_pptx) / 1024:.1f} KB")
    print(f"    Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    create_presentation()


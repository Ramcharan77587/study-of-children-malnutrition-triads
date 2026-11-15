# -*- coding: utf-8 -*-
"""
compile_guide.py - Master Compiler for NIErnaya Phase 2 Presentation Companion & Encyclopedic Glossary
"""

import os
import sys
import subprocess
from pathlib import Path

# Add sections directory to path
SECTIONS_DIR = Path(__file__).resolve().parent / "sections"
sys.path.insert(0, str(SECTIONS_DIR))

from s1_intro import get_intro_markdown
from s2_slides import get_slides_markdown
from s3_glossary import get_glossary_markdown
from s4_defense import get_defense_markdown

OUT_DIR = Path(__file__).resolve().parent
md_file = OUT_DIR / "NIErnaya_Phase2_Presentation_Guide_and_Speaker_Notes.md"
html_file = OUT_DIR / "NIErnaya_Phase2_Presentation_Guide_and_Speaker_Notes.html"
pdf_file = OUT_DIR / "NIErnaya_Phase2_Presentation_Guide_and_Speaker_Notes.pdf"

print("1. Assembling Master Markdown...")
md_content = "\n\n".join([
    get_intro_markdown(),
    get_slides_markdown(),
    get_glossary_markdown(),
    get_defense_markdown()
])

with open(md_file, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"✔ Wrote Markdown: {md_file} ({len(md_content):,} chars)")

print("2. Converting Markdown to Executive Print-Ready HTML...")
# Convert markdown to HTML using markdown library or custom clean converter
import markdown

html_body = markdown.markdown(
    md_content,
    extensions=["tables", "fenced_code", "nl2br", "sane_lists", "toc"]
)

# Custom enhancements for executive presentation styling
html_full = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Project NIErnaya — Complete Phase 2 Presentation Companion & Encyclopedic Glossary</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }}

  h1, h2, h3, h4, h5 {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0f172a;
    font-weight: 700;
    line-height: 1.25;
    margin-top: 1.4em;
    margin-bottom: 0.5em;
  }}

  h1 {{
    font-size: 20pt;
    color: #0369a1;
    border-bottom: 3px solid #0284c7;
    padding-bottom: 8px;
    margin-top: 0;
  }}

  h2 {{
    font-size: 15pt;
    color: #0f172a;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 5px;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 13pt;
    color: #0284c7;
    margin-top: 1.2em;
    page-break-after: avoid;
  }}

  h4 {{
    font-size: 11pt;
    color: #334155;
    margin-top: 1em;
    page-break-after: avoid;
  }}

  p, li {{
    font-size: 10.5pt;
    color: #334155;
  }}

  strong {{
    color: #0f172a;
    font-weight: 600;
  }}

  blockquote {{
    background: #f8fafc;
    border-left: 4px solid #0284c7;
    margin: 12px 0;
    padding: 10px 16px;
    font-style: italic;
    color: #1e293b;
    border-radius: 0 6px 6px 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  code {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 9pt;
    background: #f1f5f9;
    padding: 2px 5px;
    border-radius: 4px;
    color: #0369a1;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 24px 0;
  }}

  .cover-card {{
    background: linear-gradient(135deg, #091322 0%, #11253e 100%);
    color: #ffffff;
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 24px;
    page-break-after: always;
  }}
  .cover-card h1 {{
    color: #38bdf8;
    border-bottom: 2px solid #0284c7;
    font-size: 22pt;
  }}
  .cover-card p {{
    color: #e2e8f0;
    font-size: 11pt;
  }}

  /* Page breaks management */
  .page-break {{
    page-break-before: always;
  }}

  /* Avoid awkward breaks inside lists or slide blocks */
  ul, ol {{
    page-break-inside: auto;
  }}
  li {{
    page-break-inside: avoid;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_full)
print(f"✔ Wrote HTML: {html_file} ({len(html_full):,} chars)")

print("3. Compiling PDF via Headless Browser (Edge/Chrome)...")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

browser_bin = edge_path if os.path.exists(edge_path) else chrome_path

if not os.path.exists(browser_bin):
    print(f"ERROR: No supported headless browser found at {browser_bin}")
    sys.exit(1)

cmd = [
    browser_bin,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_file.resolve()}",
    str(html_file.resolve())
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 0:
    print(f"✔ SUCCESS! PDF generated: {pdf_file}")
    print(f"  File size: {os.path.getsize(pdf_file):,} bytes")
else:
    print(f"ERROR: PDF compilation failed. Returncode: {res.returncode}")
    print(f"Stderr: {res.stderr}")
    sys.exit(1)

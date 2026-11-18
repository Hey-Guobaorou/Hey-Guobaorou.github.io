"""Build the A3 course page from the report Markdown and A2 page styling.

Requires markdown-it-py. Run: python ARCH7476/build_a3_page.py
"""
from pathlib import Path
import html
import re
from markdown_it import MarkdownIt

here = Path(__file__).resolve().parent
source = (here / "a3-assets" / "A3_report.md").read_text(encoding="utf-8")
a2 = (here / "a2-thermal-comfort-workflow.html").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", a2, re.S).group(1)
css += """\n.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0 0}.hero-actions a{border:1px solid #b9c8cd;padding:8px 12px;text-decoration:none;font-size:14px;font-weight:600}.hero-actions a:first-child{background:#277e8e;color:white;border-color:#277e8e}figure{margin:22px 0}figure img{display:block;width:100%;height:auto;border:1px solid #d5dadd}figcaption{color:#647078;font-size:13px;margin-top:8px}.report-table{overflow-x:auto;margin:18px 0 22px}.report-table table{min-width:680px}.report-table code{white-space:nowrap}pre{background:#f4f5f6;border:1px solid #dfe3e5;padding:18px;overflow:auto;font-size:13px}code{font-family:Consolas,monospace;font-size:.9em}section h2{margin-top:0}@media print{.hero-actions{display:none}figure{break-inside:avoid}}\n"""
source = source.replace("](figure_", "](a3-assets/figure_")
source = source.replace("<!-- page -->", "")
source = re.sub(r"(?<!\]\()https?://[^\s;]+", lambda m: f"<{m.group(0)}>", source)
body = MarkdownIt("commonmark", {"html": True}).enable("table").render(source)
body = re.sub(r"<h1>.*?</h1>\s*<h1>.*?</h1>", "", body, count=1, flags=re.S)
body = re.sub(r"<p><strong>PeopleComfort v0\.2\.0.*?</p>", "", body, count=1, flags=re.S)
titles = [
    ("Four-line research summary", "summary"),
    ("Research background and question", "background"),
    ("1. Prototype Scope", "scope"),
    ("1.1 Hypothesis and rival explanations", "hypothesis"),
    ("2. Workflow Artifact and reproducibility", "artifact"),
    ("3. Workflow Description", "workflow"),
    ("4. Generative Loop and method rationale", "loop"),
    ("5. Prototype Output and design interpretation", "output"),
    ("6. Verification and Failure Log", "verification"),
    ("7. AI-Assisted Fact-Checking Card", "ai-card"),
    ("8. A4 extension", "a4"),
    ("References", "references"),
]
body = body.replace("<h3>1.1 Hypothesis", '<h3 id="hypothesis">1.1 Hypothesis')
for title, anchor in titles:
    body = body.replace(f"<h2>{html.escape(title)}</h2>", f'<h2 id="{anchor}">{html.escape(title)}</h2>', 1)
body = re.sub(r"<p><img src=\"([^\"]+)\" alt=\"([^\"]+)\" ?/?></p>", lambda m: f'<figure><a href="{m.group(1)}" target="_blank" rel="noopener"><img src="{m.group(1)}" alt="{m.group(2)}" loading="lazy"></a><figcaption>{m.group(2)}</figcaption></figure>', body)
body = re.sub(r"(<table>.*?</table>)", r'<div class="report-table">\1</div>', body, flags=re.S)
card_url = "a3-ai-fact-checking-card.html"
before, card_section = body.split('<h2 id="ai-card">7. AI-Assisted Fact-Checking Card</h2>', 1)
card_body, after = card_section.split('<h2 id="a4">', 1)
body = before + '<h2 id="a4">' + after
card_page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI-Assisted Fact-Checking Card | ARCH7476 A3</title><style>{css} .card-main{{max-width:900px;margin:auto;padding:24px}}</style></head><body><main class="card-main"><a href="a3-peoplecomfort-research.html#verification">← Back to A3 report</a><h1>AI-Assisted Fact-Checking Card</h1>{card_body}</main></body></html>"""
(here / card_url).write_text(card_page, encoding="utf-8")
toc = "".join(f'<a href="#{anchor}">{html.escape(title)}</a>' for title, anchor in titles if anchor != "ai-card")
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="ARCH7476 Assignment 03: seven-design thermal-zone capacity prototype, verified PMV calculations and uncertainty checks."><title>A3 · Thermal-zone capacity | ARCH7476</title><style>{css}</style></head><body><div class="topbar">ARCH7476 · Evidence-Based Generative Design</div><div class="layout"><main><header><div class="kicker">A3 · WORKFLOW PROTOTYPE + VERIFICATION</div><h1>Thermal-zone capacity under changing user composition</h1><p>PeopleComfort v0.2.0 · A3 submission tag: a3-submission · 18 November 2026</p><div class="hero-actions"><a href="a3-assets/A3_research_report.pdf" download>Download report PDF ↓</a><a id="ai-card" href="{card_url}">AI-Assisted Fact-Checking Card</a><a href="peoplecomfort.html">Explore the interactive tool ↗</a><a href="https://github.com/Hey-Guobaorou/peoplecomfort/tree/a3-submission">View frozen package ↗</a></div></header>{body}<footer>ARCH7476 · A3 · Thermal inputs are hypothetical until supported by site evidence.</footer></main><aside><strong>On this page</strong>{toc}<button class="print" onclick="window.print()">Print / Save PDF</button></aside></div><script>if(location.hash === '#ai-card') location.replace('{card_url}');</script></body></html>'''
(here / "a3-peoplecomfort-research.html").write_text(page, encoding="utf-8")
print("Built", here / "a3-peoplecomfort-research.html")

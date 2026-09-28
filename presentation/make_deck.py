"""Build presentation/deck.pptx (5-6 minute deck) with python-pptx."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x33, 0x33, 0x33)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_bg(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def title_slide(title, subtitle):
    s = prs.slides.add_slide(BLANK)
    add_bg(s)
    tx = s.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.5))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = NAVY
    tx2 = s.shapes.add_textbox(Inches(0.8), Inches(4.4), Inches(11.7), Inches(1.5))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(22)
    p.font.color.rgb = DARK
    return s


def content_slide(title, bullets, img_path=None):
    s = prs.slides.add_slide(BLANK)
    add_bg(s)
    tx = s.shapes.add_textbox(Inches(0.7), Inches(0.3), Inches(11.9), Inches(1.0))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = NAVY
    left = Inches(0.9)
    width = Inches(11.5) if img_path is None else Inches(5.6)
    tx = s.shapes.add_textbox(left, Inches(1.5), width, Inches(5.5))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(20)
        p.font.color.rgb = DARK
        p.space_after = Pt(14)
        p.level = 0
    if img_path:
        s.shapes.add_picture(img_path, Inches(6.9), Inches(1.5),
                             width=Inches(5.7))
    return s


title_slide(
    "Is the Canadian Home Bias\nMean-Variance Efficient?",
    "CFM301 Project 1: Constructing the Most Efficient Portfolio\nJian  |  September 2026")

content_slide("The economic question", [
    "Canadians hold \u224850% of equity in Canadian stocks (IMF, via Vanguard 2024)\u2026",
    "\u2026yet Canada is only \u22483% of world market cap \u2014 a 15\u201318x overweight.",
    "Vanguard's minimum-variance analysis recommends just 30% domestic equity.",
    "Question: is the observed home bias mean-variance efficient?",
    "Approach: trace the long-only frontier over regional equities (in CAD) and "
    "see what domestic weight the optimizer chooses.",
])

content_slide("Data & universe", [
    "Five regional equity ETFs, monthly total returns (Yahoo Finance, adjusted closes):",
    "XIU.TO Canada  \u00b7  SPY US large cap  \u00b7  IWM US small cap  \u00b7  EFA dev. ex-NA  \u00b7  EEM emerging",
    "USD series converted to CAD each month-end via USD/CAD (unhedged).",
    "Sample: Oct 2003 \u2013 Aug 2026, 275 months. Means \u00d712, covariances \u00d712.",
    "Note: brief asks for CRSP/Compustat via WRDS (no access here); ETF total returns "
    "are the reproducible proxy \u2014 pipeline accepts a WRDS extract as drop-in.",
])

content_slide("Estimated inputs (annualized, CAD)", [
    "Canada: mean 10.6%, vol 12.8% \u2014 lowest volatility of the five.",
    "US large cap: mean 12.5%, vol 16.9% \u2014 highest mean.",
    "US small cap 11.9% / 21.6%  \u00b7  EAFE 9.3% / 18.4%  \u00b7  Emerging 11.2% / 22.3%.",
    "Correlations 0.67\u20130.90: Canada ~0.68 with everyone; US large/small 0.90; EAFE/EM 0.87.",
    "High correlations \u2192 limited diversification benefit beyond 2 assets.",
])

content_slide("Frontier & selection criterion", [
    "Quadratic programs: min w\u2032\u03a3w s.t. w\u2032\u03bc = m*, \u03a3w = 1, w \u2265 0 (long-only).",
    "No risk-free asset \u2192 no tangency/Sharpe rule; we maximize mean-variance utility",
    "U = E[rp] \u2212 (g/2)\u00b7Var[rp] with g = 3 (course convention; typical range 1\u201310).",
    "Long-only: the question is about a retail investor's strategic allocation.",
], img_path="outputs/frontier.png")

content_slide("The most efficient portfolio", [
    "Optimal (g = 3):  48% Canada / 52% US large cap \u2014 E[r] = 11.6%, \u03c3 = 13.7%.",
    "US small cap, EAFE, emerging markets: 0% (corner solution \u2014 error maximization).",
    "Sensitivity: optimal Canada weight is 28% (g=2) \u2192 48% (g=3) \u2192 64% (g=5).",
    "Minimum-variance portfolio: 89% Canada / 11% US (E[r] = 10.8%, \u03c3 = 12.7%).",
])

content_slide("Economic conclusion", [
    "At g = 3 the optimizer chooses 48% domestic \u2014 essentially the \u224850% Canadians hold.",
    "The home bias is roughly mean-variance efficient for moderate risk aversion, "
    "not the glaring inefficiency its 15\u201318x cap-weight overweight suggests.",
    "Vanguard's 30% recommendation sits in the efficient zone too (implies g \u2248 4\u20135).",
    "Caveats: extreme corner solution; min-variance implies 89% domestic; sample- and "
    "criterion-dependent; unhedged currency; taxes/fees ignored.",
])

content_slide("Peer evaluation (paired group)", [
    "Three main differences vs. the paired group's solution \u2014",
    "to be completed once the paired group is assigned.",
    "The 5\u20136 minute in-class presentation will explain the paired group's work "
    "and methodology, and discuss these differences.",
])

os.makedirs("presentation", exist_ok=True)
prs.save("presentation/deck.pptx")
print(f"Wrote presentation/deck.pptx ({len(prs.slides)} slides)")

"""Build presentation/deck.pptx (5-6 minute deck) with python-pptx."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x33, 0x33, 0x33)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_bg(slide):
    fill = slide.background.fill
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


def content_slide(title, bullets, img_path=None, text_width_in=11.5,
                  img_left_in=6.9, img_width_in=5.7):
    s = prs.slides.add_slide(BLANK)
    add_bg(s)
    tx = s.shapes.add_textbox(Inches(0.7), Inches(0.3), Inches(11.9), Inches(1.0))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = NAVY
    left = Inches(0.9)
    width = Inches(text_width_in)
    tx = s.shapes.add_textbox(left, Inches(1.5), width, Inches(5.5))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(19)
        p.font.color.rgb = DARK
        p.space_after = Pt(16)
        p.level = 0
    if img_path:
        s.shapes.add_picture(img_path, Inches(img_left_in), Inches(1.5),
                             width=Inches(img_width_in))
    return s


title_slide(
    "Is the Canadian Home Bias\nMean-Variance Efficient?",
    "CFM301 Project 1: Constructing the Most Efficient Portfolio\nJian  |  September 2026")

content_slide("The economic question", [
    "Canadian investors display one of the world's strongest equity home biases: they allocate "
    "roughly 50% of their equity portfolios to domestic stocks (IMF Coordinated Portfolio "
    "Investment Survey, via Vanguard 2024).",
    "Yet Canada accounts for only about 3% of global market capitalization \u2014 an overweight "
    "of roughly 15 to 18 times.",
    "Vanguard's minimum-variance analysis, however, suggests Canadian investors should hold only "
    "about 30% in domestic equity.",
    "This project asks whether the observed home bias is actually mean-variance efficient. We trace "
    "the long-only efficient frontier over regional equity markets and see what domestic weight "
    "the optimizer chooses.",
])

content_slide("Data and universe", [
    "Our universe is five regional equity ETFs, measured in monthly total returns from Yahoo Finance "
    "adjusted closes, which reinvest distributions: XIU.TO for Canada, SPY for US large cap, IWM for "
    "US small cap, EFA for developed markets ex-North America, and EEM for emerging markets.",
    "Returns on the USD-denominated ETFs are converted to Canadian dollars each month-end using the "
    "USD/CAD spot rate, so the analysis is from the perspective of an unhedged Canadian investor.",
    "The sample runs from October 2003 to August 2026 \u2014 275 monthly observations. Means are "
    "annualized by \u00d712 and covariances by \u00d712.",
    "One caveat: the brief asks for CRSP/Compustat data via WRDS, which we could not access. The ETF "
    "series are a documented, reproducible proxy, and the code accepts a WRDS extract as a drop-in "
    "replacement.",
])

content_slide("Estimated inputs (annualized, CAD)", [
    "Canada offers the lowest volatility of the five markets at 12.8%, with a mean return of 10.6%.",
    "US large cap has the highest mean return at 12.5% with 16.9% volatility. US small cap "
    "(11.9% / 21.6%), developed ex-NA (9.3% / 18.4%), and emerging markets (11.2% / 22.3%) "
    "are all riskier.",
    "Correlations range from 0.67 to 0.90: Canada correlates about 0.68 with every other market, "
    "while US large and small caps correlate 0.90 and EAFE and emerging markets correlate 0.87.",
    "These high correlations limit the diversification benefit beyond a two-asset portfolio \u2014 "
    "a hint of why the optimizer will end up concentrating.",
])

content_slide("Frontier and selection criterion", [
    "We solve min w\u2032\u03a3w subject to w\u2032\u03bc = m*, \u03a3w = 1, w \u2265 0 for a grid of target "
    "returns \u2014 one quadratic program per point \u2014 tracing out the long-only efficient frontier "
    "shown here.",
    "With no risk-free asset there is no tangency portfolio or Sharpe-ratio rule, so we select the "
    "portfolio that maximizes mean-variance utility U = E[rp] \u2212 (\u03b3/2)\u00b7Var[rp], with \u03b3 = 3 "
    "following the course convention.",
    "The long-only constraint reflects the economic question: what would a retail investor's "
    "strategic equity allocation look like? It also keeps the answer interpretable.",
], img_path="outputs/frontier_slide.png", text_width_in=4.9,
   img_left_in=6.1, img_width_in=6.5)

content_slide("The most efficient portfolio", [
    "At \u03b3 = 3, the optimizer holds 48% Canada and 52% US large cap, with an expected return of "
    "11.6% and volatility of 13.7%.",
    "US small cap, developed ex-NA, and emerging markets receive zero weight \u2014 a corner solution "
    "typical of error-maximizing mean-variance optimizers facing highly correlated assets.",
    "The answer is sensitive to risk aversion: the optimal Canada weight rises from 28% at \u03b3 = 2 "
    "to 48% at \u03b3 = 3 and 64% at \u03b3 = 5.",
    "For reference, the minimum-variance portfolio is 89% Canada and 11% US large cap, with "
    "E[r] = 10.8% and \u03c3 = 12.7%.",
])

content_slide("Economic conclusion", [
    "At \u03b3 = 3 the optimizer chooses 48% domestic equity \u2014 essentially the 50% that Canadians "
    "actually hold.",
    "The home bias is therefore roughly mean-variance efficient for a moderately risk-averse "
    "investor, not the glaring inefficiency its 15\u201318\u00d7 market-cap overweight suggests.",
    "Vanguard's 30% recommendation sits inside the efficient zone too \u2014 it corresponds to a "
    "risk aversion of about \u03b3 = 4\u20135.",
    "Caveats: the corner solution is extreme, the minimum-variance criterion implies 89% domestic, "
    "and the results depend on the sample, the criterion, unhedged currency \u2014 and ignore taxes "
    "and fees.",
])

content_slide("Peer evaluation (paired group)", [
    "Three main differences versus the paired group's solution \u2014",
    "to be completed once the paired group is assigned.",
    "The 5\u20136 minute in-class presentation will explain the paired group's work "
    "and methodology, and discuss these differences.",
])

os.makedirs("presentation", exist_ok=True)
prs.save("presentation/deck.pptx")
print(f"Wrote presentation/deck.pptx ({len(prs.slides)} slides)")

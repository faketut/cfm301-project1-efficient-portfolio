"""Build report/report.pdf (max 3 pages) from outputs/ tables and figure."""
import os
import pandas as pd
from fpdf import FPDF

AUTHOR = "Jian"
OUT = "report/report.pdf"
os.makedirs("report", exist_ok=True)

inputs = pd.read_csv("outputs/table_inputs.csv", index_col=0)
corr = pd.read_csv("outputs/table_corr.csv", index_col=0)
weights = pd.read_csv("outputs/table_weights.csv", index_col=0)
sens = pd.read_csv("outputs/table_gamma_sensitivity.csv")


class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(110, 110, 110)
            self.cell(0, 6, "CFM301 Project 1: Constructing the Most Efficient Portfolio",
                      align="R")
            self.ln(10)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def h1(self, text):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(31, 78, 121)
        self.cell(0, 8, text)
        self.ln(9)
        self.set_text_color(0, 0, 0)

    def h2(self, text):
        self.set_font("Helvetica", "B", 10.5)
        self.cell(0, 7, text)
        self.ln(8)

    def para(self, text):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4.6, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def table(self, df, col_widths=None, fmt="{:.4f}", hdr_fmt=None):
        self.set_font("Helvetica", "B", 8)
        cols = [""] + list(df.columns)
        if col_widths is None:
            first = 34
            rest = (190 - first) / len(df.columns)
            col_widths = [first] + [rest] * len(df.columns)
        for w, c in zip(col_widths, cols):
            self.cell(w, 5.5, str(c), border=1, align="C")
        self.ln()
        self.set_font("Helvetica", "", 8)
        for idx, row in df.iterrows():
            self.cell(col_widths[0], 5.5, str(idx), border=1)
            for w, v in zip(col_widths[1:], row):
                try:
                    txt = fmt.format(float(v))
                except (ValueError, TypeError):
                    txt = str(v)
                self.cell(w, 5.5, txt, border=1, align="C")
            self.ln()
        self.ln(3)


pdf = Report(format="Letter")
pdf.alias_nb_pages()
pdf.set_margins(12, 12, 12)
pdf.set_auto_page_break(True, margin=15)

# ---------------- Page 1 ----------------
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)
pdf.multi_cell(0, 8, "Is the Canadian Home Bias Mean-Variance Efficient?\n"
                     "Constructing the Most Efficient Portfolio", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
pdf.cell(0, 7, f"CFM301 Project 1  |  {AUTHOR}  |  September 2026")
pdf.ln(10)

pdf.h1("1. Economic Goal & Motivation")
pdf.para(
    "Canadian investors display one of the world's strongest equity home biases: "
    "they allocate roughly 50% of equity portfolios to Canadian stocks (IMF "
    "Coordinated Portfolio Investment Survey, via Vanguard, 2024), even though "
    "Canada is only about 3% of global market capitalization -- a 15-18x "
    "overweight. Vanguard's own minimum-variance analysis recommends just 30% "
    "domestic equity for Canadians. This project asks: is the observed home "
    "bias mean-variance efficient? Tracing the long-only frontier over regional "
    "equity markets in Canadian dollars, we compute the domestic weight a "
    "mean-variance optimizer chooses and compare it to (i) the ~50% Canadians "
    "actually hold and (ii) Canada's ~3% market-cap weight.")

pdf.h1("2. Data")
pdf.para(
    "Source. Monthly total returns of five regional equity ETFs from Yahoo "
    "Finance (adjusted closes, which reinvest distributions): XIU.TO (Canada, "
    "S&P/TSX 60), SPY (US large cap), IWM (US small cap), EFA (developed ex-NA), "
    "EEM (emerging markets). The brief specifies CRSP/Compustat via WRDS; this "
    "environment has no WRDS access, so listed-ETF total returns serve as the "
    "reproducible proxy. The pipeline reads only data/monthly_returns_cad.csv, "
    "so a WRDS/CRSP country-index extract can be substituted without changing "
    "any downstream code.")
pdf.para(
    "Sample & cleaning. Month-end bars, January 2003-August 2026. USD-denominated "
    "ETFs are converted to CAD each month-end via the USD/CAD spot rate (CAD=X): "
    "R_CAD = (1+R_USD)(1+R_FX)-1. Simple returns are computed from adjusted "
    "closes; the incomplete September 2026 bar is dropped; the common sample is "
    "October 2003-August 2026 (275 months). Means are annualized x12, "
    "covariances x12 (volatilities x sqrt(12)).")
pdf.para(
    "Roadmap. Section 3 reports the estimated means, volatilities and "
    "correlations; Section 4 traces the frontier, states the selection "
    "criterion and gives the optimal weights; Section 5 plots the frontier "
    "with the chosen portfolio marked; Section 6 interprets the results.")

# ---------------- Page 2 ----------------
pdf.add_page()
pdf.h1("3. Estimated Inputs (annualized, CAD)")
pdf.table(inputs.rename(columns={"Mean (ann.)": "Mean", "Stdev (ann.)": "Stdev"}),
          col_widths=[40, 50, 50], fmt="{:.4f}")
pdf.h2("Correlation matrix (monthly returns)")
pdf.table(corr, fmt="{:.2f}")

pdf.h1("4. Frontier, Selection Criterion & Optimal Portfolio")
pdf.para(
    "Frontier. For target returns m* spanning the asset means, we solve "
    "min w'Sw s.t. w'mu = m*, sum(w) = 1, w >= 0 (SLSQP quadratic programs). "
    "Only the upper branch is efficient. Long-only is imposed because the "
    "question concerns the strategic allocation of a representative retail "
    "investor, for whom shorting country indices is impractical; it also keeps "
    "weights interpretable as portfolio shares.")
pdf.para(
    "Selection criterion. With no risk-free asset there is no tangency/Sharpe "
    "criterion, so we maximize mean-variance utility U = E[rp] - (g/2)Var[rp] "
    "with g = 3, the course convention (Ang, Ch. 3: typical risk aversion 1-10; "
    "the lecture's own G5 example uses g = 3 with no shorting).")
pdf.table(weights.rename(columns=lambda c: c.replace("Max Utility (gamma=3)",
                                                     "Max utility (g=3)")),
          col_widths=[40, 50, 50], fmt="{:.2%}")
pdf.para(
    "Most efficient portfolio: 48.2% Canada / 51.8% US large cap, E[r] = 11.56%, "
    "sigma = 13.68%. (Minimum-variance for reference: 88.9% Canada / 11.1% US "
    "large cap, E[r] = 10.77%, sigma = 12.68%.) Weights sum to 1 and satisfy "
    "the long-only constraint. Sensitivity to risk aversion:")
sens2 = sens.rename(columns={"gamma": "g", "E[r]": "E[r]", "sigma": "sigma",
                             "w_Canada": "Canada", "w_US Large Cap": "US LC",
                             "w_US Small Cap": "US SC", "w_Dev ex-NA": "EAFE",
                             "w_Emerging": "EM"}).set_index("g")
pdf.table(sens2, col_widths=[18, 24, 24, 24, 24, 24, 24, 24], fmt="{:.2f}")

# ---------------- Page 3 ----------------
pdf.add_page()
pdf.h1("5. Frontier Plot")
pdf.image("outputs/frontier.png", x=28, w=154)
pdf.ln(2)

pdf.h1("6. Economic Conclusion")
pdf.para(
    "The optimizer's answer is striking: at g = 3 the most efficient portfolio "
    "holds 48% Canadian equity -- essentially the ~50% home bias Canadians "
    "actually exhibit. Across the plausible risk-aversion range the optimal "
    "domestic weight runs from 28% (g = 2) to 64% (g = 5), bracketing both the "
    "observed 50% and Vanguard's 30% recommendation (which corresponds to about "
    "g = 4-5 here). In other words, the Canadian home bias is roughly "
    "mean-variance efficient for a moderately risk-averse investor -- it is "
    "not the glaring inefficiency its 15-18x market-cap overweight suggests. "
    "The intuition: Canada had the lowest volatility (12.8%) and the highest "
    "mean among the diversifiers once correlations (~0.7-0.9) are accounted for.")
pdf.para(
    "Three caveats. First, the solution is a corner: US small cap, EAFE and "
    "emerging markets receive zero weight at every risk-aversion level -- the "
    "textbook 'error maximization' problem (Michaud, 1989; Ang, Ch. 3), where "
    "small input differences produce extreme, concentrated portfolios. Second, "
    "the minimum-variance portfolio would imply 89% domestic equity, far more "
    "home bias than observed, so the 'efficient' domestic weight hinges on the "
    "criterion chosen. Third, inputs are sample estimates over 2003-2026; "
    "currency is unhedged and fees/taxes (e.g., the Canadian dividend tax "
    "credit) are ignored, all of which favor domestic holdings in practice.")
pdf.para(
    "Peer evaluation (three differences vs. paired group's solution): to be "
    "completed once the paired group is assigned.")

pdf.h1("References & Packages")
pdf.set_font("Helvetica", "", 8.5)
for ref in [
    "Ang, A. (2014). Asset Management, Ch. 3: Mean-Variance Investing (lecture slides).",
    "Michaud, R. (1989). The Markowitz optimization enigma. Financial Analysts Journal.",
    ("Vanguard Canada home-bias research (2024), via Investment Executive: Canadians hold "
     "~50% domestic equity vs ~3% world market cap; 30% recommended."),
    "Python: numpy, pandas, scipy (SLSQP), matplotlib, yfinance; report: fpdf2.",
]:
    pdf.multi_cell(0, 4.5, "- " + ref, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

pdf.output(OUT)
print(f"Wrote {OUT} ({pdf.page_no()} pages)")

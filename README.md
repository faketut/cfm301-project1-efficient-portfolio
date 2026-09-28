# CFM301 Project 1: Constructing the Most Efficient Portfolio

**Economic question:** Is the Canadian home bias mean-variance efficient?
Using regional equity ETFs, we trace the long-only mean-variance frontier in
Canadian dollars and ask what domestic (Canadian) equity weight a
mean-variance optimizer chooses — versus the ~50% Canadians actually hold
(IMF data, via Vanguard) and Canada's ~3% weight in world market cap.

## Reproduce end-to-end

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Download + clean data (writes data/monthly_returns_cad.csv)
python src/data.py

# 2. Estimate inputs, frontier, optimal portfolio -> outputs/
python run_project.py

# 3. Build the report PDF -> report/report.pdf
python report/make_report.py

# 4. Build the presentation deck -> presentation/deck.pptx
python presentation/make_deck.py
```

Step 2 onwards runs **without any downloads**: it reads only the trimmed
`data/monthly_returns_cad.csv` checked into this repo.

## Layout

| Path | Contents |
|---|---|
| `src/data.py` | Download (Yahoo Finance) + CAD conversion + cleaning |
| `src/frontier.py` | Input estimation, QP frontier, utility maximization |
| `run_project.py` | End-to-end analysis; writes `outputs/` |
| `data/monthly_returns_cad.csv` | Trimmed monthly CAD total returns actually used |
| `outputs/` | Frontier plot, input tables, weights (generated) |
| `report/report.pdf` | 3-page project report (generated) |
| `presentation/deck.pptx` | 5–6 minute presentation deck (generated) |

## Method (summary)

- Universe: 5 regional equity ETFs — XIU.TO (Canada), SPY (US large),
  IWM (US small), EFA (developed ex-NA), EEM (emerging). 100% equities.
- USD series converted to CAD with month-end USD/CAD; simple monthly total
  returns from adjusted closes; sample from first common full month.
- Inputs: sample means (×12) and covariances (×12) of monthly CAD returns.
- Frontier: quadratic programs min w′Σw s.t. w′μ = m\*, Σw = 1, w ≥ 0.
- "Most efficient" portfolio: max μ − (γ/2)σ² with γ = 3 (course
  convention), long-only. No risk-free asset exists, so no tangency/Sharpe
  criterion is available.

## Data note

The brief asks for CRSP/Compustat via WRDS. This environment has no WRDS
access, so the analysis uses publicly available ETF total-return data
(Yahoo Finance) as a reproducible proxy; the pipeline is written so a
WRDS/CRSP extract aggregated to country indices can be substituted for
`data/monthly_returns_cad.csv` without changing any downstream code.

## Packages

numpy, pandas, scipy, matplotlib, requests, fpdf2, python-pptx, nbformat.

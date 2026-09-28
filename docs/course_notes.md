# CFM301 Course Notes (condensed)

Condensation of the course files attached for Project 1:
- `Module2_Slide2_Analytics_OLS1.pdf` — Daniel Kim, "Analytics: Regression 1"
- `Module2_Slide3_Analytics_OLS2.pdf` — Daniel Kim, "Analytics: Regression 2"
- `Ch_3_Mean-Variance_Investing.pptx` — Andrew Ang, "Ch 3: Mean-Variance Investing"
- `CFM301_Project1_Efficient_Portfolio_v2.pdf` — Project 1 brief

---

## Part A — OLS & Regression (Kim)

### 1. The CEF and causality
- Any random variable decomposes as **y = E(y|x) + ε**, with E(ε|x) = 0 by construction.
- The **conditional expectation function (CEF)**, E(y|x), is the best predictor of y given x in the
  minimum-mean-squared-error sense.
- Linear model: **y = α + βx + u** (y, x observable; u, β unobservable; u = everything else).
- **OLS** finds β minimizing mean-squared error: β̂ = argmin_b E[(y − bx)²].
  First-order condition E[x(y − βx)] = 0 ⇒ **β = E(xy)/E(x²)**.
  By construction the residual y − βx is uncorrelated with x.
- **βx is the best *linear* approximation of the CEF** — true even when the CEF is nonlinear.
- Learning how x *explains* y ≠ learning the *causal effect* of x on y. Causality needs the
  **conditional mean independence (CMI)** assumption: **E(u|x) = 0** (average u the same at every x).
- **Three canonical CMI violations:** omitted variable bias, measurement error bias, simultaneity bias
  (covered in the Causality lecture). E.g., leverage-on-profitability or investment-on-Q regressions
  fail CMI because u contains bankruptcy risk, cash, distress, financing constraints…
- **You cannot test CMI with residuals** — they are mean-zero and uncorrelated with x by construction.
  Justification must come from economic argument. The "identification police" hunt for CMI violations.
- Avoid vague "endogeneity problem" talk; be specific about *which* CMI violation you suspect.
  (Some use "endogenous" broadly = any corr(x, u); the lecturer avoids the term.)

### 2. Interpretation, scaling, shifting
- Example: salaryᵢ = 963.2 + 18.5·ROEᵢ + uᵢ (salary in $000s, ROE in %).
  1 pp rise in ROE ↔ **+$18,500** salary; intercept $963,200 = average salary at ROE = 0. CMI probably fails.
- **Scaling y by c** multiplies intercept and slope by c; **scaling x by k** divides the slope by k.
  Interpretation is unchanged — rescale cosmetically (nobody wants to read 0.000000456).
- **Standardized scaling** (multiply x by 1/σₓ, y by 1/σᵧ): slope = SDs of y per 1-SD change in x
  (e.g., 0.25 = ¼ SD of y per SD of x). t-stats and inference unaffected.
- **Shifting** (adding constants) changes only the intercept, never the slope.
  Demeaning x makes the intercept = E(y | x = x̄) — useful for diff-in-diffs.

### 3. Nonlinearities and logs
- If each year of schooling gives a *proportionate* wage gain, estimate **ln(wage) = α + β·educ + u**.
- Interpretation table:

  | Model | Dep. var | Indep. var | β means |
  |---|---|---|---|
  | Level–level | y | x | dy = β·dx |
  | Level–log | y | ln(x) | dy = (β/100) per 1% Δx |
  | Log–level | ln(y) | x | %dy ≈ (100β)·dx |
  | Log–log | ln(y) | ln(x) | %dy = β·%dx (β = elasticity) |

- **100·Δln(y) ≈ %Δy only for small changes.** For large changes use the exact conversion:
  **true %Δy = 100·[exp(β·Δx) − 1]**. (A claimed "−120%" stock-price drop was really −70%.)
- Rescaling a *logged* variable changes only the intercept, never the slope.
- Logs mitigate outliers and free you from units; rule of thumb: log positive currency amounts and
  large counts; don't log years or variables that can be zero. **Don't use ln(1+y)** for
  zero-heavy variables — ln(x′+1) − ln(x+1) is not a percent change (Cohn, Liu & Wardlaw, JFE 2022).
- Percent change = [(x₁−x₀)/x₀]×100; percentage-point change = raw difference. Don't mix them.

### 4. Quadratic terms
- y = β₀ + β₁x + β₂x² + u ⇒ marginal effect **β₁ + 2β₂x** — pick an x to evaluate it at.
- Turning point at **−β₁/(2β₂)**; check it lies inside the data range, else suspect misspecification.

### 5. Multivariate OLS
- y = β₀ + β₁x₁ + … + βₖxₖ + u. Each slope is a **partial (ceteris paribus) effect**:
  Δŷ = β̂₁·Δx₁ holding x₂…xₖ fixed. Intercept = predicted y when all x = 0 (often meaningless).
- **Partial regression (Frisch–Waugh):** β̂₁ also comes from a 3-step residual-on-residual regression
  (regress y on x₂ → save residuals; regress x₁ on x₂ → save residuals; regress residuals on residuals).
- **Wrong:** "industry-adjusting" by regressing y on x and then residuals on z — you must partial x
  out of *both* y and z.
- Residual properties: mean zero; uncorrelated with every x (by construction — not a causality test);
  the point of means lies on the regression line.
- **R² = SSE/SST = 1 − SSR/SST** = share of y's variation explained (also = corr(y, ŷ)²).
  Adding any regressor never lowers R² ⇒ use **adjusted R² = 1 − (1−R²)(N−1)/(N−1−k)**, which can fall.
  A low R² does not mean the model is wrong — your β of interest can still be consistent.
- **Unbiasedness** (E[β̂] = β, finite-sample) vs **consistency** (plim β̂ = β as N→∞, asymptotic).
  OLS is unbiased under linearity + random sample + no perfect collinearity + E(u|x)=0;
  consistent under the weaker zero-correlation of each x with u. In practice, care about consistency.

### 6. Hypothesis testing and standard errors
- **Heteroskedasticity**, Var(u|x) = f(x), does **not** bias OLS — it only affects standard errors
  (and OLS is no longer the most precise linear estimator). Default SEs assume homoskedasticity.
- **Fix: use robust standard errors.** If robust SEs are *smaller*, something may be off — use the larger
  ones. Angrist–Pischke: don't bother with WLS; OLS is consistent and WLS's finite-sample properties
  can be bad and harder to interpret.
- t-stat = β̂/SE(β̂) = how many SDs the estimate is from zero; p-value = P(|estimate| this extreme | β=0).
- **Statistical ≠ economic significance.** Always check economic magnitude: implied Δy for a 1-SD
  change in x — and whether it's plausible (if not, suspect misspecification).
  Large N can make tiny effects "significant"; small N can hide large ones.
- **Variance formula:** Var(β̂ⱼ) = σ² / [Σ(xᵢ−x̄)²·(1−R²ⱼ)], R²ⱼ from regressing xⱼ on all other x's.
  More x-variation ⇒ smaller SE; more error variance ⇒ bigger SE; higher R²ⱼ ⇒ bigger SE.
- **Multicollinearity** inflates SEs but causes **no bias/inconsistency** — it's a small-sample
  precision problem. Don't add controls highly collinear with your x of interest *unless needed for
  identification* (E(u|x) ≠ 0 without them). A larger sample helps.

---

## Part B — Mean-Variance Investing (Ang, Ch. 3)

### 1. The mean-variance frontier
- Quadratic program: **min_w w′Σw s.t. w′μ = m\*, Σwᵢ = 1**. Varying the target m\* traces the frontier.
- Only the **top half** of the frontier is *efficient* (no higher mean for the same σ);
  the leftmost point is the **minimum-variance portfolio**.
- **Diversification:** imperfectly correlated assets combine into portfolios less risky than any
  single asset — when one does poorly, another may do well. Lower correlation ⇒ frontier shifts
  further left. (In the CAPM, beta measures this: high-beta stocks offer less diversification benefit,
  so investors demand higher expected returns for them.)
- G5 example (MSCI USD total returns, 1970–2011): means ≈ 10.3–12.2%, vols 15.7–23.0%,
  correlations 0.35–0.72. Adding assets expands the frontier (lower min variance, wider wings,
  higher attainable Sharpe ratio). Constraints like no-short-sales make the frontier non-parabolic.

### 2. Which portfolio? Mean-variance utility
- **U = E[rp] − (γ/2)·Var[rp]**, γ = risk aversion (typically 1–10; >10 rare).
  Indifference curves in (σ, E[r]) space; the **tangent** indifference curve to the frontier
  is the optimal portfolio. Equivalently, map γ into an E[r] or vol target.
- No-risk-free example (γ = 3, long-only G5): 44.7% US, 23.7% JP, 16.4% UK, 10.8% GR, 4.5% FR
  (Sharpe 0.669 at rf = 1%).
- Shortcomings of mean-variance utility: symmetric treatment of gains/losses, only two moments
  matter, subjective vs objective probabilities, constant risk aversion, one-period model.

### 3. Sensitivity — "error maximizers"
- Frontiers are **extremely sensitive to inputs**: small mean changes produce radically different
  weights at similar (μ, σ). E.g., at a 14% target, raising the US mean from 0.103 to 0.130 flips
  the US weight from **−1.22 to +1.65**. Michaud (1989): mean-variance portfolios are
  **"error maximization"** portfolios — garbage in, garbage out.
- Remedies: don't use raw history (short moving averages; high past returns ⇒ high valuations ⇒
  low expected returns); account for sampling error; robust mean/covariance estimates; economic
  models (CAPM, multi-factor, **Black–Litterman** reverse-engineered from market caps, valuation
  models); or simple diversified portfolios — **1/N** (DeMiguel, Garlappi & Uppal 2009),
  **risk parity** (Qian 2006), **minimum variance** — all special cases of mean-variance.

### 4. Adding a risk-free asset
- **Two-fund separation:** (1) find the max-Sharpe risky portfolio — the **MVE/tangency** portfolio;
  (2) mix it with the risk-free asset. The **Capital Allocation Line (CAL)** joins rf to MVE;
  optimal portfolios lie on it.
- All investors hold the **same** risky mix (MVE), differing only in the rf allocation.
  G5 example, rf = 1%: γ = 3 borrows 51.9% at rf to lever the MVE mix; γ = 6 holds the same mix
  at half scale plus 24.1% in rf.
- The "risk-free" asset is horizon- and currency-dependent; even Treasuries aren't literally risk-free.

---

## Part C — Project 1 brief (key requirements)

- **Task:** construct the *most efficient* portfolio for an economic question of our choice.
- **Deliverables:** reproducible code (script/notebook), trimmed raw data, ≤3-page report,
  efficient-frontier plot, and a 5–6 minute presentation **explaining the paired group's work**,
  including **three main differences** from our own solution.
- **Data:** CRSP/Compustat via WRDS required. (We had no WRDS access; the report documents
  Yahoo Finance ETF total returns as the reproducible proxy, swappable for a WRDS extract.)
- **Our choices (documented in report):** long-only, fully invested equity universe (5 regional
  ETFs, CAD-adjusted, Oct 2003–Aug 2026); selection criterion = max mean-variance utility, γ = 3.
- **Result:** 48.2% Canada / 51.8% US large cap, E[r] = 11.56%, σ = 13.68% — the Canadian home
  bias looks roughly mean-variance efficient for moderate risk aversion.
- **Pending:** paired-group assignment (peer-evaluation slides/report section are placeholders).

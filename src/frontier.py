"""
Mean-variance estimation and optimization for CFM301 Project 1.

Conventions follow the course (Ang, Ch. 3): annualized means / volatilities,
quadratic-programming frontier with weights summing to one, and a
mean-variance utility criterion U = E[rp] - (gamma/2) * Var[rp] to select a
single optimal portfolio.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize

GAMMA = 3.0  # risk aversion of the representative investor (cf. lecture: 1-10)


def load_returns(path="data/monthly_returns_cad.csv"):
    df = pd.read_csv(path, parse_dates=["date"], index_col="date")
    return df


def estimate_inputs(rets):
    """Sample means, vols, correlations from monthly returns; annualized."""
    mu_m = rets.mean()
    cov_m = rets.cov()
    mu = mu_m * 12
    vol = rets.std() * np.sqrt(12)
    corr = rets.corr()
    cov = cov_m * 12
    return {"mu": mu, "vol": vol, "corr": corr, "cov": cov,
            "nobs": len(rets),
            "start": rets.index[0].date(), "end": rets.index[-1].date()}


def _min_var_for_target(mu, cov, target):
    n = len(mu)
    x0 = np.ones(n) / n

    def obj(w):
        return w @ cov.values @ w

    cons = [{"type": "eq", "fun": lambda w: w @ mu.values - target},
            {"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    res = minimize(obj, x0, method="SLSQP", bounds=[(0, 1)] * n,
                   constraints=cons, options={"maxiter": 1000})
    if not res.success:
        raise RuntimeError(f"QP failed for target {target}: {res.message}")
    return res.x


def efficient_frontier(mu, cov, n_points=60):
    """Long-only efficient frontier: min variance for each target return m*.

    Targets start at the minimum-variance portfolio's expected return, so only
    the efficient (upper) branch is traced -- the inefficient lower branch
    below the global minimum-variance portfolio is excluded.
    """
    w_mv = min_variance_portfolio(mu, cov)
    mu_mv = float(w_mv @ mu.values)
    targets = np.linspace(mu_mv, mu.max(), n_points)
    rows = []
    for m in targets:
        w = _min_var_for_target(mu, cov, m)
        port_mu = w @ mu.values
        port_var = w @ cov.values @ w
        rows.append({"target": m, "mu": port_mu, "vol": np.sqrt(port_var),
                     **{f"w_{a}": wi for a, wi in zip(mu.index, w)}})
    return pd.DataFrame(rows)


def min_variance_portfolio(mu, cov):
    # Global min-variance: no return target
    n = len(mu)
    res = minimize(lambda w: w @ cov.values @ w, np.ones(n) / n,
                   method="SLSQP", bounds=[(0, 1)] * n,
                   constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
                   options={"maxiter": 1000})
    w = res.x
    return pd.Series(w, index=mu.index)


def max_utility_portfolio(mu, cov, gamma=GAMMA):
    """Maximize E[rp] - (gamma/2) Var[rp], long-only, weights sum to 1."""
    n = len(mu)

    def neg_u(w):
        return -(w @ mu.values - 0.5 * gamma * (w @ cov.values @ w))

    res = minimize(neg_u, np.ones(n) / n, method="SLSQP",
                   bounds=[(0, 1)] * n,
                   constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
                   options={"maxiter": 1000})
    if not res.success:
        raise RuntimeError(f"Utility maximization failed: {res.message}")
    return pd.Series(res.x, index=mu.index)


def portfolio_stats(w, mu, cov):
    m = float(w @ mu)
    v = float(w @ cov.values @ w)
    return {"mu": m, "vol": np.sqrt(v)}

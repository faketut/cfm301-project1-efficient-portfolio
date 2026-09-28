"""
End-to-end runner for CFM301 Project 1.

Reads data/monthly_returns_cad.csv (created by src/data.py), estimates
mean-variance inputs, traces the long-only efficient frontier, selects the
maximum mean-variance-utility portfolio (gamma=3), and writes all tables and
figures used by the report into outputs/.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.frontier import (load_returns, estimate_inputs, efficient_frontier,
                          min_variance_portfolio, max_utility_portfolio,
                          portfolio_stats, GAMMA)

OUT = "outputs"
os.makedirs(OUT, exist_ok=True)


def main():
    rets = load_returns()
    est = estimate_inputs(rets)
    mu, cov = est["mu"], est["cov"]
    print(f"Sample: {est['nobs']} months, {est['start']} to {est['end']}")

    # --- input tables ---
    inputs = pd.DataFrame({"Mean (ann.)": mu, "Stdev (ann.)": est["vol"]})
    inputs.to_csv(f"{OUT}/table_inputs.csv", float_format="%.4f")
    est["corr"].to_csv(f"{OUT}/table_corr.csv", float_format="%.4f")

    # --- frontier ---
    front = efficient_frontier(mu, cov)
    front.to_csv(f"{OUT}/frontier.csv", index=False, float_format="%.6f")

    # --- candidate portfolios ---
    w_mv = min_variance_portfolio(mu, cov)
    w_opt = max_utility_portfolio(mu, cov, gamma=GAMMA)
    s_mv = portfolio_stats(w_mv, mu, cov)
    s_opt = portfolio_stats(w_opt, mu, cov)

    weights = pd.DataFrame({
        "Min-Variance": w_mv,
        f"Max Utility (gamma={GAMMA:g})": w_opt,
    })
    weights.to_csv(f"{OUT}/table_weights.csv", float_format="%.4f")

    # Sensitivity of the optimal portfolio to risk aversion
    sens_rows = []
    for g in [1, 2, 3, 5, 10]:
        wg = max_utility_portfolio(mu, cov, gamma=g)
        sg = portfolio_stats(wg, mu, cov)
        sens_rows.append({"gamma": g, "E[r]": sg["mu"], "sigma": sg["vol"],
                          **{f"w_{a}": x for a, x in zip(mu.index, wg.values)}})
    sens = pd.DataFrame(sens_rows)
    sens.to_csv(f"{OUT}/table_gamma_sensitivity.csv", index=False,
                float_format="%.4f")
    print("\nGamma sensitivity:")
    print(sens.round(4).to_string(index=False))

    print("\nAnnualized means / vols:")
    print(inputs.round(4).to_string())
    print("\nCorrelation matrix:")
    print(est["corr"].round(4).to_string())
    print("\nOptimal (max mean-variance utility, gamma=3) weights:")
    print(weights.round(4).to_string())
    print(f"\nOptimal portfolio: E[r] = {s_opt['mu']:.4f}, "
          f"sigma = {s_opt['vol']:.4f}")
    print(f"Min-variance portfolio: E[r] = {s_mv['mu']:.4f}, "
          f"sigma = {s_mv['vol']:.4f}")

    # --- frontier plot ---
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(front["vol"], front["mu"], color="#1f4e79", lw=2,
            label="Efficient frontier (long-only)")
    ax.scatter(est["vol"], mu, s=60, color="#c0504d", zorder=5,
               label="Individual assets")
    for a in mu.index:
        ax.annotate(a, (est["vol"][a], mu[a]),
                    textcoords="offset points", xytext=(6, 4), fontsize=9)
    ax.scatter([s_mv["vol"]], [s_mv["mu"]], s=90, marker="s",
               color="#70ad47", zorder=6, label="Minimum-variance")
    ax.scatter([s_opt["vol"]], [s_opt["mu"]], s=110, marker="*",
               color="#ffbf00", edgecolors="black", zorder=7,
               label=f"Most efficient (max utility, gamma={GAMMA:g})")
    ax.set_xlabel("Standard deviation (annualized)")
    ax.set_ylabel("Expected return (annualized)")
    ax.set_title("Mean-Variance Efficient Frontier\n"
                 "Regional equity ETFs, CAD total returns")
    ax.legend(frameon=True, fontsize=9)
    fig.tight_layout()
    fig.savefig(f"{OUT}/frontier.png", dpi=150)
    print(f"\nWrote {OUT}/frontier.png and tables.")


if __name__ == "__main__":
    main()

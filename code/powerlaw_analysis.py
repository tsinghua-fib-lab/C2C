"""Fit and compare candidate heavy-tail distributions for positive values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import powerlaw


CANDIDATES = ("power_law", "truncated_power_law", "lognormal", "exponential")


def fit_distributions(values: np.ndarray) -> tuple[powerlaw.Fit, dict]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values) & (values > 0)]
    if values.size < 10:
        raise ValueError("at least 10 finite positive observations are required")
    fit = powerlaw.Fit(values, verbose=False)
    comparisons = {}
    for i, first in enumerate(CANDIDATES):
        for second in CANDIDATES[i + 1:]:
            ratio, p_value = fit.distribution_compare(first, second, normalized_ratio=True)
            comparisons[f"{first}_vs_{second}"] = {"normalized_loglikelihood_ratio": ratio, "p_value": p_value}
    summary = {"n": int(values.size), "xmin": float(fit.xmin), "alpha": float(fit.power_law.alpha), "comparisons": comparisons}
    return fit, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--column", required=True)
    parser.add_argument("--output", required=True, type=Path, help="output path without extension")
    args = parser.parse_args()
    values = pd.read_csv(args.input)[args.column].to_numpy()
    fit, summary = fit_distributions(values)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    ax = fit.plot_ccdf(label="observed")
    fit.power_law.plot_ccdf(ax=ax, linestyle="--", label="power law")
    fit.lognormal.plot_ccdf(ax=ax, linestyle=":", label="lognormal")
    ax.set_xlabel(args.column)
    ax.set_ylabel("CCDF")
    ax.legend()
    plt.tight_layout()
    plt.savefig(args.output.with_suffix(".pdf"))


if __name__ == "__main__":
    main()


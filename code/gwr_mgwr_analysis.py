"""Fit GWR/MGWR models to an aggregate spatial table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW


def standardize(values: np.ndarray) -> np.ndarray:
    std = values.std(axis=0)
    if np.any(std == 0):
        raise ValueError("response and predictors must have non-zero variance")
    return (values - values.mean(axis=0)) / std


def fit_models(frame: pd.DataFrame, response: str, predictors: list[str], fit_mgwr: bool):
    required = ["x", "y", response, *predictors]
    clean = frame[required].replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) <= len(predictors) + 2:
        raise ValueError("too few complete grid cells for the requested model")
    coords = list(clean[["x", "y"]].itertuples(index=False, name=None))
    y = standardize(clean[[response]].to_numpy(dtype=float))
    x = standardize(clean[predictors].to_numpy(dtype=float))

    gwr_selector = Sel_BW(coords, y, x)
    gwr_bw = gwr_selector.search()
    gwr = GWR(coords, y, x, gwr_bw).fit()
    summary = {"n": len(clean), "predictors": predictors, "gwr": {
        "bandwidth": float(gwr_bw), "aic": float(gwr.aic), "aicc": float(gwr.aicc),
        "r2": float(gwr.R2), "adjusted_r2": float(gwr.adj_R2)}}
    coefficients = clean[["x", "y"]].copy()
    for index, name in enumerate(["intercept", *predictors]):
        coefficients[f"gwr_{name}"] = gwr.params[:, index]

    if fit_mgwr:
        selector = Sel_BW(coords, y, x, multi=True)
        bandwidths = selector.search(max_iter=200, max_iter_multi=200)
        mgwr = MGWR(coords, y, x, selector).fit()
        summary["mgwr"] = {"bandwidths": [float(v) for v in bandwidths], "aicc": float(mgwr.aicc)}
        for index, name in enumerate(["intercept", *predictors]):
            coefficients[f"mgwr_{name}"] = mgwr.params[:, index]
    return summary, coefficients


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--response", required=True)
    parser.add_argument("--predictors", required=True, help="comma-separated column names")
    parser.add_argument("--output", required=True, type=Path, help="output path without extension")
    parser.add_argument("--fit-mgwr", action="store_true")
    args = parser.parse_args()
    predictors = [value.strip() for value in args.predictors.split(",") if value.strip()]
    summary, coefficients = fit_models(pd.read_csv(args.input), args.response, predictors, args.fit_mgwr)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    coefficients.to_csv(args.output.with_name(args.output.name + "_coefficients.csv"), index=False)


if __name__ == "__main__":
    main()

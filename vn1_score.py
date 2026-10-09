"""Score a forecast for the VN1 forecasting competition.

VN1 was a forecasting competition organized by Nicolas Vandeput (SupChains) in 2024.
Page, results and citation: https://supchains.com/vn1-forecasting-competition/

Usage, from the folder that holds the Phase files:
    python vn1_score.py "my forecast.csv"             # phase 2, the weeks of the final ranking
    python vn1_score.py "my forecast.csv" --phase 1   # phase 1, the warm-up

A forecast file has the layout of "Phase 2 - Sales.csv": the columns Client, Warehouse and
Product, then one column per week, labelled with its Monday date. One row per series, 13 weeks,
no missing value.

The score is the official metric of the competition:
    Score = MAE% + |Bias%| = (sum |forecast - sales| + |sum (forecast - sales)|) / sum (sales)
A perfect forecast scores 0%.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

INDEX = ["Client", "Warehouse", "Product"]
HERE = Path(__file__).resolve().parent

# The scores to compare with, computed with this file: the final ranking (phase 2) and the two
# benchmarks of vn1_benchmarks.py. The scores of phase 1 were never part of the ranking.
REFERENCE = {
    1: [
        ("12-week moving average", 0.659707),
        ("Naive forecast", 0.688207),
    ],
    2: [
        ("1st: Jakub Figura and Philip Stubbs", 0.463746),
        ("2nd: Justin Furlotte", 0.465685),
        ("3rd: Arsa Nikzad", 0.475784),
        ("4th: Antoine Schwartz", 0.477434),
        ("5th: An Hoang", 0.480808),
        ("Naive forecast", 0.506970),
        ("12-week moving average", 0.804585),
    ],
}


def read_weekly(path):
    """Read a VN1 file: one row per series (Client, Warehouse, Product), one column per week."""
    path = Path(path)
    if not path.exists():
        sys.exit(f"File not found: {path}")
    table = pd.read_csv(path)
    missing = [c for c in INDEX if c not in table.columns]
    if missing:
        sys.exit(f"{path.name}: the column(s) {', '.join(missing)} are missing.")
    table = table.set_index(INDEX)
    table.columns = pd.to_datetime(table.columns)
    return table


def align(forecast, sales, name="the forecast"):
    """Put the forecast in the order of the sales file. Stop if a series or a week is missing."""
    if forecast.index.duplicated().any():
        sys.exit(f"{name}: {int(forecast.index.duplicated().sum())} series appear twice.")
    missing_weeks = sales.columns.difference(forecast.columns)
    if len(missing_weeks):
        weeks = ", ".join(d.strftime("%Y-%m-%d") for d in missing_weeks)
        sys.exit(f"{name}: the week(s) {weeks} are missing.")
    missing_series = sales.index.difference(forecast.index)
    if len(missing_series):
        sys.exit(f"{name}: {len(missing_series)} of the {len(sales)} series are missing.")
    forecast = forecast.loc[sales.index, sales.columns]
    if forecast.isnull().any().any():
        sys.exit(f"{name}: {int(forecast.isnull().sum().sum())} cells are empty. Every cell needs a forecast.")
    return forecast


def score(forecast, sales):
    """The official VN1 score, MAE% + |Bias%|. Returns (score, MAE%, Bias%) as fractions."""
    error = forecast.values - sales.values
    total = np.nansum(sales.values)
    mae = np.nansum(np.abs(error)) / total
    bias = np.nansum(error) / total
    return mae + abs(bias), mae, bias


def main():
    parser = argparse.ArgumentParser(description="Score a VN1 forecast with the official metric, MAE% + |Bias%|.")
    parser.add_argument("forecast", help='your forecast, a CSV file laid out like "Phase 2 - Sales.csv"')
    parser.add_argument("--phase", type=int, choices=(1, 2), default=2,
                        help="1 for the warm-up, 2 for the weeks of the final ranking (default)")
    parser.add_argument("--data", default=str(HERE),
                        help="the folder that holds the Phase files (default: the folder of this script)")
    args = parser.parse_args()

    sales = read_weekly(Path(args.data) / f"Phase {args.phase} - Sales.csv")
    forecast = align(read_weekly(args.forecast), sales, Path(args.forecast).name)
    value, mae, bias = score(forecast, sales)

    print(f"Phase {args.phase} score: {value:.2%}   (MAE% {mae:.2%}, Bias% {bias:+.2%})")
    print()
    rows = REFERENCE[args.phase] + [("Your forecast", value)]
    for name, result in sorted(rows, key=lambda row: row[1]):
        mark = "   <- your forecast" if name == "Your forecast" else ""
        print(f"  {result:7.2%}  {'' if mark else name}{mark}")


if __name__ == "__main__":
    main()

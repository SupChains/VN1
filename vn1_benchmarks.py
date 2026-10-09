"""The two VN1 benchmarks: a 12-week moving average and a naive forecast.

VN1 was a forecasting competition organized by Nicolas Vandeput (SupChains) in 2024.
Page, results and citation: https://supchains.com/vn1-forecasting-competition/

Usage, from the folder that holds the Phase files:
    python vn1_benchmarks.py

For each phase, the script forecasts 13 weeks from the history the competitors had, writes the
forecasts as CSV files next to the data, and prints their scores. Phase 1 forecasts from Phase 0.
Phase 2 forecasts from Phase 0 and Phase 1 together.

Moving average: the mean of the last 12 weeks, held flat for 13 weeks.
Naive forecast: the last week of sales, held flat for 13 weeks.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from vn1_score import HERE, align, read_weekly, score

HORIZON = 13


def history(phase, data):
    """The sales the competitors had when they forecast this phase."""
    files = ["Phase 0 - Sales.csv"] + (["Phase 1 - Sales.csv"] if phase == 2 else [])
    return pd.concat([read_weekly(data / name) for name in files], axis=1)


def flat(history_, level):
    """Hold one value per series for the 13 weeks after the history (Mondays, as in the data)."""
    weeks = pd.date_range(start=history_.columns.max(), periods=HORIZON + 1, freq="W-MON")[1:]
    return pd.DataFrame(np.repeat(level.reshape(-1, 1), HORIZON, axis=1), index=history_.index, columns=weeks)


def moving_average(history_, weeks=12):
    return flat(history_, np.nanmean(history_.values[:, -weeks:], axis=1))


def naive(history_):
    return flat(history_, history_.values[:, -1])


def main():
    parser = argparse.ArgumentParser(description="Build and score the two VN1 benchmarks.")
    parser.add_argument("--data", default=str(HERE),
                        help="the folder that holds the Phase files (default: the folder of this script)")
    args = parser.parse_args()
    data = Path(args.data)

    for phase in (1, 2):
        sales = read_weekly(data / f"Phase {phase} - Sales.csv")
        past = history(phase, data)
        for name, model in (("MA12", moving_average), ("Naive", naive)):
            forecast = align(model(past), sales, f"the {name} forecast")
            out = data / f"Benchmark Phase {phase} - {name}.csv"
            forecast.rename(columns=lambda d: d.strftime("%Y-%m-%d")).to_csv(out)
            value, mae, bias = score(forecast, sales)
            print(f"Phase {phase}  {name:5s}  score {value:.2%}  (MAE% {mae:.2%}, Bias% {bias:+.2%})  -> {out.name}")


if __name__ == "__main__":
    main()

# VN1 Forecasting Competition: data, code and benchmarks

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23265103-blue.svg)](https://doi.org/10.5281/zenodo.23265103)

VN1 was a forecasting competition organized by Nicolas Vandeput ([SupChains](https://supchains.com/))
in 2024. In total, 978 participants registered to forecast 13 weeks of sales for 15,053
product-warehouse combinations, on real retail data.

This repository holds the data, the official scoring code, the two benchmarks and the five winning
forecasts. [Flieber](https://www.flieber.com/) provided the data. Flieber, Syrup and SupChains
sponsored the competition, and [DataSource.ai](https://www.datasource.ai/en/home/data-science-competitions-for-startups/phase-2-vn1-forecasting-accuracy-challenge/description)
hosted it.

- **Page, with the results:** https://supchains.com/vn1-forecasting-competition/
- **Webinar, the top 5 explain their models (November 2024):** https://www.youtube.com/watch?v=CRGA5mOqSeo
- **Article, what I learned from the best forecasters:** https://nicolas-vandeput.medium.com/vn1-forecasting-competition-what-i-learned-from-the-best-forecasters-ba8f314ec21f
- **How to cite VN1:** [at the end of this page](#how-to-cite-vn1), and in [CITATION.cff](CITATION.cff)

## Start here

The scripts need Python 3 with pandas and NumPy. Run them from the root of this repository.

```
pip install -r requirements.txt
python vn1_benchmarks.py
python vn1_score.py "Top 5 forecasts/1st - Jakub Figura and Philip Stubbs.csv"
```

The second command builds the two benchmarks and prints their scores. The third prints the score of
the winning forecast beside the final ranking:

```
Phase 2 score: 46.37%   (MAE% 45.25%, Bias% +1.12%)

   46.37%     <- your forecast
   46.37%  1st: Jakub Figura and Philip Stubbs
   46.57%  2nd: Justin Furlotte
   47.58%  3rd: Arsa Nikzad
   47.74%  4th: Antoine Schwartz
   48.08%  5th: An Hoang
   50.70%  Naive forecast
   80.46%  12-week moving average
```

The scripts were tested with Python 3.13, pandas 3.0 and NumPy 2.4.

## What this repository holds

| File or folder | What it holds |
|---|---|
| `Phase 0 - Sales.csv` | Units sold per week, 170 weeks, from 6 July 2020 to 2 October 2023 |
| `Phase 0 - Price.csv` | Price per week, from the actual transactions, for the same weeks |
| `Phase 1 - Sales.csv` | Units sold per week, 13 weeks, from 9 October 2023 to 1 January 2024 |
| `Phase 1 - Price.csv` | Price per week, for the same 13 weeks |
| `Phase 2 - Sales.csv` | Units sold per week, 13 weeks, from 8 January to 1 April 2024: the weeks of the final ranking |
| `Top 5 forecasts/` | The five winning phase 2 forecasts, as submitted. The code of the winners is not included |
| `Benchmarks/` | The forecasts of the two benchmarks, for phase 1 and for phase 2 |
| `vn1_score.py` | The official score of a forecast file |
| `vn1_benchmarks.py` | The two benchmarks: a 12-week moving average and a naive forecast |
| `CITATION.cff` | The citation, for GitHub's "Cite this repository" and for reference managers |
| `LICENSE`, `LICENSE-DATA` | The licenses of the code and of the data |

The repository holds no phase 2 prices, because competitors never received them.

## The data

Each row is one product in one warehouse. Three columns identify it: `Client`, `Warehouse` and
`Product`. They are anonymized integer codes. The data covers 46 clients (e-vendors), 328
warehouses and 11,171 products. Every file lists the same 15,053 rows in the same order.

Every other column is one week, labelled with its Monday date (`2023-10-09`).

- Sales are whole units. A sales cell is 0 when nothing sold that week.
- The price comes from the actual transactions. A price cell is empty when nothing sold that week.

Some products ran out of stock in the past. The data does not mark these weeks, so they look like
weeks without demand. We only kept products that never ran out of stock in the evaluation period.

## The two phases

**Phase 1, the warm-up** (12 September to 3 October 2024). Competitors forecast the 13 weeks of
phase 1 from the 170 weeks of phase 0. A live leaderboard showed their scores.

**Phase 2, the final** (3 to 17 October 2024). Competitors received the sales and prices of phase
1, then forecast the 13 weeks of phase 2. Only their last forecast counted, and no score showed
until the end.

To replay the competition:

1. Forecast phase 1 from phase 0. Score it with `python vn1_score.py "my phase 1 forecast.csv" --phase 1`.
2. Forecast phase 2 from phase 0 and phase 1. Score it with `python vn1_score.py "my phase 2 forecast.csv"`.

Choose your model before you score phase 2. The competitors never saw these sales.

A forecast file has the layout of `Phase 2 - Sales.csv`: the three identifying columns, then the 13
weeks, one row per series, and no missing value.

## The score

    Score = MAE% + |Bias%| = (Σ |forecast − sales| + |Σ (forecast − sales)|) / Σ sales

MAE% is the sum of the absolute errors, divided by total sales. Bias% is the total error, divided
by total sales. A perfect forecast scores 0%. This score offers an excellent trade-off between
simplicity and business value. I explain it in *Data Science for Supply Chain Forecasting* and
*Demand Forecasting Best Practices*.

The competition scored every forecast with this code:

```python
abs_err = np.nansum(abs(submission - objective))
err = np.nansum((submission - objective))
score = abs_err + abs(err)
score /= objective.sum().sum()
```

## Results and benchmarks

| Phase 2 | Score | MAE% | Bias% |
|---|---|---|---|
| 1st: Jakub Figura and Philip Stubbs | 46.37% | 45.25% | +1.12% |
| 2nd: Justin Furlotte | 46.57% | 46.26% | −0.31% |
| 3rd: Arsa Nikzad | 47.58% | 46.00% | +1.58% |
| 4th: Antoine Schwartz | 47.74% | 47.54% | −0.20% |
| 5th: An Hoang | 48.08% | 44.99% | +3.09% |
| Naive forecast | 50.70% | 50.13% | −0.56% |
| 12-week moving average | 80.46% | 60.97% | +19.49% |

| Phase 1 | Score | MAE% | Bias% |
|---|---|---|---|
| 12-week moving average | 65.97% | 54.20% | −11.77% |
| Naive forecast | 68.82% | 54.41% | −14.41% |

The two benchmarks are simple on purpose:

- **12-week moving average:** the mean of the last 12 weeks of sales, held flat for 13 weeks.
- **Naive forecast:** the last week of sales, held flat for 13 weeks.

Competitors had to beat the 12-week moving average, and most of them did. Because of the
seasonality in the data, the naive forecast did exceptionally well in phase 2, while the 12-week
moving average did very poorly. Usually, a naive forecast is easy to beat, so I do not advise it as
a benchmark.

`Benchmarks/` holds the forecast files of both benchmarks, in the layout of a submission. Running
`python vn1_benchmarks.py` writes the same files next to the data.

## What the winners did

After the competition, I interviewed the top 20 about their methods.

- They tested many models before they chose one. Their key skill was a fast and robust way to evaluate models.
- LightGBM was the most used model at the top.
- Most of them combined several models, or several runs of the same model.
- Half wrote less than 300 lines of code. Nearly all solutions ran in less than 10 minutes.
- Only two flagged outliers. None used Facebook Prophet.

Their methods match [the practices SupChains applies](https://supchains.com/supchains-way/) on every client project.

## Learn more

- The top 5 explain their models, webinar of November 2024: https://www.youtube.com/watch?v=CRGA5mOqSeo
- What I learned from the best forecasters, on Medium: https://nicolas-vandeput.medium.com/vn1-forecasting-competition-what-i-learned-from-the-best-forecasters-ba8f314ec21f
- Learnings from the VN1 Forecasting Competition, Foresight, issue 77 (2025): https://ideas.repec.org/a/for/ijafaa/y2025i77p8-13.html
- VN2, the inventory competition of 2025: https://github.com/SupChains/VN2
- The original competition pages on DataSource.ai: https://www.datasource.ai/en/home/data-science-competitions-for-startups/phase-2-vn1-forecasting-accuracy-challenge/description
- Flieber, who provided the data: https://www.flieber.com/

## How to cite VN1

The data is free to use. When you use it, please cite the competition:

> Vandeput, N. (2024). VN1 Forecasting – Accuracy Challenge. Organized by Nicolas Vandeput
> (SupChains). Data provided by Flieber. Sponsored by Flieber, Syrup and SupChains.
> https://supchains.com/vn1-forecasting-competition/

```bibtex
@misc{vandeput2024vn1,
  author       = {Vandeput, Nicolas},
  title        = {{VN1} Forecasting -- Accuracy Challenge},
  year         = {2024},
  howpublished = {\url{https://supchains.com/vn1-forecasting-competition/}},
  note         = {Organized by Nicolas Vandeput (SupChains). Data provided by Flieber. Sponsored by Flieber, Syrup and SupChains.}
}
```

GitHub's "Cite this repository" button gives the same reference in APA and BibTeX, from
[CITATION.cff](CITATION.cff).

The data and the code are archived on Zenodo, with the DOI
[10.5281/zenodo.23265103](https://doi.org/10.5281/zenodo.23265103). This DOI always points to the
latest version.

To cite what the winners did, cite the article of *Foresight*:

```bibtex
@article{vandeput2025vn1learnings,
  author  = {Vandeput, Nicolas},
  title   = {Learnings from the {VN1} Forecasting Competition},
  journal = {Foresight: The International Journal of Applied Forecasting},
  number  = {77},
  year    = {2025},
  pages   = {8--13}
}
```

## License

The code (`vn1_score.py`, `vn1_benchmarks.py`) is under the [MIT license](LICENSE). The data, the
forecasts and the documentation are under [Creative Commons Attribution 4.0](LICENSE-DATA): use them
freely, and cite the competition as above.

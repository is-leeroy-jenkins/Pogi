# Descriptive Statistics

The Descriptive Statistics tab profiles numeric columns using robust distribution summaries, outlier indicators, and visual diagnostics.

## 🧭 Purpose

This page explains how Pogi summarizes numeric features before inferential testing or model training. Descriptive statistics establish the baseline behavior of budget execution values, balances, obligations, outlays, recoveries, or other numeric fields.

## 🧱 Workflow Position

Descriptive Statistics follows Data Overview and precedes Inferential Statistics. It answers whether numeric features are well-behaved enough for conventional tests or whether transformations, winsorization, or robust methods may be needed.

## 📊 Numeric Profile

The numeric profile includes central tendency, dispersion, distribution shape, outlier rates, and normality indicators.

| Metric | Meaning | Analytical Use |
|---|---|---|
| Count | Non-missing numeric observations. | Confirms usable sample size. |
| Missing % | Share of missing observations. | Flags fields requiring imputation or exclusion. |
| Mean | Arithmetic average. | Useful for balanced distributions. |
| Trimmed mean | Mean after removing extreme tails. | More stable for outlier-prone budget data. |
| Median | Middle observation. | Robust central tendency. |
| Standard deviation | Average spread around mean. | Measures volatility or dispersion. |
| MAD | Median absolute deviation. | Robust dispersion measure. |
| IQR | Q3 minus Q1. | Helps identify outliers. |
| Skew | Distribution asymmetry. | Indicates whether a few accounts dominate totals. |
| Kurtosis | Tail weight / peakedness. | Highlights outlier-prone fields. |
| Shapiro p-value | Normality test p-value. | Useful for smaller numeric samples. |
| D’Agostino p-value | Normality test p-value. | Useful for larger samples. |
| Anderson statistic | Normality test statistic. | Additional normality diagnostic. |

## 📈 Distribution Diagnostics

The tab can produce several plots for selected numeric fields:

| Plot | Purpose |
|---|---|
| Histogram + KDE | Shows shape, skew, and modal behavior. |
| Boxplot | Highlights median, IQR, and outliers. |
| Violin plot | Shows density and quartile structure. |
| ECDF | Shows cumulative distribution behavior. |
| Q-Q plot | Compares empirical distribution to a normal distribution. |

## ✅ Recommended Sequence

1. Select a manageable subset of numeric fields.
2. Review missingness and sample sizes.
3. Check skew and outlier percentages.
4. Use Q-Q plots to assess normality assumptions.
5. Note fields that may need scaling, transformation, or winsorization.
6. Use findings to inform inferential tests and feature engineering choices.

## 🔗 Related Pages

- [Inferential Statistics](inferential-statistics.md)
- [Feature Engineering](feature-engineering.md)
- [Modeling](modeling.md)

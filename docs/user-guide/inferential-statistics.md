# Inferential Statistics

The Inferential Statistics tab evaluates statistical relationships between features and supports hypothesis-style exploration.

## 🧭 Purpose

This page explains how Pogi computes correlation matrices, p-values, normality tests, and two-group comparisons. The goal is to move beyond descriptive summaries and evaluate whether observed relationships are strong enough to guide feature selection or further modeling.

## 🧱 Workflow Position

Inferential Statistics follows Descriptive Statistics. It provides evidence about relationships, assumptions, and group differences before feature analysis and model training.

## 🔗 Correlation Inference

Pogi supports several correlation methods:

| Method | Relationship Type | Typical Use |
|---|---|---|
| Pearson | Linear association between numeric variables. | Standard relationship screening. |
| Spearman | Rank-based monotonic association. | Robust to non-linear monotonic trends. |
| Kendall | Rank concordance. | Smaller samples or ordinal relationships. |

The tab produces both a correlation heatmap and a p-value heatmap. Use the p-value heatmap to distinguish visually strong relationships from relationships that may not be statistically reliable.

## 🧪 Normality Testing

The normality-testing section summarizes normality indicators for selected numeric features:

| Test | Use |
|---|---|
| Shapiro-Wilk | Smaller samples, normally capped at practical sample sizes. |
| D’Agostino | Larger samples where skew and kurtosis matter. |
| Anderson-Darling | Distribution-sensitive normality statistic. |

Normality tests are diagnostic, not final judgment. In financial data, large samples and outliers often produce statistically significant departures from normality.

## ⚖️ Two-Group Comparisons

When categorical fields are available, Pogi can compare a numeric feature across two selected groups.

The output includes:

| Result | Meaning |
|---|---|
| Equal-variance t-test p-value | Mean difference test assuming equal variances. |
| Welch t-test p-value | Mean difference test without assuming equal variances. |
| Mann-Whitney p-value | Rank-based nonparametric group comparison. |
| Cohen’s d | Standardized effect size. |

## ✅ Recommended Sequence

1. Select numeric features that passed basic quality checks.
2. Choose Pearson for linear screening and Spearman for robust monotonic screening.
3. Review p-values along with correlation magnitudes.
4. Run normality diagnostics on candidate modeling fields.
5. Use two-group comparisons for categorical account or program groupings.
6. Carry forward statistically meaningful relationships into feature analysis.

## 🔗 Related Pages

- [Descriptive Statistics](descriptive-statistics.md)
- [Feature Analysis](feature-analysis.md)
- [Modeling](modeling.md)

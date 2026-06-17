# Feature Analysis

The Feature Analysis tab examines relationships among numeric features and identifies structure in the dataset.

## 🧭 Purpose

This page explains how Pogi uses correlation heatmaps, top correlated pairs, PCA projections, k-Means clustering, variance inflation factors, and pairwise scatterplots to help analysts understand feature relationships before engineering or modeling.

## 🧱 Workflow Position

Feature Analysis follows Inferential Statistics and precedes Feature Engineering. It informs which variables should be transformed, retained, excluded, scaled, or reviewed for multicollinearity.

## 🔥 Correlation Heatmap

The correlation heatmap visualizes pairwise numeric relationships. Strong positive or negative correlations may indicate redundant features, useful predictors, or variables that should be reviewed for collinearity.

## 🔗 Correlated Feature Pairs

Pogi ranks feature pairs by absolute correlation. This table helps identify the strongest relationships without manually scanning the entire heatmap.

Recommended review points:

- Pairs with very high absolute correlation may be redundant.
- Highly correlated budgetary measures may reflect accounting relationships.
- Unexpected correlations may reveal data quality issues or policy-relevant patterns.

## 🧭 PCA Projection

Principal Component Analysis reduces selected numeric features into a lower-dimensional representation. Pogi reports explained variance and plots the first principal components.

Use PCA to identify:

- Whether a few dimensions summarize the dataset.
- Whether records form visible clusters.
- Whether outliers separate from the main record population.

## 🧩 k-Means Clustering

Pogi applies k-Means in PCA space to show candidate groupings. These clusters are exploratory and should be interpreted carefully.

## 🧮 Variance Inflation Factor

The VIF table estimates multicollinearity among selected numeric features.

| VIF Pattern | Interpretation |
|---|---|
| Low VIF | Feature is not strongly explained by other selected features. |
| Moderate VIF | Some redundancy may exist. |
| Very high VIF | Feature may be collinear with other selected features. |

## ✅ Recommended Sequence

1. Select 10–15 high-value numeric features.
2. Review the correlation heatmap and top pairs.
3. Use PCA cumulative variance to evaluate dimensional structure.
4. Review PCA scatterplots for clustering or separation.
5. Check VIF before linear modeling.
6. Use the findings to guide Feature Engineering.

## 🔗 Related Pages

- [Inferential Statistics](inferential-statistics.md)
- [Feature Engineering](feature-engineering.md)
- [Anomaly Detection](anomaly-detection.md)

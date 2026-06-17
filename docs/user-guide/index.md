# User Guide

Pogi is a Streamlit analytics workbench for exploring federal budget execution data, especially SF-133-style account balance datasets. The application combines data profiling, descriptive statistics, inferential testing, feature analysis, feature engineering, anomaly detection, supervised modeling, and model diagnostics in one browser-based workflow.

## 🧭 Purpose

This guide explains how to move through the Pogi application from data loading through final model diagnostics. It is written for analysts who need to validate source data, understand financial-account behavior, detect unusual balances or execution patterns, and compare regression or classification models without leaving the Streamlit interface.

## 🧱 Workflow Position

The recommended workflow is sequential:

| Step | Page | Outcome |
|---:|---|---|
| 1 | Installation | Prepare the local Python and Streamlit environment. |
| 2 | Data Loading | Load fallback data or upload a CSV/Excel workbook. |
| 3 | Data Overview | Confirm rows, columns, inferred types, missingness, and feature quality. |
| 4 | Descriptive Statistics | Profile numeric distributions, outliers, and normality indicators. |
| 5 | Inferential Statistics | Test relationships, p-values, normality, and group differences. |
| 6 | Feature Analysis | Explore correlations, PCA structure, clustering, and multicollinearity. |
| 7 | Feature Engineering | Build a reusable feature matrix with imputation, scaling, winsorization, and encoding. |
| 8 | Anomaly Detection | Flag records that look unusual across multiple detectors. |
| 9 | Modeling | Train regression or classification models and compare performance. |
| 10 | Diagnostics | Evaluate the best trained model with residuals, confusion matrices, ROC/PR curves, and permutation importance. |

## ✅ Recommended Sequence

1. Start with the fallback workbook or a known-good CSV/Excel file.
2. Review the Data Overview tab before modeling.
3. Resolve missingness and type issues before feature engineering.
4. Build the feature matrix before training models.
5. Train multiple models rather than relying on a single estimator.
6. Review Diagnostics before treating a model result as analytically useful.

## 🔗 Related Pages

- [Installation](installation.md)
- [Data Loading](data-loading.md)
- [Feature Engineering](feature-engineering.md)
- [Modeling](modeling.md)
- [Diagnostics](diagnostics.md)

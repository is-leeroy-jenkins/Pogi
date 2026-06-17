# Data Overview

The Data Overview tab is the first analytical checkpoint after a dataset is loaded.

## 🧭 Purpose

This page explains the controls, tables, and metrics used to validate the loaded dataframe. The Data Overview tab helps confirm that Pogi has loaded the expected data, inferred useful data types, and identified missingness or low-quality features before heavier statistical or machine-learning work begins.

## 🧱 Workflow Position

Data Overview sits immediately after Data Loading and before Descriptive Statistics. It is the quality-control stage for the full workflow.

## 📊 Summary Metrics

The tab displays high-level dataframe metrics:

| Metric | Meaning |
|---|---|
| Rows | Number of records loaded into the analysis dataframe. |
| Columns | Number of fields available for profiling and modeling. |
| Numeric Columns | Number of columns currently available for numeric analysis. |
| Categorical Columns | Number of non-numeric columns available for grouping or encoding. |

## 🔎 Data Preview

The data preview shows the top rows of the loaded dataframe. Use the sidebar preview-row slider to increase or reduce the number of displayed records.

Use the preview to confirm:

- Column names loaded correctly.
- Account identifiers remain intact.
- Numeric values were not truncated.
- Missing values appear as expected.
- Uploaded workbook content matches the intended worksheet.

## 🧪 Feature Quality

The feature-quality table computes profiling measures for each column.

| Field | Meaning |
|---|---|
| `feature` | Source column name. |
| `dtype` | Pandas dtype after loading and coercion. |
| `completeness_pct` | Percentage of non-missing values. |
| `unique_values` | Count of distinct non-null values. |
| `cardinality_ratio` | Unique values divided by non-missing records. |
| `variance` | Numeric variance when applicable. |
| `entropy` | Categorical entropy when applicable. |

## 🧩 Missingness Profile

The missingness table identifies fields with missing values and ranks them by missing percentage. High missingness should be reviewed before feature engineering or model training.

## ✅ Recommended Sequence

1. Confirm the row count matches the expected extract.
2. Confirm the column count matches the source file.
3. Check whether key amount fields are numeric.
4. Review fields with high missingness.
5. Identify high-cardinality identifier fields before modeling.
6. Move to Descriptive Statistics only after the dataset passes basic validation.

## 🔗 Related Pages

- [Data Loading](data-loading.md)
- [Descriptive Statistics](descriptive-statistics.md)
- [Feature Engineering](feature-engineering.md)

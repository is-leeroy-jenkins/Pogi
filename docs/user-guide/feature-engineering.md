# Feature Engineering

The Feature Engineering tab builds a reusable modeling matrix from selected numeric and categorical features.

## 🧭 Purpose

This page explains how Pogi prepares data for anomaly detection and supervised modeling. Feature engineering converts raw dataframe columns into a cleaner analytical matrix through numeric selection, missing-value imputation, optional winsorization, scaling, and one-hot encoding.

## 🧱 Workflow Position

Feature Engineering follows Feature Analysis and precedes Anomaly Detection and Modeling. The produced feature matrix is stored in Streamlit session state and reused by the Modeling tab when available.

## 🔢 Numeric Feature Controls

| Control | Purpose |
|---|---|
| Numeric Features | Select numeric columns to include in the feature matrix. |
| Scaler | Choose no scaling, standard scaling, min-max scaling, or robust scaling. |
| Winsorize | Clip extreme tails to reduce outlier influence. |
| Winsorize limits | Set lower and upper tail clipping proportions. |

## 🧩 Missing-Value Controls

| Control | Purpose |
|---|---|
| Numeric Imputation | Fill missing values using median, mean, or most frequent value. |
| kNN Impute | Use K-nearest-neighbor imputation for numeric fields. |
| kNN Neighbors | Set the number of neighbors used during kNN imputation. |

## 🏷️ Categorical Encoding

Selected categorical features are one-hot encoded with `pandas.get_dummies`. This creates binary indicator columns for categorical levels and appends them to the numeric feature matrix.

## 📦 Feature Matrix Output

After selecting options and clicking **Build Feature Matrix**, Pogi stores the result as:

```text
st.session_state['feature_matrix']
```

The Modeling tab uses this engineered matrix automatically when it exists. If no feature matrix exists, Modeling falls back to raw numeric features.

## ✅ Recommended Sequence

1. Exclude identifier-only columns unless they have analytical meaning.
2. Use median imputation for skewed budget data.
3. Use RobustScaler when outliers are material.
4. Use StandardScaler for PCA-style or distance-sensitive workflows.
5. Winsorize only when extreme values are likely to distort models.
6. Build the feature matrix before training models.
7. Review the resulting matrix shape and preview before modeling.

## 🔗 Related Pages

- [Feature Analysis](feature-analysis.md)
- [Anomaly Detection](anomaly-detection.md)
- [Modeling](modeling.md)

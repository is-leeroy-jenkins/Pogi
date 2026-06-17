# Modeling

The Modeling tab trains and compares regression or classification models using the engineered feature matrix when available.

## 🧭 Purpose

This page explains how Pogi trains supervised machine-learning models and compares model performance. Modeling helps determine whether selected features can predict a numeric target, classify account behavior, or separate high-level analytical categories.

## 🧱 Workflow Position

Modeling follows Feature Engineering. It produces the fitted best-model payload that the Diagnostics tab uses for residual analysis, confusion matrices, ROC/PR curves, and feature importance.

## 🎯 Target Selection

The target column is selected from the loaded dataframe. The selected task type determines how Pogi interprets the target.

| Task | Target Handling | Output Metrics |
|---|---|---|
| Regression | Target is coerced to numeric values. | RMSE, MAE, R². |
| Classification | Target is label-encoded or converted into classes. | Accuracy and classification diagnostics. |

## 🧮 Regression Models

Pogi supports several regression estimators, including:

- Linear Regression
- Ridge
- Lasso
- ElasticNet
- Bayesian Ridge
- SGD Regressor
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- Extra Trees Regressor
- K-Neighbors Regressor
- Support Vector Regressor

## ✅ Classification Models

Pogi supports several classification estimators, including:

- Logistic Regression
- Linear SVC
- RBF SVC
- SGD Classifier
- Decision Tree Classifier
- Random Forest Classifier
- Gradient Boosting Classifier
- Extra Trees Classifier
- K-Neighbors Classifier
- Gaussian Naive Bayes
- Linear Discriminant Analysis, when available
- Quadratic Discriminant Analysis, when available

## 📦 Diagnostics Payload

After training, Pogi saves the best model and related arrays in session state:

```text
st.session_state['last_model_payload']
```

The Diagnostics tab reads this payload to render model-specific diagnostic outputs.

## ✅ Recommended Sequence

1. Build a feature matrix before modeling.
2. Select a target column with analytical meaning.
3. Choose regression for continuous numeric outcomes.
4. Choose classification for categorical or binned outcomes.
5. Train multiple models for comparison.
6. Review the best model in Diagnostics before using results.

## 🔗 Related Pages

- [Feature Engineering](feature-engineering.md)
- [Diagnostics](diagnostics.md)
- [Descriptive Statistics](descriptive-statistics.md)

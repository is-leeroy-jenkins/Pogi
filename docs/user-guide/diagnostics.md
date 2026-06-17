# Diagnostics

The Diagnostics tab evaluates the best model produced by the Modeling tab.

## 🧭 Purpose

This page explains how Pogi reviews fitted model behavior after training. Diagnostics help determine whether a model is accurate, stable, interpretable, and appropriate for the analytical question.

## 🧱 Workflow Position

Diagnostics is the final analytical stage in the Pogi workflow. It depends on the model payload produced by the Modeling tab.

## 📦 Required Session State

Diagnostics requires:

```text
st.session_state['last_model_payload']
```

If no model has been trained, the Diagnostics tab prompts the user to train models first.

## 📈 Regression Diagnostics

For regression tasks, Pogi displays:

| Diagnostic | Purpose |
|---|---|
| Residuals vs Predicted | Checks misspecification and non-constant variance. |
| Residual Distribution | Shows whether residuals are centered and symmetric. |
| Residual Q-Q Plot | Compares residuals to a normal distribution. |
| Permutation Importance | Estimates which features affect model performance most. |

Review residual diagnostics carefully. Strong residual patterns can indicate omitted variables, nonlinear relationships, heteroskedasticity, or an inappropriate model family.

## ✅ Classification Diagnostics

For classification tasks, Pogi displays:

| Diagnostic | Purpose |
|---|---|
| Confusion Matrix | Shows correct and incorrect class predictions. |
| Classification Report | Reports precision, recall, F1-score, and support. |
| ROC Curve | Shows binary classifier ranking performance when scores are available. |
| Precision-Recall Curve | Useful for imbalanced classes. |
| Permutation Importance | Estimates which features affect model performance most. |

## 🧠 Permutation Importance

Permutation importance measures the average performance drop when a feature is shuffled. Higher values suggest a feature contributes more to model performance. This is model-agnostic, but it should be interpreted alongside correlation, domain knowledge, and data quality.

## ✅ Recommended Sequence

1. Confirm which model was selected as best.
2. Review regression residuals or classification errors.
3. Check whether performance metrics align with the analytical objective.
4. Review permutation importance for interpretability.
5. Return to Feature Engineering if diagnostics are weak.
6. Treat model results as decision support, not as standalone proof.

## 🔗 Related Pages

- [Modeling](modeling.md)
- [Feature Engineering](feature-engineering.md)
- [Anomaly Detection](anomaly-detection.md)

# Data Loading

Pogi can load a fallback workbook from the repository or accept a user-uploaded CSV or Excel workbook through the Streamlit sidebar.

## 🧭 Purpose

This page explains how source data enters the Pogi workflow. Data loading establishes the dataframe used by every downstream tab, including data overview, statistics, feature engineering, anomaly detection, modeling, and diagnostics.

## 🧱 Workflow Position

Data loading occurs before all analytical work. The loaded dataframe is immediately normalized for numeric-like columns and then reused across the application.

## 📥 Supported Inputs

| Source | Description | Typical Use |
|---|---|---|
| Fallback workbook | Loads `data/excel/Account Balances.xlsx` when fallback loading is enabled. | Standard demo or known test data. |
| CSV upload | Loads a comma-separated dataset through the sidebar uploader. | Flat analytical extract. |
| Excel upload | Loads workbook formats such as `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, or `.ods`. | Agency workbooks or analyst-prepared extracts. |
| Worksheet selector | Displays available worksheets for supported workbook uploads. | Select the correct tab from a multi-sheet workbook. |

## 🔢 Numeric Coercion

After loading, Pogi attempts to convert object/string columns into numeric columns when most non-null values parse as numbers. This is important for budget data because amounts may arrive as text with commas, dollar signs, parentheses, or placeholder characters.

Examples of values that can be normalized include:

```text
"1,250,000"
"$45,000"
"(12,500)"
"-"
"—"
```

## ✅ Recommended Sequence

1. Use fallback data first to confirm the application works.
2. Turn fallback loading off when using your own file.
3. Upload a CSV or workbook.
4. Select the correct worksheet when applicable.
5. Review the Data Overview tab immediately after loading.
6. Confirm numeric fields were inferred correctly before modeling.

## ⚠️ Data Loading Risks

| Risk | Why It Matters | Mitigation |
|---|---|---|
| Wrong worksheet selected | Downstream analysis may use the wrong table. | Confirm row and column counts in Data Overview. |
| Numeric values stored as text | Models and statistical functions may exclude important columns. | Review numeric/categorical counts and feature quality. |
| Missing fallback file | App cannot load the default workbook. | Confirm the fallback path exists or upload a file. |
| Mixed-format columns | Coercion may leave fields categorical. | Clean source data before upload or adjust source formatting. |

## 🔗 Related Pages

- [Data Overview](data-overview.md)
- [Feature Engineering](feature-engineering.md)

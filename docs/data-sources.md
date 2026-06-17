# Data Sources

Pogi is designed for structured federal budget execution and account-balance data. The application
can work with any compatible CSV or Excel dataset, but its primary analytical context is SF-133,
Treasury Account Symbol, File A, and account-level budget execution reporting.

The data-source architecture is intentionally flexible. Pogi does not require a fixed schema before
loading data. Instead, it loads tabular records, infers numeric and categorical fields, promotes
numeric-like strings into numeric columns when appropriate, and allows the analyst to validate the
resulting dataset before running statistics, anomaly detection, or modeling.

---

## 🧭 Purpose

This page explains the data sources, budget-reporting context, ingestion model, and validation
expectations for Pogi.

Pogi supports analysis of:

1. Budgetary resources.
2. Obligations.
3. Outlays.
4. Recoveries.
5. Unobligated balances.
6. Treasury Account Symbol-level records.
7. Account balance datasets.
8. SF-133-style reporting extracts.
9. DATA Act File A-style account records.
10. Other structured financial or operational datasets.

The application is not limited to one source file. It is a reusable analytics workbench for tabular
financial data.

---

## 🏛️ Federal Budget Data Context

Pogi’s primary subject area is federal budget execution. In this context, the most relevant data
sources include SF-133 reports, Treasury Account Symbol balances, Governmentwide Treasury Account
Symbol Adjusted Trial Balance System data, and DATA Act account-level files.

| Source                                                    | Role in Budget Analysis                                                            |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| SF-133 Report on Budget Execution and Budgetary Resources | Provides budget execution reporting by account                                     |
| Treasury Account Symbol data                              | Identifies accounts, funding structure, and account-level balances                 |
| GTAS data                                                 | Provides trial-balance information submitted by federal agencies                   |
| DATA Act File A                                           | Provides account-level budgetary information used in federal spending transparency |
| Account Balances workbook                                 | Local analytical dataset used by the application fallback mode                     |
| CSV or Excel uploads                                      | User-provided analytical datasets                                                  |

Pogi is built to help analysts inspect these records, profile their quality, identify anomalies, and
compare statistical or machine-learning models.

---

## 🧾 SF-133 Reports

The SF-133 Report on Budget Execution and Budgetary Resources is a major federal budget execution
report. It provides account-level information about budgetary resources, obligations, outlays,
recoveries, and unobligated balances.

In a Pogi workflow, SF-133-style data can support:

| Analytical Question                                          | Pogi Capability                                               |
| ------------------------------------------------------------ | ------------------------------------------------------------- |
| Which accounts have unusually high or low balances?          | Descriptive statistics and anomaly detection                  |
| Which variables are correlated with obligations or outlays?  | Correlation analysis and feature analysis                     |
| Which records appear unusual compared with similar accounts? | Isolation Forest, Local Outlier Factor, PCA-distance voting   |
| Which fields explain a target balance or category?           | Regression/classification modeling and permutation importance |
| Which accounts should be reviewed before reporting?          | Missingness, feature quality, and diagnostics                 |

SF-133 data is especially useful when the analyst needs to evaluate budget execution behavior across
accounts, agencies, reporting periods, or fiscal categories.

---

## 🧮 Treasury Account Symbol Data

Treasury Account Symbols identify federal accounts and support account-level budget execution
analysis.

Typical TAS-related fields may include:

| Field Type                | Examples                                                           |
| ------------------------- | ------------------------------------------------------------------ |
| Account identifiers       | Treasury Account Symbol, main account, bureau code, agency code    |
| Account descriptions      | Account name, program name, fund title                             |
| Fiscal structure          | fiscal year, availability period, account type                     |
| Budget execution measures | budgetary resources, obligations, outlays, recoveries, balances    |
| Classification fields     | discretionary/mandatory, appropriation type, function, subfunction |

Pogi does not require every field to be present. The application works with whatever columns exist
in the loaded dataframe and allows the analyst to choose target variables and features at runtime.

---

## 📊 DATA Act File A Context

DATA Act File A contains account-level budgetary data. It is commonly used to connect federal
account balances and execution amounts to broader spending and transparency reporting.

File A-style data is useful in Pogi because it may contain:

| Category              | Example Analytical Use                                    |
| --------------------- | --------------------------------------------------------- |
| Budgetary resources   | Identify accounts with unusually high available resources |
| Obligations           | Analyze commitment patterns                               |
| Outlays               | Support spend-out analysis                                |
| Unobligated balances  | Detect accounts with large residual balances              |
| TAS-level identifiers | Join or group records by account                          |
| Agency/bureau fields  | Compare execution behavior across organizations           |

Pogi can ingest File A-style extracts when they are saved as CSV or Excel files.

---

## 🗃️ Fallback Dataset

Pogi includes a fallback loading mode for local use.

The default fallback file path is:

```
data/excel/Account Balances.xlsx
```

When fallback mode is enabled, the application loads this workbook instead of requiring a user
upload.

Fallback mode is useful for:

| Use Case                  | Reason                                                             |
| ------------------------- | ------------------------------------------------------------------ |
| Demonstrations            | Allows the app to run immediately with bundled data                |
| Development               | Provides a stable dataset for testing interface changes            |
| Documentation screenshots | Gives consistent application behavior                              |
| Training                  | Lets new users explore the workflow before bringing their own data |

If the fallback file is missing, Pogi stops the run and displays a Streamlit error message. This
prevents the rest of the application from running against an undefined dataframe.

---

## 📥 Uploaded Data

When fallback mode is disabled, Pogi accepts user-uploaded local files through the Streamlit
sidebar.

Supported upload formats include:

| Format  | Notes                                                                       |
| ------- | --------------------------------------------------------------------------- |
| `.csv`  | Loaded with `pandas.read_csv`                                               |
| `.xls`  | Loaded as an Excel workbook                                                 |
| `.xlsx` | Loaded as an Excel workbook through `openpyxl`                              |
| `.xlsm` | Loaded as a macro-enabled Excel workbook                                    |
| `.xlsb` | Loaded as a binary Excel workbook when the required engine is available     |
| `.ods`  | Loaded as an OpenDocument spreadsheet when the required engine is available |

For multi-sheet workbooks, Pogi attempts to discover worksheet names and allows the user to select
the worksheet to import.

---

## 🔄 Data Loading Flow

The application uses a two-path data loading flow.

```
Start
│
├── Use fallback data = enabled
│       │
│       ├── Load data/excel/Account Balances.xlsx
│       └── Stop with error if fallback file is missing
│
└── Use fallback data = disabled
        │
        ├── Wait for uploaded CSV or Excel file
        ├── Discover worksheet names when applicable
        ├── Load selected file or worksheet
        └── Stop with error if file parsing fails
```

After loading, Pogi applies numeric coercion and column classification before the user begins
analysis.

---

## 🧹 Numeric-Like Column Coercion

Budget and accounting data often arrive with numeric values stored as text. This can happen when
data includes commas, dollar signs, parentheses for negatives, dashes, blank strings, or mixed
formatting.

Pogi includes a numeric-coercion step that attempts to convert object or string columns into numeric
columns when the column is predominantly numeric-like.

Examples of values that may be cleaned include:

| Raw Value    | Intended Meaning             |
| ------------ | ---------------------------- |
| `1,250,000`  | numeric value                |
| `$450,000`   | numeric value                |
| `(25,000)`   | negative numeric value       |
| `-`          | missing or placeholder value |
| blank string | missing value                |

The coercion process helps ensure that budget amounts are available for descriptive statistics,
correlations, feature engineering, anomaly detection, and modeling.

---

## 🧠 Type Inference

After data loading and numeric coercion, Pogi separates columns into analytical groups.

```
Loaded DataFrame
│
├── Floating-point columns
├── Integer columns
├── Boolean columns
├── Numeric columns
└── Non-numeric columns
```

These groups are used throughout the interface.

| Column Group        | Used For                                                                    |
| ------------------- | --------------------------------------------------------------------------- |
| Numeric columns     | Descriptive statistics, correlations, PCA, anomaly detection, modeling      |
| Non-numeric columns | Group comparisons, categorical selection, one-hot encoding                  |
| Integer columns     | Included in numeric analysis when the user enables the integer-coded option |
| Boolean columns     | Identified separately from continuous numeric fields                        |

The analyst should review the inferred types in the Data Overview tab before modeling.

---

## ✅ Data Quality Checks

Pogi includes multiple data-quality checks before advanced modeling.

| Check                | Purpose                                                                      |
| -------------------- | ---------------------------------------------------------------------------- |
| Row count            | Confirms record volume                                                       |
| Column count         | Confirms feature volume                                                      |
| Missingness profile  | Identifies null-heavy fields                                                 |
| Feature quality      | Evaluates completeness, uniqueness, cardinality ratio, variance, and entropy |
| Numeric profile      | Reviews central tendency, dispersion, distribution shape, and outlier rates  |
| Correlation analysis | Detects relationships and redundant features                                 |
| VIF analysis         | Identifies multicollinearity                                                 |
| Normality tests      | Reviews distribution assumptions                                             |

These checks help determine whether the dataset is ready for modeling or requires cleaning.

---

## 📉 Common Budget Execution Measures

Pogi can analyze any numeric field, but the following budget execution measures are common
candidates.

| Measure                | Analytical Use                                    |
| ---------------------- | ------------------------------------------------- |
| Budgetary resources    | Measures available funding authority or resources |
| Obligations            | Measures legally binding commitments              |
| Outlays                | Measures disbursements or payments                |
| Recoveries             | Measures recovered prior obligations or balances  |
| Unobligated balances   | Measures available balances not yet obligated     |
| Gross outlays          | Supports spend-out and execution-rate analysis    |
| Offsetting collections | Supports net resource and receipt analysis        |
| Transfers              | Supports account movement and execution review    |

These measures can be used as targets, predictors, grouping dimensions, or anomaly-review variables
depending on the dataset.

---

## 🧪 Recommended Data Preparation Sequence

Use this sequence before running modeling or anomaly detection:

1. Load the fallback workbook or upload a CSV/Excel file.
2. Confirm that the expected rows and columns loaded.
3. Review inferred numeric and non-numeric columns.
4. Inspect missingness and feature quality.
5. Identify ID-like fields that should not be treated as predictive numeric variables.
6. Review descriptive statistics for major budget fields.
7. Check distributions and outliers.
8. Review correlations and VIF before feature engineering.
9. Build the feature matrix.
10. Run anomaly detection or modeling.

This sequence helps prevent common modeling problems caused by missing values, misclassified
columns, high-cardinality identifiers, or highly collinear fields.

---

## 🚫 Fields to Treat Carefully

Some fields may be numeric but should not automatically be treated as continuous modeling features.

| Field Type                | Reason for Caution                                     |
| ------------------------- | ------------------------------------------------------ |
| Account codes             | Numeric identifiers may not have mathematical distance |
| Treasury symbols          | Often categorical even when they contain numbers       |
| Bureau codes              | Usually identifiers rather than continuous measures    |
| Agency codes              | Usually grouping variables                             |
| Fiscal years              | May be ordinal but should be handled intentionally     |
| Line numbers              | Often report structure, not measured values            |
| Unique record identifiers | Can create leakage or meaningless model splits         |

The sidebar option to include integer-coded columns is useful, but the analyst should validate
whether those columns are true measures or identifiers.

---

## 🔍 Data Validation Checklist

Before using Pogi outputs for analysis, confirm:

| Question                                 | Why It Matters                                  |
| ---------------------------------------- | ----------------------------------------------- |
| Did the expected file load?              | Prevents analysis on stale or fallback data     |
| Did the expected worksheet load?         | Prevents analysis on the wrong workbook tab     |
| Are numeric fields correctly typed?      | Required for statistics and modeling            |
| Are categorical fields preserved?        | Required for grouping and encoding              |
| Are missing values understood?           | Prevents biased or unstable models              |
| Are ID fields excluded when appropriate? | Prevents meaningless feature importance         |
| Are extreme outliers valid?              | Distinguishes real anomalies from data errors   |
| Is the target variable appropriate?      | Prevents invalid regression/classification runs |
| Is the sample size sufficient?           | Supports meaningful model comparison            |

---

## 🧱 Data Architecture Diagram

```
Data Source
│
├── Fallback Workbook
│   └── data/excel/Account Balances.xlsx
│
└── User Upload
    ├── CSV
    └── Excel Workbook
        ├── XLS
        ├── XLSX
        ├── XLSM
        ├── XLSB
        └── ODS

Loaded DataFrame
│
├── Numeric-Like Coercion
│   ├── remove commas
│   ├── remove dollar signs
│   ├── convert parentheses to negatives
│   ├── normalize blanks and placeholders
│   └── parse numeric values
│
├── Column Classification
│   ├── numeric columns
│   ├── non-numeric columns
│   ├── floating-point columns
│   ├── integer columns
│   └── boolean columns
│
├── Quality Review
│   ├── feature quality
│   ├── missingness
│   ├── descriptive profile
│   └── outlier rates
│
└── Analytical Workflow
    ├── inferential statistics
    ├── feature analysis
    ├── feature engineering
    ├── anomaly detection
    ├── modeling
    └── diagnostics
```

---

## 🔐 Data Handling Notes

Pogi runs locally in the Streamlit session. Uploaded files are processed through the running
application session and used to create dataframes, charts, model inputs, and diagnostics.

Recommended handling practices:

1. Use approved local datasets.
2. Validate data sensitivity before uploading files into the application.
3. Avoid loading files that contain unnecessary personally identifiable information.
4. Keep authoritative records in their official source systems.
5. Treat Pogi outputs as analytical aids, not official determinations.
6. Preserve source data lineage when exporting or sharing results.
7. Validate results against authoritative budget and accounting systems before operational use.

---

## 🏛️ Government Use Considerations

For government budget analysis, Pogi should be treated as an exploratory analytics tool.

Appropriate uses include:

| Appropriate Use            | Description                                                |
| -------------------------- | ---------------------------------------------------------- |
| Initial data profiling     | Identify missingness, outliers, and feature quality issues |
| Analytical review          | Explore correlations, distributions, and account behavior  |
| Anomaly triage             | Identify records that may require analyst review           |
| Model comparison           | Compare candidate forecasting or classification approaches |
| Audit support              | Prepare issue lists, outlier tables, and diagnostic views  |
| Training and demonstration | Explain data-science workflows using budget data           |

Pogi should not replace official financial systems, certified reporting processes, or authoritative
budget execution controls.

---

## 🛠️ Development Implications

The current data-source architecture is flexible, but future development may benefit from additional
structure.

Recommended future improvements include:

| Improvement               | Value                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------- |
| Schema profiles           | Validate expected SF-133, File A, or TAS columns                                      |
| Data dictionary support   | Explain fields directly in the interface                                              |
| Source metadata capture   | Track filename, worksheet, upload time, and row counts                                |
| Validation rules          | Flag invalid fiscal years, missing TAS values, or negative values where inappropriate |
| Exportable audit trail    | Preserve analysis settings and data quality findings                                  |
| Column role tagging       | Mark fields as identifier, measure, category, target, or excluded                     |
| Data lineage panel        | Show where the active dataframe came from                                             |
| Automated sample datasets | Support training and repeatable demonstrations                                        |

These enhancements would make Pogi more reliable for repeatable analytical workflows while
preserving its flexible exploratory design.

---

## ✅ Summary

Pogi’s data-source model is built around practical tabular ingestion. It supports fallback data,
user-uploaded CSV files, user-uploaded Excel workbooks, worksheet selection, numeric-like field
coercion, and flexible type inference.

The application is especially useful for SF-133, Treasury Account Symbol, File A, and
account-balance analysis, but it can support any compatible structured dataset. The most important
user responsibility is to validate the loaded data before relying on statistical, anomaly-detection,
or modeling outputs.


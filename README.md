###### Pogi
![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/git/pogi_project.png)
___


[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/pogi/)

SF-133 Forecasting Tool
- A machine-learning pipeline for forecasting and reporting Treasury Account Symbol balances using active data.
- Project federal balances using generative ai
- Analyze funding metrics with classification and regression models

## 🎥 Demo
![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/pogi-demo.gif)

---

![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/Pogi-nb.gif)  


## ☁️ Cloud

<table>
<tr>
<td align="center">
<img width="190" height="1" alt=""><br>
<a href="https://pogi.nicemoss-d8fe9d95.centralus.azurecontainerapps.io">
<img src="https://img.shields.io/badge/Docker-App-2496ED?logo=docker&logoColor=white" alt="Docker App">
</a>
</td>

<td align="center">
<img width="190" height="1" alt=""><br>
<a href="https://pogi-py.streamlit.app/">
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit App">
</a>
</td>

<td align="center">
<img width="190" height="1" alt=""><br>
<a href="https://colab.research.google.com/github/is-leeroy-jenkins/sake/blob/master/models.ipynb">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">
</a>
</td>

<td align="center">
<img width="190" height="1" alt=""><br>
<a href="https://dbc-a0c21f80-7bb3.cloud.databricks.com/editor/notebooks/1460524320197769?o=7474645703081351">
<img src="https://img.shields.io/badge/Databricks%20Repo-Cutey--Py-FF3621?logo=databricks&logoColor=white" alt="Databricks Notebook">
</a>
</td>

<td align="center">
<a href="https://leeroy.usw-16.palantirfoundry.com/shares/links/f7n2aa6beh6q2">
<img width="190" height="1" alt=""><br>
<img src="https://img.shields.io/badge/Palantir%20Foundry-Repo-101113?logo=palantir&logoColor=white" alt="Palantir Repo">
</a>
</td>
</tr>
</table>

### ![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/assets/images/github/Appropriation.png) Modeling Budget Execution & Available Resources


#### 📊 Regression
- Linear, Ridge, Lasso, ElasticNet
- Decision Tree, Random Forest, Gradient Boosting
- SVR, KNN, MLP Regressor, Bayesian Ridge, Huber Regressor

#### ✅ Classification
- Logistic Regression, Perceptron, SVM, KNN
- Decision Tree, Random Forest, Extra Trees, AdaBoost, Gradient Boosting
- MLP Classifier, Naive Bayes

## 📊 Diagnostics & Evaluation

- Scatter plots, residuals, precision-recall, ROC curves
- Confusion matrices, ANOVA tests, statistical fitting
- PCA visualizations and correlation heatmaps

## 📁 Data & Engineering

- Excel and CSV ingestion
- Imputation (`SimpleImputer`, `KNNImputer`)
- Scaling (`StandardScaler`, `MinMaxScaler`, `RobustScaler`)
- Feature creation via polynomial expansion
- Dimensionality reduction and outlier detection



## 🏛️ Use in Government

- 📉 Budget Execution forecasting
- 🏛️ Congressional Appropriations scenario testing
- 🧮 Audit prep and fiscal behavior anomaly detection



## 🚀 How to Run

```bash

git clone https://github.com/your-username/pogi.git
cd pogi
pip install -r requirements.txt
jupyter notebook models.ipynb
```


### Option A — Google Colab (no local setup)

```
1. Click the **Open In Colab** badge above.
2. Upload your CSV or mount Google Drive.
3. Set `DATA_PATH` near the top of the notebook.
4. **Runtime → Run all**.
```

### Option B — Local (conda or venv)

#### 1) Create environment
```

  bash
  
  conda create -n pogi python=3.11 -y
  conda activate pogi

```

#### 2) Install dependencies
```

  pip install -U pip wheel setuptools
  pip install pandas numpy scipy matplotlib seaborn scikit-learn jupyter

```

#### 3) Launch Jupyter
```

  jupyter notebook

```

- Open `ipynb/schedule-x.ipynb` and run cells top-to-bottom.


### 📥 Clone the Repository

- First, clone the Pogi repository from GitHub and navigate into the project directory:

```bash

git clone https://github.com/<your-org-or-username>/pogi.git
cd pogi
```



### 🐍 Create a Python Virtual Environment (Recommended)

- Using a virtual environment is strongly recommended to isolate dependencies and avoid version conflicts.

**Windows (PowerShell):**

```bash

python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash

python3 -m venv .venv
source .venv/bin/activate
```



### 📦 Install Dependencies

- Install the required Python packages using `pip`:

```bash

pip install --upgrade pip
pip install -r requirements.txt
```

- This installs only the libraries required to run the Streamlit application (no notebook-only or experimental dependencies).


### ▶️ Run the Streamlit App

- Start the application using Streamlit:

```bash

streamlit run app.py
```

- Once launched, Streamlit will display a local URL (typically `http://localhost:8501`) in the terminal. Open this link in your web browser to access the app.


### 📊 Using the Application

After the app starts:

1. Upload a CSV or Excel dataset.
2. Select the target variable and feature columns.
3. Choose:

   * Regression or classification
   * Preprocessing options (imputation, scaling)
   * A machine-learning model
4. Click **Train Model** to view diagnostics and performance metrics.

- All model training and evaluation occur locally in your browser session.



### 🛑 Stopping the App

- To stop the Streamlit server, return to the terminal and press:

```text

CTRL + C
```



## 🧩 Troubleshooting

* Ensure Python **3.10 or newer** is installed.
* If `streamlit` is not found, verify the virtual environment is activated.
* If installation fails, try:

  ```bash
  
  pip install --no-cache-dir -r requirements.txt
  ```


## 🔬 Data Sources

- The SF 133 Report on Budget Execution and Budgetary Resources fulfills the requirement in 31 U.S.C. 1511 - 1514
- That is, the President reviews Federal expenditures at least four times a year.
- SF 133s provide historical reference that can be used to help prepare the President's Budget, program operating plans, and spend-out rate estimates.
- For further information on the SF 133 from the US Treasury [here](https://tfx.treasury.gov/taxonomy/term/10991) 
- SF 133 inventory of reports from 1998 - 2025 can be found on OMB's MAX [here](https://portal.max.gov/portal/document/SF133/Budget/FACTS%20II%20-%20SF%20133%20Report%20on%20Budget%20Execution%20and%20Budgetary%20Resources.html)
- Agencies submit the data that appear on these reports to the Department of the Treasury Bureau of Fiscal Service.
- While OMB publishes these reports, the underlying data is submitted by the agencies.
- File A (Account Balances) published monthly by agencies on [USASpending](https://www.usaspending.gov/federal_account)
- Required by the DATA Act.
- Pulled automatically from data in the [Governmentwide Treasury Account Symbol Adjusted Trial Balance System (GTAS)](https://fiscal.treasury.gov/gtas/)
- Contains Budgetary resources, obligation, and outlay data for all the relevant Treasury Account Symbols (TAS) in a reporting agency.
- It includes both award and non-award spending (grouped together), and crosswalks with the [SF 133 report](https://portal.max.gov/portal/document/SF133/Budget/FACTS%20II%20-%20SF%20133%20Report%20on%20Budget%20Execution%20and%20Budgetary%20Resources.html).

___

## 📊 Descriptive Statistics

| Statistic         | Description                             | Use in Budget Analysis                                               |
|------------------|-----------------------------------------|----------------------------------------------------------------------|
| **Mean**         | Average value                           | Avg. Outlays, Obligations, etc., across accounts                |
| **Median**       | Middle value                            | Robust central tendency in skewed financial data                    |
| **Mode**         | Most frequent value                     | Identify common MainAccountCodes or Availability categories     |
| **Standard Deviation** | Spread around the mean                | Indicates variability in execution rates or balances                |
| **Variance**     | Square of standard deviation            | Used in statistical tests and model diagnostics                     |
| **Range**        | Difference between max and min          | Measures total spread of financial metrics                          |
| **Interquartile Range (IQR)** | Spread of middle 50% of data           | Identifies budget outliers and extreme accounts                     |
| **Skewness**     | Asymmetry of distribution               | Skewed obligations suggest few accounts dominate totals             |
| **Kurtosis**     | "Peakedness" of distribution            | High values indicate outlier-prone financial data                   |





## 🔍 Inferrential Statistics


| Metric           | Description                                            | Use in Budget Analysis                                               |
|-------------------------|--------------------------------------------------------|----------------------------------------------------------------------|
| **Pearson Correlation** | Linear relationship between variables                  | E.g., TotalResources vs. Obligations                                 |
| **Spearman Correlation**| Monotonic (rank-based) relationship                    | More robust to non-linear trends in financial execution              |
| **t-test**              | Compare means between 2 groups                         | Discretionary vs. Mandatory accounts' execution rates                |
| **ANOVA**               | Compare means across multiple groups                   | Obligations across availability periods or account types             |
| **Chi-square Test**     | Categorical independence                               | Are Main Account Codes related to availability or a specific agency? |
| **Confidence Intervals**| Estimate range of a population mean                    | Upper and lower bound expected obligations or recoveries             |
| **Regression Coefficients (p-values)** | Test variable significance                             | Are Recoveries a significant predictor of UnobligatedBalance?        |
| **F-statistic (overall regression)**   | Test whole model fit                                   | Determines the combined influence of all predictors                  |
| **Z-score / Outlier Tests** | Deviation from standard mean                           | Identify abnormal balances or lapse rates                            |
| **Boxplots**            | Visual outlier detection                               | Discover obligation anomalies within agencies                        |



## 📈 Feature Correlations

![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/git/PogiCorrelationAnalysis.gif)



## 🧠 Machine-Learning Models
![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/git/PogiLearningModels.gif)


## Fine-Tuning Dataset

| File Name                                                                                                                                                                 | Description                                                                                                            |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| [Balanced Budget and Emergency Deficit Control Act of 1985](https://huggingface.co/datasets/leeroy-jankins/The-Balanced-Budget-And-Emergency-Deficit-Control-Act-of-1985) | Establishes statutory limits on federal spending and deficit control mechanisms, including sequestration procedures.   |
| [Budget Control Act of 2011](https://huggingface.co/datasets/leeroy-jankins/The-Budget-Control-Act-2011)                                                                  | Sets discretionary spending caps and establishes enforcement mechanisms to control federal deficits.                   |
| [Digital Accountability And Transparency Act of 2014](https://huggingface.co/datasets/leeroy-jankins/Data-Act-2014)                                                       | Requires standardized federal spending data and improved transparency through government-wide financial reporting.     |
| [Federal Account Symbols And Titles Book](https://huggingface.co/datasets/leeroy-jankins/FastBook)                                                                        | Defines Treasury account symbols and official titles used for federal budgetary and accounting purposes.               |
| [Federal Acquisition Regulation](https://huggingface.co/datasets/leeroy-jankins/Federal-Acquisition-Regulation)                                                           | Establishes uniform policies and procedures governing the acquisition of goods and services by federal agencies.       |
| [Federal Government Standards For Internal Controls](https://huggingface.co/datasets/leeroy-jankins/Federal-Government-Standards-For-Internal-Controls)                   | Defines the internal control framework for federal agencies to ensure accountability, integrity, and compliance.       |
| [Federal Managers Financial Integrity Act of 1982](https://huggingface.co/datasets/leeroy-jankins/FMFIA-1982)                                                             | Requires agencies to establish internal controls and report annually on their effectiveness.                           |
| [Federal Trust Fund Accounting Guide](https://huggingface.co/datasets/leeroy-jankins/Federal-Trust-Fund-Accounting-Guide)                                                 | Provides accounting guidance for the management and reporting of federal trust funds.                                  |
| [Financial Management Regulations DOD 7000-14-R](https://huggingface.co/datasets/leeroy-jankins/DOD-7000-14-Financial-Management-Regulation)                                                                                                                        | Establishes DoD-specific financial management policies, procedures, and accounting requirements.                       |
| [Fiscal Responsibility Act](https://huggingface.co/datasets/leeroy-jankins/The-Fiscal-Responsibility-Act-of-2023)                                                                                                                                                 | Establishes statutory measures intended to improve fiscal discipline and control federal spending.                     |
| [Government Auditing Standards](https://huggingface.co/datasets/leeroy-jankins/Government-Auditing-Standards)                                                                                                                                             | Sets professional standards for audits of government organizations, programs, activities, and functions.               |
| [Government Invoicing User Guide](https://huggingface.co/datasets/leeroy-jankins/Government-Performance-and-Results-Act)                                                                                                                                           | Provides guidance on federal invoicing standards and processes for government transactions.                            |
| [Government Performance and Results Act of 1993](https://huggingface.co/datasets/leeroy-jankins/Government-Performance-and-Results-Act)                                                                                                                            | Requires agencies to engage in strategic planning and performance measurement to improve program effectiveness.        |
| [GPRA Modernization Act of 2010](https://huggingface.co/datasets/leeroy-jankins/The-GPRA-Modernization-Act-Of-2010)                                                                                                                                            | Updates GPRA by strengthening performance management, cross-agency goals, and accountability.                          |
| [OMB Circular A-11 Preparation Submission And Execution Of The Budget](https://huggingface.co/datasets/leeroy-jankins/OMB-Circular-A-11)                                                                                                      | Provides comprehensive guidance for preparing, submitting, and executing the President’s Budget.                       |
| [OMB Circular A-11 Section 120 Apportionment Process](https://huggingface.co/datasets/leeroy-jankins/OMB-Circular-A11-Section-120-Apportionment-Process)                                                                                                                       | Defines the apportionment process used to control the rate of obligation of budgetary resources.                       |
| [OMB Circular A-123 Managements Responsibility for Enterprise Risk Management and Internal Control](https://huggingface.co/datasets/leeroy-jankins/OMB-Circular-A-123)                                                                         | Defines management responsibilities for internal control and enterprise risk management across federal agencies.       |
| [Federal Trust Fund Accounting Guide](https://huggingface.co/datasets/leeroy-jankins/Federal-Trust-Fund-Accounting-Guide)                                                                                                                       | Establishes requirements for federal agency financial statements and reporting.                                        |
| [Principles Of Federal Appropriations Law Volume One](https://huggingface.co/datasets/leeroy-jankins/Principles-Of-Federal-Appropriations-Law)                                                                                                                       | Authoritative GAO guidance on foundational principles governing the use of federal appropriations.                     |
| [Statements of Federal Federal Financial Accounting Concepts and Standards](https://huggingface.co/datasets/leeroy-jankins/Statements-Of-Federal-Financial-Accounting-Concepts-And-Standards)                                                                                                 | Establishes accounting concepts and standards for federal financial reporting.                                         |
| [The Anti-Deficiency Act PL 97-258](https://huggingface.co/datasets/leeroy-jankins/The-Anti-Deficiency-Act)                                                                                                                                         | Prohibits federal agencies from obligating or expending funds in excess of appropriations or before enactment.         |
| [The Anti-Deficiency Reform and Enforcement Act of 2018](https://huggingface.co/datasets/leeroy-jankins/The-Anti-Deficiency-Reform-And-Enforcement-Act-Of-2018)                                                                                                                    | Strengthens Anti-Deficiency Act enforcement and reporting requirements to improve fiscal accountability.               |
| [The Chief Financial Officers Act of 1990](https://huggingface.co/datasets/leeroy-jankins/The-Chief-Financial-Officers-Act-1990)                                                                                                                                  | Establishes agency Chief Financial Officers and modernizes federal financial management practices.                     |
| [The Congressional Budget and Impoundment Control Act of 1974](https://huggingface.co/datasets/leeroy-jankins/The-Congressional-Budget-And-Impoundment-Control-Act-Of-1974)                                                                                                              | Establishes the congressional budget process and restricts executive impoundment of appropriated funds.                |
| [Statutory Pay As You Go Act of 2010](https://huggingface.co/datasets/leeroy-jankins/Statutory-Pay-As-You-Go-Act-of-2010)                                                                                                                                                   | Authorizes interagency agreements for the provision of goods and services on a reimbursable basis.                     |
| [The Stafford Act](https://huggingface.co/datasets/leeroy-jankins/The-Stafford-Act)                                                                                                                                                          | Provides the statutory framework for federal disaster response and emergency assistance.                               |
| [Federal Trust Fund Accounting Guide](https://huggingface.co/datasets/leeroy-jankins/Federal-Trust-Fund-Accounting-Guide)                                                                                                                                  | Provides additional appropriations authority beyond regular annual funding acts.                                       |
| [Title 2 Code of Federal Regulations – Uniform Administrative Requirements, Cost Principles, and Audit](https://huggingface.co/datasets/leeroy-jankins/Title-2-CFR-Uniform-Administrative-Requirements-Cost-Principles-And-Audit)                                                                     | Establishes uniform administrative, cost, and audit requirements for federal financial assistance.                     |
| [Title 31 Code of Federal Regulations – Money and Finance](https://huggingface.co/datasets/leeroy-jankins/Title-31-CFR-Money-and-Finance)                                                                                                                  | Codifies Treasury and federal financial management regulations governing money and finance.                            |
| [US Standard General Ledger Account Definitions](https://huggingface.co/datasets/leeroy-jankins/US-Standard-General-Ledger-Accounts-And-Definitions)                                                                                                                            | Defines standardized account structures used for federal accounting and financial reporting.                           |



## 📦 Dependencies

| Package       | Description                          | Link                                               |
|---------------|--------------------------------------|----------------------------------------------------|
| numpy         | Numerical computing                   | [numpy.org](https://numpy.org/)                    |
| pandas        | Data manipulation                     | [pandas.pydata.org](https://pandas.pydata.org/)    |
| matplotlib    | Plotting                              | [matplotlib.org](https://matplotlib.org/)          |
| seaborn       | Statistical plots                     | [seaborn.pydata.org](https://seaborn.pydata.org/)  |
| scikit-learn  | Machine learning models               | [scikit-learn.org](https://scikit-learn.org/)      |
| xgboost       | Extreme gradient boosting             | [xgboost.readthedocs.io](https://xgboost.readthedocs.io/) |
| statsmodels   | Statistical modeling & ANOVA          | [statsmodels.org](https://www.statsmodels.org/)    |
| openpyxl      | Excel I/O                             | [openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/) |
| fitz (PyMuPDF)| PDF parsing                           | [pymupdf.readthedocs.io](https://pymupdf.readthedocs.io/) |
| loguru        | Logging                               | [github.com/Delgan/loguru](https://github.com/Delgan/loguru) |




> **Disclaimer**: This is for analytical exploration, research, and education purposes.  
> This is **not** an official government product; validate against authoritative sources before use.

## 📝 License

- Pogi is published under the [MIT General Public License v3](https://github.com/is-leeroy-jenkins/Pogi/blob/main/LICENSE).

###### Pogi
![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/git/pogi_project.png)

- A machine-learning pipeline for forecasting and reporting Treasury Account Symbol balances using active data.
- Project federal balances using generative ai
- Analyze funding metrics with classification and regression models

### SF-133 Forecasting Tool

---

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

## 🎯 Quickstart ( Colab )
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/is-leeroy-jenkins/Pogi/blob/main/models.ipynb)

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




##  🎯 Quickstart (Streamlit)

- This section explains how to clone the repository, set up the Python environment, and launch the **Pogi** Streamlit application locally.



## 📥 Clone the Repository

First, clone the Pogi repository from GitHub and navigate into the project directory:

```bash
git clone https://github.com/<your-org-or-username>/pogi.git
cd pogi
```



## 🐍 Create a Python Virtual Environment (Recommended)

Using a virtual environment is strongly recommended to isolate dependencies and avoid version conflicts.

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



## 📦 Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

- This installs only the libraries required to run the Streamlit application (no notebook-only or experimental dependencies).



## ▶️ Run the Streamlit App

- Start the application using Streamlit:

```bash
streamlit run app.py
```

Once launched, Streamlit will display a local URL (typically `http://localhost:8501`) in the terminal. Open this link in your web browser to access the app.



## 📊 Using the Application

After the app starts:

1. Upload a CSV or Excel dataset.
2. Select the target variable and feature columns.
3. Choose:

   * Regression or classification
   * Preprocessing options (imputation, scaling)
   * A machine-learning model
4. Click **Train Model** to view diagnostics and performance metrics.

- All model training and evaluation occur locally in your browser session.



## 🛑 Stopping the App

To stop the Streamlit server, return to the terminal and press:

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

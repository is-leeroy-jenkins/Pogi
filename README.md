###### Pogi
![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/assets/images/github/PogiProjectTemplate.png)

- A pipeline for forecasting and reporting Treasury Account Symbol balances using active data.
- Project federal balances using generative ai
- Analyze funding metrics with a compendium of machine-leaning models

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/is-leeroy-jenkins/Pogi/blob/main/models.ipynb)

---

## ![](https://github.com/is-leeroy-jenkins/Pogi/blob/main/resources/assets/images/github/Appropriation.png) Modeling Budget Execution & Available Resources

### 📊 Regression
- Linear, Ridge, Lasso, ElasticNet
- Decision Tree, Random Forest, Gradient Boosting
- SVR, KNN, MLP Regressor, Bayesian Ridge, Huber Regressor

### ✅ Classification
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

---

## 🚀 How to Run

```bash
git clone https://github.com/your-username/chismis.git
cd chismis
pip install -r requirements.txt
jupyter notebook models.ipynb
```


## 🔬 Data Source

- The SF 133 Report on Budget Execution and Budgetary Resources fulfills the requirement in 31 U.S.C. 1511 - 1514
- That is, the President reviews Federal expenditures at least four times a year.
- SF 133s provide historical reference that can be used to help prepare the President's Budget, program operating plans, and spend-out rate estimates.
- For further information on the SF 133 [here](https://tfx.treasury.gov/taxonomy/term/10991)
- Agencies submit the data that appear on these reports to the Department of the Treasury Bureau of Fiscal Service.
- While OMB publishes these reports, the underlying data is submitted by the agencies.
- File A (Account Balances) published monthly by agencies on [USASpending](https://www.usaspending.gov/federal_account)
- Required by the DATA Act.
- Pulled automatically from data in the [Governmentwide Treasury Account Symbol Adjusted Trial Balance System (GTAS)](https://fiscal.treasury.gov/gtas/)
- Contains Budgetary resources, obligation, and outlay data for all the relevant Treasury Account Symbols (TAS) in a reporting agency.
- It includes both award and non-award spending (grouped together), and crosswalks with the [SF 133 report](https://portal.max.gov/portal/document/SF133/Budget/FACTS%20II%20-%20SF%20133%20Report%20on%20Budget%20Execution%20and%20Budgetary%20Resources.html).


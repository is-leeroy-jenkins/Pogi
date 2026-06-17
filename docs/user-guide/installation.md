# Installation

Pogi runs as a local Streamlit application. The standard setup is a Python virtual environment with dependencies installed from `requirements.txt`.

## 🧭 Purpose

This page provides the local installation and launch workflow for the Pogi analytics workbench. The goal is to create a clean Python environment, install the required analytical and documentation packages, and run the Streamlit app from the project root.

## 🧱 Workflow Position

Installation is the first operational step. Complete it before attempting data loading, MkDocs builds, or Streamlit execution.

## 🐍 Create a Virtual Environment

From the project root, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Upgrade packaging tools:

```powershell
python -m pip install --upgrade pip wheel setuptools
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

## ▶️ Run Pogi

Launch the Streamlit application:

```powershell
streamlit run app.py
```

Streamlit will normally open the application at:

```text
http://localhost:8501
```

## 🧪 Verify the Environment

Run these checks from the activated virtual environment:

```powershell
python -m py_compile .\app.py
python -m compileall .
mkdocs build
```

## ✅ Recommended Sequence

1. Confirm Python 3.10 or newer is installed.
2. Create and activate `.venv`.
3. Install dependencies from `requirements.txt`.
4. Run `streamlit run app.py`.
5. Confirm the application loads in the browser.
6. Run `mkdocs build` after documentation files are created.

## 🧩 Troubleshooting

| Symptom | Likely Cause | Correction |
|---|---|---|
| `streamlit` not recognized | Virtual environment is not active or Streamlit is not installed | Activate `.venv` and rerun `pip install -r requirements.txt`. |
| Import error for Excel files | Missing optional workbook reader | Confirm `openpyxl` is installed. |
| Browser does not open | Streamlit launched but browser did not auto-open | Manually browse to `http://localhost:8501`. |
| PowerShell script paste error | PSReadLine rendering issue | Run `Remove-Module PSReadLine` and paste again. |

## 🔗 Related Pages

- [Data Loading](data-loading.md)
- [Development](../development.md)

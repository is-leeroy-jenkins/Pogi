'''
  ******************************************************************************************
      Assembly:                Name
      Filename:                name.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022
      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="app.py" company="Terry D. Eppler">

	     app.py
	     Copyright ©  2022  Terry Eppler

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

  </copyright>
  <summary>
    app.py
  </summary>
  ******************************************************************************************
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import os
import math
import numpy as np
import matplotlib.ticker as mticker
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import scipy.stats as stats
from scipy.stats.mstats import winsorize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import (
    IsolationForest,
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingRegressor,
    GradientBoostingClassifier,
    ExtraTreesRegressor,
    ExtraTreesClassifier,
)
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression,
    Ridge,
    Lasso,
    ElasticNet,
    BayesianRidge,
    SGDRegressor,
    SGDClassifier,
)
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_curve,
    r2_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import (
    LocalOutlierFactor,
    KNeighborsRegressor,
    KNeighborsClassifier,
)
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, RobustScaler, StandardScaler
from sklearn.svm import LinearSVC, SVC, SVR
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

try:
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
    _HAS_DA = True
except Exception:
    _HAS_DA = False

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
LOGO = r'resources/pogi_logo.png'
BLUE_DIVIDER = "<div style='height:2px;align:left;background:#0078FC;margin:6px 0 10px 0;'></div>"
FAVICON = r'resources/favicon.ico'

# ======================================================================================
# Display & Formatting Utilities
# ======================================================================================
def _humanize_number(x: Any, decimals: int = 2) -> str:
    """
    Purpose:
    --------
    Convert a number to a human-readable string with suffixes K/M/B/T, keeping decimals reasonable.

    Parameters:
    -----------
    x: Any
        Input value.
    decimals: int
        Decimal places for the mantissa.

    Returns:
    --------
    str
        Human-readable string.
    """
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return ""
        v = float(x)
    except Exception:
        return str(x)

    av = abs(v)
    if av < 1_000:
        # Small number: keep a modest decimal policy
        if av < 10:
            return f"{v:,.{min(4, max(0, decimals + 2))}f}"
        return f"{v:,.{decimals}f}"

    suffixes = [
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]
    for base, suf in suffixes:
        if av >= base:
            return f"{v / base:,.{decimals}f}{suf}"
    return f"{v:,.{decimals}f}"

def _apply_plain_ticks(ax: plt.Axes, humanize: bool = True) -> None:
    """
    Purpose:
    --------
    Improve readability of plot ticks safely:
      - add gridlines
      - disable scientific notation ONLY when ScalarFormatter is active
      - optionally humanize large magnitudes

    This avoids AttributeError when axes use non-ScalarFormatter
    (e.g., seaborn heatmaps, categorical plots).
    """
    ax.grid(True, linewidth=0.3, alpha=0.65)

    # Safely disable scientific notation only if ScalarFormatter is in use
    for axis in (ax.xaxis, ax.yaxis):
        formatter = axis.get_major_formatter()
        if isinstance(formatter, mticker.ScalarFormatter):
            formatter.set_scientific(False)
            formatter.set_useOffset(False)

    if humanize:
        def fmt(v: float, _: int) -> str:
            return _humanize_number(v, decimals=2)

        ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt))

def _enhance_spines(ax: plt.Axes, lw: float = 1.4) -> None:
    for spine in ax.spines.values():
        spine.set_linewidth(lw)

def _safe_numeric_series(df: pd.DataFrame, col: str) -> np.ndarray:
    return pd.to_numeric(df[col], errors="coerce").dropna().values.astype(float)

def _cardinality_ratio(s: pd.Series) -> float:
    non_missing = int(s.notna().sum())
    
    if non_missing <= 0:
        return 0.0
    return float(s.nunique(dropna=True) / non_missing)

# ======================================================================================
# Table Rendering
# ======================================================================================
def render_table( df: pd.DataFrame, title=None, caption=None, precision=4,
    dark_mode=True, max_rows=500, humanize_large=True ) -> None:
    """
    
	    Purpose:
	    --------
	    Render a DataFrame as a readable HTML table with sane decimals
	    and optional humanized magnitudes.
	
	    Parameters:
	    -----------
	    df: pd.DataFrame
	        Table to render.
	    title: str | None
	        Optional heading.
	    caption: str | None
	        Optional caption.
	    precision: int
	        Default numeric precision.
	    dark_mode: bool
	        Dark palette if True.
	    max_rows: int
	        Max rows to render.
	    humanize_large: bool
	        If True, large values are shown with suffixes K/M/B/T.
	        
    """
    if title:
        st.markdown(f"#### {title}")
    if df is None or df.empty:
        st.info("No data to display.")
        return

    df_show = df.copy()
    if len(df_show) > max_rows:
        df_show = df_show.head(max_rows)
        
    num_cols = df_show.select_dtypes( include=[ np.number ] ).columns.tolist( )

    def _fmt_cell(v: Any) -> str:
        if humanize_large:
            return _humanize_number(v, decimals=min(2, max(0, precision - 2)))
        # fallback: fixed precision
        try:
            if v is None or (isinstance(v, float) and np.isnan(v)):
                return ""
            return f"{float(v):,.{precision}f}"
        except Exception:
            return str(v)

    for c in num_cols:
        df_show[c] = df_show[c].map(_fmt_cell)

    if dark_mode:
        text = "#F9FAFB"
        header_bg = "#1F2937"
        row_even = "#0B1220"
        row_odd = "#111827"
        border = "#374151"
    else:
        text = "#111111"
        header_bg = "#F3F5F7"
        row_even = "#FCFCFD"
        row_odd = "#FFFFFF"
        border = "#D0D0D0"

    styler = (
        df_show.style
        .set_table_styles([
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]},
            {"selector": "th", "props": [
                ("background-color", header_bg),
                ("color", text),
                ("border", f"1px solid {border}"),
                ("padding", "6px"),
                ("font-weight", "600"),
                ("text-align", "left"),
                ("white-space", "nowrap"),
            ]},
            {"selector": "td", "props": [
                ("color", text),
                ("border", f"1px solid {border}"),
                ("padding", "6px"),
                ("white-space", "nowrap"),
            ]},
            {"selector": "tr:nth-child(even) td", "props": [("background-color", row_even)]},
            {"selector": "tr:nth-child(odd) td", "props": [("background-color", row_odd)]},
        ])
    )

    st.markdown(styler.to_html(), unsafe_allow_html=True)

    if caption:
        st.caption(caption)


# ======================================================================================
# Analytical Helpers
# ======================================================================================
def feature_quality( df: pd.DataFrame ) -> pd.DataFrame:
    """
	    
	    Purpose:
	    --------
	    Compute feature quality metrics: completeness, uniqueness, cardinality ratio, variance/entropy.
	
	    Returns:
	    --------
	    pd.DataFrame
	        Feature quality table.
        
    """
    n = df.shape[0]
    rows: List[Dict[str, Any]] = []

    for c in df.columns:
        s = df[c]
        non_missing = int(s.notna().sum())
        completeness = float((non_missing / n) * 100.0) if n else 0.0
        uniq = int(s.nunique(dropna=True))
        card_ratio = float(uniq / non_missing) if non_missing else 0.0

        variance = np.nan
        entropy = np.nan

        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce").dropna().values.astype(float)
            variance = float(np.var(v)) if v.size else np.nan
        else:
            vc = s.dropna().astype(str).value_counts(normalize=True)
            entropy = float(stats.entropy(vc.values)) if vc.size > 1 else 0.0

        rows.append({
            "feature": c,
            "dtype": str(s.dtype),
            "completeness_pct": completeness,
            "unique_values": uniq,
            "cardinality_ratio": card_ratio,
            "variance": variance,
            "entropy": entropy,
        })

    out = pd.DataFrame(rows)
    return out.sort_values(["completeness_pct", "cardinality_ratio"], ascending=[False, False])

def descriptive_profile( df: pd.DataFrame, cols: List[str] ) -> pd.DataFrame:
    """
	    
	    Purpose:
	    --------
	    Rich descriptive profile: percentiles, robust stats, outlier rates, normality p-values.
	
	    Returns:
	    --------
	    pd.DataFrame
	        Profile table.
	        
    """
    rows: List[Dict[str, Any]] = []
    n = df.shape[0]
    percentiles = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]

    for c in cols:
        v = _safe_numeric_series(df, c)
        non_missing = int(np.isfinite(v).sum())
        missing = int(n - non_missing)

        if non_missing <= 0:
            continue

        q_vals = np.nanpercentile(v, percentiles)
        q = dict(zip(percentiles, q_vals))
        mean = float(np.nanmean(v))
        std = float(np.nanstd(v, ddof=0))
        mad = float(stats.median_abs_deviation(v, nan_policy="omit"))
        iqr = float(q[75] - q[25])

        # trimmed mean (10%)
        tmean = float(stats.trim_mean(v, 0.10)) if v.size >= 10 else float(np.nanmean(v))

        # outlier rates
        lo = q[25] - 1.5 * iqr
        hi = q[75] + 1.5 * iqr
        out_iqr = float(((v < lo) | (v > hi)).mean() * 100.0)

        z = (v - mean) / (std + 1e-12)
        out_z3 = float((np.abs(z) > 3.0).mean() * 100.0)

        skew = float(stats.skew(v)) if v.size >= 3 else 0.0
        kurt = float(stats.kurtosis(v)) if v.size >= 4 else 0.0

        # normality tests (best-effort)
        shapiro_p = np.nan
        dagostino_p = np.nan
        anderson_stat = np.nan
        try:
            if 8 <= v.size <= 5000:
                shapiro_p = float(stats.shapiro(v)[1])
            if v.size >= 20:
                dagostino_p = float(stats.normaltest(v[:5000] if v.size > 5000 else v)[1])
            if v.size >= 8:
                anderson_stat = float(stats.anderson(v, dist="norm").statistic)
        except Exception:
            pass

        rows.append({
            "feature": c,
            "count": int(v.size),
            "missing_pct": float((missing / n) * 100.0) if n else 0.0,
            "mean": mean,
            "trimmed_mean_10pct": tmean,
            "median": float(q[50]),
            "std": std,
            "mad": mad,
            "min": float(q[0]),
            "q1": float(q[25]),
            "q3": float(q[75]),
            "max": float(q[100]),
            "iqr": iqr,
            "skew": skew,
            "kurtosis": kurt,
            "outlier_iqr_pct": out_iqr,
            "outlier_z3_pct": out_z3,
            "shapiro_p": shapiro_p,
            "dagostino_p": dagostino_p,
            "anderson_stat": anderson_stat,
        })

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["missing_pct", "outlier_iqr_pct"], ascending=[True, False])

def corr_with_pvalues( df: pd.DataFrame, cols: List[str],  method: str ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Purpose:
    --------
    Compute correlation matrix and p-values for Pearson / Spearman / Kendall.

    Returns:
    --------
    (corr, pvals)
    """
    corr = pd.DataFrame(index=cols, columns=cols, dtype=float)
    pval = pd.DataFrame(index=cols, columns=cols, dtype=float)

    for i, a in enumerate(cols):
        for j, b in enumerate(cols):
            if j < i:
                corr.loc[a, b] = corr.loc[b, a]
                pval.loc[a, b] = pval.loc[b, a]
                continue

            x = pd.to_numeric(df[a], errors="coerce")
            y = pd.to_numeric(df[b], errors="coerce")
            m = x.notna() & y.notna()
            if int(m.sum()) < 3:
                r, p = np.nan, np.nan
            else:
                if method == "pearson":
                    r, p = stats.pearsonr(x[m].values, y[m].values)
                elif method == "kendall":
                    r, p = stats.kendalltau(x[m].values, y[m].values)
                else:
                    r, p = stats.spearmanr(x[m].values, y[m].values)

            corr.loc[a, b] = float(r)
            pval.loc[a, b] = float(p)

    return corr, pval

def vif_table(X: pd.DataFrame) -> pd.DataFrame:
    """
	    
	    Purpose:
	    --------
	    Compute Variance Inflation Factor without statsmodels dependency.
	
	    Parameters:
	    -----------
	    X: pd.DataFrame
	        Numeric design matrix.
	
	    Returns:
	    --------
	    pd.DataFrame
	        VIF per feature.
        
    """
    Xv = X.values.astype(float)
    n, p = Xv.shape
    rows: List[Dict[str, Any]] = []
    eps = 1e-12

    for j in range(p):
        y = Xv[:, j]
        X_other = np.delete(Xv, j, axis=1)

        if X_other.shape[1] == 0:
            rows.append({"feature": X.columns[j], "vif": np.nan, "r2": np.nan})
            continue

        # add intercept
        Xo = np.column_stack([np.ones(X_other.shape[0]), X_other])
        try:
            beta, _, _, _ = np.linalg.lstsq(Xo, y, rcond=None)
            yhat = Xo @ beta
            ss_res = float(np.sum((y - yhat) ** 2))
            ss_tot = float(np.sum((y - np.mean(y)) ** 2)) + eps
            r2 = 1.0 - ss_res / ss_tot
            vif = 1.0 / max(eps, (1.0 - r2))
        except Exception:
            r2 = np.nan
            vif = np.nan

        rows.append({"feature": X.columns[j], "vif": float(vif), "r2": float(r2)})

    out = pd.DataFrame(rows).sort_values("vif", ascending=False)
    return out


# ======================================================================================
# Streamlit Config
# ======================================================================================
st.logo( LOGO, size='large' )
st.set_page_config(page_title="Pogi", layout="wide", page_icon=FAVICON )
st.markdown("#### 🏛️ Analytics Workbench")
st.caption("Exploratory Analysis")

# ======================================================================================
# Sidebar: Data Input + Global Controls
# ======================================================================================

st.sidebar.header("📁 Data Input")

use_fallback = st.sidebar.checkbox(
    "Use fallback data",
    value=True,
    help="Loads data/excel/Account Balances.xlsx when enabled.",
    key="use_fallback",
)

uploaded = None
if not use_fallback:
    uploaded = st.sidebar.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"],
        key="upload",
    )

def load_data() -> pd.DataFrame:
    if use_fallback:
        fallback_path = os.path.join("data", "excel", "Account Balances.xlsx")
        if not os.path.exists(fallback_path):
            st.error(f"Fallback file not found: {fallback_path}")
            st.stop()
        try:
            return pd.read_excel(fallback_path)
        except Exception as e:
            st.error(f"Failed to read fallback file: {e}")
            st.stop()

    if not uploaded:
        st.info("Upload a CSV or Excel file to begin, or enable fallback loading.")
        st.stop()

    try:
        return pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        st.stop()

df = load_data( )
float_cols = df.select_dtypes(include=[np.floating]).columns.tolist( )
int_cols = df.select_dtypes(include=[np.integer]).columns.tolist()
bool_cols = df.select_dtypes(include=[bool]).columns.tolist()

st.sidebar.subheader("⚙️ Global Controls")

preview_rows = st.sidebar.slider("Preview rows", 10, 500, 50, 10, key="preview_rows")
dark_tables = st.sidebar.toggle("Use dark tables", value=True, key="dark_tables")
plot_theme = st.sidebar.selectbox("Plot theme", ["Light", "Dark"], index=1, key="plot_theme")
humanize_tables = st.sidebar.toggle(
    "Humanize Large Numbers",
    value=True,
    help="Shows large magnitudes as K/M/B/T to keep tables usable.",
    key="humanize_tables",
)
include_int_as_numeric = st.sidebar.toggle(
    "Include integer-coded columns in numeric analyses",
    value=False,
    help="Off by default.",
    key="include_int_as_numeric",
)

# Use float-only numeric by default
numeric_cols = list(float_cols) + (list(int_cols) if include_int_as_numeric else [])
non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

# Plot theme
plt.style.use("dark_background" if plot_theme == "Dark" else "default")

# ======================================================================================
# Tabs
# ======================================================================================
tabs = st.tabs([
    "1) Data Overview",
    "2) Descriptive Statistics",
    "3) Inferential Statistics",
    "4) Feature Analysis",
    "5) Feature Engineering",
    "6) Anomaly Detection",
    "7) Modeling",
    "8) Diagnostics",
])


# ======================================================================================
# 1) Data Overview (More visuals)
# ======================================================================================
with tabs[0]:
    st.markdown("##### 1) Data Overview")

    c1, c2, c3, c4 = st.columns( 4, border=True )
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", f"{df.shape[1]:,}")
    c3.metric("Numeric Columns", f"{len(numeric_cols):,}")
    c4.metric("Categorical Columns", f"{len(non_numeric_cols):,}")

    st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    st.markdown("##### Data Preview")
    st.dataframe(df.head(int(preview_rows)), use_container_width=True, height=420)

    st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    st.markdown("##### Feature Quality")
    fq = feature_quality(df)
    render_table(
        fq,
        caption=(
            "Completeness is the percent of non-missing values. Cardinality ratio near 1.0 suggests ID-like fields. "
            "Variance/entropy are coarse indicators of informational content."
        ),
        dark_mode=dark_tables,
        precision=4,
        max_rows=500,
        humanize_large=humanize_tables,
    )

    st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    st.markdown("##### Missingness Profile")
    miss = pd.DataFrame({
        "feature": df.columns,
        "missing": [int(df[c].isna().sum()) for c in df.columns],
        "missing_pct": [float(df[c].isna().mean() * 100.0) for c in df.columns],
    }).sort_values("missing_pct", ascending=False)

    colA, colB = st.columns([1, 1], border=True )

    with colA:
        render_table(
            miss,
            dark_mode=dark_tables,
            precision=2,
            max_rows=200,
            humanize_large=humanize_tables,
        )

    with colB:
        top = miss.head(25).iloc[::-1]
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.barh(top["feature"].astype(str), top["missing_pct"].values)
        ax.set_title("Top Missingness (%)")
        ax.set_xlabel("Missing %")
        _apply_plain_ticks(ax, humanize=False)
        st.pyplot(fig)

    st.caption(
        "Use this page to validate inferred types, quickly identify missingness, and ID-like fields before analysis."
    )

# ======================================================================================
# 2) Descriptive Statistics (Substantially expanded models + more visuals)
# ======================================================================================
with tabs[1]:
    st.markdown("##### 2) Descriptive Statistics")

    if not numeric_cols:
        st.warning("No numeric columns detected under the current numeric policy.")
    else:
        st.text("Numeric Profile")
        prof = descriptive_profile(df, numeric_cols)
        render_table(
            prof,
            dark_mode=dark_tables,
            precision=4,
            max_rows=500,
            humanize_large=humanize_tables,
            caption=(
                "Outlier Rates (IQR and |z|>3), and Normality Diagnostics. "
                "Use Shapiro/D’Agostino p-values as indicators, not absolutes."
            ),
        )

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        # Exclude ID-like columns for distribution plotting by default
        cont_cols: List[str] = []
        for c in numeric_cols:
            ratio = _cardinality_ratio(df[c])
            # keep columns that are not near-unique
            if ratio < 0.50:
                cont_cols.append(c)

        st.markdown("##### Distribution Diagnostics")
        chosen = st.multiselect(
            "Select numeric features to visualize",
            options=cont_cols if cont_cols else numeric_cols,
            default=(cont_cols if cont_cols else numeric_cols)[: min(6, len(cont_cols if cont_cols else numeric_cols))],
            key="desc_chosen",
        )
        bins = st.slider("Histogram Bins", 10, 120, 40, 5, key="desc_bins")

        if chosen:
            per_row = 2
            for i in range(0, len(chosen), per_row):
                row = chosen[i:i + per_row]
                cols_ui = st.columns(per_row)

                for j, c in enumerate(row):
                    v = _safe_numeric_series(df, c)
                    if v.size < 2:
                        continue

                    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
                    ax1, ax2, ax3, ax4 = axes.ravel()
                    sns.histplot(v, bins=bins, kde=True, ax=ax1, edgecolor="black", linewidth=0.4)
                    ax1.set_title(f"{c}: Histogram + KDE")
                    _apply_plain_ticks(ax1)
                    sns.boxplot(x=v, ax=ax2)
                    ax2.set_title("Boxplot")
                    _apply_plain_ticks(ax2)
                    sns.violinplot(x=v, ax=ax3, inner="quartile")
                    ax3.set_title("Violin (density + quartiles)")
                    _apply_plain_ticks(ax3)

                    try:
                        sns.ecdfplot(v, ax=ax4)
                        ax4.set_title("ECDF")
                        _apply_plain_ticks(ax4)
                    except Exception:
                        ax4.text(0.5, 0.5, "ECDF unavailable", ha="center", va="center")
                        _enhance_spines(ax4)

                    fig.tight_layout()
                    cols_ui[j].pyplot(fig)
    
            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            # Enhanced Q–Q plots (boundaries improved)
            st.markdown("##### Q–Q Plots")
            qq_cols = st.multiselect(
                "Select features for Q–Q plots",
                options=chosen,
                default=chosen[: min(3, len(chosen))],
                key="desc_qq_cols",
            )

            for c in qq_cols:
                v = _safe_numeric_series(df, c)
                if v.size < 20:
                    continue

                fig, ax = plt.subplots(figsize=(6, 4))
                stats.probplot(v, dist="norm", plot=ax)

                # Boundary enhancements
                if ax.lines:
                    ax.lines[0].set_marker("o")
                    ax.lines[0].set_markersize(4)
                    ax.lines[0].set_markeredgewidth(0.9)
                    ax.lines[0].set_markeredgecolor("black")
                    ax.lines[0].set_alpha(0.9)

                    if len(ax.lines) > 1:
                        ax.lines[1].set_linewidth(2.6)
                        ax.lines[1].set_alpha(0.95)

            
                _enhance_spines(ax, lw=1.6)
                ax.set_title(f"Q–Q Plot: {c}")
                _apply_plain_ticks(ax, humanize=False)
                st.pyplot(fig)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
# ======================================================================================
# 3) Inferential Statistics (Substantially expanded)
# ======================================================================================
with tabs[2]:
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for inferential analysis.")
    else:
        st.markdown("##### Correlation Inference")
        corr_cols = st.multiselect(
            "Select numeric features (subset)",
            options=numeric_cols,
            default=numeric_cols[: min(12, len(numeric_cols))],
            key="inf_corr_cols",
        )

        corr_method = st.selectbox(
            "Method",
            ["pearson", "spearman", "kendall"],
            index=0,
            key="inf_corr_method",
        )

        if len(corr_cols) >= 2:
            corr_mat, p_mat = corr_with_pvalues(df, corr_cols, corr_method)
            alpha = st.slider("Significance alpha", 0.001, 0.10, 0.05, 0.001, key="inf_alpha")
            sig_mask = (p_mat.values <= alpha)

            col1, col2 = st.columns( 2, border=True )

            with col1:
                fig, ax = plt.subplots(figsize=(10, 7))
                sns.heatmap(
                    corr_mat,
                    cmap="coolwarm",
                    center=0.0,
                    annot=True,
                    fmt=".2f",
                    linewidths=0.6,
                    linecolor="black",
                    annot_kws={"size": 8},
                    cbar_kws={"shrink": 0.85},
                    ax=ax,
                )
                ax.set_title(f"{corr_method.title()} Correlations")
                st.pyplot(fig)

            with col2:
                fig2, ax2 = plt.subplots(figsize=(10, 7))
                sns.heatmap(
                    p_mat,
                    cmap="viridis_r",
                    annot=True,
                    fmt=".3f",
                    linewidths=0.6,
                    linecolor="black",
                    annot_kws={"size": 8},
                    cbar_kws={"shrink": 0.85},
                    ax=ax2,
                )
                ax2.set_title("Correlation P-values")
                st.pyplot(fig2)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            # Significance mask heatmap
            fig3, ax3 = plt.subplots(figsize=(10, 7))
            sns.heatmap(
                sig_mask.astype(int),
                cmap="Greys",
                annot=True,
                fmt="d",
                linewidths=0.6,
                linecolor="black",
                cbar=False,
                ax=ax3,
            )
            ax3.set_title(f"Significant pairs (p <= {alpha:.3f})")
            st.pyplot(fig3)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            render_table(
                corr_mat.reset_index().rename(columns={"index": "feature"}),
                title="Correlation Matrix",
                dark_mode=dark_tables,
                precision=4,
                max_rows=200,
                humanize_large=False,
            )
            
            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            render_table(
                p_mat.reset_index().rename(columns={"index": "feature"}),
                title="P-Value Matrix",
                dark_mode=dark_tables,
                precision=6,
                max_rows=200,
                humanize_large=False,
            )

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        st.markdown("##### Normality Testing")
        ntest_cols = st.multiselect(
            "Select Numeric Features",
            options=numeric_cols,
            default=numeric_cols[: min(10, len(numeric_cols))],
            key="inf_norm_cols",
        )
        rows: List[Dict[str, Any]] = []
        for c in ntest_cols:
            v = _safe_numeric_series(df, c)
            if v.size >= 8:
                sh_p = np.nan
                dag_p = np.nan
                ad_stat = np.nan
                try:
                    if v.size <= 5000:
                        sh_p = float(stats.shapiro(v)[1])
                    if v.size >= 20:
                        dag_p = float(stats.normaltest(v[:5000] if v.size > 5000 else v)[1])
                    ad_stat = float(stats.anderson(v, dist="norm").statistic)
                except Exception:
                    pass
                rows.append({"feature": c, "n": int(v.size), "shapiro_p": sh_p, "dagostino_p": dag_p, "anderson_stat": ad_stat})

        render_table(
            pd.DataFrame(rows),
            caption="Normality tests help choose parametric vs non-parametric tests; p-values are sample-size sensitive.",
            dark_mode=dark_tables,
            precision=6,
            max_rows=200,
            humanize_large=False,
        )

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        st.markdown("##### Two-Group Comparisons")
        if non_numeric_cols:
            num = st.selectbox("Numeric Feature", options=numeric_cols, key="inf_2g_num")
            grp = st.selectbox("Grouping Feature (Categorical)", options=non_numeric_cols, key="inf_2g_grp")
            groups = sorted(df[grp].dropna().astype(str).unique().tolist())

            if len(groups) >= 2:
                gsel = st.multiselect(
                    "Select Two Groups",
                    options=groups,
                    default=groups[:2],
                    key="inf_2g_groups",
                )

                if len(gsel) == 2:
                    a = pd.to_numeric(df.loc[df[grp].astype(str) == gsel[0], num], errors="coerce").dropna().values
                    b = pd.to_numeric(df.loc[df[grp].astype(str) == gsel[1], num], errors="coerce").dropna().values
                    if a.size >= 2 and b.size >= 2:
                        t_stat_eq, p_eq = stats.ttest_ind(a, b, equal_var=True)
                        t_stat_w, p_w = stats.ttest_ind(a, b, equal_var=False)
                        u_stat, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")
                        pooled = math.sqrt(((a.size - 1) * np.var(a, ddof=1) + (b.size - 1) * np.var(b, ddof=1)) / max(1, (a.size + b.size - 2)))
                        d = float((np.mean(a) - np.mean(b)) / (pooled + 1e-12))

                        out = pd.DataFrame([{
                            "group_A": gsel[0],
                            "group_B": gsel[1],
                            "n_A": int(a.size),
                            "n_B": int(b.size),
                            "mean_A": float(np.mean(a)),
                            "mean_B": float(np.mean(b)),
                            "median_A": float(np.median(a)),
                            "median_B": float(np.median(b)),
                            "t_equalvar_p": float(p_eq),
                            "t_welch_p": float(p_w),
                            "mannwhitney_p": float(p_u),
                            "cohens_d": d,
                        }])

                        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
                        render_table(
                            out,
                            dark_mode=dark_tables,
                            precision=6,
                            max_rows=10,
                            humanize_large=humanize_tables,
                            caption="Includes both parametric (t-tests) and non-parametric (Mann–Whitney) tests plus Cohen's d effect size.",
                        )


                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.hist(a, bins=30, alpha=0.45, label=gsel[0], edgecolor="black", linewidth=0.3)
                        ax.hist(b, bins=30, alpha=0.45, label=gsel[1], edgecolor="black", linewidth=0.3)
                        ax.set_title(f"{num} by {grp} (two groups)")
                        ax.set_xlabel(num)
                        ax.set_ylabel("Count")
                        ax.legend()
                        _apply_plain_ticks(ax)
                        st.pyplot(fig)

                        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
                        fig2, ax2 = plt.subplots(figsize=(10, 4))
                        sns.kdeplot(a, ax=ax2, label=gsel[0])
                        sns.kdeplot(b, ax=ax2, label=gsel[1])
                        ax2.set_title("KDE comparison (shape differences)")
                        ax2.legend()
                        _apply_plain_ticks(ax2)
                        st.pyplot(fig2)

# ======================================================================================
# 4) Feature Analysis (Substantially expanded)
# ======================================================================================
with tabs[3]:
    if not numeric_cols:
        st.warning("Feature analysis requires numeric columns.")
    else:
        st.markdown("##### Correlation Heatmap")
        fa_cols = st.multiselect(
            "Select numeric features",
            options=numeric_cols,
            default=numeric_cols[: min(15, len(numeric_cols))],
            key="fa_cols",
        )

        if len(fa_cols) >= 2:
            corr = df[fa_cols].corr()

            fig, ax = plt.subplots(figsize=(10, 7))
            sns.heatmap(
                corr,
                cmap="coolwarm",
                center=0.0,
                annot=True,
                fmt=".2f",
                linewidths=0.6,
                linecolor="black",
                annot_kws={"size": 8},
                cbar_kws={"shrink": 0.85},
                ax=ax,
            )
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            # Strongest pairs
            pairs: List[Dict[str, Any]] = []
            for i in range(len(fa_cols)):
                for j in range(i + 1, len(fa_cols)):
                    a, b = fa_cols[i], fa_cols[j]
                    r = float(corr.loc[a, b])
                    pairs.append({"feature_A": a, "feature_B": b, "corr": r, "abs_corr": abs(r)})
            top_pairs = pd.DataFrame(pairs).sort_values("abs_corr", ascending=False).head(25)
            
            render_table(
                top_pairs.drop(columns=["abs_corr"]),
                title="Top correlated feature pairs",
                dark_mode=dark_tables,
                precision=4,
                max_rows=25,
                humanize_large=False,
            )

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        
        st.markdown("##### PCA + Scree + 2D Projection + k-Means")
        pca_cols = st.multiselect(
            "Select features for PCA",
            options=numeric_cols,
            default=numeric_cols[: min(12, len(numeric_cols))],
            key="fa_pca_cols",
        )

        if len(pca_cols) >= 2:
            X = df[pca_cols].apply(pd.to_numeric, errors="coerce")
            X = X.fillna(X.median(numeric_only=True))
            Xs = StandardScaler().fit_transform(X.values)

            n_comp = st.slider("PCA components", 2, min(10, len(pca_cols)), 3, 1, key="fa_pca_comp")
            pca = PCA(n_components=int(n_comp), random_state=42)
            Z = pca.fit_transform(Xs)

            evr = pd.DataFrame({
                "component": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
                "explained_variance_ratio": pca.explained_variance_ratio_,
                "cumulative": np.cumsum(pca.explained_variance_ratio_),
            })
            
            st.divider( )
            
            render_table(
                evr,
                title="Explained Variance",
                dark_mode=dark_tables,
                precision=6,
                max_rows=20,
                humanize_large=False,
                caption="Use cumulative variance to decide whether a reduced-dimensional representation is viable.",
            )

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(np.arange(1, evr.shape[0] + 1), evr["cumulative"].values, marker="o")
            ax.set_title("PCA Cumulative Explained Variance")
            ax.set_xlabel("Components")
            ax.set_ylabel("Cumulative variance")
            _apply_plain_ticks(ax, humanize=False)
            st.pyplot(fig)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            if Z.shape[1] >= 2:
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                ax2.scatter(Z[:, 0], Z[:, 1], s=18, edgecolor="black", linewidth=0.3)
                ax2.set_title("PCA Projection (PC1 vs PC2)")
                ax2.set_xlabel("PC1")
                ax2.set_ylabel("PC2")
                _apply_plain_ticks(ax2, humanize=False)
                st.pyplot(fig2)

                st.divider( )
                
                k = st.slider("k-Means Clusters (PCA space)", 2, 12, 3, 1, key="fa_k")
                km = KMeans(n_clusters=int(k), n_init="auto", random_state=42)
                labels = km.fit_predict(Z)
                fig3, ax3 = plt.subplots(figsize=(8, 6))
                ax3.scatter(Z[:, 0], Z[:, 1], c=labels, s=18, edgecolor="black", linewidth=0.3)
                ax3.set_title("k-Means Clusters (PCA space)")
                ax3.set_xlabel("PC1")
                ax3.set_ylabel("PC2")
                _apply_plain_ticks(ax3, humanize=False)
                st.pyplot(fig3)

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        
        st.markdown("##### Multicollinearity (VIF)")
        if len(fa_cols) >= 2:
            Xv = df[fa_cols].apply(pd.to_numeric, errors="coerce").fillna(df[fa_cols].median(numeric_only=True))
            vt = vif_table(Xv)
            render_table(
                vt,
                dark_mode=dark_tables,
                precision=4,
                max_rows=50,
                humanize_large=False,
                caption="Consider dropping/recombining features or using PCA.",
            )

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        
        st.markdown("##### Pairwise Scatter")
        if len(fa_cols) >= 2:
            scatter_cols = fa_cols[: min(5, len(fa_cols))]
            for i in range(len(scatter_cols)):
                for j in range(i + 1, len(scatter_cols)):
                    a, b = scatter_cols[i], scatter_cols[j]
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.scatter(
                        pd.to_numeric(df[a], errors="coerce"),
                        pd.to_numeric(df[b], errors="coerce"),
                        s=12,
                        edgecolor="black",
                        linewidth=0.3,
                        alpha=0.75,
                    )
                    
                    st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
                    
                    ax.set_title(f"{a} vs {b}")
                    ax.set_xlabel(a)
                    ax.set_ylabel(b)
                    _apply_plain_ticks(ax)
                    st.pyplot(fig)
        

# ======================================================================================
# 5) Feature Engineering (non-temporal, not empty, more visuals)
# ======================================================================================
with tabs[4]:
    left, right = st.columns(2, border=True )
    with left:
        num_feats = st.multiselect(
            "Numeric Features",
            options=numeric_cols,
            default=numeric_cols[: min(10, len(numeric_cols))],
            key="fe_num_feats",
        )
        scaler_name = st.selectbox(
            "Scaler",
            ["None", "StandardScaler", "MinMaxScaler", "RobustScaler"],
            index=1,
            key="fe_scaler",
        )
        winsor = st.toggle("Winsorize (clip extreme tails)", value=False, key="fe_winsor")
        win_limits = st.slider("Winsorize limits", 0.0, 0.20, (0.01, 0.01), 0.005, key="fe_win_lim")

    with right:
        cat_feats = st.multiselect(
            "Categorical Features (One-Hot)",
            options=non_numeric_cols,
            default=non_numeric_cols[: min(6, len(non_numeric_cols))],
            key="fe_cat_feats",
        )
        impute_strategy = st.selectbox(
            "Numeric Imputation",
            ["median", "mean", "most_frequent"],
            index=0,
            key="fe_impute",
        )
        knn_impute = st.toggle("KNN impute (numeric)", value=False, key="fe_knn")
        knn_k = st.slider("KNN neighbors", 2, 15, 5, 1, key="fe_knn_k")

    st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
    if st.button("Build Feature Matrix", type="primary", key="fe_build"):
        X_num = df[num_feats].apply(pd.to_numeric, errors="coerce") if num_feats else pd.DataFrame(index=df.index)

        if winsor and not X_num.empty:
            Xw = X_num.copy()
            for c in Xw.columns:
                v = Xw[c].values.astype(float)
                if np.isfinite(v).sum() > 0:
                    Xw[c] = winsorize(v, limits=win_limits)
            X_num = Xw

        if not X_num.empty:
            if knn_impute:
                imp = KNNImputer(n_neighbors=int(knn_k))
                X_num = pd.DataFrame(imp.fit_transform(X_num), columns=X_num.columns, index=X_num.index)
            else:
                imp = SimpleImputer(strategy=impute_strategy)
                X_num = pd.DataFrame(imp.fit_transform(X_num), columns=X_num.columns, index=X_num.index)

            if scaler_name != "None":
                if scaler_name == "StandardScaler":
                    scaler = StandardScaler()
                elif scaler_name == "MinMaxScaler":
                    scaler = MinMaxScaler()
                else:
                    scaler = RobustScaler()

                X_num = pd.DataFrame(scaler.fit_transform(X_num), columns=X_num.columns, index=X_num.index)

        X_cat = pd.get_dummies(df[cat_feats].astype(str), drop_first=False) if cat_feats else pd.DataFrame(index=df.index)

        X_fe = pd.concat([X_num, X_cat], axis=1)
        st.session_state["feature_matrix"] = X_fe

        st.success(f"Feature matrix built: {X_fe.shape[0]:,} rows × {X_fe.shape[1]:,} columns")

        # Preview table
        render_table(
            X_fe.head(50),
            title="Feature Matrix Preview",
            dark_mode=dark_tables,
            precision=4,
            max_rows=50,
            humanize_large=humanize_tables,
        )

        # Visual: correlation heatmap of numeric engineered features (subset)
        num_engineered = X_num.columns.tolist()
        if len(num_engineered) >= 2:
            st.markdown("### Engineered Numeric Correlation")
            sub = num_engineered[: min(20, len(num_engineered))]
            corr = pd.DataFrame(X_num[sub]).corr()
            fig, ax = plt.subplots(figsize=(10, 7))
            sns.heatmap(
                corr,
                cmap="coolwarm",
                center=0.0,
                annot=True,
                fmt=".2f",
                linewidths=0.6,
                linecolor="black",
                annot_kws={"size": 8},
                cbar_kws={"shrink": 0.85},
                ax=ax,
            )
            ax.set_title("Engineered Numeric Correlation Heatmap")
            st.pyplot(fig)

# ======================================================================================
# 6) Anomaly Detection (not empty, more visuals)
# ======================================================================================
with tabs[5]:
    st.caption(
        "Flags potential anomalies using multiple detectors: non-mutating"
    )

    if len(numeric_cols) < 2:
        st.warning("Anomaly detection requires at least 2 numeric columns under the current numeric policy.")
    else:
        cols = st.multiselect(
            "Numeric Features for Anomaly Detection",
            options=numeric_cols,
            default=numeric_cols[: min(12, len(numeric_cols))],
            key="ad_cols",
        )

        if len(cols) >= 2:
            X = df[cols].apply(pd.to_numeric, errors="coerce")
            X = X.fillna(X.median(numeric_only=True))

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            st.markdown("##### Detector Controls")
            c1, c2, c3 = st.columns(3, border=True )

            with c1:
                iso_n = st.slider("IsolationForest estimators", 50, 500, 200, 25, key="ad_iso_n")
                iso_cont = st.slider("IsolationForest contamination", 0.001, 0.20, 0.02, 0.001, key="ad_iso_c")

            with c2:
                lof_k = st.slider("LOF neighbors", 5, 100, 20, 1, key="ad_lof_k")
                lof_cont = st.slider("LOF contamination", 0.001, 0.20, 0.02, 0.001, key="ad_lof_c")

            with c3:
                pca_comp = st.slider("PCA components (viz)", 2, min(6, X.shape[1]), 2, 1, key="ad_pca_comp")

            if st.button("Run Detectors", type="primary", key="ad_run"):
                flags = pd.DataFrame(index=df.index)

                iso = IsolationForest(
                    n_estimators=int(iso_n),
                    contamination=float(iso_cont),
                    random_state=42,
                )
                iso_pred = iso.fit_predict(X.values)
                flags["isolationforest_anomaly"] = (iso_pred == -1).astype(int)

                lof = LocalOutlierFactor(
                    n_neighbors=int(lof_k),
                    contamination=float(lof_cont),
                )
                lof_pred = lof.fit_predict(X.values)
                flags["lof_anomaly"] = (lof_pred == -1).astype(int)

                # PCA distance anomaly proxy
                Xs = StandardScaler().fit_transform(X.values)
                pca = PCA(n_components=int(pca_comp), random_state=42)
                Z = pca.fit_transform(Xs)
                dist = np.linalg.norm(Z - np.mean(Z, axis=0), axis=1)
                thr = np.quantile(dist, 0.98)
                flags["pca_far"] = (dist >= thr).astype(int)
                flags["pca_distance"] = dist

                flags["anomaly_votes"] = (
                    flags["isolationforest_anomaly"] + flags["lof_anomaly"] + flags["pca_far"]
                )
                flags["is_anomaly"] = (flags["anomaly_votes"] >= 2).astype(int)

                st.session_state["anomaly_flags"] = flags
                st.success(
                    f"Flagged anomalies: {int(flags['is_anomaly'].sum()):,} "
                    f"({float(flags['is_anomaly'].mean() * 100.0):.2f}%)"
                )

                st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
                
                # Visual: votes distribution
                fig, ax = plt.subplots(figsize=(8, 4))
                vc = flags["anomaly_votes"].value_counts().sort_index()
                ax.bar(vc.index.astype(int), vc.values.astype(int), edgecolor="black", linewidth=0.4)
                ax.set_title("Anomaly vote counts")
                ax.set_xlabel("Votes (0–3)")
                ax.set_ylabel("Rows")
                _apply_plain_ticks(ax, humanize=False)
                st.pyplot(fig)

                st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
                # Visual: PCA scatter (colored by anomaly)
                if Z.shape[1] >= 2:
                    fig2, ax2 = plt.subplots(figsize=(8, 6))
                    ax2.scatter(Z[:, 0], Z[:, 1], c=flags["is_anomaly"].values, s=16, edgecolor="black", linewidth=0.3)
                    ax2.set_title("PCA space (colored by anomaly flag)")
                    ax2.set_xlabel("PC1")
                    ax2.set_ylabel("PC2")
                    _apply_plain_ticks(ax2, humanize=False)
                    st.pyplot(fig2)

                st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
                render_table(
                    flags.sort_values(["is_anomaly", "anomaly_votes"], ascending=[False, False]).head(250),
                    title="Anomaly Flags",
                    dark_mode=dark_tables,
                    precision=4,
                    max_rows=250,
                    humanize_large=humanize_tables,
                    caption="Rows flagged by multiple detectors are higher-confidence candidates for review.",
                )

# ======================================================================================
# 7) Modeling (>=10 regression + >=10 classification)
# ======================================================================================
with tabs[6]:
    X_fe: Optional[pd.DataFrame] = st.session_state.get("feature_matrix")
    if X_fe is None:
        st.info("No engineered feature matrix found. Using raw numeric features (per current numeric policy).")
        if not numeric_cols:
            st.stop()
        X_fe = df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(df[numeric_cols].median(numeric_only=True))

    target = st.selectbox("Target column", options=df.columns.tolist(), key="model_target")
    task = st.radio("Task type", ["Regression", "Classification"], horizontal=True, key="model_task")
    test_size = st.slider("Test size", 0.10, 0.50, 0.25, 0.05, key="model_test")
    seed = st.number_input("Random seed", 0, 10_000, 42, 1, key="model_seed")
    y_raw = df[target]

    if task == "Regression":
        y = pd.to_numeric(y_raw, errors="coerce")
        m = y.notna()
        X = X_fe.loc[m].copy()
        yv = y.loc[m].values.astype(float)

        models: Dict[str, Any] = {
            "LinearRegression": LinearRegression(),
            "Ridge": Ridge(),
            "Lasso": Lasso(),
            "ElasticNet": ElasticNet(),
            "BayesianRidge": BayesianRidge(),
            "SGDRegressor": SGDRegressor(random_state=42),
            "DecisionTreeRegressor": DecisionTreeRegressor(random_state=42),
            "RandomForestRegressor": RandomForestRegressor(random_state=42),
            "GradientBoostingRegressor": GradientBoostingRegressor(random_state=42),
            "ExtraTreesRegressor": ExtraTreesRegressor(random_state=42),
            "KNeighborsRegressor": KNeighborsRegressor(),
            "SVR": SVR(),
        }

    else:
        # Classification: label-encode non-numeric, else cast to int categories
        if pd.api.types.is_numeric_dtype(y_raw):
            # If numeric, treat as categories only if low-ish cardinality; else median split
            y_num = pd.to_numeric(y_raw, errors="coerce")
            u = y_num.dropna().nunique()
            if u <= 20:
                yv = y_num.fillna(y_num.median()).astype(int).values
            else:
                yv = (y_num.fillna(y_num.median()) > y_num.median()).astype(int).values
        else:
            le = LabelEncoder()
            yv = le.fit_transform(y_raw.astype(str).fillna("(missing)"))

        X = X_fe.copy()

        models = {
            "LogisticRegression": LogisticRegression(max_iter=4000, random_state=42),
            "LinearSVC": LinearSVC(random_state=42),
            "SVC_RBF": SVC(kernel="rbf", probability=False, random_state=42),
            "SGDClassifier": SGDClassifier(random_state=42),
            "DecisionTreeClassifier": DecisionTreeClassifier(random_state=42),
            "RandomForestClassifier": RandomForestClassifier(random_state=42),
            "GradientBoostingClassifier": GradientBoostingClassifier(random_state=42),
            "ExtraTreesClassifier": ExtraTreesClassifier(random_state=42),
            "KNeighborsClassifier": KNeighborsClassifier(),
            "GaussianNB": GaussianNB(),
        }
        if _HAS_DA:
            models["LinearDiscriminantAnalysis"] = LinearDiscriminantAnalysis()
            models["QuadraticDiscriminantAnalysis"] = QuadraticDiscriminantAnalysis()

    chosen_models = st.multiselect(
        "Models to train",
        options=list(models.keys()),
        default=list(models.keys())[: min(6, len(models))],
        key="model_choices",
    )

    if st.button("Train Models", type="primary", key="model_train"):
        # train/test split
        strat = yv if task == "Classification" and len(np.unique(yv)) > 1 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X.values,
            yv,
            test_size=float(test_size),
            random_state=int(seed),
            stratify=strat,
        )

        rows: List[Dict[str, Any]] = []
        fitted: Dict[str, Any] = {}

        for name in chosen_models:
            m = models[name]
            try:
                m.fit(X_train, y_train)
                preds = m.predict(X_test)

                if task == "Regression":
                    rmse = float(mean_squared_error(y_test, preds ))
                    mae = float(mean_absolute_error(y_test, preds))
                    r2 = float(r2_score(y_test, preds))
                    rows.append({"model": name, "rmse": rmse, "mae": mae, "r2": r2})
                else:
                    acc = float(accuracy_score(y_test, preds))
                    rows.append({"model": name, "accuracy": acc})

                fitted[name] = {"model": m, "preds": preds}

            except Exception as e:
                rows.append({"model": name, "error": str(e)})

        res = pd.DataFrame(rows)
        if task == "Regression" and "rmse" in res.columns:
            res_sorted = res.sort_values("rmse", ascending=True)
        elif task == "Classification" and "accuracy" in res.columns:
            res_sorted = res.sort_values("accuracy", ascending=False)
        else:
            res_sorted = res

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
        
        render_table(
            res_sorted,
            title="Model Comparison",
            dark_mode=dark_tables,
            precision=4,
            max_rows=200,
            humanize_large=humanize_tables,
        )


        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
        # choose best model
        best_name: Optional[str] = None
        if task == "Regression" and "rmse" in res_sorted.columns and len(res_sorted) > 0:
            best_name = str(res_sorted.iloc[0]["model"])
        if task == "Classification" and "accuracy" in res_sorted.columns and len(res_sorted) > 0:
            best_name = str(res_sorted.iloc[0]["model"])

        if best_name and best_name in fitted:
            st.session_state["last_model_payload"] = {
                "task": task,
                "best_name": best_name,
                "best_model": fitted[best_name]["model"],
                "X_test": X_test,
                "y_test": y_test,
                "preds": fitted[best_name]["preds"],
                "feature_names": list(X.columns),
                "X_train": X_train,
                "y_train": y_train,
            }
            st.success(f"Diagnostics payload saved for best model: {best_name}")

# ======================================================================================
# 8) Diagnostics (more visuals + reasonable formatting)
# ======================================================================================
with tabs[7]:
    payload = st.session_state.get("last_model_payload")
    if not payload:
        st.info("Train models in the Modeling tab to enable diagnostics.")
    else:
        task = payload["task"]
        model = payload["best_model"]
        preds = payload["preds"]
        y_test = payload["y_test"]
        X_test = payload["X_test"]
        best_name = payload["best_name"]
        feature_names = payload.get("feature_names", [])
        X_train = payload.get("X_train")
        y_train = payload.get("y_train")

        st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
        st.markdown(f"##### Best Model: `{best_name}`")

        if task == "Regression":
            resid = y_test - preds

            col1, col2 = st.columns( 2, border=True )

            with col1:
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.scatter(preds, resid, s=12, edgecolor="black", linewidth=0.3, alpha=0.75)
                ax.axhline(0, color="white" if plot_theme == "Dark" else "black", linewidth=1.2)
                ax.set_xlabel("Predicted")
                ax.set_ylabel("Residual")
                ax.set_title("Residuals vs Predicted")
                _apply_plain_ticks(ax)
                _enhance_spines(ax)
                st.pyplot(fig)

            with col2:
                fig2, ax2 = plt.subplots(figsize=(7, 4))
                ax2.hist(resid, bins=40, edgecolor="black", linewidth=0.4)
                ax2.set_title("Residual Distribution")
                ax2.set_xlabel("Residual")
                ax2.set_ylabel("Count")
                _apply_plain_ticks(ax2)
                _enhance_spines(ax2)
                st.pyplot(fig2)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
            # Q–Q plot for residuals (enhanced)
            fig3, ax3 = plt.subplots(figsize=(7, 4))
            stats.probplot(resid, dist="norm", plot=ax3)
            if ax3.lines:
                ax3.lines[0].set_marker("o")
                ax3.lines[0].set_markersize(4)
                ax3.lines[0].set_markeredgewidth(0.9)
                ax3.lines[0].set_markeredgecolor("black")
                if len(ax3.lines) > 1:
                    ax3.lines[1].set_linewidth(2.6)
            ax3.set_title("Residual Q–Q Plot")
            _apply_plain_ticks(ax3, humanize=False)
            _enhance_spines(ax3, lw=1.6)
            st.pyplot(fig3)

            st.caption(
                "Residual patterns indicate model misspecification or heteroskedasticity. "
                "If residual Q–Q deviates strongly, consider robust models or transformations."
            )


            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
            # Permutation importance (if feasible)
            if feature_names and X_train is not None and y_train is not None:
                st.markdown("##### Permutation Importance (sampled)")
                try:
                    r = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42)
                    imp = pd.DataFrame({"feature": feature_names, "importance_mean": r.importances_mean})
                    imp = imp.sort_values("importance_mean", ascending=False).head(30)
                    render_table(
                        imp,
                        dark_mode=dark_tables,
                        precision=6,
                        max_rows=30,
                        humanize_large=False,
                        caption="Higher values indicate larger average performance drop when the feature is permuted.",
                    )

                    fig4, ax4 = plt.subplots(figsize=(8, 6))
                    ax4.barh(imp["feature"].iloc[::-1], imp["importance_mean"].iloc[::-1], edgecolor="black", linewidth=0.3)
                    ax4.set_title("Permutation Importance (Top 30)")
                    ax4.set_xlabel("Mean importance")
                    _apply_plain_ticks(ax4, humanize=False)
                    st.pyplot(fig4)
                except Exception as e:
                    st.info(f"Permutation importance not available for this model: {e}")

        else:
        
            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            # Confusion matrix
            cm = confusion_matrix(y_test, preds)
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, linewidths=0.6, linecolor="black")
            ax.set_title("Confusion Matrix")
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            st.pyplot(fig)


            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
            
            # Classification report
            st.markdown("##### Classification Report")
            rep = classification_report(y_test, preds, output_dict=True, zero_division=0)
            render_table(pd.DataFrame(rep).T, dark_mode=dark_tables, precision=4, max_rows=200, humanize_large=False)

            st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
    
            # ROC/PR if possible
            st.markdown("##### ROC / Precision–Recall")
            can_proba = hasattr(model, "predict_proba")
            can_dec = hasattr(model, "decision_function")
            if (can_proba or can_dec) and len(np.unique(y_test)) == 2:
                scores = model.predict_proba(X_test)[:, 1] if can_proba else model.decision_function(X_test)
                auc = roc_auc_score(y_test, scores)

                fpr, tpr, _ = roc_curve(y_test, scores)
                fig2, ax2 = plt.subplots(figsize=(7, 4))
                ax2.plot(fpr, tpr, linewidth=2.0)
                ax2.plot([0, 1], [0, 1], linestyle="--", linewidth=1.0)
                ax2.set_title(f"ROC Curve (AUC={auc:.3f})")
                ax2.set_xlabel("False Positive Rate")
                ax2.set_ylabel("True Positive Rate")
                _apply_plain_ticks(ax2, humanize=False)
                st.pyplot(fig2)

                pr, rc, _ = precision_recall_curve(y_test, scores)
                fig3, ax3 = plt.subplots(figsize=(7, 4))
                ax3.plot(rc, pr, linewidth=2.0)
                ax3.set_title("Precision–Recall Curve")
                ax3.set_xlabel("Recall")
                ax3.set_ylabel("Precision")
                _apply_plain_ticks(ax3, humanize=False)
                st.pyplot(fig3)

            # Permutation importance (if feasible)
            if feature_names:
            
                st.markdown( BLUE_DIVIDER, unsafe_allow_html=True )
                
                st.markdown("##### Permutation Importance")
                try:
                    r = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42)
                    imp = pd.DataFrame({"feature": feature_names, "importance_mean": r.importances_mean})
                    imp = imp.sort_values("importance_mean", ascending=False).head(30)

                    render_table(
                        imp,
                        dark_mode=dark_tables,
                        precision=6,
                        max_rows=30,
                        humanize_large=False,
                        caption="Higher values indicate larger average performance drop when the feature is permuted.",
                    )

                    fig4, ax4 = plt.subplots(figsize=(8, 6))
                    ax4.barh(imp["feature"].iloc[::-1], imp["importance_mean"].iloc[::-1], edgecolor="black", linewidth=0.3)
                    ax4.set_title("Permutation Importance (Top 30)")
                    ax4.set_xlabel("Mean importance")
                    _apply_plain_ticks(ax4, humanize=False)
                    st.pyplot(fig4)
                except Exception as e:
                    st.info(f"Permutation importance not available for this model: {e}")

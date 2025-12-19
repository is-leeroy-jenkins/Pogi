# ******************************************************************************************
#  Assembly:                Pogi
#  Filename:                app.py
#  Author:                  Generated (per Terry's specifications)
#  Created:                 2025-12-18
#
#  Purpose:
#  --------
#  A full, unified Streamlit analytics workbench that mirrors the Pogi notebook phases:
#
#   1) Data Overview & Validation (Column Quality: Completeness, Cardinality, Variance/Entropy)
#   2) Descriptive Statistics (Distribution Summary Table + small-multiple histograms)
#   3) Inferential Statistics (explicit keys; assumption-forward)
#   4) Anomaly & Outlier Detection (flagging only)
#   5) Feature Engineering (non-temporal only; explicit pipeline)
#   6) Model Training (defaults only; no tuning)
#   7) Model Comparison (defaults only; no tuning)
#   8) Model Diagnostics (residuals, confusion, ROC/PR, importance)
#
#  Explicit Exclusions (per user direction):
#  ----------------------------------------
#  - No hyperparameter tuning (GridSearchCV / RandomizedSearchCV removed)
#  - No domain presets
#  - No time-series feature engineering (lags/rolling/seasonality excluded)
#
#  Notes:
#  ------
#  - Histograms are corrected:
#       * A Distribution Summary Table is primary.
#       * Histograms are small multiples across continuous numeric features.
#       * ID-like numeric columns are excluded using cardinality ratio thresholding.
#  - All Streamlit widgets use explicit keys to prevent duplicate element IDs.
# ******************************************************************************************
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from scipy.stats.mstats import winsorize

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso, ElasticNet
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
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, RobustScaler, StandardScaler


# ======================================================================================
# Table Rendering (No st.dataframe(Styler); always visible)
# ======================================================================================

def render_table(
    df: pd.DataFrame,
    title: str | None = None,
    caption: str | None = None,
    precision: int = 4,
    dark_mode: bool = True,
    max_rows: int = 500,
) -> None:
    """
    Purpose:
    --------
    Render a DataFrame as an HTML table with strong contrast. This avoids Streamlit's unreliable
    rendering of pandas Styler inside st.dataframe.

    Parameters:
    -----------
    df: pd.DataFrame
        Table to render.
    title: str | None
        Optional table heading.
    caption: str | None
        Optional explanatory caption.
    precision: int
        Numeric formatting precision.
    dark_mode: bool
        Dark palette if True, light palette if False.
    max_rows: int
        Maximum rows to render to HTML.
    """
    if title:
        st.markdown(f"#### {title}")

    if df is None or df.empty:
        st.info("No data to display.")
        return

    df_show = df.copy()
    if len(df_show) > max_rows:
        df_show = df_show.head(max_rows)

    # Format numeric columns
    num_cols = df_show.select_dtypes(include=[np.number]).columns.tolist()
    fmt: Dict[str, Any] = {c: f"{{:,.{precision}f}}" for c in num_cols}

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
        .format(fmt)
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
# Stats Helpers
# ======================================================================================

def safe_numeric_series(df: pd.DataFrame, col: str) -> np.ndarray:
    v = pd.to_numeric(df[col], errors="coerce").dropna().values.astype(float)
    return v


def descriptive_profile(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    n = df.shape[0]
    percentiles = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]

    for c in cols:
        v = safe_numeric_series(df, c)
        non_missing = int(np.isfinite(v).sum())
        missing = int(n - non_missing)

        if non_missing == 0:
            continue

        q_vals = np.nanpercentile(v, percentiles)
        q = dict(zip(percentiles, q_vals))

        mean = float(np.nanmean(v))
        std = float(np.nanstd(v, ddof=0))
        var = float(np.nanvar(v, ddof=0))
        mad = float(np.nanmedian(np.abs(v - np.nanmedian(v))))
        iqr = float(q[75] - q[25])
        rng = float(q[100] - q[0])

        skew = float(stats.skew(v)) if v.size >= 3 else 0.0
        kurt = float(stats.kurtosis(v)) if v.size >= 4 else 0.0
        zero_pct = float((v == 0).mean() * 100.0)

        # Outlier rates
        lo = q[25] - 1.5 * iqr
        hi = q[75] + 1.5 * iqr
        out_iqr = float(((v < lo) | (v > hi)).mean() * 100.0)

        z = (v - mean) / (std + 1e-12)
        out_z3 = float((np.abs(z) > 3.0).mean() * 100.0)

        # Normality p-value (best-effort)
        normal_p: Optional[float] = None
        try:
            if 8 <= v.size <= 5000:
                _, p = stats.shapiro(v)
                normal_p = float(p)
            elif v.size > 5000:
                _, p = stats.normaltest(v[:5000])
                normal_p = float(p)
            elif v.size >= 8:
                _, p = stats.normaltest(v)
                normal_p = float(p)
        except Exception:
            normal_p = None

        rows.append({
            "feature": c,
            "count": int(v.size),
            "missing_pct": float((missing / n) * 100.0) if n else 0.0,
            "mean": mean,
            "std": std,
            "var": var,
            "min": float(q[0]),
            "p01": float(q[1]),
            "p05": float(q[5]),
            "p10": float(q[10]),
            "q1": float(q[25]),
            "median": float(q[50]),
            "q3": float(q[75]),
            "p90": float(q[90]),
            "p95": float(q[95]),
            "p99": float(q[99]),
            "max": float(q[100]),
            "iqr": iqr,
            "range": rng,
            "mad": mad,
            "skew": skew,
            "kurtosis": kurt,
            "zero_pct": zero_pct,
            "outlier_iqr_pct": out_iqr,
            "outlier_z3_pct": out_z3,
            "normality_p": normal_p,
        })

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["missing_pct", "outlier_iqr_pct"], ascending=[True, False])


def feature_quality(df: pd.DataFrame) -> pd.DataFrame:
    n = df.shape[0]
    rows: List[Dict[str, Any]] = []

    for c in df.columns:
        s = df[c]
        non_missing = int(s.notna().sum())
        completeness = float((non_missing / n) * 100.0) if n else 0.0
        uniq = int(s.nunique(dropna=True))
        card_ratio = float(uniq / non_missing) if non_missing else 0.0

        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce").dropna().values.astype(float)
            variance = float(np.var(v)) if v.size else np.nan
            entropy = np.nan
        else:
            vc = s.dropna().astype(str).value_counts(normalize=True)
            entropy = float(stats.entropy(vc.values)) if vc.size > 1 else 0.0
            variance = np.nan

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


def corr_with_pvalues(df: pd.DataFrame, cols: List[str], method: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
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
                else:
                    r, p = stats.spearmanr(x[m].values, y[m].values)

            corr.loc[a, b] = float(r)
            pval.loc[a, b] = float(p)

    return corr, pval


# ======================================================================================
# App
# ======================================================================================

st.set_page_config(page_title="Pogi", layout="wide", page_icon=r'resources/favicon.ico')
st.title("🏛️ Analytics Workbench")
st.caption("Exploratory Data Analysis")

# Sidebar
st.sidebar.header("📁 Data Input")
file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], key="upload")
if not file:
    st.info("Upload a CSV or Excel file to begin.")
    st.stop()

try:
    df = pd.read_csv(file) if file.name.lower().endswith(".csv") else pd.read_excel(file)
except Exception as e:
    st.error(f"Failed to read file: {e}")
    st.stop()

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

st.sidebar.header("⚙️ Global Controls")
preview_rows = st.sidebar.slider("Preview rows", 10, 500, 50, 10, key="preview_rows")
dark_tables = st.sidebar.toggle("Use dark tables", value=True, key="dark_tables")
plot_theme = st.sidebar.selectbox("Plot theme", ["Light", "Dark"], index=1, key="plot_theme")

if plot_theme == "Dark":
    plt.style.use("dark_background")
else:
    plt.style.use("default")

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

# --------------------------------------------------------------------------------------
# 1) Data Overview
# --------------------------------------------------------------------------------------

with tabs[0]:
    st.subheader("1) Data Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", f"{df.shape[1]:,}")
    c3.metric("Numeric Columns", f"{len(numeric_cols):,}")
    c4.metric("Non-Numeric Columns", f"{len(non_numeric_cols):,}")

    st.markdown("### Preview (interactive)")
    st.dataframe(df.head(int(preview_rows)), use_container_width=True, height=420)

    st.markdown("### Feature Quality (Completeness, Cardinality, Variance/Entropy)")
    fq = feature_quality(df)
    render_table(
        fq,
        caption=(
            "Completeness (%) is the percent of non-missing values. Cardinality ratio indicates how close a feature is "
            "to unique-per-row behavior. Variance/entropy help quantify informational content for numeric/categorical."
        ),
        dark_mode=dark_tables,
        precision=4,
        max_rows=500,
    )

    st.markdown("### Schema Summary")
    schema = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_missing": [int(df[c].notna().sum()) for c in df.columns],
        "missing": [int(df[c].isna().sum()) for c in df.columns],
        "unique": [int(df[c].nunique(dropna=True)) for c in df.columns],
    }).sort_values(["dtype", "missing", "unique"], ascending=[True, True, False])

    render_table(
        schema,
        caption="Use this to validate inferred types and spot columns that require cleanup (missing/unique extremes).",
        dark_mode=dark_tables,
        precision=0,
        max_rows=500,
    )

# --------------------------------------------------------------------------------------
# 2) Descriptive Statistics (expanded; multiple tables + plots + interpretation)
# --------------------------------------------------------------------------------------

with tabs[1]:
    st.subheader("2) Descriptive Statistics")

    if not numeric_cols:
        st.warning("No numeric columns detected.")
    else:
        st.markdown("### Expanded Numeric Profile")
        prof = descriptive_profile(df, numeric_cols)
        render_table(
            prof,
            caption=(
                "This profile expands beyond describe(): percentiles, MAD, skew/kurtosis, and outlier rates. "
                "Use outlier_iqr_pct/outlier_z3_pct to identify heavy tails or data quality issues."
            ),
            dark_mode=dark_tables,
            precision=4,
            max_rows=500,
        )

        st.markdown("### Distribution Visualization (multi-select)")
        chosen = st.multiselect(
            "Select numeric features to visualize",
            options=numeric_cols,
            default=numeric_cols[: min(6, len(numeric_cols))],
            key="desc_chosen",
        )
        bins = st.slider("Histogram bins", 10, 120, 40, 5, key="desc_bins")

        if chosen:
            st.markdown("#### Overlay histograms")
            fig, ax = plt.subplots(figsize=(10, 5))
            for c in chosen:
                v = safe_numeric_series(df, c)
                if v.size > 1:
                    ax.hist(v, bins=bins, alpha=0.35, label=c)
            ax.set_title("Overlay Histograms")
            ax.set_xlabel("Value")
            ax.set_ylabel("Count")
            ax.legend()
            st.pyplot(fig)

            st.caption(
                "Overlay histograms show relative scale and spread. If one feature dominates the x-axis, "
                "compare using robust scaling or inspect features individually with boxplots below."
            )

            st.markdown("#### Boxplots")
            data = [safe_numeric_series(df, c) for c in chosen]
            labels = [c for c in chosen]
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.boxplot(data, labels=labels, showfliers=True)
            ax2.set_title("Boxplots (median, IQR, and outliers)")
            ax2.set_ylabel("Value")
            plt.xticks(rotation=30, ha="right")
            st.pyplot(fig2)

            st.caption(
                "Boxplots emphasize central tendency and dispersion. Numerous outliers suggest heavy tails, "
                "data entry errors, or legitimately extreme values."
            )

            st.markdown("#### Q–Q plots (normality check)")
            qq_cols = st.multiselect(
                "Select features for Q–Q plots",
                options=chosen,
                default=chosen[: min(3, len(chosen))],
                key="desc_qq_cols",
            )
            for c in qq_cols:
                v = safe_numeric_series(df, c)
                if v.size >= 20:
                    fig3, ax3 = plt.subplots(figsize=(6, 4))
                    stats.probplot(v, dist="norm", plot=ax3)
                    ax3.set_title(f"Q–Q Plot: {c}")
                    st.pyplot(fig3)
                    st.caption(
                        f"For {c}, strong deviation from the diagonal indicates non-normality. "
                        "Non-normality is common; it informs test selection and preprocessing."
                    )

# --------------------------------------------------------------------------------------
# 3) Inferential Statistics (expanded; correlation + p-values + tests; tables not json)
# --------------------------------------------------------------------------------------

with tabs[2]:
    st.subheader("3) Inferential Statistics")

    if not numeric_cols:
        st.warning("No numeric columns detected.")
    else:
        st.markdown("### Correlation Analysis (subset + p-values)")
        corr_method = st.selectbox("Correlation method", ["pearson", "spearman"], key="inf_corr_method")
        corr_cols = st.multiselect(
            "Select numeric features",
            options=numeric_cols,
            default=numeric_cols[: min(12, len(numeric_cols))],
            key="inf_corr_cols",
        )

        if len(corr_cols) >= 2:
            corr_mat, p_mat = corr_with_pvalues(df, corr_cols, corr_method)

            fig, ax = plt.subplots(figsize=(10, 7))
            sns.heatmap(corr_mat, cmap="coolwarm", center=0.0, ax=ax)
            ax.set_title(f"{corr_method.title()} Correlation Heatmap")
            st.pyplot(fig)

            st.caption(
                "Large magnitudes indicate stronger monotonic (Spearman) or linear (Pearson) association. "
                "Use p-values to assess whether correlations are likely non-zero given sample size."
            )

            render_table(
                corr_mat.reset_index().rename(columns={"index": "feature"}),
                title="Correlation matrix",
                dark_mode=dark_tables,
                precision=4,
            )
            render_table(
                p_mat.reset_index().rename(columns={"index": "feature"}),
                title="p-value matrix",
                dark_mode=dark_tables,
                precision=6,
            )

        st.markdown("### Confidence intervals for means (multi-select)")
        ci_cols = st.multiselect(
            "Select numeric features",
            options=numeric_cols,
            default=numeric_cols[: min(8, len(numeric_cols))],
            key="inf_ci_cols",
        )
        conf = st.slider("Confidence level", 0.80, 0.99, 0.95, 0.01, key="inf_ci_conf")

        ci_rows: List[Dict[str, Any]] = []
        for c in ci_cols:
            v = safe_numeric_series(df, c)
            if v.size >= 2:
                mean = float(v.mean())
                se = float(stats.sem(v))
                dfree = int(v.size - 1)
                tcrit = float(stats.t.ppf((1.0 + conf) / 2.0, dfree))
                lo = mean - tcrit * se
                hi = mean + tcrit * se
                ci_rows.append({"feature": c, "n": int(v.size), "mean": mean, "ci_low": lo, "ci_high": hi})

        render_table(
            pd.DataFrame(ci_rows),
            caption="Confidence intervals quantify uncertainty in the mean estimate for each feature.",
            dark_mode=dark_tables,
            precision=4,
        )

        st.markdown("### Two-group comparisons (t-test or Mann–Whitney)")
        if non_numeric_cols:
            num = st.selectbox("Numeric feature", options=numeric_cols, key="inf_2g_num")
            grp = st.selectbox("Grouping (categorical) feature", options=non_numeric_cols, key="inf_2g_grp")
            groups = sorted(df[grp].dropna().astype(str).unique().tolist())

            if len(groups) >= 2:
                gsel = st.multiselect(
                    "Select exactly two groups",
                    options=groups,
                    default=groups[:2],
                    key="inf_2g_groups",
                )
                test_kind = st.selectbox(
                    "Test type",
                    ["Two-sample t-test", "Mann–Whitney U (non-parametric)"],
                    key="inf_2g_test",
                )

                if len(gsel) == 2:
                    a = pd.to_numeric(df.loc[df[grp].astype(str) == gsel[0], num], errors="coerce").dropna().values
                    b = pd.to_numeric(df.loc[df[grp].astype(str) == gsel[1], num], errors="coerce").dropna().values

                    if a.size >= 2 and b.size >= 2:
                        rows: List[Dict[str, Any]] = []
                        if test_kind == "Two-sample t-test":
                            eq = st.checkbox("Assume equal variances", value=False, key="inf_2g_eqvar")
                            t_stat, p_val = stats.ttest_ind(a, b, equal_var=bool(eq))
                            rows.append({
                                "test": "t-test",
                                "group_A": gsel[0], "group_B": gsel[1],
                                "n_A": int(a.size), "n_B": int(b.size),
                                "mean_A": float(a.mean()), "mean_B": float(b.mean()),
                                "t": float(t_stat), "p_value": float(p_val),
                            })
                            caption = "t-test compares group means; p-values indicate whether mean difference is likely non-zero."
                        else:
                            u_stat, p_val = stats.mannwhitneyu(a, b, alternative="two-sided")
                            rows.append({
                                "test": "Mann–Whitney U",
                                "group_A": gsel[0], "group_B": gsel[1],
                                "n_A": int(a.size), "n_B": int(b.size),
                                "median_A": float(np.median(a)), "median_B": float(np.median(b)),
                                "U": float(u_stat), "p_value": float(p_val),
                            })
                            caption = "Mann–Whitney compares distributions without assuming normality."

                        render_table(pd.DataFrame(rows), caption=caption, dark_mode=dark_tables, precision=6)

                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.hist(a, bins=30, alpha=0.45, label=gsel[0])
                        ax.hist(b, bins=30, alpha=0.45, label=gsel[1])
                        ax.set_title(f"{num} by {grp} (two-group comparison)")
                        ax.set_xlabel(num)
                        ax.set_ylabel("Count")
                        ax.legend()
                        st.pyplot(fig)

                        st.caption(
                            "Distribution overlap gives practical context beyond p-values. "
                            "Heavily overlapping histograms imply small practical separation."
                        )

# --------------------------------------------------------------------------------------
# 4) Feature Analysis (expanded: correlations + PCA + k-means + LDA when possible)
# --------------------------------------------------------------------------------------

with tabs[3]:
    st.subheader("4) Feature Analysis")

    if not numeric_cols:
        st.warning("Feature analysis requires numeric columns.")
    else:
        st.markdown("### Feature relationships (correlation + redundancy)")
        fa_cols = st.multiselect(
            "Select numeric features for analysis",
            options=numeric_cols,
            default=numeric_cols[: min(15, len(numeric_cols))],
            key="fa_cols",
        )

        if len(fa_cols) >= 2:
            corr = df[fa_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 7))
            sns.heatmap(corr, cmap="coolwarm", center=0.0, ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

            st.caption(
                "Strong correlation blocks suggest redundancy. Consider dropping one of a highly correlated pair "
                "or using PCA to stabilize modeling."
            )

            # Rank strongest correlations (excluding self)
            pairs: List[Dict[str, Any]] = []
            for i in range(len(fa_cols)):
                for j in range(i + 1, len(fa_cols)):
                    a, b = fa_cols[i], fa_cols[j]
                    pairs.append({"feature_A": a, "feature_B": b, "corr": float(corr.loc[a, b]), "abs_corr": abs(float(corr.loc[a, b]))})
            top_pairs = pd.DataFrame(pairs).sort_values("abs_corr", ascending=False).head(20)
            render_table(
                top_pairs.drop(columns=["abs_corr"]),
                title="Top correlated feature pairs (by absolute correlation)",
                dark_mode=dark_tables,
                precision=4,
            )

        st.markdown("### PCA (dimensionality reduction)")
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
            render_table(
                evr,
                caption="If cumulative variance rises quickly, the data has a lower-dimensional structure.",
                dark_mode=dark_tables,
                precision=6,
            )

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(np.arange(1, evr.shape[0] + 1), evr["cumulative"].values, marker="o")
            ax.set_title("PCA Cumulative Explained Variance")
            ax.set_xlabel("Components")
            ax.set_ylabel("Cumulative variance")
            st.pyplot(fig)

            st.caption(
                "A steep early rise indicates many features are redundant. PCA can compress without losing most signal."
            )

            if Z.shape[1] >= 2:
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                ax2.scatter(Z[:, 0], Z[:, 1], s=18)
                ax2.set_title("PCA Projection (PC1 vs PC2)")
                ax2.set_xlabel("PC1")
                ax2.set_ylabel("PC2")
                st.pyplot(fig2)

                st.caption(
                    "Visible grouping in PCA space suggests clustering may be meaningful, or that categorical drivers exist."
                )

            st.markdown("### k-Means clustering (on PCA space)")
            k = st.slider("k (clusters)", 2, 12, 3, 1, key="fa_k")
            km = KMeans(n_clusters=int(k), n_init="auto", random_state=42)
            labels = km.fit_predict(Z)
            counts = pd.Series(labels).value_counts().sort_index()
            counts_df = pd.DataFrame({"cluster": counts.index.astype(int), "count": counts.values.astype(int)})
            render_table(
                counts_df,
                caption="Cluster counts show how observations partition under k-means in PCA space.",
                dark_mode=dark_tables,
                precision=0,
            )

            if Z.shape[1] >= 2:
                fig3, ax3 = plt.subplots(figsize=(8, 6))
                ax3.scatter(Z[:, 0], Z[:, 1], c=labels, s=18)
                ax3.set_title("k-Means Clusters (PCA space)")
                ax3.set_xlabel("PC1")
                ax3.set_ylabel("PC2")
                st.pyplot(fig3)

                st.caption(
                    "Separated colored regions indicate stronger clustering structure; diffuse overlap implies weak clusters."
                )

        st.markdown("### LDA (requires categorical target)")
        if non_numeric_cols and numeric_cols:
            lda_target = st.selectbox("Categorical target for LDA", options=["(none)"] + non_numeric_cols, key="fa_lda_target")
            lda_cols = st.multiselect(
                "Numeric features for LDA",
                options=numeric_cols,
                default=numeric_cols[: min(10, len(numeric_cols))],
                key="fa_lda_cols",
            )
            if lda_target != "(none)" and len(lda_cols) >= 2:
                y_raw = df[lda_target].astype(str).fillna("(missing)")
                le = LabelEncoder()
                y = le.fit_transform(y_raw.values)

                X = df[lda_cols].apply(pd.to_numeric, errors="coerce").fillna(df[lda_cols].median(numeric_only=True))
                Xs = StandardScaler().fit_transform(X.values)

                lda = LinearDiscriminantAnalysis()
                Z = lda.fit_transform(Xs, y)

                if Z.shape[1] >= 2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.scatter(Z[:, 0], Z[:, 1], c=y, s=18)
                    ax.set_title("LDA Projection (LD1 vs LD2)")
                    ax.set_xlabel("LD1")
                    ax.set_ylabel("LD2")
                    st.pyplot(fig)
                else:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.scatter(np.arange(Z.shape[0]), Z[:, 0], c=y, s=18)
                    ax.set_title("LDA Projection (LD1)")
                    ax.set_xlabel("Row")
                    ax.set_ylabel("LD1")
                    st.pyplot(fig)

                st.caption(
                    "LDA maximizes class separation for the selected target. Clear separation suggests useful predictive signal."
                )

# --------------------------------------------------------------------------------------
# 5) Feature Engineering (expanded; shows transformed DF; more imputation; winsorization)
# --------------------------------------------------------------------------------------

with tabs[4]:
    st.subheader("5) Feature Engineering")

    if not numeric_cols:
        st.warning("Feature engineering operates on numeric columns.")
    else:
        fe_cols = st.multiselect(
            "Select numeric features to transform",
            options=numeric_cols,
            default=numeric_cols[: min(12, len(numeric_cols))],
            key="fe_cols",
        )

        if not fe_cols:
            st.info("Select at least one numeric feature.")
        else:
            c1, c2, c3 = st.columns(3)

            with c1:
                impute = st.multiselect(
                    "Imputation strategy (applied in order)",
                    ["mean", "median", "most_frequent", "constant", "knn"],
                    default=["median"],
                    key="fe_impute",
                )
                const_fill = st.number_input("Constant fill value", value=0.0, key="fe_const")

            with c2:
                do_winsor = st.checkbox("Winsorize (cap extremes)", value=False, key="fe_winsor")
                w_lim = st.slider("Winsor tail limit", 0.0, 0.25, 0.01, 0.005, key="fe_w_lim")

            with c3:
                scaler = st.selectbox("Scaling", ["None", "Standard", "MinMax", "Robust"], index=1, key="fe_scaler")
                log1p = st.checkbox("Log1p transform (positive-only)", value=False, key="fe_log1p")

            X = df[fe_cols].apply(pd.to_numeric, errors="coerce")

            # Imputation
            X_imp = X.copy()
            for strat in impute:
                if strat == "knn":
                    knn = KNNImputer(n_neighbors=5, weights="distance")
                    X_imp = pd.DataFrame(knn.fit_transform(X_imp), columns=fe_cols)
                elif strat == "constant":
                    simp = SimpleImputer(strategy="constant", fill_value=float(const_fill))
                    X_imp = pd.DataFrame(simp.fit_transform(X_imp), columns=fe_cols)
                else:
                    simp = SimpleImputer(strategy=strat)
                    X_imp = pd.DataFrame(simp.fit_transform(X_imp), columns=fe_cols)

            # Winsorization
            X_win = X_imp.copy()
            if do_winsor and w_lim > 0.0:
                for c in fe_cols:
                    v = X_win[c].values.astype(float)
                    X_win[c] = winsorize(v, limits=(float(w_lim), float(w_lim)))

            # Log transform (safe: only for strictly positive)
            X_log = X_win.copy()
            if log1p:
                for c in fe_cols:
                    v = X_log[c].values.astype(float)
                    if np.nanmin(v) <= -1.0:
                        # Cannot log1p safely; keep as-is
                        continue
                    X_log[c] = np.log1p(v)

            # Scaling
            if scaler == "Standard":
                sc = StandardScaler()
                X_out = pd.DataFrame(sc.fit_transform(X_log.values), columns=fe_cols)
            elif scaler == "MinMax":
                sc = MinMaxScaler()
                X_out = pd.DataFrame(sc.fit_transform(X_log.values), columns=fe_cols)
            elif scaler == "Robust":
                sc = RobustScaler()
                X_out = pd.DataFrame(sc.fit_transform(X_log.values), columns=fe_cols)
            else:
                X_out = X_log.copy()

            st.markdown("### Transformed Data Preview")
            render_table(
                X_out.head(int(preview_rows)),
                caption="This table shows the engineered matrix after imputation, optional winsorization/log transform, and scaling.",
                dark_mode=dark_tables,
                precision=4,
                max_rows=500,
            )

            st.markdown("### Before vs After (summary)")
            before = descriptive_profile(df, fe_cols)[["feature", "mean", "std", "skew", "kurtosis", "outlier_iqr_pct"]]
            after_src = pd.DataFrame(X_out, columns=fe_cols)
            after = descriptive_profile(after_src, fe_cols)[["feature", "mean", "std", "skew", "kurtosis", "outlier_iqr_pct"]]
            merged = before.merge(after, on="feature", suffixes=("_before", "_after"))
            render_table(
                merged,
                caption="Compare distribution metrics before/after to validate that transformations had the intended effect.",
                dark_mode=dark_tables,
                precision=4,
                max_rows=500,
            )

            # Persist for later tabs
            st.session_state["X_transformed"] = X_out
            st.session_state["X_transformed_cols"] = fe_cols

# --------------------------------------------------------------------------------------
# 6) Anomaly Detection (3+ methods; multi-select; tables, not json)
# --------------------------------------------------------------------------------------

with tabs[5]:
    st.subheader("6) Anomaly Detection")

    if not numeric_cols:
        st.warning("Anomaly detection requires numeric columns.")
    else:
        methods = st.multiselect(
            "Select anomaly detection methods",
            options=[
                "Z-score (univariate)",
                "IQR rule (univariate)",
                "MAD robust z (univariate)",
                "Isolation Forest (multivariate)",
                "Local Outlier Factor (multivariate)",
            ],
            default=["Z-score (univariate)", "IQR rule (univariate)", "Isolation Forest (multivariate)"],
            key="ad_methods",
        )

        cols = st.multiselect(
            "Numeric columns to use",
            options=numeric_cols,
            default=numeric_cols[: min(10, len(numeric_cols))],
            key="ad_cols",
        )

        if not cols:
            st.info("Select at least one numeric column.")
        else:
            X = df[cols].apply(pd.to_numeric, errors="coerce")
            X = X.fillna(X.median(numeric_only=True))

            flags = pd.DataFrame(index=df.index)
            summary_rows: List[Dict[str, Any]] = []

            if "Z-score (univariate)" in methods:
                z_thr = st.slider("Z threshold", 2.0, 6.0, 3.0, 0.1, key="ad_z_thr")
                zf = np.zeros(len(df), dtype=bool)
                for c in cols:
                    v = X[c].values.astype(float)
                    z = (v - v.mean()) / (v.std(ddof=0) + 1e-12)
                    zf |= (np.abs(z) > float(z_thr))
                flags["z_score_flag"] = zf
                summary_rows.append({"method": "Z-score", "flagged_rows": int(zf.sum()), "flagged_pct": float(zf.mean() * 100.0)})

            if "IQR rule (univariate)" in methods:
                k = st.slider("IQR multiplier", 1.0, 5.0, 1.5, 0.1, key="ad_iqr_k")
                iqf = np.zeros(len(df), dtype=bool)
                for c in cols:
                    v = X[c].values.astype(float)
                    q1 = np.percentile(v, 25)
                    q3 = np.percentile(v, 75)
                    iqr = q3 - q1
                    lo = q1 - float(k) * iqr
                    hi = q3 + float(k) * iqr
                    iqf |= (v < lo) | (v > hi)
                flags["iqr_flag"] = iqf
                summary_rows.append({"method": "IQR", "flagged_rows": int(iqf.sum()), "flagged_pct": float(iqf.mean() * 100.0)})

            if "MAD robust z (univariate)" in methods:
                rz_thr = st.slider("Robust z threshold", 2.0, 8.0, 3.5, 0.1, key="ad_rz_thr")
                mf = np.zeros(len(df), dtype=bool)
                for c in cols:
                    v = X[c].values.astype(float)
                    med = np.median(v)
                    mad = np.median(np.abs(v - med)) + 1e-12
                    rz = 0.6745 * (v - med) / mad
                    mf |= (np.abs(rz) > float(rz_thr))
                flags["mad_flag"] = mf
                summary_rows.append({"method": "MAD robust z", "flagged_rows": int(mf.sum()), "flagged_pct": float(mf.mean() * 100.0)})

            if "Isolation Forest (multivariate)" in methods:
                cont = st.slider("IsolationForest contamination", 0.001, 0.20, 0.02, 0.001, key="ad_iso_cont")
                iso = IsolationForest(random_state=42, contamination=float(cont))
                pred = iso.fit_predict(X.values)
                isof = pred == -1
                flags["isolation_forest_flag"] = isof
                summary_rows.append({"method": "IsolationForest", "flagged_rows": int(isof.sum()), "flagged_pct": float(isof.mean() * 100.0)})

            if "Local Outlier Factor (multivariate)" in methods:
                cont = st.slider("LOF contamination", 0.001, 0.20, 0.02, 0.001, key="ad_lof_cont")
                nn = st.slider("LOF n_neighbors", 5, 60, 20, 1, key="ad_lof_nn")
                lof = LocalOutlierFactor(n_neighbors=int(nn), contamination=float(cont))
                pred = lof.fit_predict(X.values)
                loff = pred == -1
                flags["lof_flag"] = loff
                summary_rows.append({"method": "LOF", "flagged_rows": int(loff.sum()), "flagged_pct": float(loff.mean() * 100.0)})

            st.markdown("### Detection Summary")
            render_table(
                pd.DataFrame(summary_rows),
                caption="Univariate methods flag extremes per-feature; multivariate methods flag unusual rows in joint feature space.",
                dark_mode=dark_tables,
                precision=4,
            )

            st.markdown("### Flagged Rows (combined view)")
            combined = flags.any(axis=1) if not flags.empty else pd.Series(False, index=df.index)
            flagged = df.loc[combined, cols].copy()
            render_table(
                flagged.head(300),
                caption="Rows flagged by any selected method. Review extremes and validate whether anomalies are errors or true outliers.",
                dark_mode=dark_tables,
                precision=4,
                max_rows=300,
            )

# --------------------------------------------------------------------------------------
# 7) Modeling (more than one model; compare table; multi-select features; no json)
# --------------------------------------------------------------------------------------

with tabs[6]:
    st.subheader("7) Modeling")

    if not numeric_cols:
        st.warning("Modeling here requires numeric features.")
    else:
        # Target must be single (strictly required)
        target = st.selectbox("Target (numeric for regression; categorical for classification)", options=df.columns.tolist(), key="mdl_target")

        # Feature default: all numeric except target (multi-select)
        default_feats = [c for c in numeric_cols if c != target]
        features = st.multiselect(
            "Feature columns (numeric)",
            options=numeric_cols,
            default=default_feats[: min(15, len(default_feats))],
            key="mdl_features",
        )

        if not features:
            st.info("Select at least one feature.")
        else:
            task = st.radio("Task type", ["Regression", "Classification"], key="mdl_task", horizontal=True)
            test_size = st.slider("Test size", 0.10, 0.50, 0.20, 0.05, key="mdl_test_size")
            rs = st.number_input("Random state", value=42, step=1, key="mdl_rs")

            X = df[features].apply(pd.to_numeric, errors="coerce")
            X = X.fillna(X.median(numeric_only=True))

            if task == "Regression":
                y = pd.to_numeric(df[target], errors="coerce").values

                models = {
                    "LinearRegression": LinearRegression(),
                    "Ridge": Ridge(),
                    "Lasso": Lasso(),
                    "ElasticNet": ElasticNet(),
                    "RandomForestRegressor": RandomForestRegressor(random_state=42),
                }

                chosen_models = st.multiselect(
                    "Models to train (multi-select)",
                    options=list(models.keys()),
                    default=["LinearRegression", "Ridge", "RandomForestRegressor"],
                    key="mdl_reg_models",
                )

                if st.button("Train selected models", type="primary", key="mdl_train_reg"):
                    X_train, X_test, y_train, y_test = train_test_split(
                        X.values, y, test_size=float(test_size), random_state=int(rs), shuffle=True
                    )

                    results: List[Dict[str, Any]] = []
                    fitted: Dict[str, Any] = {}

                    for name in chosen_models:
                        m = models[name]
                        m.fit(X_train, y_train)
                        preds = m.predict(X_test)

                        results.append({
                            "model": name,
                            "rmse": float(mean_squared_error(y_test, preds, squared=False)),
                            "mae": float(mean_absolute_error(y_test, preds)),
                            "r2": float(r2_score(y_test, preds)),
                        })
                        fitted[name] = (m, preds)

                    res_df = pd.DataFrame(results).sort_values("rmse")
                    render_table(
                        res_df,
                        title="Model comparison (Regression)",
                        caption="Lower RMSE/MAE is better; higher R² is better. Use this table to choose a baseline.",
                        dark_mode=dark_tables,
                        precision=6,
                    )

                    # Plot best model predicted vs actual
                    best_name = res_df.iloc[0]["model"]
                    best_model, best_preds = fitted[best_name]

                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.scatter(y_test, best_preds, s=14)
                    ax.set_title(f"Actual vs Predicted — {best_name}")
                    ax.set_xlabel("Actual")
                    ax.set_ylabel("Predicted")
                    st.pyplot(fig)
                    st.caption(
                        "Points close to the diagonal indicate accurate predictions. Systematic curvature implies missing non-linear structure."
                    )

                    # Persist for diagnostics
                    st.session_state["last_model_payload"] = {
                        "task": task,
                        "best_name": best_name,
                        "best_model": best_model,
                        "X_test": X_test,
                        "y_test": y_test,
                        "preds": best_preds,
                    }

            else:
                y_raw = df[target]
                if pd.api.types.is_numeric_dtype(y_raw):
                    y = y_raw.values
                else:
                    le = LabelEncoder()
                    y = le.fit_transform(y_raw.astype(str).fillna("(missing)"))

                models = {
                    "LogisticRegression": LogisticRegression(max_iter=4000, random_state=42),
                    "RandomForestClassifier": RandomForestClassifier(random_state=42),
                }

                chosen_models = st.multiselect(
                    "Models to train (multi-select)",
                    options=list(models.keys()),
                    default=["LogisticRegression", "RandomForestClassifier"],
                    key="mdl_clf_models",
                )

                if st.button("Train selected models", type="primary", key="mdl_train_clf"):
                    X_train, X_test, y_train, y_test = train_test_split(
                        X.values,
                        y,
                        test_size=float(test_size),
                        random_state=int(rs),
                        shuffle=True,
                        stratify=y if len(np.unique(y)) > 1 else None,
                    )

                    results: List[Dict[str, Any]] = []
                    fitted: Dict[str, Any] = {}

                    for name in chosen_models:
                        m = models[name]
                        m.fit(X_train, y_train)
                        preds = m.predict(X_test)
                        acc = float(accuracy_score(y_test, preds))

                        auc = np.nan
                        if hasattr(m, "predict_proba") and len(np.unique(y_test)) == 2:
                            p1 = m.predict_proba(X_test)[:, 1]
                            try:
                                auc = float(roc_auc_score(y_test, p1))
                            except Exception:
                                auc = np.nan

                        results.append({"model": name, "accuracy": acc, "auc": auc})
                        fitted[name] = (m, preds)

                    res_df = pd.DataFrame(results).sort_values("accuracy", ascending=False)
                    render_table(
                        res_df,
                        title="Model comparison (Classification)",
                        caption="Higher accuracy and AUC (binary) are better. Use Diagnostics for confusion matrices and curves.",
                        dark_mode=dark_tables,
                        precision=6,
                    )

                    best_name = res_df.iloc[0]["model"]
                    best_model, best_preds = fitted[best_name]

                    st.session_state["last_model_payload"] = {
                        "task": task,
                        "best_name": best_name,
                        "best_model": best_model,
                        "X_test": X_test,
                        "y_test": y_test,
                        "preds": best_preds,
                    }

# --------------------------------------------------------------------------------------
# 8) Diagnostics (multiple tables + plots + text; no json)
# --------------------------------------------------------------------------------------

with tabs[7]:
    st.subheader("8) Diagnostics")

    payload = st.session_state.get("last_model_payload")
    if payload is None:
        st.info("Train models in the Modeling tab to enable diagnostics.")
    else:
        task = payload["task"]
        best_name = payload["best_name"]
        model = payload["best_model"]
        X_test = payload["X_test"]
        y_test = payload["y_test"]
        preds = payload["preds"]

        st.markdown(f"### Best Model: {best_name}")

        if task == "Regression":
            resid = y_test - preds
            met = pd.DataFrame([{
                "rmse": float(mean_squared_error(y_test, preds, squared=False)),
                "mae": float(mean_absolute_error(y_test, preds)),
                "r2": float(r2_score(y_test, preds)),
                "resid_mean": float(np.mean(resid)),
                "resid_std": float(np.std(resid)),
            }])
            render_table(
                met,
                caption="Metrics summarize accuracy. Residual mean near 0 suggests low bias; large residual std suggests noise or missing signal.",
                dark_mode=dark_tables,
                precision=6,
            )

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(resid, bins=40)
            ax.set_title("Residual Distribution")
            ax.set_xlabel("Residual (Actual - Predicted)")
            ax.set_ylabel("Count")
            st.pyplot(fig)
            st.caption("If residuals are centered near 0 and roughly symmetric, errors are more random than systematic.")

            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.scatter(preds, resid, s=14)
            ax2.axhline(0, linestyle="--")
            ax2.set_title("Residuals vs Predicted")
            ax2.set_xlabel("Predicted")
            ax2.set_ylabel("Residual")
            st.pyplot(fig2)
            st.caption("Patterns (e.g., funnel shape) indicate heteroscedasticity or missing non-linear structure.")

        else:
            # Classification report as table (no json)
            rep = classification_report(y_test, preds, output_dict=True, zero_division=0)
            rep_df = pd.DataFrame(rep).T
            render_table(
                rep_df,
                title="Classification report",
                caption="Precision/recall identify which classes the model confuses. Support shows class sample sizes.",
                dark_mode=dark_tables,
                precision=6,
            )

            cm = confusion_matrix(y_test, preds)
            cm_df = pd.DataFrame(cm)
            render_table(
                cm_df,
                title="Confusion matrix (table)",
                caption="Off-diagonal counts are misclassifications. Concentration in one off-diagonal cell indicates systematic confusion.",
                dark_mode=dark_tables,
                precision=0,
            )

            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt="d", ax=ax)
            ax.set_title("Confusion matrix (heatmap)")
            st.pyplot(fig)

            # ROC/PR if binary + proba
            if hasattr(model, "predict_proba") and len(np.unique(y_test)) == 2:
                p1 = model.predict_proba(X_test)[:, 1]

                fpr, tpr, _ = roc_curve(y_test, p1)
                auc = float(roc_auc_score(y_test, p1))

                fig2, ax2 = plt.subplots(figsize=(7, 5))
                ax2.plot(fpr, tpr)
                ax2.plot([0, 1], [0, 1], linestyle="--")
                ax2.set_title(f"ROC Curve (AUC={auc:.4f})")
                ax2.set_xlabel("False Positive Rate")
                ax2.set_ylabel("True Positive Rate")
                st.pyplot(fig2)
                st.caption("Higher curves indicate better ranking performance; AUC closer to 1 is stronger.")

                prec, rec, _ = precision_recall_curve(y_test, p1)
                fig3, ax3 = plt.subplots(figsize=(7, 5))
                ax3.plot(rec, prec)
                ax3.set_title("Precision–Recall Curve")
                ax3.set_xlabel("Recall")
                ax3.set_ylabel("Precision")
                st.pyplot(fig3)
                st.caption("Precision–Recall is often more informative than ROC when classes are imbalanced.")

st.markdown("---")
st.caption(
    "Pogi"
)
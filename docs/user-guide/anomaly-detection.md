# Anomaly Detection

The Anomaly Detection tab flags potentially unusual records using multiple unsupervised detectors.

## 🧭 Purpose

This page explains how Pogi identifies candidate anomalies in budget execution or account balance data. The tab does not mutate the source dataframe; it creates a separate set of anomaly flags that can be reviewed alongside the original data.

## 🧱 Workflow Position

Anomaly Detection follows Feature Engineering or Feature Analysis. It can be used before supervised modeling to identify unusual records that may deserve audit review, policy review, exclusion, or separate analysis.

## 🧪 Detection Methods

Pogi uses a voting approach across several detectors:

| Detector | Signal | Purpose |
|---|---|---|
| Isolation Forest | Tree-based isolation score | Finds records that separate quickly from the rest of the population. |
| Local Outlier Factor | Local density difference | Finds records that are sparse relative to neighboring records. |
| PCA distance | Distance in reduced PCA space | Finds records far from the center of principal-component space. |

## 🗳️ Anomaly Voting

Pogi creates multiple flags and sums them into an anomaly vote count.

| Output Field | Meaning |
|---|---|
| `isolationforest_anomaly` | Isolation Forest flagged the record. |
| `lof_anomaly` | Local Outlier Factor flagged the record. |
| `pca_far` | PCA-distance rule flagged the record. |
| `pca_distance` | Distance from the center of PCA space. |
| `anomaly_votes` | Total detector votes. |
| `is_anomaly` | Final flag when enough detectors agree. |

## 🎛️ Detector Controls

| Control | Purpose |
|---|---|
| IsolationForest estimators | Number of trees used by Isolation Forest. |
| IsolationForest contamination | Expected share of outliers. |
| LOF neighbors | Neighborhood size for local density comparison. |
| LOF contamination | Expected share of outliers. |
| PCA components | Number of PCA dimensions used for distance scoring. |

## ✅ Recommended Sequence

1. Select numeric features with meaningful analytical content.
2. Avoid pure ID fields or arbitrary codes.
3. Start with conservative contamination values.
4. Run detectors and review vote distribution.
5. Investigate records flagged by two or more methods.
6. Treat anomaly flags as review candidates, not final findings.

## 🔗 Related Pages

- [Feature Engineering](feature-engineering.md)
- [Feature Analysis](feature-analysis.md)
- [Diagnostics](diagnostics.md)

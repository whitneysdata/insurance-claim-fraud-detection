# Insurance Claim Fraud Detection
### SQL + Python Research Project | Masters Scholarship Portfolio

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL%2016-336791?logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Abstract

This project investigates patterns of fraudulent insurance claims through a structured
end-to-end data science pipeline combining SQL-based data engineering and Python-based
statistical modelling. Leveraging a labelled auto-insurance claims dataset (Kaggle,
10,000 records across 6 insurance types), a normalised relational database is
constructed in PostgreSQL, from which actuarial KPIs — claim frequency, loss ratio,
and claim severity — are derived. Advanced SQL techniques including CTEs, window
functions, and multi-table joins are applied before transitioning to Python for
exploratory data analysis, hypothesis testing, and a logistic regression fraud
classification model validated against the ground-truth `CLAIM_STATUS` label.

**Background:** BSc Actuarial Science | Transitioning to Data Science

---

## Dataset

| Attribute | Detail |
|---|---|
| Source | [Insurance Claims Fraud Data — Kaggle (mastmustu)](https://www.kaggle.com/datasets/mastmustu/insurance-claims-fraud-data) |
| File used | `insurance_data.csv` (Claims Data only) |
| Rows | 10,000 |
| Columns | 38 |
| Period | June 2020 – June 2021 |
| Insurance types | Health, Life, Mobile, Motor, Property, Travel |
| Fraud label | `CLAIM_STATUS` — A (Approved) / D (Denied) |
| Denied claims | 503 (5.03%) — used as fraud proxy |

> **Data ethics note:** Columns `SSN`, `ROUTING_NUMBER`, and `ACCT_NUMBER` are
> present in the raw CSV but are intentionally excluded from the analytical schema.
> This PII exclusion is documented as a data governance decision in the methodology.

---

## Project Structure

```
insurance-claim-fraud-detection/
│
├── data/
│   ├── insurance_data.csv      # (gitignored)
│   └── exports/                # 5 SQL output CSVs
│
├── sql/                        # All SQL scripts (numbered in execution order)
│   ├── 01_create_staging.sql
│   ├── 02_create_tables.sql
│   ├── 03_data_audit.sql
│   ├── 04_etl_load.sql
│   ├── 05_frequency_severity.sql
│   ├── 06_loss_ratio.sql
│   ├── 07_high_risk.sql
│   ├── 08_fraud_detection.sql
│   ├── 09_settlement_lag.sql
│   └── 10_cte_denied_risk_profile.sql
│
├── src/                        # Reusable Python modules
│   ├── __init__.py
│   ├── config.py               # Paths, constants, colour palette, plot style
│   ├── data_loader.py          # load_raw(), load_processed()
│   ├── features.py             # encode_for_model(), get_feature_summary()
│   ├── viz.py                  # save_fig(), plot helpers
│   └── stats_utils.py          # run_anova(), run_chisquare(), run_ttest()
│
├── notebooks/                  # Jupyter notebooks (full research workflow)
│   ├── ch0_ch1_foundation.ipynb        # Research foundation + data preparation
│   ├── ch2_eda.ipynb                   # Exploratory Data Analysis (7 figures)
│   ├── ch3_hypothesis.ipynb            # Hypothesis testing (4 tests, 4 figures)
│   ├── ch4_visualisations.ipynb        # Publication-quality dashboard (4 figures)
│   └── ch5_ch6_model_conclusions.ipynb # Fraud model + conclusions (8 figures)
│
├── reports/                    # 20 figures exported at 180 DPI
├── requirements.txt
└── README.md
```

---

## Tools & Technologies

| Layer | Tool | Purpose |
|---|---|---|
| Database | PostgreSQL 16 + pgAdmin 4 | Schema design, ETL, SQL analysis |
| Language | Python 3 | Statistical analysis, modelling |
| Data | pandas, numpy | Data manipulation, feature engineering |
| Visualisation | matplotlib, seaborn | All figures (20 total) |
| Statistics | scipy | ANOVA, Chi-square, t-test, Mann-Whitney U |
| Modelling | scikit-learn | Logistic regression, cross-validation |
| Notebook | Jupyter Notebook | Full research workflow presentation |
| Version control | Git + GitHub | Commit history, portfolio visibility |

---

## Phase 1 — SQL (PostgreSQL)

A **Third Normal Form (3NF)** relational database was designed and implemented:

- `policyholders` — 17 demographic attributes per customer
- `policies` — 6 policy-level attributes (type, premium, agent, effective date)
- `claims` — 15 claim transaction attributes (dates, severity, amount, status)

A staging table buffered the raw CSV import with all columns as TEXT, preventing
type casting errors. An ETL pipeline then cleaned and loaded data into the
normalised schema, replacing `?` placeholders with NULL and casting types.

**SQL analyses conducted:**

| Script | Analysis |
|---|---|
| `05_frequency_severity.sql` | Claim frequency & severity by insurance type |
| `06_loss_ratio.sql` | Loss ratio (claims / premiums × 100) by type |
| `07_high_risk.sql` | High-risk customer segmentation (RISK_SEGMENTATION = H) |
| `08_fraud_detection.sql` | Window function fraud flag (claim > 2× type avg + no police report) |
| `09_settlement_lag.sql` | Report and processing lag (LOSS_DT → REPORT_DT → TXN_DATE_TIME) |
| `10_cte_denied_risk_profile.sql` | CTE: denial rate by risk segment, social class, employment |

---

## Phase 2 — Python (Jupyter Notebook)

### Research Questions

> **Primary:** What policyholder and claim characteristics are most strongly
> associated with claim denial in a multi-line insurance portfolio?

> **RQ2:** Is there a statistically significant difference in claim amounts across
> insurance types?

> **RQ3:** Does risk segmentation (H/M/L) significantly predict claim denial rate?

> **RQ4:** Do high-risk policyholders exhibit detectably different claim-filing
> behaviour (lag, severity) compared to low-risk policyholders?

### Hypothesis Testing Results

| # | Test | Statistic | p-value | Decision | Finding |
|---|---|---|---|---|---|
| H1 | One-Way ANOVA | F = 5,229.78 | < 0.001 | **Reject H₀** | Claim amounts differ significantly across types |
| H2 | Chi-Square | χ² = 3.26 | 0.196 | Fail to reject | Risk score does **not** predict denial |
| H3 | t-test + MW | t = −0.258 | 0.797 | Fail to reject | Denied ≠ simply the largest claims |
| H4 | One-Way ANOVA | F = 1.448 | 0.235 | Fail to reject | Lag is uniform — not a fraud signal |

> The most significant finding: H2 establishes that the insurer's existing risk
> segmentation system has **no statistically significant association** with claim denial.
> This directly motivates the fraud classification model.

### Fraud Classification Model

| Metric | Value |
|---|---|
| Algorithm | Logistic Regression (`class_weight='balanced'`) |
| Features | 33 (12 numeric + 21 one-hot encoded) |
| ROC-AUC (hold-out) | 0.532 |
| ROC-AUC (5-fold CV) | 0.521 ± 0.013 |
| Recall (Denied) | 0.515 |
| Cross-val stability | Low std (0.013) — no overfitting |

> **Honest assessment:** The AUC of 0.532 is modest, lying between random (0.50) and
> ideal (1.00). This is consistent with the hypothesis testing findings — no single
> feature or linear combination strongly separates denied from approved claims. This
> result transparently establishes a linear baseline and motivates future non-linear
> modelling (Random Forest, XGBoost) with richer feature engineering.

### Top Feature Importance (Logistic Regression Coefficients)

| Feature | Coefficient | Direction |
|---|---|---|
| `REPORT_LAG_DAYS` | −0.295 | Faster reporting → lower denial probability |
| `CLAIM_AMOUNT` | +0.200 | Higher claims → higher denial probability |
| `PROCESS_LAG_DAYS` | +0.195 | Longer processing → more complex/contested |
| `INSURANCE_TYPE_Life` | −0.178 | Life claims less likely denied |
| `CUSTOMER_EDUCATION_LEVEL_Masters` | −0.156 | Masters holders lowest denial rate (3.06%) |

---

## Key Findings Summary

1. **Life insurance** dominates claim severity ($54,386 avg vs Mobile $407 avg — 133× difference)
2. **Motor insurance** has the highest denial rate at 5.40%
3. The insurer's **risk segmentation (H/M/L) does not predict claim denial** (χ² = 3.26, p = 0.196)
4. Claim denial is **not driven by claim size** — denied and approved claims have nearly identical mean amounts (p = 0.797)
5. Claims investigated by a **vendor** have lower denial rates (4.71%) vs no vendor (5.70%)
6. **Faster reporting** after the loss event is the strongest approval signal (coefficient −0.295)

---

## Figures Produced

20 publication-quality figures exported to `reports/` at 180 DPI, including:

- Portfolio 6-panel dashboard (Fig 13)
- Risk × Severity heatmaps (Fig 14)
- ROC curve + Confusion matrix + Precision-Recall curve (Fig 17)
- Standardised feature importance (Fig 18)
- Full hypothesis test visualisations (Figs 8–12)

---

## How to Run

### Prerequisites
```bash
# Clone the repo
git clone https://github.com/YourUsername/insurance-claim-fraud-detection.git
cd insurance-claim-fraud-detection

# Install dependencies
pip install -r requirements.txt
```

### Download the dataset
1. Download `insurance_data.csv` from [Kaggle](https://www.kaggle.com/datasets/mastmustu/insurance-claims-fraud-data) (Claims Data file)
2. Place it in `data/raw/insurance_data.csv`

### Phase 1 — SQL
1. Create database `insurance_fraud_db` in PostgreSQL / pgAdmin 4
2. Run SQL scripts in `sql/` in numbered order (01 → 10)
3. Export 5 query result CSVs to `data/exports/`

### Phase 2 — Python
```bash
# Open Jupyter from the project ROOT (important for src/ imports)
cd insurance-claim-fraud-detection
jupyter notebook

# Run notebooks in order:
# notebooks/ch0_ch1_foundation.ipynb
# notebooks/ch2_eda.ipynb
# notebooks/ch3_hypothesis.ipynb
# notebooks/ch4_visualisations.ipynb
# notebooks/ch5_ch6_model_conclusions.ipynb
```

> **Important:** Always open Jupyter from the project root directory so that
> `from src.config import *` resolves correctly. If you see
> `ModuleNotFoundError: No module named 'src'`, add
> `import sys; sys.path.insert(0, '..')` at the top of the notebook.

---

## Limitations

- `CLAIM_STATUS = 'D'` proxies for fraud but also captures legitimate disputes (policy coverage gaps)
- Class imbalance (19:1) limits precision of the denied class
- No claim history, social network, or geospatial features available in this dataset
- Linear baseline only — non-linear models are future work
- 13-month observation window; fraud patterns may shift over time

---

## Research Progress

- [x] Phase 1: Database design + SQL analysis (PostgreSQL)
- [x] Phase 2: EDA + Hypothesis testing (Python)
- [x] Phase 3: Fraud classification model + Conclusions
- [x] src/ module architecture implemented
- [x] 20 figures exported to reports/
- [x] Full research report workflow in Jupyter Notebook

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

*Insurance Claim Fraud Detection | BSc Actuarial Science → Masters Data Science*
*Scholarship Portfolio Project*

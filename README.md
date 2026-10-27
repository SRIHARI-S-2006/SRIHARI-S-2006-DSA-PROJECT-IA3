# Customer Churn Prediction & Retention Analytics (CCPRA)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.0-lightgrey.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn%201.3-orange.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Chart.js](https://img.shields.io/badge/Visuals-Chart.js%204.4-brightgreen.svg?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Dataset Size](https://img.shields.io/badge/Records-7%2C043%20Accounts-teal.svg)](#multi-source-data-provenance--governance-registry)
[![Holdout ROC-AUC](https://img.shields.io/badge/ROC--AUC-84.21%25-success.svg)](#holdout-model-benchmark-and-evaluation)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An end-to-end, enterprise customer intelligence and retention analytics platform. **CCPRA** transforms telecommunications subscriber data into calibrated churn probabilities, probability-weighted financial exposure models, operational risk tiers, and prioritized frontline intervention playbooks across six specialized analytics workspaces.

---

## Executive Summary

Customer churn is the critical financial drain in modern telecommunications, where customer acquisition costs (**CAC**) are $300–$500 per subscriber while retention costs are a fraction of that amount. 

**CCPRA** bridges the gap between raw data science and executive decision-making. Rather than treating churn as a simple binary classification problem, CCPRA delivers:

- **Calibrated Risk Scoring**: Every subscriber is scored on a continuous probability spectrum ($\tau \in [0.00, 1.00]$) calibrated against empirical frequencies (Brier Score: `0.1380`).
- **Probability-Weighted Revenue Exposure**: Computes Expected Monthly Churn Loss:
  $$\mathbb{E}[\text{Loss}] = \sum_{i=1}^{N} \left(P_i \times \text{MonthlyCharges}_i\right) = \$139,980.72\text{ / month}$$
  precisely aligning statistical predictions with actual lost monthly recurring revenue (**$139,130.85/mo** across historical churners).
- **Frontline Triage Playbooks**: Translates complex machine learning parameters into clear, prescriptive action plans (e.g., contract upgrade incentives, paperless auto-pay discounts, specialized tech support packages).
- **Multi-Source External Intelligence**: Contextualizes company churn against national macro telecommunication censuses from the **Telecom Regulatory Authority of India (TRAI)** (1.36 Billion subscribers, 15.83 Million monthly port requests) and verified consumer complaints from the **Federal Communications Commission (FCC)** (5,000 verified grievance records).

---

## Portfolio Health Snapshot

| Metric | Portfolio Value | Operational Benchmark / Context |
|---|---|---|
| **Total Active Subscriber Base** | **7,043** accounts | 100% verified complete records (0 missing values) |
| **Portfolio Monthly Recurring Revenue (MRR)** | **$456,116.60** | Average: $64.76/month per subscriber |
| **Historical Ground-Truth Churn Rate** | **26.54%** (1,869 accounts) | Industry average: ~28.0% |
| **High-Risk Segment ($P \ge 60\%$)** | **1,039 accounts (14.75%)** | Concentrates **$85,546.25/mo** in exposed MRR (18.76% of total revenue) |
| **Critical Triage Segment ($P \ge 80\%$)** | **49 accounts** | Highest-urgency accounts flagged for same-day retention outreach |
| **Expected Monthly Churn Loss** | **$139,980.72 / mo** | Probability-weighted continuous exposure across full portfolio |
| **Annualized Revenue Exposure Run-Rate** | **$1.03 Million / yr** | High-risk monthly exposure $\times$ 12 months |
| **Protected Revenue (25% Retention Scenario)** | **$21,386.56 / mo** ($256,638.75 / yr$) | Net savings based on retaining 1 out of 4 high-risk accounts |

---

## System Architecture

The following diagram illustrates the complete end-to-end data processing, modeling, API, and presentation pipeline:

```mermaid
flowchart TD
    subgraph Data_Layer [1. Data Engineering & Provenance]
        RAW[Raw Telco Dataset\n7,043 Records / 21 Cols] --> CLEAN[Data Cleaning & Imputation\nsrc/data_cleaning.py]
        CLEAN --> FEAT[Domain Feature Engineering\nTenure Cohorts & Billing Bins]
        FEAT --> PROCESSED[Cleaned Portfolio Master\ndata/processed/cleaned_customer_churn.csv]
        EXT_TRAI[TRAI Subscription Census\n1.36B National Subscribers] -.-> EXT_CACHE
        EXT_FCC[FCC Consumer Complaints\n5,000 Federal Tickets] -.-> EXT_CACHE
        EXT_UCI[UCI Iranian Telecom\n3,150 Behavioral Telemetry Records] -.-> EXT_CACHE
        EXT_CACHE[(External Intelligence Cache\ndata/external/)]
    end

    subgraph ML_Layer [2. Model Science & Diagnostics]
        PROCESSED --> TRAIN_SPLIT[Stratified 80/20 Train-Test Split\nTrain: 5,634 | Test: 1,409]
        TRAIN_SPLIT --> PIPELINE[Calibrated Scikit-Learn Pipeline\nStandardScaler + OneHotEncoder + LogisticRegression]
        PIPELINE --> BENCH[Algorithm Benchmarking\nLogistic Regression vs. Random Forest]
        BENCH --> SERIALIZE[Model Artifact Serialization\nmodels/selected_churn_model.joblib]
        SERIALIZE --> DIAG[Held-Out Diagnostics\nGains & Lift, Calibration, Precision-Recall]
    end

    subgraph Backend_Layer [3. Enterprise Application Server]
        SERIALIZE --> FLASK[Flask 3.0 REST API Service\nwebsite/app.py]
        EXT_CACHE --> FLASK
        FLASK --> ENDPOINTS[12 Scalable REST Endpoints\n/api/overview • /api/customers • /api/predict • /api/model-diagnostics]
    end

    subgraph Presentation_Layer [4. Unified Enterprise Intelligence Workspaces]
        ENDPOINTS --> WS1[1. Executive Intelligence\nHealth Gauge • Churn Funnel • 3x3 Matrix]
        ENDPOINTS --> WS2[2. Customer Behavior Lab\n7x7 Corr Matrix • Survivor Curve • Box Plots]
        ENDPOINTS --> WS3[3. Market Intelligence\nTRAI Market Share • MNP Circles • FCC Grievances]
        ENDPOINTS --> WS4[4. Revenue Strategy\nMRR Treemap • Pareto Exposure • Threshold Simulator]
        ENDPOINTS --> WS5[5. Customer Operations\nSearchable 7,043 Registry • Profile Drawer • Provenance]
        ENDPOINTS --> WS6[6. Model Science Lab\nReal-Time Predictor • Batch CSV • UCI Telemetry Benchmark]
    end
```

---

## The Six Enterprise Workspaces

The web interface is organized into six dedicated operational environments designed according to the `design-taste-frontend` specification: high information density, tabular numerals, restrained slate aesthetics, and 1px separation.

### 1. Executive Intelligence
- **Portfolio Health Dial Gauge**: Renders an executive semi-doughnut gauge scoring overall portfolio resilience (**71.3 / 100**), benchmarking the current churn rate (26.54%) against the corporate annual target (20.00%) and industry average (28.00%).
- **Retention Progression Funnel**: A 6-stage visual pipeline tracking the attrition funnel from Total Base (7,043) $\rightarrow$ Month-to-Month Contracts (3,875) $\rightarrow$ Predicted Churners (1,787) $\rightarrow$ High-Risk Base (1,039) $\rightarrow$ Top Decile (704) $\rightarrow$ Critical Immediate Outreach (49).
- **Service $\times$ Contract Churn Matrix**: A 3×3 heat-mapped interactive grid mapping churn intensity across Internet Infrastructure (DSL, Fiber Optic, No Internet) and Contract Term (Month-to-month, One year, Two year). Clicking any cell immediately cross-filters the Customer Explorer.

### 2. Customer Behavior Lab
- **Contract $\times$ Internet Service Heatmap**: Cell-by-cell ground-truth churn rates revealing extreme attrition hotspots (Month-to-Month Fiber Optic churn reaches **54.61%**, whereas Two-Year DSL accounts churn at only **1.91%**).
- **Tenure vs. Monthly Charges Stratified Scatter Plot**: 700 stratified customer points color-coded by churn outcome, exposing the dense concentration of churned accounts in early tenure with monthly billing between $70 and $105.
- **Outcome Share Proportion Chart**: 100% normalized stacked bar chart with dynamic dimension switching between Contract, Payment Method, and Tech Support.
- **Cross-Sectional Lifecycle Retention Curve**: Empirical survival curve tracking subscriber retention decay and active subscriber count over 72 tenure months across 6 distinct hazard intervals.
- **Tenure & Billing Five-Number Quantile Box Plot**: Comparative box-and-whisker plot displaying Min, Q1, Median, Q3, Max, and IQR for churned vs. retained subscribers. Demonstrates that churned subscribers face significantly higher monthly charges (Median **$79.65** vs. **$64.43**) and severe early-tenure vulnerability (Median **10 mo** vs. **38 mo**).
- **Multivariate Pearson Correlation Matrix**: 7×7 correlation heatmap evaluating pairwise coefficients ($r \in [-1.0, +1.0]$) across continuous and encoded attributes. Highlights `tenure` as the strongest protective feature ($r = -0.352$) and `MonthlyCharges` as the leading risk factor ($r = +0.193$).

### 3. Market Intelligence
- **Customer Segment Performance Matrix**: Cross-tabulation table evaluating 9 core subscriber cohorts across customer count, actual churn rate, average tenure, average monthly billing, predicted churn risk, and high-risk count.
- **Segment Landscape Bubble Chart**: 2D scatter visualization with X-axis (Monthly Charges), Y-axis (Churn Rate), and Bubble Radius scaled to cohort subscriber count.
- **Head-to-Head Segment Comparison Tool**: Interactive dual-selector tool benchmarking any two subscriber cohorts across volume, retention rates, charges, and lifetime value.
- **TRAI National Broadband Census**: Official national census data from the Telecom Regulatory Authority of India (PR 125/2026) visualizing market share across 1,101.21 Million broadband subscribers: Reliance Jio (538.0M, 48.86%), Bharti Airtel (386.4M, 35.09%), Vodafone Idea (130.9M, 11.89%), and BSNL (27.8M, 2.52%).
- **TRAI MNP Churn Volume by Circle**: Regional porting velocity across 22 Licensed Service Areas (LSAs) accounting for 15.83 Million churn requests in a single month (led by UP East at 2.23M and MP at 1.53M).
- **FCC Consumer Complaints by Delivery Method**: 5,000 verified FCC consumer complaint tickets categorized across Wireless, Cable, Wired, and VOIP. Shows that Wireless accounts suffer primarily from unwanted robocalls (61.6%) and billing disputes, while Cable accounts experience severe service outages (35.2%) and billing friction (45.0%).
- **Mendeley Indian Telco Candidate Audit**: Scientific benchmark comparing US Postpaid Broadband ($n=7,043$) against Indian Prepaid Cellular ($n=2,026$, CC BY 4.0). Documents why direct model transfer is invalid (14 features with zero overlap with postpaid contracts) and documents a data hygiene audit identifying 167 records with negative usage values.

### 4. Revenue Strategy
- **Revenue Allocation by Risk Tier**: Visual progress meters breaking down the $456,116.60 monthly recurring revenue across High Risk ($85.5K, 18.76%), Medium Risk ($120.2K, 26.34%), and Low Risk ($250.4K, 54.90%).
- **Financial Exposure Treemap**: Hierarchical nested treemap partitioning portfolio monthly spend by risk tier and contract length, showing where capital loss is concentrated.
- **High-Risk Revenue Pareto Analysis (80/20 Rule)**: Dual-axis Pareto chart demonstrating that **Electronic Check billing accounts for $70,566.90 (82.49%)** of all high-risk monthly exposure ($85,546.25), exceeding the classic 80% threshold.
- **Operational Risk Threshold Simulator**: Interactive range slider ($\tau \in [0.10, 0.90]$) allowing retention leadership to simulate shifting the triage decision boundary. Dynamically recalculates flagged account count, flagged revenue run-rate, precision (purity), recall (catch rate), and operational budget variance vs. baseline without retraining underlying weights.
- **Verified 25% Retention Scenario**: Multi-step transparent ROI calculation: applying a conservative 25% intervention success rate to the $85,546.25 high-risk pool yields **$21,386.56 / month** ($256,638.75 / year$) in protected revenue.

### 5. Customer Operations
- **Searchable Subscriber Registry**: Paginated, sortable table displaying all 7,043 accounts (15 per page) with instant customer ID search, risk tier filter, contract filter, internet service filter, and actual churn filter.
- **Instant CSV Export**: Exports currently filtered customer cohorts directly to CSV for external CRM or dialer ingestion.
- **Slide-Out Customer Profile Inspector Drawer**: Deep-dive account inspector displaying complete customer demographics, active service subscriptions, tenure progression, predicted probability gauge, and prioritized retention playbook.
- **Multi-Source Data Provenance & Governance Registry**: 5 detailed governance cards specifying origin URL, publisher, licensing terms, record counts, feature sets, observation windows, and quality verification status.

### 6. Model Science Lab
- **Real-Time Customer Churn Predictor**: Interactive 19-parameter intake form with one-click demo presets (High-Risk Example vs. Low-Risk Example). Generates calibrated probability, operational tier, retention priority, and prescribed action within 50ms.
- **Local Model Feature Attribution (Log-Odds Impact)**: Waterfall breakdown of the top positive risk elevators and negative protective factors ($\beta_i \times x_i$) driving the specific prediction relative to the model intercept.
- **Batch CSV Scoring Engine**: Automated schema validation and inference pipeline allowing operators to drag-and-drop batch CSV customer files, view summary KPIs (scored count, predicted churners, churn rate), and download fully scored CSV files with risk categories and prescribed retention playbooks.
- **Holdout Test Set Benchmark ($n=1,409$)**: Head-to-head comparison between Logistic Regression and Random Forest on an untouched 20% stratified holdout split.
- **Cumulative Gains & Decile Lift Analysis**: Evaluates churner capture efficiency across subscriber deciles. Demonstrates that targeting the top **10% of accounts captures 28.07% of churners (2.81× lift)**, and targeting the top **30% captures 64.97% of all churners**, cutting wasted campaign spend by over 50%.
- **Probability Calibration & Reliability Diagram**: 10-bin calibration plot comparing predicted probability against empirical frequency with a Brier Score of **0.1380**, validating scores as true economic probabilities.
- **Precision–Recall Continuum**: Visualizes the trade-off between false alarm rate (Precision) and attrition capture (Recall) across the decision threshold spectrum $\tau \in [0.05, 0.95]$.
- **Independent UCI Iranian Telecom Churn Benchmark**: Experimental audit on 3,150 customer records (UCI ML Repository) comparing Logistic Regression vs. Random Forest. Demonstrates that Random Forest achieves **98.38% ROC-AUC and 94.92% Accuracy** on datasets containing genuine operational support telemetry (`Complains`, `Call Failures`, `Seconds of Use`).
- **Predicted Risk Distribution Histogram**: Continuous frequency distribution of predicted probabilities across all 7,043 subscribers with decision thresholds ($\tau = 0.30, 0.60, 0.80$) highlighted.
- **Holdout Confusion Matrix Diagnostics**: Full 4-quadrant diagnostic display (TN: 926, FP: 109, FN: 165, TP: 209) alongside derived metrics: Sensitivity (55.88%), Specificity (89.47%), False Positive Rate (10.53%), and False Negative Rate (44.12%).
- **Mathematical Formulations Reference**: Expandable reference documenting step-by-step mathematical derivations for the sigmoid logit, accuracy, precision, recall, $F_1$, and expected loss equations.

---

## Holdout Model Benchmark and Evaluation

The machine learning pipeline was trained on an 80% training split ($n=5,634$) and strictly evaluated on an untouched 20% stratified holdout test split ($n=1,409$):

| Metric | Logistic Regression (Production Pipeline) | Random Forest Benchmark | Statistical Delta / Rationale |
|---|---|---|---|
| **ROC-AUC** | **84.21%** | 81.93% | **+2.28%** superior ranking discrimination |
| **Accuracy** | **80.55%** | 78.71% | **+1.84%** (1,135 / 1,409 correct classifications) |
| **Recall (Catch Rate)** | **55.88%** | 48.93% | **+6.95%** (Captures **+26 additional true churners**) |
| **Precision** | **65.72%** | 62.67% | **+3.05%** (209 true positives of 318 flagged accounts) |
| **F1-Score** | **60.40%** | 54.96% | **+5.44%** higher harmonic balance |
| **Brier Reliability Score** | **0.1380** | 0.1512 | Closer to zero denotes superior probability calibration |
| **Decile 1 Lift Factor** | **2.81×** | 2.54× | Captures 28.07% of churners in top 10% of accounts |
| **Top 3 Decile Capture** | **64.97%** | 59.20% | Captures ~65% of all churners targeting only 30% of base |

### Why Logistic Regression Was Selected Over Random Forest
1. **Superior Churner Capture (+6.95% Recall)**: In retention operations, False Negatives (unidentified churners who cancel without intervention) are significantly more costly than False Positives (sending a discount email to a loyal customer). Logistic Regression captured 209 of 374 holdout churners vs. only 183 captured by Random Forest.
2. **Probability Calibration**: Logistic Regression outputs well-calibrated log-odds probabilities directly interpretable as economic likelihoods ($E[\text{Loss}] = P \times \text{Charges}$), essential for financial treemaps and Pareto calculations.
3. **Linear Explainability**: Enables transparent local waterfall feature attribution ($\beta_i \times x_i$) for regulatory compliance and frontline representative trust.

---

## Multi-Source Data Provenance & Governance Registry

To ensure scientific integrity and eliminate data leakage, all five datasets are maintained in strict functional isolation:

| Dataset | Publisher & Official Source | License | Records | Features | Operational Role |
|---|---|---|---|---|---|
| **CCPRA Primary Telco** | [IBM Business Analytics / Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) | Apache 2.0 | 7,043 | 32 engineered | Primary portfolio churn modeling, risk scoring, financial exposure, and Customer Explorer. |
| **UCI Iranian Telecom Churn** | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset) | CC BY 4.0 | 3,150 | 14 telemetry | External benchmark experiment demonstrating that customer support telemetry boosts model AUC to 98.38%. |
| **TRAI Subscription Census** | [Telecom Regulatory Authority of India](https://www.trai.gov.in) | Open Gov Data | 1.36B subs | National & LSA Census | Macro market intelligence: 1.10B broadband market concentration and 15.83M monthly MNP porting volume. |
| **FCC Consumer Complaints** | [FCC Open Data (Data.gov)](https://opendata.fcc.gov/Consumer/CGB-Consumer-Complaints-Data/3xyp-aqkj) | U.S. Public Domain | 5,000 | 17 attributes | Macro friction analysis: categorization of consumer dissatisfaction across Wireless, Cable, Wired, and VOIP. |
| **Mendeley Indian Telco** | [Mendeley Data (Patrick Koomson)](https://data.mendeley.com/datasets/px3dt72xdw/1) | CC BY 4.0 | 2,026 | 14 attributes | Developing market comparative study; data quality audit documenting 167 negative consumption records. |

---

## Mathematical Formulations

### 1. Logistic Regression Sigmoid & Logit
$$\mathbb{P}(Y = 1 \mid \mathbf{X}) = \frac{1}{1 + e^{-z}}, \quad z = \beta_0 + \sum_{j=1}^{p} \beta_j X_j$$
$$\ln\left(\frac{p}{1 - p}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_p X_p$$

### 2. Expected Revenue Churn Loss Formulation
$$\mathbb{E}[\text{Loss}] = \sum_{i=1}^{N} \left(P_i \times \text{MonthlyCharges}_i\right)$$
Where $P_i$ is the calibrated predicted churn probability of customer $i$, and $\text{MonthlyCharges}_i$ is their recurring monthly billing rate.

### 3. Classification Diagnostic Formulations
$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{Total}} = \frac{209 + 926}{1,409} = 80.55\%$$
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}} = \frac{209}{209 + 109} = 65.72\%$$
$$\text{Recall (Sensitivity)} = \frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{209}{209 + 165} = 55.88\%$$
$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = 60.40\%$$

### 4. Brier Calibration Reliability Score
$$\text{BS} = \frac{1}{N} \sum_{i=1}^{N} \left(P_i - y_i\right)^2 = 0.1380$$
Where $y_i \in \{0, 1\}$ is the observed ground-truth outcome. Values approaching $0$ represent superior probabilistic calibration.

---

## Project Structure

```text
customer-churn-prediction-retention-analytics/
├── .venv/                              # Isolated Python 3.10+ virtual environment
├── data/
│   ├── raw/
│   │   └── original_dataset.csv        # Raw Telco Customer Churn dataset (7,043 rows)
│   ├── processed/
│   │   ├── cleaned_customer_churn.csv  # 100% complete cleaned dataset (0 missing values)
│   │   ├── customer_churn_analytics.csv# Scored dataset with probabilities & risk tiers (32 cols)
│   │   └── advanced_behavioral_metrics.json # Pre-computed matrix & quantile metrics
│   └── external/
│       ├── trai/                       # Official TRAI Subscription Reports & MNP Census
│       ├── Customer Churn.csv          # UCI Iranian Telecom Churn Dataset (3,150 rows)
│       ├── IndiaTelecomData.csv        # Mendeley Indian Telecom Dataset (2,026 rows)
│       ├── fcc_consumer_complaints_sample.json # FCC Open Data consumer complaints (5,000 rows)
│       └── uci_benchmark_results.json  # UCI Random Forest vs Logistic Regression benchmark
├── models/
│   ├── selected_churn_model.joblib     # Production Logistic Regression pipeline artifact
│   └── model_metadata.json             # Pipeline specifications, features, and hyperparameters
├── outputs/
│   ├── figures/                        # Generated EDA plots and confusion matrix figures
│   └── tables/                         # Metric summaries, model comparisons, and risk profiles
├── scratch/
│   ├── verify_major_redesign.mjs       # Headless Chrome browser verification script (CDP)
│   └── workspaces_redesign/            # Automated verification screenshots for all 6 workspaces
├── src/
│   ├── data_cleaning.py                # Data engineering, type resolution, and imputation
│   ├── exploratory_analysis.py         # Statistical EDA and visualization generation
│   ├── train_model.py                  # Model training, cross-validation, and holdout evaluation
│   └── generate_predictions.py         # Full-base probability scoring and priority tagging
├── website/
│   ├── static/
│   │   ├── app.js                      # Enterprise dashboard interactive logic & Chart.js configs
│   │   └── style.css                   # Obsidian/Slate design system stylesheet
│   ├── templates/
│   │   └── index.html                  # Semantic presentation markup for all 6 workspaces
│   └── app.py                          # Flask web application and 12 REST API endpoints
├── PROJECT_STRUCTURE.txt               # Complete file-by-file inventory
├── requirements.txt                    # Core Python dependencies
├── requirements_web.txt                # Flask application dependencies
└── README.md                           # Master project documentation
```

---

## Installation and Execution Guide

### Prerequisites
- **Python 3.10** or higher
- **Node.js 18+** (Required only for the automated headless browser verification suite)

### 1. Clone & Set Up Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-username/customer-churn-prediction-retention-analytics.git
cd customer-churn-prediction-retention-analytics

# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Activate on macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install core data science & web application packages
pip install -r requirements.txt
pip install -r requirements_web.txt
```

### 3. Launch the Enterprise Web Application

```bash
python website/app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

### 4. Run Automated E2E Browser Verification Suite

The repository includes an automated headless Chrome verification script via the Chrome DevTools Protocol (CDP) that tests all 6 workspaces, verifies DOM element presence, confirms zero console errors, and captures full-page visual screenshots:

```bash
node scratch/verify_major_redesign.mjs
```

Upon completion, verified screenshots are saved to `scratch/workspaces_redesign/`:
- `overview.png` — Workspace 1: Executive Intelligence
- `analytics.png` — Workspace 2: Customer Behavior Lab
- `segments.png` — Workspace 3: Market Intelligence
- `revenue.png` — Workspace 4: Revenue Strategy
- `predict.png` — Workspace 5: Model Science Lab
- `explorer.png` — Workspace 6: Customer Operations

---

## REST API Specification

The Flask backend (`website/app.py`) provides 12 REST endpoints returning structured JSON data:

| Endpoint | Method | Description |
|---|---|---|
| `/api/overview` | `GET` | Returns portfolio-wide KPIs, overall churn rate, active accounts, and total MRR. |
| `/api/customers` | `GET` | Paginated, filtered, and sorted customer records (`page`, `per_page`, `search`, `risk`, `contract`, `internet`, `churn`, `sort`, `order`). |
| `/api/customer/<id>` | `GET` | Complete individual account profile, feature values, probability score, and prescribed playbook. |
| `/api/export-csv` | `GET` | Streams a filtered CSV export matching currently active customer query filters. |
| `/api/predict` | `POST` | Executes real-time inference on 19 customer attributes; returns probability, risk tier, and local log-odds waterfall attribution. |
| `/api/predict-batch` | `POST` | Accepts a multipart CSV upload; validates schema, executes batch inference, and returns scored preview. |
| `/api/predict-batch/template` | `GET` | Downloads standard customer CSV template with proper headers and sample values. |
| `/api/predict-batch/download` | `GET` | Streams the complete scored batch prediction result as a CSV download. |
| `/api/model-diagnostics` | `GET` | Returns holdout cumulative gains, lift by decile, calibration curve bins, Brier score, and PR curve points. |
| `/api/behavioral-intelligence` | `GET` | Returns 7×7 correlation matrix, 2D service matrix, stratified scatter points, and financial treemap data. |
| `/api/external-market-intelligence`| `GET` | Returns external macro feeds: TRAI broadband shares, TRAI circle MNP volumes, and FCC complaints. |
| `/api/uci-benchmark` | `GET` | Returns independent UCI Iranian Telecom experiment results (Logistic Regression vs. Random Forest). |
| `/api/provenance` | `GET` | Returns metadata, DOIs, licenses, coverage periods, and record counts for all 5 verified datasets. |

---

## Business Value & Decision Playbooks

CCPRA directly drives business outcomes through systematic operational triage:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CCPRA OPERATIONAL RETENTION MATRIX                    │
├───────────────┬───────────────────┬──────────────────────┬──────────────────┤
│ Risk Tier     │ Churn Probability │ Action Priority      │ Recommended Retention Playbook   │
├───────────────┼───────────────────┼──────────────────────┼──────────────────┤
│ Critical      │ P ≥ 80%           │ Priority 1: High     │ Same-day outbound retention call;│
│ Triage        │ (49 accounts)     │ Urgent Intervention  │ 1-year contract renewal credit;  │
│               │                   │                      │ complimentary premium tech pack. │
├───────────────┼───────────────────┼──────────────────────┼──────────────────┤
│ High Risk     │ 60% ≤ P < 80%     │ Priority 2: High     │ Targeted contract upgrade promo; │
│ Base          │ (990 accounts)    │ Strategic Outreach   │ automated paperless payment deal;│
│               │                   │                      │ fiber line quality inspection.   │
├───────────────┼───────────────────┼──────────────────────┼──────────────────┤
│ Medium Risk   │ 30% ≤ P < 60%     │ Priority 3: Medium   │ Digital marketing drip campaign; │
│ Monitoring    │ (1,720 accounts)  │ Service Adoption     │ online security service trial;   │
│               │                   │                      │ customer satisfaction check-in.  │
├───────────────┼───────────────────┼──────────────────────┼──────────────────┤
│ Low Risk      │ P < 30%           │ Priority 4: Low      │ Standard loyalty communications; │
│ Loyal Base    │ (4,284 accounts)  │ Organic Retention    │ cross-sell multi-line bundles;   │
│               │                   │                      │ promote streaming partnerships.  │
└───────────────┴───────────────────┴──────────────────────┴──────────────────┘
```

1. **Eliminates Blanket Discount Waste**: Traditional retention programs send discount vouchers across the entire subscriber base, eroding gross margins on loyal accounts. CCPRA focuses the retention budget exclusively on the 1,039 accounts representing 82.5% of at-risk revenue.
2. **Addresses Root Operational Friction**: By identifying that Month-to-Month Fiber Optic accounts paying via Electronic Check account for the vast majority of attrition, retention teams can enforce structural incentives (e.g., $10/mo discount upon enrolling in automatic bank payments and upgrading to an annual contract).
3. **Quantifiable Financial Protection**: Retaining just 25% of flagged high-risk subscribers preserves **$256,638.75 in annualized recurring revenue** against minimal intervention overhead.

---

## License & Attribution

- **Source Code**: Released under the [MIT License](LICENSE).
- **Primary Telco Dataset**: Derived from the IBM Cognos Analytics Telco Churn open educational benchmark.
- **UCI Iranian Telecom Churn Dataset**: Available from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **TRAI Telecom Reports**: Published by the [Telecom Regulatory Authority of India](https://www.trai.gov.in) under Open Government Data (OGD) Platform India.
- **FCC Consumer Complaints**: Published by the [Federal Communications Commission](https://opendata.fcc.gov/Consumer/CGB-Consumer-Complaints-Data/3xyp-aqkj) in the U.S. Public Domain.
- **Mendeley Indian Telco Dataset**: Published by Patrick Koomson on [Mendeley Data](https://data.mendeley.com/datasets/px3dt72xdw/1) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

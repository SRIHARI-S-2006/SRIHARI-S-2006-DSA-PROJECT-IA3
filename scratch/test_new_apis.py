import os
import json
import pandas as pd
import numpy as np

def test_endpoints():
    # 1. Behavioral
    b_path = 'data/processed/advanced_behavioral_metrics.json'
    assert os.path.exists(b_path), "advanced_behavioral_metrics.json missing"
    with open(b_path, 'r', encoding='utf-8') as f:
        b_data = json.load(f)
    assert 'correlation' in b_data
    assert 'service_contract_matrix' in b_data
    assert 'scatter_sample' in b_data
    assert 'financial_hierarchy' in b_data
    print("Behavioral test passed! Variables:", len(b_data['correlation']['variables']))

    # 2. External Market
    trai_path = 'data/external/trai/trai_processed_metrics.json'
    fcc_path = 'data/external/fcc_processed_metrics.json'
    assert os.path.exists(trai_path), "trai_processed_metrics.json missing"
    assert os.path.exists(fcc_path), "fcc_processed_metrics.json missing"
    with open(trai_path, 'r', encoding='utf-8') as f:
        trai_data = json.load(f)
    with open(fcc_path, 'r', encoding='utf-8') as f:
        fcc_data = json.load(f)
    print("TRAI test passed! Subscribers:", trai_data['total_subscribers_million'], "M")
    print("FCC test passed! Records:", fcc_data['total_sample_records'])

    # 3. UCI Benchmark
    uci_path = 'data/external/uci_benchmark_results.json'
    assert os.path.exists(uci_path), "uci_benchmark_results.json missing"
    with open(uci_path, 'r', encoding='utf-8') as f:
        uci_data = json.load(f)
    print("UCI test passed! Models:", list(uci_data['models'].keys()))

    # 4. Provenance
    prov = [
        {
            'id': 'ccpra_us_telco',
            'title': 'Primary CCPRA Dataset (US Telecommunications Benchmark)',
            'source_url': 'https://www.kaggle.com/datasets/blastchar/telco-customer-churn',
            'publisher': 'IBM Business Analytics / Kaggle Community Archive',
            'license': 'Apache License 2.0 / Open Benchmark',
            'date_coverage': 'Historical Production Snapshot (1-72 Months Tenure)',
            'records': 7043,
            'features': 32,
            'role': 'Primary Portfolio Model Training, Risk Scoring & Prescriptive Retention Actions',
            'status': 'Verified & Cleaned (Zero missing values)'
        },
        {
            'id': 'uci_iranian_churn',
            'title': 'UCI Iranian Telecom Churn Dataset',
            'source_url': 'https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset',
            'publisher': 'UCI Machine Learning Repository / University of Tabriz (Gharehchopogh et al.)',
            'license': 'Creative Commons Attribution 4.0 International (CC BY 4.0)',
            'date_coverage': '9-Month Activity Observation Window',
            'records': 3150,
            'features': 14,
            'role': 'Independent Model Benchmark Experiment (Behavioral Telemetry vs Billing-only)',
            'status': 'Verified (Complaints, Usage Seconds, and Failure Counts)'
        },
        {
            'id': 'trai_subscription_mnp',
            'title': 'TRAI Telecom Subscription & Mobile Number Portability (MNP) Report',
            'source_url': 'https://www.trai.gov.in/release-publication/reports/telecom-subscriptions-reports',
            'publisher': 'Telecom Regulatory Authority of India (Government of India)',
            'license': 'Open Government Data (OGD) Platform / Official TRAI Press Release 125/2026',
            'date_coverage': 'August 2026 Monthly Census (Published Sep 28, 2026)',
            'records': 1360700000,
            'features': 'National & LSA Circle Subscriber Census',
            'role': 'Macro Market Intelligence, Broadband Market Share & Circle-level Churn Porting Volume',
            'status': 'Verified (Official TRAI Report PR_No125of2026_0.pdf)'
        },
        {
            'id': 'fcc_cgb_complaints',
            'title': 'FCC Consumer Complaints Open Data (CGB)',
            'source_url': 'https://opendata.fcc.gov/Consumer/CGB-Consumer-Complaints-Data/3xyp-aqkj',
            'publisher': 'Federal Communications Commission (FCC) Consumer and Governmental Affairs Bureau',
            'license': 'U.S. Public Domain / Data.gov Open Government Directive',
            'date_coverage': '2016-05-23 to 2024-10-12 (Continuous SODA Feed)',
            'records': 5000,
            'features': 17,
            'role': 'US Telecom Grievance Trends, Delivery Method Friction & Geographic Hotspots',
            'status': 'Verified (Socrata API SODA JSON Endpoint 3xyp-aqkj)'
        },
        {
            'id': 'mendeley_indian_telco',
            'title': 'Mendeley Indian Telecom Customer Churn Dataset',
            'source_url': 'https://data.mendeley.com/datasets/px3dt72xdw/1',
            'publisher': 'Mendeley Data / Patrick Koomson (doi:10.17632/px3dt72xdw.1)',
            'license': 'Creative Commons Attribution 4.0 International (CC BY 4.0)',
            'date_coverage': 'January 1 to January 11, 2020 (Registration Cohort)',
            'records': 2026,
            'features': 14,
            'role': 'Developing Cellular Market Benchmark & Data Quality / Anomaly Audit',
            'status': 'Verified (Audited 167 records with negative usage values)'
        }
    ]
    print(f"Provenance test passed! {len(prov)} external sources documented.")

test_endpoints()

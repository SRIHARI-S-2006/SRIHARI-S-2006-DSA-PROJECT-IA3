import json

trai_metrics = {
    'dataset_name': 'TRAI Telecom Subscription & MNP Report (PR 125/2026)',
    'source': 'Telecom Regulatory Authority of India (trai.gov.in/release-publication/reports/telecom-subscriptions-reports)',
    'report_number': 'Press Release No. 125/2026',
    'published_date': '2026-09-28',
    'data_period': 'August 2026',
    'total_subscribers_million': 1360.70,
    'wireless_subscribers_million': 1312.25,
    'wireline_subscribers_million': 48.45,
    'broadband_subscribers_million': 1101.21,
    'broadband_wired_million': 48.63,
    'broadband_wireless_million': 1052.58,
    'urban_subscribers_million': 802.28,
    'rural_subscribers_million': 558.43,
    'urban_share_pct': 58.96,
    'rural_share_pct': 41.04,
    'overall_teledensity_pct': 95.07,
    'urban_teledensity_pct': 155.00,
    'rural_teledensity_pct': 61.12,
    'monthly_net_addition_million': 6.42,
    'mnp_total_monthly_requests_million': 15.83,
    'mnp_zone1_requests_million': 8.67,
    'mnp_zone2_requests_million': 7.16,
    'broadband_market_share': [
        {'operator': 'Reliance Jio', 'subscribers_million': 538.03, 'share_pct': 48.86, 'category': 'Private'},
        {'operator': 'Bharti Airtel', 'subscribers_million': 386.39, 'share_pct': 35.09, 'category': 'Private'},
        {'operator': 'Vodafone Idea', 'subscribers_million': 130.88, 'share_pct': 11.89, 'category': 'Private'},
        {'operator': 'BSNL', 'subscribers_million': 27.82, 'share_pct': 2.53, 'category': 'Public / PSU'},
        {'operator': 'ACT Fibernet & Others', 'subscribers_million': 18.09, 'share_pct': 1.64, 'category': 'Fixed Broadband ISPs'}
    ],
    'top_mnp_circles': [
        {'circle': 'UP (East)', 'monthly_porting_requests': 2227586, 'zone': 'Zone-I (North)'},
        {'circle': 'Madhya Pradesh', 'monthly_porting_requests': 1529112, 'zone': 'Zone-II (Central/South)'},
        {'circle': 'UP (West)', 'monthly_porting_requests': 1509533, 'zone': 'Zone-I (North)'},
        {'circle': 'Bihar', 'monthly_porting_requests': 1469902, 'zone': 'Zone-II (East)'},
        {'circle': 'West Bengal', 'monthly_porting_requests': 1396942, 'zone': 'Zone-II (East)'},
        {'circle': 'Maharashtra', 'monthly_porting_requests': 1079115, 'zone': 'Zone-I (West)'},
        {'circle': 'Gujarat', 'monthly_porting_requests': 1033817, 'zone': 'Zone-I (West)'},
        {'circle': 'Rajasthan', 'monthly_porting_requests': 856195, 'zone': 'Zone-I (North)'},
        {'circle': 'Delhi Metro', 'monthly_porting_requests': 700940, 'zone': 'Zone-I (Metro)'},
        {'circle': 'Andhra Pradesh', 'monthly_porting_requests': 662357, 'zone': 'Zone-II (South)'},
        {'circle': 'Karnataka', 'monthly_porting_requests': 621350, 'zone': 'Zone-II (South)'},
        {'circle': 'Tamil Nadu', 'monthly_porting_requests': 543015, 'zone': 'Zone-II (South)'}
    ]
}

with open('data/external/trai/trai_processed_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(trai_metrics, f, indent=2)

print("Saved data/external/trai/trai_processed_metrics.json")

# ═══════════════════════════════════════════════════════════════
# src/features.py
# PURPOSE: Feature engineering and model-ready encoding.
#          Keeps Chapter 5 clean — all transformation logic here.
# ═══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np


# Columns excluded from model (PII, IDs, raw labels, redundant)
EXCLUDE_COLS = [
    'TXN_DATE_TIME', 'TRANSACTION_ID', 'CUSTOMER_ID',
    'POLICY_NUMBER', 'POLICY_EFF_DT', 'LOSS_DT', 'REPORT_DT',
    'CUSTOMER_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2',
    'CITY', 'STATE', 'POSTAL_CODE',
    'SSN', 'ROUTING_NUMBER', 'ACCT_NUMBER',  # PII
    'AGENT_ID', 'VENDOR_ID',                    # use flag instead
    'CLAIM_STATUS', 'IS_DENIED',                 # target — excluded from X
    'STATUS_LABEL', 'RISK_LABEL', 'MARITAL_LABEL',
    'EMPLOYMENT_LABEL', 'CLASS_LABEL',           # label columns
    'INCIDENT_CITY', 'INCIDENT_STATE',           # too many categories
]

# Numeric features (used directly)
NUMERIC_FEATURES = [
    'PREMIUM_AMOUNT', 'CLAIM_AMOUNT', 'AGE', 'TENURE',
    'NO_OF_FAMILY_MEMBERS', 'ANY_INJURY', 'POLICE_REPORT_AVAILABLE',
    'INCIDENT_HOUR_OF_THE_DAY', 'REPORT_LAG_DAYS', 'PROCESS_LAG_DAYS',
    'POLICY_AGE_AT_LOSS_DAYS', 'VENDOR_INVOLVED',
]

# Categorical features (will be one-hot encoded)
CATEGORICAL_FEATURES = [
    'INSURANCE_TYPE', 'RISK_SEGMENTATION', 'MARITAL_STATUS',
    'EMPLOYMENT_STATUS', 'SOCIAL_CLASS', 'HOUSE_TYPE',
    'CUSTOMER_EDUCATION_LEVEL', 'INCIDENT_SEVERITY',
]


def encode_for_model(df: pd.DataFrame) -> tuple:
    """
    Prepare model-ready X and y from a processed DataFrame.

    Returns:
        X  (pd.DataFrame) : feature matrix, one-hot encoded
        y  (pd.Series)    : binary target (IS_DENIED)
        feature_names (list): column names in X
    """
    y = df['IS_DENIED'].copy()

    # Select only model features
    X_num = df[NUMERIC_FEATURES].copy()
    X_cat = pd.get_dummies(df[CATEGORICAL_FEATURES], drop_first=True)

    X = pd.concat([X_num, X_cat], axis=1)
    X.columns = X.columns.astype(str)

    return X, y, X.columns.tolist()


def get_feature_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary table of all model features:
    type (numeric/categorical), null count, unique values.
    Useful for Chapter 1 reporting.
    """
    rows = []
    for col in NUMERIC_FEATURES + CATEGORICAL_FEATURES:
        rows.append({
            'Feature'    : col,
            'Type'       : 'Numeric' if col in NUMERIC_FEATURES else 'Categorical',
            'Nulls'      : df[col].isnull().sum(),
            'Unique'     : df[col].nunique(),
            'Sample'     : str(df[col].iloc[0]),
        })
    return pd.DataFrame(rows)
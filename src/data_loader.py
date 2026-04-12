# ═══════════════════════════════════════════════════════════════
# src/data_loader.py
# PURPOSE: Load raw CSV and export CSVs consistently across all
#          notebooks. Single entry point for all data access.
# ═══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
from src.config import (
    DATA_RAW, CSV_FREQUENCY, CSV_LOSS_RATIO,
    CSV_FRAUD_FLAGS, CSV_LAG, CSV_FULL
)


def load_raw(verbose=True) -> pd.DataFrame:
    """
    Load the raw insurance_claims.csv as is.
    Returns the unprocessed DataFrame.
    Use this only for Chapter 1 inspection.
    """
    df = pd.read_csv(DATA_RAW, low_memory=False)
    if verbose:
        print(f" Raw data loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def load_processed(verbose=True) -> pd.DataFrame:
    """
    Load raw CSV and apply all preprocessing + feature engineering.
    This is the standard entry point for Ch 2, 3, 4, 5.

    Steps applied:
      1. Cast date columns to datetime
      2. Create IS_DENIED binary target
      3. Engineer lag features
      4. Engineer POLICY_AGE_AT_LOSS_DAYS
      5. Create VENDOR_INVOLVED flag
      6. Fill CUSTOMER_EDUCATION_LEVEL nulls → 'Unknown'
      7. Add readable label columns for plots
    Returns the fully processed DataFrame.
    """
    df = pd.read_csv(DATA_RAW, low_memory=False)

    # 1. Date casting
    for col in ['POLICY_EFF_DT', 'LOSS_DT', 'REPORT_DT']:
        df[col] = pd.to_datetime(df[col])
    df['TXN_DATE_TIME'] = pd.to_datetime(df['TXN_DATE_TIME'])

    # 2. Binary target: A=0 approved, D=1 denied (fraud proxy)
    df['IS_DENIED'] = (df['CLAIM_STATUS'] == 'D').astype(int)

    # 3. Lag features
    df['REPORT_LAG_DAYS']  = (df['REPORT_DT'] - df['LOSS_DT']).dt.days
    df['PROCESS_LAG_DAYS'] = (df['TXN_DATE_TIME'].dt.normalize() - df['REPORT_DT']).dt.days
    df['TOTAL_LAG_DAYS']   = (df['TXN_DATE_TIME'].dt.normalize() - df['LOSS_DT']).dt.days

    # 4. Policy age at time of loss (days)
    df['POLICY_AGE_AT_LOSS_DAYS'] = (df['LOSS_DT'] - df['POLICY_EFF_DT']).dt.days

    # 5. Vendor involvement flag
    df['VENDOR_INVOLVED'] = df['VENDOR_ID'].notnull().astype(int)

    # 6. Fill education nulls
    df['CUSTOMER_EDUCATION_LEVEL'] = df['CUSTOMER_EDUCATION_LEVEL'].fillna('Unknown')

    # 7. Readable label columns (for chart axes)
    df['STATUS_LABEL']     = df['CLAIM_STATUS'].map({'A': 'Approved', 'D': 'Denied'})
    df['RISK_LABEL']       = df['RISK_SEGMENTATION'].map({'H': 'High', 'M': 'Medium', 'L': 'Low'})
    df['MARITAL_LABEL']    = df['MARITAL_STATUS'].map({'Y': 'Married', 'N': 'Single'})
    df['EMPLOYMENT_LABEL'] = df['EMPLOYMENT_STATUS'].map({'Y': 'Employed', 'N': 'Unemployed'})
    df['CLASS_LABEL']      = df['SOCIAL_CLASS'].map({
        'HI': 'High Income', 'MI': 'Mid Income', 'LI': 'Low Income'
    })

    if verbose:
        print(f" Processed data loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"  IS_DENIED: {df['IS_DENIED'].sum():,} denied ({df['IS_DENIED'].mean()*100:.2f}%)")
    return df


def load_export(name: str, verbose=True) -> pd.DataFrame:
    """
    Load one of the 5 SQL export CSVs by short name.
    name options: 'frequency', 'loss_ratio', 'fraud_flags', 'lag', 'full'
    """
    _map = {
        'frequency'  : CSV_FREQUENCY,
        'loss_ratio' : CSV_LOSS_RATIO,
        'fraud_flags': CSV_FRAUD_FLAGS,
        'lag'        : CSV_LAG,
        'full'       : CSV_FULL,
    }
    if name not in _map:
        raise ValueError(f"Unknown export name '{name}'. Choose from: {list(_map.keys())}")
    path = _map[name]
    df   = pd.read_csv(path)
    if verbose:
        print(f" Export '{name}' loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df
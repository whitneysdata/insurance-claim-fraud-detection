# ═══════════════════════════════════════════════════════════════
# src/config.py
# PROJECT: Insurance Claim Fraud Detection
# PURPOSE: Central configuration — paths, constants, visual style
#          Import this in every notebook: from src.config import *
# ═══════════════════════════════════════════════════════════════

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── Project root ────────────────────────────────────────────────
# Resolves to Desktop/insurance-claim-fraud-detection/
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

# ── Data paths ──────────────────────────────────────────────────
DATA_RAW     = os.path.join(PROJECT_ROOT, 'data', 'insurance_claims.csv')
DATA_EXPORTS = os.path.join(PROJECT_ROOT, 'data', 'exports')

# ── Output paths ────────────────────────────────────────────────
REPORTS_DIR  = os.path.join(PROJECT_ROOT, 'reports')
ASSETS_DIR   = os.path.join(PROJECT_ROOT, 'assets')

# Auto-create output directories
for _dir in [REPORTS_DIR, ASSETS_DIR]:
    os.makedirs(_dir, exist_ok=True)

# ── Export CSV filenames ────────────────────────────────────────
CSV_FREQUENCY  = os.path.join(DATA_EXPORTS, '01_frequency_severity.csv')
CSV_LOSS_RATIO = os.path.join(DATA_EXPORTS, '02_loss_ratio.csv')
CSV_FRAUD_FLAGS= os.path.join(DATA_EXPORTS, '03_fraud_flags.csv')
CSV_LAG        = os.path.join(DATA_EXPORTS, '04_settlement_lag.csv')
CSV_FULL       = os.path.join(DATA_EXPORTS, '05_full_profile_for_python.csv')

# ── Dataset constants ───────────────────────────────────────────
TOTAL_ROWS      = 10_000
N_DENIED        = 503
N_APPROVED      = 9_497
DENIAL_RATE     = 0.0503
ALPHA           = 0.05       # significance level for all tests
RANDOM_STATE    = 42

INSURANCE_TYPES = ['Health', 'Life', 'Mobile', 'Motor', 'Property', 'Travel']
RISK_SEGMENTS   = ['Low', 'Medium', 'High']
SEVERITY_LEVELS = ['Minor Loss', 'Major Loss', 'Total Loss']

# ── Colour palette ──────────────────────────────────────────────
PALETTE      = ['#2E86AB', '#E84855', '#F9C74F', '#43AA8B', '#9B5DE5', '#F77F00']
DENY_COLOR   = '#E84855'   # red  → denied claims
APPR_COLOR   = '#2E86AB'   # blue → approved claims
GOLD_COLOR   = '#d4a847'   # gold → reference lines / averages
NEUTRAL      = '#aaaaaa'   # grey → expected / baseline bars

# Insurance type colour map (consistent across all charts)
TYPE_COLORS = {
    'Health'  : '#2E86AB',
    'Life'    : '#E84855',
    'Mobile'  : '#F9C74F',
    'Motor'   : '#43AA8B',
    'Property': '#9B5DE5',
    'Travel'  : '#F77F00',
}

# ── Global matplotlib style ─────────────────────────────────────
plt.rcParams.update({
    'figure.dpi'        : 150,
    'figure.facecolor'  : 'white',
    'axes.facecolor'    : '#fafafa',
    'axes.spines.top'   : False,
    'axes.spines.right' : False,
    'axes.grid'         : True,
    'grid.alpha'        : 0.4,
    'grid.linestyle'    : '--',
    'font.family'       : 'DejaVu Sans',
    'axes.titlesize'    : 13,
    'axes.titleweight'  : 'bold',
    'axes.labelsize'    : 11,
    'xtick.labelsize'   : 10,
    'ytick.labelsize'   : 10,
    'legend.fontsize'   : 10,
})

print(f" config loaded | project root: {PROJECT_ROOT}")
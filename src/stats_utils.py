# ═══════════════════════════════════════════════════════════════
# src/stats_utils.py
# PURPOSE: Hypothesis test runners. Each function runs the test,
#          prints a formatted results table, and returns a dict.
#          Chapter 3 calls these — no test logic in the notebook.
# ═══════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd
from scipy import stats
from src.config import ALPHA


def run_anova(df: pd.DataFrame, group_col: str,
               value_col: str, label: str = '') -> dict:
    """
    One-way ANOVA + Kruskal-Wallis + Eta-squared effect size.
    Prints a formatted results table.
    Returns dict with all statistics.
    """
    groups      = [g[value_col].values for _, g in df.groupby(group_col)]
    f_stat, p_f = stats.f_oneway(*groups)
    h_stat, p_h = stats.kruskal(*groups)

    grand_mean = df[value_col].mean()
    ss_between = sum(
        len(g) * (g.mean() - grand_mean) ** 2
        for g in [df[df[group_col] == lvl][value_col] for lvl in df[group_col].unique()]
    )
    ss_total = ((df[value_col] - grand_mean) ** 2).sum()
    eta_sq   = ss_between / ss_total

    decision = "Reject H₀ " if p_f < ALPHA else "Fail to reject H₀"

    print(f"{'='*55}")
    print(f"  ANOVA: {label}")
    print(f"{'='*55}")
    print(f"  F-statistic      : {f_stat:>12,.4f}")
    print(f"  ANOVA p-value    : {p_f:>12.4e}")
    print(f"  Eta-squared (η²) : {eta_sq:>12.4f}")
    print(f"  Kruskal-Wallis H : {h_stat:>12.4f}")
    print(f"  Kruskal p-value  : {p_h:>12.4e}")
    print(f"  α                : {ALPHA}")
    print(f"  Decision         : {decision}")
    print()

    return {'f_stat': f_stat, 'p_anova': p_f,
             'h_stat': h_stat, 'p_kruskal': p_h,
             'eta_sq': eta_sq, 'reject': p_f < ALPHA}


def run_chisquare(df: pd.DataFrame, group_col: str,
                   target_col: str, label: str = '') -> dict:
    """
    Chi-square test of independence + Cramér's V effect size.
    Prints a formatted results table.
    Returns dict with all statistics.
    """
    ct              = pd.crosstab(df[group_col], df[target_col])
    chi2, p, dof, exp = stats.chi2_contingency(ct)
    n               = ct.sum().sum()
    cramers_v       = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    decision        = "Reject H₀ ✓" if p < ALPHA else "Fail to reject H₀"

    print(f"{'='*55}")
    print(f"  Chi-Square: {label}")
    print(f"{'='*55}")
    print(f"  χ² statistic  : {chi2:>12.4f}")
    print(f"  p-value       : {p:>12.4e}")
    print(f"  Degrees of freedom: {dof}")
    print(f"  Cramér's V    : {cramers_v:>12.4f}")
    print(f"  α             : {ALPHA}")
    print(f"  Decision      : {decision}")
    print()

    return {'chi2': chi2, 'p': p, 'dof': dof,
             'cramers_v': cramers_v, 'reject': p < ALPHA,
             'contingency_table': ct}


def run_ttest(group_a: pd.Series, group_b: pd.Series,
               label_a: str = 'Group A', label_b: str = 'Group B',
               label: str = '') -> dict:
    """
    Independent t-test + Mann-Whitney U + Cohen's d effect size.
    Levene's test determines whether to use equal or Welch variance.
    Prints a formatted results table.
    Returns dict with all statistics.
    """
    lev_stat, lev_p = stats.levene(group_a, group_b)
    equal_var        = lev_p > ALPHA
    t_stat, p_t      = stats.ttest_ind(group_a, group_b, equal_var=equal_var)
    u_stat, p_mw     = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')

    n_a, n_b = len(group_a), len(group_b)
    pooled   = np.sqrt(
        ((n_a - 1) * group_a.std()**2 + (n_b - 1) * group_b.std()**2) /
        (n_a + n_b - 2)
    )
    cohens_d = (group_a.mean() - group_b.mean()) / pooled
    decision = "Reject H₀ " if p_t < ALPHA else "Fail to reject H₀"

    print(f"{'='*55}")
    print(f"  t-test: {label}")
    print(f"{'='*55}")
    print(f"  {label_a} mean : {group_a.mean():>12,.2f}  (n={n_a:,})")
    print(f"  {label_b} mean : {group_b.mean():>12,.2f}  (n={n_b:,})")
    print(f"  Levene p-value: {lev_p:>12.4f}  → {'equal var' if equal_var else 'Welch t-test'}")
    print(f"  t-statistic   : {t_stat:>12.4f}")
    print(f"  t-test p-value: {p_t:>12.4f}")
    print(f"  Cohen's d     : {cohens_d:>12.4f}")
    print(f"  Mann-Whitney U: {u_stat:>12,.0f}")
    print(f"  MW p-value    : {p_mw:>12.4f}")
    print(f"  α             : {ALPHA}")
    print(f"  Decision      : {decision}")
    print()

    return {'t_stat': t_stat, 'p_ttest': p_t,
             'u_stat': u_stat, 'p_mw': p_mw,
             'cohens_d': cohens_d, 'reject': p_t < ALPHA}
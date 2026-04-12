# ═══════════════════════════════════════════════════════════════
# src/viz.py
# PURPOSE: Shared visualisation utilities.
#          Every chart-saving call goes through save_fig()
#          so every figure lands in reports/ consistently.
# ═══════════════════════════════════════════════════════════════

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from src.config import REPORTS_DIR, DENY_COLOR, APPR_COLOR, GOLD_COLOR, PALETTE


def save_fig(filename: str, dpi: int = 180, tight: bool = True) -> None:
    """
    Save the current matplotlib figure to the reports/ directory.
    Always call this BEFORE plt.show().

    Args:
        filename : e.g. 'fig01_target_distribution.png'
        dpi      : resolution (default 180 for publication quality)
        tight    : apply tight_layout before saving
    """
    if tight:
        plt.tight_layout()
    path = os.path.join(REPORTS_DIR, filename)
    plt.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f" Saved → reports/{filename}")


def fmt_currency(ax, axis: str = 'x') -> None:
    """Apply $XX,XXX currency formatting to an axis."""
    formatter = mticker.FuncFormatter(lambda x, _: f'${int(x):,}')
    if axis == 'x':
        ax.xaxis.set_major_formatter(formatter)
    else:
        ax.yaxis.set_major_formatter(formatter)


def fmt_comma(ax, axis: str = 'y') -> None:
    """Apply comma-separated number formatting to an axis."""
    formatter = mticker.FuncFormatter(lambda x, _: f'{int(x):,}')
    if axis == 'x':
        ax.xaxis.set_major_formatter(formatter)
    else:
        ax.yaxis.set_major_formatter(formatter)


def add_bar_labels(ax, bars, fmt: str = '{:.1f}%',
                     offset: float = 0.1, color: str = 'black',
                     fontsize: int = 10) -> None:
    """Add value labels above vertical bar chart bars."""
    for bar in bars:
        val = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + offset,
            fmt.format(val),
            ha='center', va='bottom',
            fontsize=fontsize, fontweight='bold', color=color
        )


def add_hbar_labels(ax, bars, fmt: str = '{:.2f}%',
                      offset: float = 0.05, fontsize: int = 10) -> None:
    """Add value labels beside horizontal bar chart bars."""
    for bar in bars:
        val = bar.get_width()
        ax.text(
            val + offset,
            bar.get_y() + bar.get_height() / 2,
            fmt.format(val),
            va='center', fontsize=fontsize, fontweight='bold'
        )


def add_avg_line(ax, value: float, label: str = None,
                   orient: str = 'h', color: str = None) -> None:
    """
    Add a dashed reference line (average / benchmark).
    orient: 'h' for horizontal (axhline), 'v' for vertical (axvline)
    """
    color = color or GOLD_COLOR
    label = label or f'Average: {value:.2f}'
    if orient == 'h':
        ax.axhline(value, color=color, linestyle='--', linewidth=2, label=label)
    else:
        ax.axvline(value, color=color, linestyle='--', linewidth=2, label=label)
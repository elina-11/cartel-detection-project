from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from final_project.final.heatmap_helpers import (
    _compute_heatmap_collusion_rate,
    _compute_heatmap_counts,
)

BIN_SIZE = 20


def _set_decimal_ticks(ax: plt.Axes, bins: int) -> None:
    """Format axes to show 0.0 to 1.0 instead of bin numbers."""
    tick_positions = np.linspace(0.5, bins - 0.5, 6)
    tick_labels = [f"{value:.1f}" for value in np.linspace(0.0, 1.0, 6)]

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=0)

    ax.set_yticks(tick_positions)
    ax.set_yticklabels(tick_labels[::-1], rotation=0)


def _format_percent_colorbar(ax: plt.Axes) -> None:
    """Formats the colorbar labels with percent signs."""
    colorbar = ax.collections[0].colorbar
    colorbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
    colorbar.update_ticks()


def generate_figure_a(
    group_data: pd.DataFrame,
    bins: int = BIN_SIZE,
) -> plt.Figure:
    """Generate Figure A: distribution of detected groups."""
    heatmap_counts = _compute_heatmap_counts(group_data, bins=bins)
    heatmap_percent = 100 * heatmap_counts / heatmap_counts.to_numpy().sum()

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        heatmap_percent,
        cmap="viridis",
        ax=ax,
        cbar=True,
        square=True,
        xticklabels=False,
        yticklabels=False,
    )

    _set_decimal_ticks(ax, bins)

    ax.set_xlabel("Coherence")
    ax.set_ylabel("Exclusivity")
    ax.set_title("Figure A: Distribution of detected groups")

    return fig


def generate_figure_b(
    group_data: pd.DataFrame,
    bins: int = BIN_SIZE,
) -> plt.Figure:
    """Generate Figure B: average collusion rate by bin."""
    heatmap_rates = _compute_heatmap_collusion_rate(group_data, bins=bins)
    heatmap_percent = 100 * heatmap_rates

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        heatmap_percent,
        cmap="viridis",
        ax=ax,
        cbar=True,
        square=True,
        xticklabels=False,
        yticklabels=False,
    )

    _set_decimal_ticks(ax, bins)

    ax.set_xlabel("Coherence")
    ax.set_ylabel("Exclusivity")
    ax.set_title("Figure B: Rate of collusion")

    return fig

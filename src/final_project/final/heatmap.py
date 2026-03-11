from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from final_project.final.heatmap_helpers import (
    _compute_heatmap_collusion_rate,
    _compute_heatmap_counts,
)


def generate_figure_a(
    group_data: pd.DataFrame,
    bins: int = 10,
) -> plt.Figure:
    """Generate Figure A: distribution of detected groups."""
    heatmap_data = _compute_heatmap_counts(group_data, bins=bins)

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        heatmap_data,
        cmap="viridis",
        ax=ax,
    )

    ax.set_xlabel("Exclusivity bin")
    ax.set_ylabel("Coherence bin")
    ax.set_title("Figure A: Distribution of detected groups")

    return fig


def generate_figure_b(
    group_data: pd.DataFrame,
    bins: int = 10,
) -> plt.Figure:
    """Generate Figure B: average collusion rate by bin."""
    heatmap_data = _compute_heatmap_collusion_rate(group_data, bins=bins)

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        heatmap_data,
        cmap="viridis",
        ax=ax,
    )

    ax.set_xlabel("Exclusivity bin")
    ax.set_ylabel("Coherence bin")
    ax.set_title("Figure B: Rate of collusion")

    return fig

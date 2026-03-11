import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from final_project.final.heatmap_helpers import _compute_heatmap_counts


def generate_figure(
    group_features: pd.DataFrame,
    bins: int = 10,
) -> plt.Figure:
    """Generates heatmap.

    Args:
        group_features (pd.DataFrame): Group features table.
        bins (int): Number of bins for each dimension.

    Returns:
        matplotlib.figure.Figure
    """
    heatmap_data = _compute_heatmap_counts(group_features, bins=bins)

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(
        heatmap_data,
        cmap="viridis",
        ax=ax,
    )

    ax.set_xlabel("Exclusivity bin")
    ax.set_ylabel("Coherence bin")
    ax.set_title("Figure 3A: Distribution of detected groups")

    return fig

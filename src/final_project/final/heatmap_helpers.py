from __future__ import annotations

import numpy as np
import pandas as pd


def _validate_group_features(df: pd.DataFrame) -> None:
    """Validate the structure of the group features DataFrame."""
    required_columns = {"group_id", "coherence", "exclusivity"}

    if set(df.columns) != required_columns:
        msg = (
            "group_features must contain exactly: "
            "'group_id', 'coherence', 'exclusivity'."
        )
        raise ValueError(msg)


def _compute_heatmap_counts(
    group_features: pd.DataFrame,
    bins: int = 10,
) -> pd.DataFrame:
    """Compute the 2D bin counts for the heatmap.

    Args:
        group_features (pd.DataFrame): Group features table.
        bins (int): Number of bins for coherence and exclusivity.

    Returns:
        pd.DataFrame: Matrix suitable for seaborn heatmap plotting.
    """
    _validate_group_features(group_features)

    coherence_bins = np.linspace(0.0, 1.0, bins + 1)
    exclusivity_bins = np.linspace(0.0, 1.0, bins + 1)

    df = group_features.copy()

    df["coherence_bin"] = pd.cut(
        df["coherence"],
        bins=coherence_bins,
        include_lowest=True,
        labels=False,
    )

    df["exclusivity_bin"] = pd.cut(
        df["exclusivity"],
        bins=exclusivity_bins,
        include_lowest=True,
        labels=False,
    )

    heatmap_counts = (
        df.groupby(["coherence_bin", "exclusivity_bin"]).size().unstack(fill_value=0)
    )

    all_bins = range(bins)

    heatmap_counts = heatmap_counts.reindex(
        index=all_bins,
        columns=all_bins,
        fill_value=0,
    )

    heatmap_counts = heatmap_counts.sort_index(ascending=False)

    return heatmap_counts

from __future__ import annotations

import numpy as np
import pandas as pd


def _validate_group_features(df: pd.DataFrame) -> None:
    """Helper function validates group features DataFrame."""
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
    """Helper function computes the 2D bin counts for the heatmap.

    Args:
        group_features (pd.DataFrame): Group features table.
        bins (int): Number of bins for coherence and exclusivity.

    Returns:
        pd.DataFrame: Pivot table suitable for heatmap plotting.
    """
    _validate_group_features(group_features)

    coherence_bins = np.linspace(0, 1, bins + 1)
    exclusivity_bins = np.linspace(0, 1, bins + 1)

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
        df.groupby(["coherence_bin", "exclusivity_bin"])
        .size()
        .pivit_table(fill_value=0)
    )

    return heatmap_counts

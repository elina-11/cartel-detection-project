from __future__ import annotations

import numpy as np
import pandas as pd

BIN_SIZE = 20


def _validate_group_features(df: pd.DataFrame) -> None:
    """Helper function validates the group-level DataFrame for final figures."""
    required_columns = {
        "group_id",
        "coherence",
        "exclusivity",
        "collusion_rate",
        "simulation_id",
    }

    if set(df.columns) != required_columns:
        msg = (
            "heatmap_data must contain exactly: 'group_id', 'coherence', "
            "'exclusivity', 'collusion_rate', 'simulation_id'."
        )
        raise ValueError(msg)


def _bin_group_data(
    group_data: pd.DataFrame,
    bins: int = BIN_SIZE,
) -> pd.DataFrame:
    """Helper function adds coherence and exclusivity bin columns."""
    _validate_group_features(group_data)

    coherence_bins = np.linspace(0.0, 1.0, bins + 1)
    exclusivity_bins = np.linspace(0.0, 1.0, bins + 1)

    df = group_data.copy()

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

    return df


def _compute_heatmap_counts(
    group_data: pd.DataFrame,
    bins: int = BIN_SIZE,
) -> pd.DataFrame:
    """Helper function computes 2D bin counts for Figure A."""
    df = _bin_group_data(group_data, bins=bins)

    heatmap_counts = (
        df.groupby(["exclusivity_bin", "coherence_bin"]).size().unstack(fill_value=0)
    )

    all_bins = range(bins)

    heatmap_counts = heatmap_counts.reindex(
        index=all_bins,
        columns=all_bins,
        fill_value=0,
    )

    return heatmap_counts.sort_index(ascending=False)


def _compute_heatmap_collusion_rate(
    group_data: pd.DataFrame,
    bins: int = BIN_SIZE,
) -> pd.DataFrame:
    """Function computes average collusion rate in each 2D bin for Figure B."""
    df = _bin_group_data(group_data, bins=bins)

    heatmap_rates = (
        df.groupby(["exclusivity_bin", "coherence_bin"])["collusion_rate"]
        .mean()
        .unstack(fill_value=0.0)
    )

    all_bins = range(bins)

    heatmap_rates = heatmap_rates.reindex(
        index=all_bins,
        columns=all_bins,
        fill_value=0.0,
    )

    return heatmap_rates.sort_index(ascending=False)

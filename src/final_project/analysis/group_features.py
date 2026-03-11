import pandas as pd

from final_project.analysis.group_features_helpers import (
    _compute_group_features_table,
)


def compute_group_features(
    network_df: pd.DataFrame,
    groups_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compute group-level features from the co-bidding network.

    Args:
        network_df (pd.DataFrame): Co-bidding network edge list.
        groups_df (pd.DataFrame): Long-format detected groups.

    Returns:
        pd.DataFrame: Group-level features including coherence and exclusivity.
    """
    return _compute_group_features_table(network_df, groups_df)

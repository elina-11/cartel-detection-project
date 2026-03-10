from __future__ import annotations

import pandas as pd


def _validate_co_bidding_network(network_df: pd.DataFrame) -> None:
    """Helper function validates the structure of the co-bidding network edge list.

    Args:
        network_df (pd.DataFrame): Edge list of the co-bidding network.

    Returns:
        None

    Raises:
        ValueError: If the required columns are missing.
    """
    required_columns = {"firm_id_1", "firm_id_2", "weight"}
    observed_columns = set(network_df.columns)

    if observed_columns != required_columns:
        msg = (
            "The co-bidding network must have exactly these columns: "
            "'firm_id_1', 'firm_id_2', and 'weight'."
        )
        raise ValueError(msg)

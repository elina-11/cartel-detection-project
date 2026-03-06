import numpy as np
import pandas as pd


def _compute_firm_distances(
    firms_df: pd.DataFrame,
    contract_x: float,
    contract_y: float,
) -> pd.Series:
    """Helper function that computes Euclidean distances from all firms
    to a contract location.

    Args:
        firms_df (pd.DataFrame): DataFrame containing firm_id, x, y.
        contract_x (float): X-coordinate of the contract.
        contract_y (float): Y-coordinate of the contract.

    Returns:
        pd.Series: Distances indexed by firm_id.
    """
    dx = firms_df["x"] - contract_x
    dy = firms_df["y"] - contract_y

    distances = np.sqrt(dx**2 + dy**2)

    return pd.Series(distances.values, index=firms_df["firm_id"])

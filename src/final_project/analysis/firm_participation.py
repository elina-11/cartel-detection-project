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
 

def select_participating_firms(
    firms_df: pd.DataFrame,
    contract_x: float,
    contract_y: float,
    initial_radius: float = 0.1,
    radius_increment: float = 0.1,
) -> dict:
    
    """
    The function selects firms participating in the auction 
    based on distance to the contract.

    Firms within the current radius participate. If no firms fall within the
    radius, the radius expands repeatedly until at least one firm is included.

    Args:
        firms_df (pd.DataFrame): DataFrame containing firm_id, x, y.
        contract_x (float): X-coordinate of the contract.
        contract_y (float): Y-coordinate of the contract.
        initial_radius (float): Starting radius for participation.
        radius_increment (float): Radius increase if no firms are found.

    Returns:
        dict: Contains the participating firm IDs and the radius used.
    """

    distances = _compute_firm_distances(firms_df, contract_x, contract_y)

    radius = initial_radius

    while True:
        participating = distances[distances <= radius]

        if not participating.empty:
            break

        radius += radius_increment

    participating_firms = participating.index.tolist()

    return {
        "participating_firms": participating_firms,
        "radius_used": radius,
    }

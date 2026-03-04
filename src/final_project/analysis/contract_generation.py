import numpy as np
import pandas as pd


def generate_contract_near_issuer(
    issuers_df: pd.DataFrame,
    rng: np.random.Generator,
    std: float = 0.3,
) -> dict:
    """Generate a contract location near a randomly selected issuer.

    The contract location is drawn from a 2D normal distribution centered
    at the issuer's location. The resulting coordinates are clipped to lie
    within the unit square [0, 1] * [0, 1].

    Args:
        issuers_df (pd.DataFrame): DataFrame containing issuer_id, x, y.
        rng (np.random.Generator): Random number generator for reproducibility.
        std (float): Standard deviation of the 2D normal draw.

    Returns:
        dict: Dictionary containing issuer_id, contract_x, contract_y.
    """
    # Select a random issuer
    integer_index = rng.integers(low=0, high=len(issuers_df))
    issuer_row = issuers_df.iloc[integer_index]

    issuer_id = int(issuer_row["issuer_id"])
    issuer_x = float(issuer_row["x"])
    issuer_y = float(issuer_row["y"])

    # Draw contract location near issuer
    contract_location = rng.normal(loc=[issuer_x, issuer_y], scale=std, size=2)

    # Clip coordinates to stay inside the unit square
    contract_location = np.clip(contract_location, 0.0, 1.0)

    contract_x = float(contract_location[0])
    contract_y = float(contract_location[1])

    return {
        "issuer_id": issuer_id,
        "contract_x": contract_x,
        "contract_y": contract_y,
    }

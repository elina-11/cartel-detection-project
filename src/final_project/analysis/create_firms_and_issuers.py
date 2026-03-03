from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Firm:
    """To represent a firm located in a unit square.

    Attributes:
    firm_id (int) : Uniquely identifies a firm
    x (float) : X-coordinate of the firm in the unit square
    y (float) : Y-coordinate of the firm in the unit square
    """

    firm_id: int
    x: float
    y: float


@dataclass
class Issuer:
    """To represent an issuer of contract located in the unit square.

    Attributes:
    issuer_id (int) : Uniquely identifies the issuer of the contract.
    x (float) : X-coordinate in the unit square.
    y (float) : Y-coordinate in the unit square.
    """

    issuer_id: int
    x: float
    y: float


def create_firms(n_firms: int, seed: int) -> pd.DataFrame:
    """This function generates firms placed uniformly
    at random in the unit square.

    Args:
        n_firms(int) : The number of firms to generate.
        seed(int) : Seed for reproducibility.

    Returns:
        pd.DataFrame : DataFrame with columns ['firm_id', 'x', 'y']."""

    rng = np.random.default_rng(seed)
    coordinates = rng.uniform(low=0.0, high=1.0, size=(n_firms, 2))

    firms = pd.DataFrame(
        {
            "firm_id": np.arange(n_firms),
            "x": coordinates[:, 0],
            "y": coordinates[:, 1],
        }
    )
    return firms

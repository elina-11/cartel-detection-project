from __future__ import annotations

from collections import defaultdict

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


def _build_adjacency_dict(network_df: pd.DataFrame) -> dict[int, dict[int, float]]:
    """Helper function converts the co-bidding edge list into an adjacency dictionary.

    Args:
        network_df (pd.DataFrame): Edge list with columns
            ['firm_id_1', 'firm_id_2', 'weight'].

    Returns:
        dict[int, dict[int, float]]: Mapping from each firm to its neighbors
        and the corresponding edge weights.
    """
    adjacency: dict[int, dict[int, float]] = defaultdict(dict)

    for row in network_df.itertuples(index=False):
        firm_id_1 = int(row.firm_id_1)
        firm_id_2 = int(row.firm_id_2)
        weight = float(row.weight)

        adjacency[firm_id_1][firm_id_2] = weight
        adjacency[firm_id_2][firm_id_1] = weight

    return dict(adjacency)


def _compute_internal_strength(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
) -> float:
    """Helper function computes the internal strength of a candidate group.

    Internal strength is the sum of weights of all edges where both
    endpoints are inside the group.

    Args:
        group (set[int]): Set of firm IDs in the candidate group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.

    Returns:
        float: Internal strength of the group.
    """
    internal_strength = 0.0

    for node in group:
        for neighbor, weight in adjacency.get(node, {}).items():
            if neighbor in group and neighbor > node:
                internal_strength += weight

    return internal_strength

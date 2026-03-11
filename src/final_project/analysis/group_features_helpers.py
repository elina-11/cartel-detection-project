from __future__ import annotations

from math import prod

import pandas as pd

from final_project.analysis.group_detection_helpers import (
    _build_adjacency_dict,
    _compute_external_strength,
    _compute_internal_strength,
    _validate_co_bidding_network,
)


def _validate_detected_groups(groups_df: pd.DataFrame) -> None:
    """Helper validates the structure of the detected groups DataFrame.

    Args:
        groups_df (pd.DataFrame): Long-format detected groups DataFrame.

    Returns:
        None

    Raises:
        ValueError: If the required columns are missing.
    """
    required_columns = {"group_id", "firm_id"}
    observed_columns = set(groups_df.columns)

    if observed_columns != required_columns:
        msg = (
            "The detected groups DataFrame must have exactly these columns: "
            "'group_id' and 'firm_id'."
        )
        raise ValueError(msg)


def _validate_group_feature_inputs(
    network_df: pd.DataFrame,
    groups_df: pd.DataFrame,
) -> None:
    """Helper function validates the inputs required for group feature computation.

    Args:
        network_df (pd.DataFrame): Co-bidding network edge list.
        groups_df (pd.DataFrame): Long-format detected groups DataFrame.

    Returns:
        None
    """
    _validate_co_bidding_network(network_df)
    _validate_detected_groups(groups_df)


def _recover_group_members(
    groups_df: pd.DataFrame,
) -> dict[int, set[int]]:
    """Helper recovers group membership sets from the long-format groups DataFrame.

    Args:
        groups_df (pd.DataFrame): Long-format detected groups DataFrame.

    Returns:
        dict[int, set[int]]: Mapping from group_id to the set of member firms.
    """
    grouped = groups_df.groupby("group_id")["firm_id"]

    return {
        int(group_id): {int(firm_id) for firm_id in firm_ids}
        for group_id, firm_ids in grouped
    }


def _get_internal_edge_weights(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
) -> list[float]:
    """Helper function extracts the internal edge weights of a candidate group.

    Args:
        group (set[int]): Set of firm IDs in the group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.

    Returns:
        list[float]: List of internal edge weights, counting each undirected
            edge exactly once.
    """
    internal_weights: list[float] = []

    for node in group:
        for neighbor, weight in adjacency.get(node, {}).items():
            if neighbor in group and neighbor > node:
                internal_weights.append(weight)

    return internal_weights


def _compute_coherence(
    internal_weights: list[float],
) -> float:
    """Helper function computes group coherence from internal edge weights.

    Coherence is the ratio of the geometric mean to the arithmetic mean of
    the internal edge weights.

    Args:
        internal_weights (list[float]): Internal edge weights of a group.

    Returns:
        float: Coherence of the group.
    """
    if not internal_weights:
        return 0.0

    arithmetic_mean = sum(internal_weights) / len(internal_weights)

    if arithmetic_mean == 0.0:
        return 0.0

    geometric_mean = prod(internal_weights) ** (1 / len(internal_weights))

    return geometric_mean / arithmetic_mean


def _compute_exclusivity(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
) -> float:
    """Helper function computes group exclusivity.

    Exclusivity is the ratio of internal strength to total strength
    (internal plus external).

    Args:
        group (set[int]): Set of firm IDs in the group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.

    Returns:
        float: Exclusivity of the group.
    """
    internal_strength = _compute_internal_strength(group, adjacency)
    external_strength = _compute_external_strength(group, adjacency)

    total_strength = internal_strength + external_strength

    if total_strength == 0.0:
        return 0.0

    return internal_strength / total_strength


def _compute_single_group_features(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
) -> tuple[float, float]:
    """Helper function computes coherence and exclusivity for a single group.

    Args:
        group (set[int]): Set of firm IDs in the group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.

    Returns:
        tuple[float, float]: (coherence, exclusivity)
    """
    internal_weights = _get_internal_edge_weights(group, adjacency)

    coherence = _compute_coherence(internal_weights)
    exclusivity = _compute_exclusivity(group, adjacency)

    return coherence, exclusivity


def _compute_group_features_table(
    network_df: pd.DataFrame,
    groups_df: pd.DataFrame,
) -> pd.DataFrame:
    """Function computes coherence and exclusivity for all detected groups.

    Args:
        network_df (pd.DataFrame): Co-bidding network edge list.
        groups_df (pd.DataFrame): Long-format detected groups.

    Returns:
        pd.DataFrame: DataFrame with columns ['group_id', 'coherence', 'exclusivity'].
    """
    _validate_group_feature_inputs(network_df, groups_df)

    adjacency = _build_adjacency_dict(network_df)

    group_members = _recover_group_members(groups_df)

    rows: list[dict[str, float]] = []

    for group_id, group in group_members.items():
        coherence, exclusivity = _compute_single_group_features(group, adjacency)

        rows.append(
            {
                "group_id": group_id,
                "coherence": coherence,
                "exclusivity": exclusivity,
            }
        )

    return pd.DataFrame(rows, columns=["group_id", "coherence", "exclusivity"])

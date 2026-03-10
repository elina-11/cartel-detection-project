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


def _compute_external_strength(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
) -> float:
    """Helper function computes the external strength of a candidate group.

    External strength is the sum of weights of all edges that connect a node
    inside the group to a node outside the group.

    Args:
        group (set[int]): Set of firm IDs in the candidate group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.

    Returns:
        float: External strength of the group.
    """
    external_strength = 0.0

    for node in group:
        for neighbor, weight in adjacency.get(node, {}).items():
            if neighbor not in group:
                external_strength += weight

    return external_strength


def _compute_group_fitness(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
    alpha: float = 1.5,
    beta: float = 1.5,
) -> float:
    """Helper function computes the fitness of a candidate group.

    The fitness function rewards groups with strong internal ties, weak
    external ties, and relatively small size.

    Args:
        group (set[int]): Set of firm IDs in the candidate group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.
        alpha (float): Exponent controlling the penalty on total strength.
        beta (float): Exponent controlling the penalty on group size.

    Returns:
        float: Fitness value of the candidate group.
    """
    internal_strength = _compute_internal_strength(group, adjacency)
    external_strength = _compute_external_strength(group, adjacency)
    group_size = len(group)

    total_strength = internal_strength + external_strength

    if total_strength == 0.0:
        return 0.0

    return internal_strength / ((total_strength**alpha) * (group_size**beta))


def _get_candidate_neighbors(
    group: set[int],
    adjacency: dict[int, dict[int, float]],
) -> set[int]:
    """Helper function gets all candidate neighbors of a candidate group.

    A candidate neighbor is a node that is adjacent to at least one member
    of the group but is not already inside the group.

    Args:
        group (set[int]): Set of firm IDs in the candidate group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.

    Returns:
        set[int]: Set of candidate nodes that could be added to the group.
    """
    candidate_neighbors: set[int] = set()

    for node in group:
        for neighbor in adjacency.get(node, {}):
            if neighbor not in group:
                candidate_neighbors.add(neighbor)

    return candidate_neighbors


def _compute_node_fitness_gain(
    group: set[int],
    candidate_node: int,
    adjacency: dict[int, dict[int, float]],
    alpha: float = 1.5,
    beta: float = 1.5,
) -> float:
    """Helper computes the fitness gain from adding one node to a candidate group.

    The gain is the difference between the fitness of the expanded group
    and the fitness of the current group.

    Args:
        group (set[int]): Current candidate group.
        candidate_node (int): Node being considered for addition.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.
        alpha (float): Exponent controlling the penalty on total strength.
        beta (float): Exponent controlling the penalty on group size.

    Returns:
        float: Fitness gain from adding the candidate node.
    """
    current_fitness = _compute_group_fitness(
        group=group,
        adjacency=adjacency,
        alpha=alpha,
        beta=beta,
    )

    expanded_group = set(group)
    expanded_group.add(candidate_node)

    expanded_fitness = _compute_group_fitness(
        group=expanded_group,
        adjacency=adjacency,
        alpha=alpha,
        beta=beta,
    )

    return expanded_fitness - current_fitness


def _expand_group_from_seed(
    seed_node: int,
    adjacency: dict[int, dict[int, float]],
    alpha: float = 1.5,
    beta: float = 1.5,
) -> set[int]:
    """Helper function expands a group greedily starting from a seed node.

    The group grows by repeatedly adding the neighboring node that gives
    the largest positive improvement in group fitness. Expansion stops when
    no candidate node increases the fitness.

    Args:
        seed_node (int): Starting node for the group.
        adjacency (dict[int, dict[int, float]]): Adjacency dictionary of the
            co-bidding network.
        alpha (float): Fitness parameter controlling strength penalty.
        beta (float): Fitness parameter controlling size penalty.

    Returns:
        set[int]: Final group grown from the seed node.
    """
    group: set[int] = {seed_node}

    while True:
        candidate_neighbors = _get_candidate_neighbors(group, adjacency)

        best_candidate = None
        best_gain = 0.0

        for candidate in candidate_neighbors:
            gain = _compute_node_fitness_gain(
                group=group,
                candidate_node=candidate,
                adjacency=adjacency,
                alpha=alpha,
                beta=beta,
            )

            if gain > best_gain:
                best_gain = gain
                best_candidate = candidate

        if best_candidate is None:
            break

        group.add(best_candidate)

    return group

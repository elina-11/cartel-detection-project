from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import Any

import pandas as pd

from final_project.analysis.auction_framework import SimulationState

FIRMS_IN_AUCTION = 2


def _build_firm_contract_sets(
    round_log: list[dict[str, Any]],
) -> dict[int, set[int]]:
    """Helper function builds the set of contracts each firm bid on.

    Each retained auction round is treated as one contract. The contract ID
    is taken from the round_number stored in the round log.

    Args:
        round_log (list[dict[str, Any]]): Retained simulation rounds.

    Returns:
        dict[int, set[int]]: Mapping from firm_id to set of contract IDs.
    """
    firm_contracts: dict[int, set[int]] = defaultdict(set)

    for entry in round_log:
        contract_id = int(entry["round_number"])
        participating_firms = entry["participating_firms"]

        for firm_id in participating_firms:
            firm_contracts[int(firm_id)].add(contract_id)

    return dict(firm_contracts)


def _compute_jaccard_weight(
    contracts_a: set[int],
    contracts_b: set[int],
) -> float:
    """Helper function computes the Jaccard similarity between two firms' contract sets.

    Args:
        contracts_a (set[int]): Contracts bid on by firm A.
        contracts_b (set[int]): Contracts bid on by firm B.

    Returns:
        float: Jaccard similarity.
    """
    union = contracts_a | contracts_b

    if not union:
        return 0.0

    intersection = contracts_a & contracts_b
    return len(intersection) / len(union)


def build_co_bidding_network(state: SimulationState) -> pd.DataFrame:
    """The function builds the weighted co-bidding network from the simulation state.

    The network is the projection of the contract-firm bipartite structure
    onto firms. Two firms are linked if they co-bid on at least one retained
    contract. The edge weight is the Jaccard similarity of their contract sets.

    Args:
        state (SimulationState): Simulation output after burn-in trimming.

    Returns:
        pd.DataFrame: Edge list with columns
            ['firm_id_1', 'firm_id_2', 'weight'].
    """
    firm_contracts = _build_firm_contract_sets(state.round_log)

    co_bidding_pairs: set[tuple[int, int]] = set()

    for entry in state.round_log:
        participating_firms = sorted(
            {int(firm_id) for firm_id in entry["participating_firms"]}
        )

        if len(participating_firms) < FIRMS_IN_AUCTION:
            continue

        for firm_id_1, firm_id_2 in combinations(participating_firms, 2):
            co_bidding_pairs.add((firm_id_1, firm_id_2))

    edge_rows: list[dict[str, float | int]] = []

    for firm_id_1, firm_id_2 in sorted(co_bidding_pairs):
        weight = _compute_jaccard_weight(
            contracts_a=firm_contracts[firm_id_1],
            contracts_b=firm_contracts[firm_id_2],
        )

        edge_rows.append(
            {
                "firm_id_1": firm_id_1,
                "firm_id_2": firm_id_2,
                "weight": weight,
            }
        )

    return pd.DataFrame(edge_rows, columns=["firm_id_1", "firm_id_2", "weight"])

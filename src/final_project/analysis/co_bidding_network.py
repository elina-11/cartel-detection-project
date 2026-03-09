from __future__ import annotations

from collections import defaultdict
from typing import Any


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
    """Helper function computes the Jaccard similarity.

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

from typing import Any

import numpy as np

from final_project.analysis.decision_metrics import (
    _compute_frequency_metric,
    _compute_memory_metric,
)


def decide_action(
    focal_firm: int,
    participating_firms: list[int],
    interaction_memory: dict[tuple[int, int], str],
    round_log: list[dict[str, Any]],
    rng: np.random.Generator,
    memory_threshold: float = 0.5,
    noise_std: float = 0.05,
) -> str:
    """The function decides whether a firm colludes or competes in the current auction.

    The decision is based on the memory metric and frequency metric.
    Firms are more likely to collude if rivals previously colluded and
    if they frequently interact with the same rivals.

    Args:
        focal_firm (int): The firm whose decision is being computed.
        participating_firms (list[int]): Firms participating in the auction.
        interaction_memory (dict[tuple[int, int], str]): Pairwise memory of
            last observed actions.
        round_log (list[dict[str, Any]]): History of previous auction rounds.
        rng (np.random.Generator): Random number generator for noise.
        memory_threshold (float): Minimum memory metric required to collude.
        noise_std (float): Standard deviation of noise added to the decision.

    Returns:
        str: "collude" or "compete".

    """
    memory_metric = _compute_memory_metric(
        focal_firm=focal_firm,
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
    )

    frequency_metric = _compute_frequency_metric(
        focal_firm=focal_firm,
        participating_firms=participating_firms,
        round_log=round_log,
    )

    decision_score = memory_metric + frequency_metric

    decision_score += rng.normal(0.0, noise_std)

    if decision_score >= memory_threshold:
        return "collude"

    return "compete"

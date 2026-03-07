from typing import Any

import numpy as np

from final_project.analysis.firm_decision import decide_action


def decide_actions_for_auction(
    participating_firms: list[int],
    interaction_memory: dict[tuple[int, int], str],
    round_log: list[dict[str, Any]],
    rng: np.random.Generator,
) -> dict[int, str]:
    """Determine decisions for all firms in the current auction.

    The function loops over participating firms and determines whether each
    firm chooses to collude or compete.

    Args:
        participating_firms (list[int]): Firms participating in the auction.
        interaction_memory (dict[tuple[int, int], str]): Pairwise memory of
            previous firm actions.
        round_log (list[dict[str, Any]]): History of previous auction rounds.
        rng (np.random.Generator): Random number generator used for noise.

    Returns:
        dict[int, str]: Mapping of firm_id to decision ("collude" or "compete").
    """
    actions: dict[int, str] = {}

    for firm in participating_firms:
        actions[firm] = decide_action(
            focal_firm=firm,
            participating_firms=participating_firms,
            interaction_memory=interaction_memory,
            round_log=round_log,
            rng=rng,
        )

    return actions

from typing import Any



def _compute_memory_metric(
    focal_firm: int,
    participating_firms: list[int],
    interaction_memory: dict[tuple[int, int], str],
) -> float:
    """This helper function computes the memory metric for one focal firm.

    The metric is the share of current rival firms that the focal firm
    remembers as having colluded the last time they met.

    Args:
        focal_firm (int): The firm whose decision is being evaluated.
        participating_firms (list[int]): Firms participating in the current auction.
        interaction_memory (dict[tuple[int, int], str]): Pairwise memory dictionary
            storing the last remembered action of firm_j from firm_i's perspective.

    Returns:
        float: Share of rival firms remembered as colluders.
    """

    rival_firms = [firm for firm in participating_firms if firm != focal_firm]

    if not rival_firms:
        return 0.0

    n_previous_colluders = 0

    for rival_firm in rival_firms:
        last_action = interaction_memory.get((focal_firm, rival_firm), "compete")

        if last_action == "collude":
            n_previous_colluders += 1

    return n_previous_colluders / len(rival_firms)



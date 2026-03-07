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


def _compute_frequency_metric(
    focal_firm: int,
    participating_firms: list[int],
    round_log: list[dict[str, Any]],
    k: int = 10,
) -> int:
    """This helper function computes the familiarity/frequency metric
      for one focal firm.

    The metric equals 1 if, in at least two-thirds of the last k auctions
    in which the focal firm participated, the current rival firms were a
    subset of the participating firms in those past auctions. Otherwise it
    equals 0.

    Args:
        focal_firm (int): The firm whose decision is being evaluated.
        participating_firms (list[int]): Firms participating in the current auction.
        round_log (list[dict[str, Any]]): Log of previous auction rounds.
        k (int): Number of recent relevant auctions to inspect.

    Returns:
        int: 1 if the current rivals are familiar, 0 otherwise.
    """
    current_rivals = {firm for firm in participating_firms if firm != focal_firm}

    if not current_rivals:
        return 0

    recent_participation_sets: list[set[int]] = []

    for entry in reversed(round_log):
        past_participants = entry.get("participating_firms", [])

        if focal_firm in past_participants:
            past_rivals = {firm for firm in past_participants if firm != focal_firm}
            recent_participation_sets.append(past_rivals)

        if len(recent_participation_sets) == k:
            break

    if len(recent_participation_sets) < k:
        return 0

    n_matches = 0

    for past_rivals in recent_participation_sets:
        if current_rivals.issubset(past_rivals):
            n_matches += 1

    if (n_matches / k) >= (2 / 3):
        return 1

    return 0

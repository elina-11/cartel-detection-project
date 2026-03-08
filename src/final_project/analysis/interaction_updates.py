def _update_interaction_memory(
    participating_firms: list[int],
    actions: dict[int, str],
    interaction_memory: dict[tuple[int, int], str],
) -> None:
    """This helper function updates pairwise memory after an auction round.

    For each focal firm, store the most recent action of every other
    participating firm.

    Args:
        participating_firms (list[int]): Firms participating in the auction.
        actions (dict[int, str]): Mapping of firm_id to action taken
            ("collude" or "compete").
        interaction_memory (dict[tuple[int, int], str]): Pairwise memory of
            the most recent observed action.

    Returns:
        None
    """
    for focal_firm in participating_firms:
        for other_firm in participating_firms:
            if focal_firm != other_firm:
                interaction_memory[(focal_firm, other_firm)] = actions[other_firm]


def _update_interaction_counts(
    participating_firms: list[int],
    interaction_count: dict[tuple[int, int], int],
) -> None:
    """The helper function updates pairwise interaction counts after an auction round.

    For each ordered pair of distinct participating firms, increment the
    count of how many times they have met.

    Args:
        participating_firms (list[int]): Firms participating in the auction.
        interaction_count (dict[tuple[int, int], int]): Pairwise interaction
            counts.

    Returns:
        None
    """
    for focal_firm in participating_firms:
        for other_firm in participating_firms:
            if focal_firm != other_firm:
                pair = (focal_firm, other_firm)
                interaction_count[pair] = interaction_count.get(pair, 0) + 1

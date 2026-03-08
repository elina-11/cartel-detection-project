from final_project.analysis.interaction_updates import (
    _update_interaction_counts,
    _update_interaction_memory,
)

INTERACTION_count = 2


def test_update_interaction_memory_basic() -> None:
    participating_firms = [1, 2, 3]

    actions = {
        1: "collude",
        2: "compete",
        3: "collude",
    }

    interaction_memory = {}

    _update_interaction_memory(
        participating_firms=participating_firms,
        actions=actions,
        interaction_memory=interaction_memory,
    )

    assert interaction_memory[(1, 2)] == "compete"
    assert interaction_memory[(1, 3)] == "collude"
    assert interaction_memory[(2, 1)] == "collude"
    assert interaction_memory[(2, 3)] == "collude"
    assert interaction_memory[(3, 1)] == "collude"
    assert interaction_memory[(3, 2)] == "compete"


def test_update_interaction_memory_overwrites_previous() -> None:
    participating_firms = [1, 2]

    interaction_memory = {
        (1, 2): "collude",
        (2, 1): "collude",
    }

    actions = {
        1: "compete",
        2: "compete",
    }

    _update_interaction_memory(
        participating_firms=participating_firms,
        actions=actions,
        interaction_memory=interaction_memory,
    )

    assert interaction_memory[(1, 2)] == "compete"
    assert interaction_memory[(2, 1)] == "compete"


def test_update_interaction_counts_basic() -> None:
    participating_firms = [1, 2, 3]
    interaction_count = {}

    _update_interaction_counts(
        participating_firms=participating_firms,
        interaction_count=interaction_count,
    )

    assert interaction_count[(1, 2)] == 1
    assert interaction_count[(1, 3)] == 1
    assert interaction_count[(2, 1)] == 1
    assert interaction_count[(2, 3)] == 1
    assert interaction_count[(3, 1)] == 1
    assert interaction_count[(3, 2)] == 1


def test_update_interaction_counts_accumulates() -> None:
    participating_firms = [1, 2]
    interaction_count = {}

    _update_interaction_counts(
        participating_firms=participating_firms,
        interaction_count=interaction_count,
    )

    _update_interaction_counts(
        participating_firms=participating_firms,
        interaction_count=interaction_count,
    )

    assert interaction_count[(1, 2)] == INTERACTION_count
    assert interaction_count[(2, 1)] == INTERACTION_count

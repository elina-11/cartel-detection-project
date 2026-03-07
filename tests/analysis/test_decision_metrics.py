from final_project.analysis.decision_metrics import (
    _compute_frequency_metric,
    _compute_memory_metric,
)

SHARE = 0.5


def test_memory_metric_all_colluded() -> None:
    participating_firms = [1, 2, 3]

    interaction_memory = {
        (1, 2): "collude",
        (1, 3): "collude",
    }

    result = _compute_memory_metric(
        focal_firm=1,
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
    )

    assert result == 1.0


def test_memory_metric_partial_collusion() -> None:
    participating_firms = [1, 2, 3]

    interaction_memory = {
        (1, 2): "collude",
        (1, 3): "compete",
    }

    result = _compute_memory_metric(
        focal_firm=1,
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
    )

    assert result == SHARE


def test_memory_metric_default_compete() -> None:
    participating_firms = [1, 2]

    interaction_memory = {}

    result = _compute_memory_metric(
        focal_firm=1,
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
    )

    assert result == 0.0


def test_frequency_metric_familiar_group() -> None:
    focal_firm = 1
    participating_firms = [1, 2, 3]

    round_log = [{"participating_firms": [1, 2, 3]} for _ in range(10)]

    result = _compute_frequency_metric(
        focal_firm=focal_firm,
        participating_firms=participating_firms,
        round_log=round_log,
        k=10,
    )

    assert result == 1


def test_frequency_metric_insufficient_history() -> None:
    focal_firm = 1
    participating_firms = [1, 2]

    round_log = [
        {"participating_firms": [1, 2]},
        {"participating_firms": [1, 3]},
    ]

    result = _compute_frequency_metric(
        focal_firm=focal_firm,
        participating_firms=participating_firms,
        round_log=round_log,
        k=10,
    )

    assert result == 0

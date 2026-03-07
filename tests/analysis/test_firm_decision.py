import numpy as np

from final_project.analysis.firm_decision import decide_action

SEED = 250


def test_decide_action_collude() -> None:
    rng = np.random.default_rng(SEED)

    participating_firms = [1, 2]

    interaction_memory = {(1, 2): "collude"}

    round_log = []

    result = decide_action(
        focal_firm=1,
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
        round_log=round_log,
        rng=rng,
        noise_std=0.0,
    )

    assert result == "collude"


def test_decide_action_compete() -> None:
    """Firm should compete when memory metric is below threshold."""
    rng = np.random.default_rng(SEED)

    participating_firms = [1, 2]

    interaction_memory = {(1, 2): "compete"}

    round_log = []

    result = decide_action(
        focal_firm=1,
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
        round_log=round_log,
        rng=rng,
        noise_std=0.0,
    )

    assert result == "compete"

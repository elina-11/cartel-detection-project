import numpy as np

from final_project.analysis.auction_decisions import decide_actions_for_auction

SEED = 926


def test_decide_actions_for_auction_returns_actions_for_all_firms() -> None:
    rng = np.random.default_rng(SEED)

    participating_firms = [1, 2]

    interaction_memory = {(1, 2): "collude", (2, 1): "collude"}

    round_log = []

    result = decide_actions_for_auction(
        participating_firms=participating_firms,
        interaction_memory=interaction_memory,
        round_log=round_log,
        rng=rng,
    )

    assert isinstance(result, dict)
    assert set(result.keys()) == {1, 2}
    assert result[1] in {"collude", "compete"}
    assert result[2] in {"collude", "compete"}

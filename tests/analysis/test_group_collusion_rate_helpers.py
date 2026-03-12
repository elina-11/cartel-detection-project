import pandas as pd
import pytest

from final_project.analysis.group_collusion_rate_helpers import (
    _compute_single_group_collusion_rate,
    _recover_group_members,
    _validate_detected_groups,
)

COLLUSION_RATE = 0.5


def test_validate_detected_groups_raises_error() -> None:
    df = pd.DataFrame({"a": [1], "b": [2]})

    with pytest.raises(
        ValueError,
        match="must have exactly these columns",
    ):
        _validate_detected_groups(df)


def test_recover_group_members() -> None:
    df = pd.DataFrame(
        {
            "group_id": [0, 0, 1],
            "firm_id": [1, 2, 3],
        }
    )

    result = _recover_group_members(df)

    assert result == {0: {1, 2}, 1: {3}}


def test_compute_single_group_collusion_rate() -> None:
    group = {1, 2}

    round_log = [
        {
            "participating_firms": [1, 2],
            "collusion_success": True,
        },
        {
            "participating_firms": [1, 2],
            "collusion_success": False,
        },
        {
            "participating_firms": [1, 3],
            "collusion_success": True,
        },
    ]

    result = _compute_single_group_collusion_rate(group, round_log)

    assert result == COLLUSION_RATE

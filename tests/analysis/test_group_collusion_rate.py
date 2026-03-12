import pandas as pd

from final_project.analysis.group_collusion_rate import compute_group_collusion_rates

COLLUSION_RATE = 0.5


def test_compute_group_collusion_rates() -> None:
    groups_df = pd.DataFrame(
        {
            "group_id": [0, 0],
            "firm_id": [1, 2],
        }
    )

    round_log = [
        {
            "participating_firms": [1, 2],
            "collusion_success": True,
        },
        {
            "participating_firms": [1, 2],
            "collusion_success": False,
        },
    ]

    result = compute_group_collusion_rates(groups_df, round_log)

    assert "group_id" in result.columns
    assert "collusion_rate" in result.columns

    assert result.loc[0, "collusion_rate"] == COLLUSION_RATE

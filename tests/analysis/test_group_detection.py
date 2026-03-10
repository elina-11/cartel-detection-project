import pandas as pd

from final_project.analysis.group_detection import detect_groups


def test_detect_groups_returns_dataframe() -> None:
    network_df = pd.DataFrame(
        {
            "firm_id_1": [0, 0, 1, 2],
            "firm_id_2": [1, 2, 2, 3],
            "weight": [0.8, 0.7, 0.9, 0.1],
        }
    )

    result = detect_groups(network_df)

    assert isinstance(result, pd.DataFrame)

    assert set(result.columns) == {"group_id", "firm_id"}

    assert len(result) > 0

    assert result["group_id"].min() == 0

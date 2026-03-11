import pandas as pd

from final_project.analysis.group_features import compute_group_features

RESULT_LENGTH = 2


def test_compute_group_features_returns_dataframe() -> None:
    network_df = pd.DataFrame(
        {
            "firm_id_1": [0, 0, 1, 2],
            "firm_id_2": [1, 2, 2, 3],
            "weight": [0.8, 0.7, 0.9, 0.1],
        }
    )

    groups_df = pd.DataFrame(
        {
            "group_id": [0, 0, 0, 1],
            "firm_id": [0, 1, 2, 3],
        }
    )

    result = compute_group_features(network_df, groups_df)

    assert isinstance(result, pd.DataFrame)

    assert set(result.columns) == {"group_id", "coherence", "exclusivity"}

    assert len(result) == RESULT_LENGTH

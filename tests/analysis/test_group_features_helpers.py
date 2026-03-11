import pandas as pd
import pytest

from final_project.analysis.group_features_helpers import (
    _compute_coherence,
    _compute_exclusivity,
    _compute_group_features_table,
    _compute_single_group_features,
    _get_internal_edge_weights,
    _recover_group_members,
    _validate_detected_groups,
    _validate_group_feature_inputs,
)

RESULT_LENGTH = 2


@pytest.fixture
def network_df() -> pd.DataFrame:
    """Small co-bidding network for testing."""
    return pd.DataFrame(
        {
            "firm_id_1": [0, 0, 1, 2],
            "firm_id_2": [1, 2, 2, 3],
            "weight": [0.8, 0.7, 0.9, 0.1],
        }
    )


@pytest.fixture
def groups_df() -> pd.DataFrame:
    """Detected groups in long format."""
    return pd.DataFrame(
        {
            "group_id": [0, 0, 0, 1],
            "firm_id": [0, 1, 2, 3],
        }
    )


@pytest.fixture
def adjacency():
    """Adjacency dictionary used for group feature tests."""
    return {
        0: {1: 0.8, 2: 0.7},
        1: {0: 0.8, 2: 0.9},
        2: {0: 0.7, 1: 0.9, 3: 0.1},
        3: {2: 0.1},
    }


def test_validate_detected_groups_invalid_columns() -> None:
    invalid_df = pd.DataFrame({"a": [0], "b": [1]})

    error_message = (
        "The detected groups DataFrame must have exactly these columns: "
        "'group_id' and 'firm_id'."
    )

    with pytest.raises(ValueError, match=error_message):
        _validate_detected_groups(invalid_df)


def test_validate_group_feature_inputs(
    network_df: pd.DataFrame, groups_df: pd.DataFrame
) -> None:
    # Should run without raising errors
    _validate_group_feature_inputs(network_df, groups_df)


def test_recover_group_members(groups_df: pd.DataFrame) -> None:
    result = _recover_group_members(groups_df)

    expected = {0: {0, 1, 2}, 1: {3}}

    assert result == expected


def test_get_internal_edge_weights(adjacency) -> None:
    group = {0, 1, 2}

    result = _get_internal_edge_weights(group, adjacency)

    assert sorted(result) == sorted([0.8, 0.7, 0.9])


def test_compute_coherence() -> None:
    weights = [0.8, 0.7, 0.9]

    result = _compute_coherence(weights)

    arithmetic_mean = sum(weights) / len(weights)
    geometric_mean = (0.8 * 0.7 * 0.9) ** (1 / 3)

    expected = geometric_mean / arithmetic_mean

    assert result == pytest.approx(expected)


def test_compute_exclusivity(adjacency) -> None:
    group = {0, 1, 2}

    result = _compute_exclusivity(group, adjacency)

    internal_strength = 2.4
    external_strength = 0.1

    expected = internal_strength / (internal_strength + external_strength)

    assert result == pytest.approx(expected)


def test_compute_single_group_features(adjacency) -> None:
    group = {0, 1, 2}

    coherence, exclusivity = _compute_single_group_features(group, adjacency)

    assert coherence > 0
    assert exclusivity > 0


def test_compute_group_features_table(
    network_df: pd.DataFrame,
    groups_df: pd.DataFrame,
) -> None:
    result = _compute_group_features_table(network_df, groups_df)

    assert isinstance(result, pd.DataFrame)

    assert set(result.columns) == {"group_id", "coherence", "exclusivity"}

    assert len(result) == RESULT_LENGTH

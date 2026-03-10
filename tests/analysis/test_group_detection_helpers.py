import pandas as pd
import pytest

from final_project.analysis.group_detection_helpers import (
    _build_adjacency_dict,
    _compute_external_strength,
    _compute_group_fitness,
    _compute_internal_strength,
    _compute_node_fitness_gain,
    _deduplicate_groups,
    _detect_groups_from_all_seeds,
    _expand_group_from_seed,
    _get_candidate_neighbors,
    _validate_co_bidding_network,
)


@pytest.fixture
def network_df() -> pd.DataFrame:
    """Function creates a small co-bidding network edge list for testing."""
    return pd.DataFrame(
        {
            "firm_id_1": [0, 0, 1, 2],
            "firm_id_2": [1, 2, 2, 3],
            "weight": [0.8, 0.7, 0.9, 0.1],
        }
    )


@pytest.fixture
def adjacency() -> dict[int, dict[int, float]]:
    """This creates a small adjacency dictionary for testing."""
    return {
        0: {1: 0.8, 2: 0.7},
        1: {0: 0.8, 2: 0.9},
        2: {0: 0.7, 1: 0.9, 3: 0.1},
        3: {2: 0.1},
    }


def test_validate_co_bidding_network_raises_error_for_invalid_columns() -> None:
    invalid_df = pd.DataFrame(
        {
            "firm_a": [0],
            "firm_b": [1],
            "weight": [0.5],
        }
    )

    error_message = (
        "The co-bidding network must have exactly these columns: "
        "'firm_id_1', 'firm_id_2', and 'weight'."
    )

    with pytest.raises(ValueError, match=error_message):
        _validate_co_bidding_network(invalid_df)


def test_build_adjacency_dict(network_df: pd.DataFrame) -> None:
    result = _build_adjacency_dict(network_df)

    expected = {
        0: {1: 0.8, 2: 0.7},
        1: {0: 0.8, 2: 0.9},
        2: {0: 0.7, 1: 0.9, 3: 0.1},
        3: {2: 0.1},
    }

    assert result == expected


def test_compute_internal_strength(
    adjacency: dict[int, dict[int, float]],
) -> None:
    group = {0, 1, 2}

    result = _compute_internal_strength(group, adjacency)

    assert result == pytest.approx(2.4)


def test_compute_external_strength(
    adjacency: dict[int, dict[int, float]],
) -> None:
    group = {0, 1, 2}

    result = _compute_external_strength(group, adjacency)

    assert result == pytest.approx(0.1)


def test_compute_group_fitness(
    adjacency: dict[int, dict[int, float]],
) -> None:
    group = {0, 1, 2}

    result = _compute_group_fitness(group, adjacency, alpha=1.5, beta=1.5)

    expected = 2.4 / ((2.5**1.5) * (3**1.5))
    assert result == pytest.approx(expected)


def test_get_candidate_neighbors(
    adjacency: dict[int, dict[int, float]],
) -> None:
    group = {0, 1}

    result = _get_candidate_neighbors(group, adjacency)

    assert result == {2}


def test_compute_node_fitness_gain(
    adjacency: dict[int, dict[int, float]],
) -> None:
    group = {0, 1}
    candidate_node = 2

    result = _compute_node_fitness_gain(
        group=group,
        candidate_node=candidate_node,
        adjacency=adjacency,
        alpha=1.5,
        beta=1.5,
    )

    current_fitness = _compute_group_fitness(
        group={0, 1},
        adjacency=adjacency,
        alpha=1.5,
        beta=1.5,
    )
    expanded_fitness = _compute_group_fitness(
        group={0, 1, 2},
        adjacency=adjacency,
        alpha=1.5,
        beta=1.5,
    )
    expected = expanded_fitness - current_fitness

    assert result == pytest.approx(expected)
    assert result > 0


def test_expand_group_from_seed(
    adjacency: dict[int, dict[int, float]],
) -> None:
    result = _expand_group_from_seed(
        seed_node=0,
        adjacency=adjacency,
        alpha=1.5,
        beta=1.5,
    )

    assert result == {0, 1, 2}


def test_detect_groups_from_all_seeds(
    adjacency: dict[int, dict[int, float]],
) -> None:
    result = _detect_groups_from_all_seeds(
        adjacency=adjacency,
        alpha=1.5,
        beta=1.5,
    )

    expected = [{0, 1, 2}, {0, 1, 2}, {0, 1, 2}, {0, 1, 2, 3}]
    assert result == expected


def test_deduplicate_groups() -> None:
    groups = [{0, 1, 2}, {0, 1, 2}, {0, 1, 2}, {3}]

    result = _deduplicate_groups(groups)

    assert result == [{0, 1, 2}]

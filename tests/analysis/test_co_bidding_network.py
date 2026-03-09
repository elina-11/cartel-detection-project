import pandas as pd
import pytest

from final_project.analysis.auction_framework import SimulationState
from final_project.analysis.co_bidding_network import (
    _build_firm_contract_sets,
    _compute_jaccard_weight,
    build_co_bidding_network,
)


@pytest.fixture
def empty_state() -> SimulationState:
    """Create an empty simulation state for testing."""
    firms_df = pd.DataFrame(
        {
            "firm_id": [0, 1, 2, 3],
            "x": [0.1, 0.2, 0.3, 0.4],
            "y": [0.1, 0.2, 0.3, 0.4],
        }
    )
    issuers_df = pd.DataFrame(
        {
            "issuer_id": [0, 1],
            "x": [0.5, 0.6],
            "y": [0.5, 0.6],
        }
    )
    return SimulationState(firms_df=firms_df, issuers_df=issuers_df)


@pytest.fixture
def state_with_round_log(empty_state: SimulationState) -> SimulationState:
    """Create a simulation state with a small retained round log."""
    empty_state.round_log = [
        {
            "round_number": 1001,
            "issuer_id": 0,
            "contract_x": 0.2,
            "contract_y": 0.2,
            "participating_firms": [0, 1, 2],
            "radius_used": 0.1,
            "actions": {0: "collude", 1: "compete", 2: "collude"},
            "collusion_success": False,
        },
        {
            "round_number": 1002,
            "issuer_id": 1,
            "contract_x": 0.7,
            "contract_y": 0.7,
            "participating_firms": [1, 2],
            "radius_used": 0.1,
            "actions": {1: "collude", 2: "collude"},
            "collusion_success": True,
        },
        {
            "round_number": 1003,
            "issuer_id": 0,
            "contract_x": 0.4,
            "contract_y": 0.4,
            "participating_firms": [0, 2],
            "radius_used": 0.1,
            "actions": {0: "compete", 2: "collude"},
            "collusion_success": False,
        },
        {
            "round_number": 1004,
            "issuer_id": 1,
            "contract_x": 0.9,
            "contract_y": 0.9,
            "participating_firms": [3],
            "radius_used": 0.2,
            "actions": {3: "compete"},
            "collusion_success": False,
        },
    ]
    return empty_state


def test_build_firm_contract_sets(
    state_with_round_log: SimulationState,
) -> None:
    firm_contracts = _build_firm_contract_sets(state_with_round_log.round_log)

    expected = {
        0: {1001, 1003},
        1: {1001, 1002},
        2: {1001, 1002, 1003},
        3: {1004},
    }

    assert firm_contracts == expected


@pytest.mark.parametrize(
    ("contracts_a", "contracts_b", "expected_weight"),
    [
        ({1, 2, 3}, {2, 3, 4}, 2 / 4),
        ({1, 2}, {1, 2}, 1.0),
        ({1, 2}, {3, 4}, 0.0),
        (set(), set(), 0.0),
    ],
)
def test_compute_jaccard_weight(
    contracts_a: set[int],
    contracts_b: set[int],
    expected_weight: float,
) -> None:
    result = _compute_jaccard_weight(
        contracts_a=contracts_a,
        contracts_b=contracts_b,
    )

    assert result == expected_weight


def test_build_co_bidding_network_returns_expected_columns(
    state_with_round_log: SimulationState,
) -> None:
    network_df = build_co_bidding_network(state_with_round_log)

    expected_columns = ["firm_id_1", "firm_id_2", "weight"]
    assert list(network_df.columns) == expected_columns


def test_build_co_bidding_network_skips_single_firm_rounds(
    state_with_round_log: SimulationState,
) -> None:
    network_df = build_co_bidding_network(state_with_round_log)

    observed_edges = {
        (row.firm_id_1, row.firm_id_2) for row in network_df.itertuples(index=False)
    }

    assert (3, 0) not in observed_edges
    assert (0, 3) not in observed_edges
    assert (1, 3) not in observed_edges
    assert (2, 3) not in observed_edges


def test_build_co_bidding_network_returns_expected_edges_and_weights(
    state_with_round_log: SimulationState,
) -> None:
    network_df = build_co_bidding_network(state_with_round_log)

    observed = {
        (row.firm_id_1, row.firm_id_2): row.weight
        for row in network_df.itertuples(index=False)
    }

    expected = {
        (0, 1): 1 / 3,  # {1001,1003} ∩ {1001,1002} = 1, union = 3
        (0, 2): 2 / 3,  # {1001,1003} ∩ {1001,1002,1003} = 2, union = 3
        (1, 2): 2 / 3,  # {1001,1002} ∩ {1001,1002,1003} = 2, union = 3
    }

    assert observed.keys() == expected.keys()

    for edge, expected_weight in expected.items():
        assert observed[edge] == expected_weight


def test_build_co_bidding_network_returns_empty_dataframe_for_empty_log(
    empty_state: SimulationState,
) -> None:
    network_df = build_co_bidding_network(empty_state)

    assert isinstance(network_df, pd.DataFrame)
    assert list(network_df.columns) == ["firm_id_1", "firm_id_2", "weight"]
    assert network_df.empty

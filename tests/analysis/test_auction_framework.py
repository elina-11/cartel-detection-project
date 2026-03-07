import numpy as np
import pandas as pd
import pytest

from final_project.analysis.auction_framework import (
    SimulationState,
    run_simulation,
    run_single_round,
)
from final_project.analysis.create_firms_and_issuers import create_firms, create_issuers

N_FIRMS = 20
N_ISSUERS = 5
FIRM_SEED = 67
ISSUER_SEED = 42
SIMULATION_SEED = 246
MIN_RADIUS = 0.1
N_ROUNDS = 3


@pytest.fixture
def firms_df() -> pd.DataFrame:
    """The function creates a small DataFrame for testing."""
    return create_firms(n_firms=N_FIRMS, seed=FIRM_SEED)


@pytest.fixture
def issuers_df() -> pd.DataFrame:
    """The function creates a small issuers DataFrame for testing."""
    return create_issuers(n_issuers=N_ISSUERS, seed=ISSUER_SEED)


@pytest.fixture
def state(firms_df: pd.DataFrame, issuers_df: pd.DataFrame) -> SimulationState:
    """The function initialises the simulation state."""
    return SimulationState(firms_df=firms_df, issuers_df=issuers_df)


def test_simulation_state_initialization(
    state: SimulationState,
    firms_df: pd.DataFrame,
    issuers_df: pd.DataFrame,
) -> None:
    pd.testing.assert_frame_equal(state.firms_df, firms_df)
    pd.testing.assert_frame_equal(state.issuers_df, issuers_df)

    # Checks if memory and interaction counts are empty dictionaries
    assert isinstance(state.interaction_memory, dict)
    assert state.interaction_memory == {}

    assert isinstance(state.interaction_count, dict)
    assert state.interaction_count == {}

    # Checks if round log is empty list
    assert isinstance(state.round_log, list)
    assert state.round_log == []


def test_run_single_round_logs_information(state: SimulationState) -> None:
    rng = np.random.default_rng(seed=SIMULATION_SEED)

    run_single_round(round_number=1, state=state, rng=rng)

    assert len(state.round_log) == 1

    log_entry = state.round_log[0]

    expected_keys = {
        "round_number",
        "issuer_id",
        "contract_x",
        "contract_y",
        "participating_firms",
        "radius_used",
        "memory_metrics",
        "frequency_metrics",
    }

    assert set(log_entry.keys()) == expected_keys
    assert isinstance(log_entry["participating_firms"], list)
    assert log_entry["radius_used"] >= MIN_RADIUS
    assert isinstance(log_entry["memory_metrics"], dict)
    assert isinstance(log_entry["frequency_metrics"], dict)

    for firm in log_entry["participating_firms"]:
        assert firm in log_entry["memory_metrics"]
        assert firm in log_entry["frequency_metrics"]
        assert 0.0 <= log_entry["memory_metrics"][firm] <= 1.0
        assert log_entry["frequency_metrics"][firm] in {0, 1}


def test_run_simulation_runs(state: SimulationState) -> None:
    # Run for 3 rounds to test
    updated_state = run_simulation(n_rounds=3, state=state, seed=SIMULATION_SEED)

    # It should return a SimulationState object
    assert isinstance(updated_state, SimulationState)

    # After 3 rounds we should have 3 log entries
    assert len(updated_state.round_log) == N_ROUNDS

    for entry in updated_state.round_log:
        assert set(entry.keys()) == {
            "round_number",
            "issuer_id",
            "contract_x",
            "contract_y",
            "participating_firms",
            "radius_used",
            "memory_metrics",
            "frequency_metrics",
        }
        assert isinstance(entry["participating_firms"], list)
        assert isinstance(entry["memory_metrics"], dict)
        assert isinstance(entry["frequency_metrics"], dict)

        for firm in entry["participating_firms"]:
            assert firm in entry["memory_metrics"]
            assert firm in entry["frequency_metrics"]
            assert 0.0 <= entry["memory_metrics"][firm] <= 1.0
            assert entry["frequency_metrics"][firm] in {0, 1}

    # Memory and interaction counts still empty since not yet implemented(placeholder)
    assert updated_state.interaction_memory == {}
    assert updated_state.interaction_count == {}

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
        "actions",
        "collusion_success",
    }

    assert set(log_entry.keys()) == expected_keys
    assert isinstance(log_entry["participating_firms"], list)
    assert log_entry["radius_used"] >= MIN_RADIUS
    assert isinstance(log_entry["actions"], dict)
    assert isinstance(log_entry["collusion_success"], bool)

    for firm in log_entry["participating_firms"]:
        assert firm in log_entry["actions"]
        assert log_entry["actions"][firm] in {"collude", "compete"}

    if len(log_entry["participating_firms"]) > 1:
        assert state.interaction_memory != {}
        assert state.interaction_count != {}


def test_run_simulation_runs(state: SimulationState) -> None:
    updated_state = run_simulation(n_rounds=N_ROUNDS, state=state, seed=SIMULATION_SEED)

    assert isinstance(updated_state, SimulationState)

    assert len(updated_state.round_log) == N_ROUNDS

    for entry in updated_state.round_log:
        assert set(entry.keys()) == {
            "round_number",
            "issuer_id",
            "contract_x",
            "contract_y",
            "participating_firms",
            "radius_used",
            "actions",
            "collusion_success",
        }
        assert isinstance(entry["participating_firms"], list)
        assert isinstance(entry["actions"], dict)
        assert isinstance(entry["collusion_success"], bool)

        for firm in entry["participating_firms"]:
            assert firm in entry["actions"]
            assert entry["actions"][firm] in {"collude", "compete"}

    # Memory and interaction counts should not be empty anymore
    if any(len(entry["participating_firms"]) > 1 for entry in updated_state.round_log):
        assert updated_state.interaction_memory != {}
        assert updated_state.interaction_count != {}

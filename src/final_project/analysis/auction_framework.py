from typing import Any

import numpy as np
import pandas as pd


class SimulationState:
    """Stores the evolving state of the simulation."""

    def __init__(self, firms_df: pd.DataFrame, issuers_df: pd.DataFrame):
        self.firms_df = firms_df
        self.issuers_df = issuers_df
        self.interaction_memory: dict[
            tuple[int, int], list[str]
        ] = {}  # Memory of past interactions: {(firm_i, firm_j): [decisions]}
        self.interaction_count: dict[
            tuple[int, int], int
        ] = {}  # Count of interactions between firms
        self.round_log: list[dict[str, Any]] = []  # Log of all rounds


def run_single_round(
    round_number: int, state: SimulationState, rng: np.random.Generator
) -> None:
    """Placeholder for one auction round.

    In later steps, this will:
    - Select a random issuer
    - Generate contract location
    - Compute participating firms
    - Decide if firms collude or compete
    - Update memory and interaction counts
    """


def run_simulation(
    n_rounds: int, state: SimulationState, seed: int = 42
) -> SimulationState:
    """Run the auction simulation for n_rounds.

    Args:
        n_rounds (int) : Number of auction rounds to simulate.
        state (SimulationState) : Object storing the evolving state of the simulation.
        seed (int) : Random seed for reproducibility.

    Returns:
        SimulationState : Updated state after running all rounds.
    """
    rng = np.random.default_rng(seed)

    for round_number in range(1, n_rounds + 1):
        run_single_round(round_number, state, rng)

    return state

from typing import Any

import numpy as np
import pandas as pd

from final_project.analysis.contract_generation import generate_contract_near_issuer

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
    """This will run one auction round.

    Now this step:
    - Selects a random issuer
    - Generates a contract location near the issuer within the unit square
    - logs the generated contract information in the state.
    
    Later the function will also:
    - Compute participating firms
    - Decide if firms collude or compete
    - Update memory and interaction counts
    """
    contract = generate_contract_near_issuer(state.issuers_df, rng)
    state.round_log.append(
        {
            "round_number": round_number,
            "issuer_id": contract["issuer_id"],
            "contract_x": contract["contract_x"],
            "contract_y": contract["contract_y"],
        }
    )
    
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

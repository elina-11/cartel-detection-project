from typing import Any

import numpy as np
import pandas as pd

from final_project.analysis.auction_decisions import (
    collusion_success,
    decide_actions_for_auction,
)
from final_project.analysis.contract_generation import generate_contract_near_issuer
from final_project.analysis.firm_participation import select_participating_firms


class SimulationState:
    """Stores the evolving state of the simulation."""

    def __init__(self, firms_df: pd.DataFrame, issuers_df: pd.DataFrame):
        self.firms_df = firms_df
        self.issuers_df = issuers_df
        self.interaction_memory: dict[tuple[int, int], str] = {}
        self.interaction_count: dict[tuple[int, int], int] = {}
        self.round_log: list[dict[str, Any]] = []


def run_single_round(
    round_number: int, state: SimulationState, rng: np.random.Generator
) -> None:
    """This will run one auction round.

    Now this step:
    - Selects a random issuer
    - Generates a contract location near the issuer within the unit square
    - Selects participating firms based on the distance from the contract
    - Computes memory and frequency metrics for participating firms
    - logs the generated contract information in the state.
    - Decides if firms collude or compete

    Later the function will also:

    - Update memory and interaction counts
    """
    contract = generate_contract_near_issuer(state.issuers_df, rng)
    participation = select_participating_firms(
        state.firms_df,
        contract_x=contract["contract_x"],
        contract_y=contract["contract_y"],
    )
    participating_firms = participation["participating_firms"]

    actions = decide_actions_for_auction(
        participating_firms=participating_firms,
        interaction_memory=state.interaction_memory,
        round_log=state.round_log,
        rng=rng,
    )

    collusion_outcome = collusion_success(actions)

    state.round_log.append(
        {
            "round_number": round_number,
            "issuer_id": contract["issuer_id"],
            "contract_x": contract["contract_x"],
            "contract_y": contract["contract_y"],
            "participating_firms": participating_firms,
            "radius_used": participation["radius_used"],
            "actions": actions,
            "collusion_success": collusion_outcome,
        }
    )


def run_simulation(
    n_rounds: int, state: SimulationState, seed: int = 42
) -> SimulationState:
    """This function runs the auction simulation for n_rounds.

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

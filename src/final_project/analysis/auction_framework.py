from typing import Any

import numpy as np
import pandas as pd

from final_project.analysis.auction_decisions import (
    collusion_success,
    decide_actions_for_auction,
)
from final_project.analysis.contract_generation import generate_contract_near_issuer
from final_project.analysis.firm_participation import select_participating_firms
from final_project.analysis.interaction_updates import (
    _update_interaction_counts,
    _update_interaction_memory,
)


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

    This step:
    - Selects a random issuer
    - Generates a contract location near the issuer within the unit square
    - Selects participating firms based on the distance from the contract
    - Computes memory and frequency metrics for participating firms
    - logs the generated contract information in the state.
    - Decides if firms collude or competes
    - Updates memory and interaction counts
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
    _update_interaction_memory(
        participating_firms=participating_firms,
        actions=actions,
        interaction_memory=state.interaction_memory,
    )

    _update_interaction_counts(
        participating_firms=participating_firms,
        interaction_count=state.interaction_count,
    )

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
    n_rounds: int,
    state: SimulationState,
    seed: int = 42,
    burn_in_rounds: int = 0,
) -> SimulationState:
    """This function runs the auction simulation for n_rounds.

    Firms are learning during the burn-in period.
    After the simulation ends the first burn_in_round outcomes are
    discarded from round log.

    Args:
        n_rounds (int) : Number of auction rounds to simulate.
        state (SimulationState) : Object storing the evolving state of the simulation.
        seed (int) : Random seed for reproducibility.
        burn_in_rounds (int) : Number of initial rounds to discard from
        recorded outcomes after simulation completes.

    Returns:
        SimulationState : Updated state after running all rounds.
    """
    if burn_in_rounds < 0:
        msg = "burn_in_rounds must be non-negative."
        raise ValueError(msg)
    if burn_in_rounds > n_rounds:
        msg = "burn_in_rounds cannot exceed n_rounds."
        raise ValueError(msg)

    rng = np.random.default_rng(seed)

    for round_number in range(1, n_rounds + 1):
        run_single_round(round_number, state, rng)

    if burn_in_rounds > 0:
        state.round_log = state.round_log[burn_in_rounds:]

    return state

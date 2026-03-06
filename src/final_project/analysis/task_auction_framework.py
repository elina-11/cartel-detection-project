from pathlib import Path

import pandas as pd

from final_project.analysis.auction_framework import SimulationState, run_simulation
from final_project.analysis.create_firms_and_issuers import create_firms, create_issuers
from final_project.config import BLD, SRC

N_FIRMS: int = 50
N_ISSUERS: int = 75
FIRMS_SEED: int = 42
ISSUERS_SEED: int = 24
SIMULATION_SEED: int = 246
N_ROUNDS: int = 3


def task_run_auction_simulation(
    depends_on: dict[str, Path] = {
        "auction_framework": SRC / "analysis" / "auction_framework.py",
        "create_firms_and_issuers": SRC / "analysis" / "create_firms_and_issuers.py",
        "contract_generation" : SRC / "analysis" / "contract_generation.py", 
        "participation" : SRC / "analysis" / "participation.py"

    },
    produces: Path = BLD / "data" / "simulation_state.pickle",
) -> None:
    """The function initializes the simulation state with firms and issuers,
    runs a few rounds of the auction framework, and saves the state.
    """
    # Generating firms and issuers
    firms_df = create_firms(n_firms=N_FIRMS, seed=FIRMS_SEED)
    issuers_df = create_issuers(n_issuers=N_ISSUERS, seed=ISSUERS_SEED)

    # Initialising simulation state
    state = SimulationState(firms_df=firms_df, issuers_df=issuers_df)

    # Running the simulation
    updated_state = run_simulation(n_rounds=N_ROUNDS, state=state, seed=SIMULATION_SEED)

    # Ensuring output directory exists
    produces.parent.mkdir(parents=True, exist_ok=True)

    # Saving the SimulationState object directly
    pd.to_pickle(updated_state, produces)

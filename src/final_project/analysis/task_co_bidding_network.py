from pathlib import Path

import pandas as pd

from final_project.analysis.co_bidding_network import build_co_bidding_network
from final_project.config import BLD


def task_build_co_bidding_network(
    simulation_state: Path = BLD / "data" / "simulation_state.pickle",
    produces: Path = BLD / "data" / "co_bidding_network.pickle",
) -> None:
    """Build weighted co-bidding network from simulated auction history."""
    state = pd.read_pickle(simulation_state)
    co_bidding_network = build_co_bidding_network(state)

    produces.parent.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(co_bidding_network, produces)

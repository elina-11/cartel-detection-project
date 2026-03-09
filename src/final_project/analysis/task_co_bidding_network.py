from pathlib import Path

import pandas as pd

from final_project.analysis.co_bidding_network import build_co_bidding_network
from final_project.config import BLD, SRC


def task_build_co_bidding_network(
    depends_on: dict[str, Path] | None = None,
    produces: Path = BLD / "data" / "co_bidding_network.pickle",
) -> None:
    """Function builds weighted co-bidding network from simulated auction history."""
    if depends_on is None:
        depends_on = {
            "simulation_state": BLD / "data" / "simulation_state.pickle",
            "co_bidding_network": SRC / "analysis" / "co_bidding_network.py",
        }

    simulation_state = pd.read_pickle(depends_on["simulation_state"])
    co_bidding_network = build_co_bidding_network(simulation_state)

    produces.parent.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(co_bidding_network, produces)

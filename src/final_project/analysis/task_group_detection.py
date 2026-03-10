from pathlib import Path

import pandas as pd

from final_project.analysis.group_detection import detect_groups
from final_project.config import BLD


def task_detect_groups(
    co_bidding_network: Path = BLD / "data" / "co_bidding_network.pickle",
    produces: Path = BLD / "data" / "detected_groups.pickle",
) -> None:
    """Detect groups of firms from the co-bidding network."""
    network_df = pd.read_pickle(co_bidding_network)
    detected_groups = detect_groups(network_df)

    produces.parent.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(detected_groups, produces)

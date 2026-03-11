from pathlib import Path

import pandas as pd

from final_project.analysis.group_features import compute_group_features
from final_project.config import BLD


def task_compute_group_features(
    co_bidding_network: Path = BLD / "data" / "co_bidding_network.pickle",
    detected_groups: Path = BLD / "data" / "detected_groups.pickle",
    produces: Path = BLD / "data" / "group_features.pickle",
) -> None:
    """Compute group-level features for detected groups."""
    network_df = pd.read_pickle(co_bidding_network)
    groups_df = pd.read_pickle(detected_groups)

    group_features = compute_group_features(network_df, groups_df)

    produces.parent.mkdir(parents=True, exist_ok=True)

    pd.to_pickle(group_features, produces)

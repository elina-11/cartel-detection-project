import pandas as pd

from final_project.analysis.group_detection_helpers import (
    _build_adjacency_dict,
    _deduplicate_groups,
    _detect_groups_from_all_seeds,
    _validate_co_bidding_network,
)


def detect_groups(
    network_df: pd.DataFrame,
    alpha: float = 1.5,
    beta: float = 1.5,
) -> pd.DataFrame:
    """Function detects overlapping groups of firms from the co-bidding network."""
    _validate_co_bidding_network(network_df)

    adjacency = _build_adjacency_dict(network_df)

    raw_groups = _detect_groups_from_all_seeds(
        adjacency=adjacency,
        alpha=alpha,
        beta=beta,
    )

    unique_groups = _deduplicate_groups(raw_groups)

    rows: list[dict[str, int]] = []

    for group_id, group in enumerate(sorted(unique_groups, key=lambda g: sorted(g))):
        rows.extend(
            {
                "group_id": group_id,
                "firm_id": firm_id,
            }
            for firm_id in sorted(group)
        )

    return pd.DataFrame(rows, columns=["group_id", "firm_id"])

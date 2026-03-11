from __future__ import annotations

from typing import Any

import pandas as pd

from final_project.analysis.group_collusion_rate_helpers import (
    _compute_single_group_collusion_rate,
    _recover_group_members,
    _validate_detected_groups,
)


def compute_group_collusion_rates(
    groups_df: pd.DataFrame,
    round_log: list[dict[str, Any]],
) -> pd.DataFrame:
    """Function computes collusion rates for all detected groups.

    Args:
        groups_df (pd.DataFrame): Long-format detected groups table.
        round_log (list[dict[str, Any]]): Retained simulation rounds.

    Returns:
        pd.DataFrame: DataFrame with columns ['group_id', 'collusion_rate'].
    """
    _validate_detected_groups(groups_df)

    group_members = _recover_group_members(groups_df)

    rows: list[dict[str, float | int]] = []

    for group_id, group in group_members.items():
        collusion_rate = _compute_single_group_collusion_rate(group, round_log)
        rows.append(
            {
                "group_id": group_id,
                "collusion_rate": collusion_rate,
            }
        )

    return pd.DataFrame(rows, columns=["group_id", "collusion_rate"])

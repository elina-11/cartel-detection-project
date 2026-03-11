from __future__ import annotations

from typing import Any

import pandas as pd


def _validate_detected_groups(groups_df: pd.DataFrame) -> None:
    """Helper function validates the detected groups DataFrame."""
    required_columns = {"group_id", "firm_id"}
    observed_columns = set(groups_df.columns)

    if observed_columns != required_columns:
        msg = (
            "The detected groups DataFrame must have exactly these columns: "
            "'group_id' and 'firm_id'."
        )
        raise ValueError(msg)


def _recover_group_members(groups_df: pd.DataFrame) -> dict[int, set[int]]:
    """Recovers group membership sets from the long-format groups DataFrame."""
    grouped = groups_df.groupby("group_id")["firm_id"]

    return {
        int(group_id): {int(firm_id) for firm_id in firm_ids}
        for group_id, firm_ids in grouped
    }


def _is_group_only_round(
    participating_firms: list[int],
    group: set[int],
) -> bool:
    """Checks whether all participating firms belong to the detected group."""
    return set(participating_firms).issubset(group) and len(participating_firms) > 1


def _compute_single_group_collusion_rate(
    group: set[int],
    round_log: list[dict[str, Any]],
) -> float:
    """Helper function computes collusion rate for one detected group.

    The denominator is the number of rounds where all participating firms
    belong to the group and there is more than one participant.
    The numerator is the number of such rounds with successful collusion.
    """
    relevant_rounds = 0
    successful_rounds = 0

    for entry in round_log:
        participating_firms = entry["participating_firms"]

        if _is_group_only_round(participating_firms, group):
            relevant_rounds += 1

            if entry["collusion_success"]:
                successful_rounds += 1

    if relevant_rounds == 0:
        return 0.0

    return successful_rounds / relevant_rounds

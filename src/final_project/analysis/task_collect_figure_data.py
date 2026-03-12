from __future__ import annotations

from pathlib import Path

import pandas as pd

from final_project.analysis.auction_framework import SimulationState, run_simulation
from final_project.analysis.co_bidding_network import build_co_bidding_network
from final_project.analysis.create_firms_and_issuers import create_firms, create_issuers
from final_project.analysis.group_collusion_rate import compute_group_collusion_rates
from final_project.analysis.group_detection import detect_groups
from final_project.analysis.group_features import compute_group_features
from final_project.config import (
    BLD,
    BURN_IN_ROUNDS,
    FIRMS_SEED_BASE,
    ISSUERS_SEED_BASE,
    N_FIRMS,
    N_ISSUERS,
    N_ROUNDS,
    N_SIMULATIONS,
    SIMULATION_SEED_BASE,
    SRC,
)


def task_collect_figure_data(
    auction_framework_source: Path = SRC / "analysis" / "auction_framework.py",
    create_firms_and_issuers_source: Path = (
        SRC / "analysis" / "create_firms_and_issuers.py"
    ),
    co_bidding_network_source: Path = SRC / "analysis" / "co_bidding_network.py",
    group_detection_source: Path = SRC / "analysis" / "group_detection.py",
    group_detection_helpers_source: Path = (
        SRC / "analysis" / "group_detection_helpers.py"
    ),
    group_features_source: Path = SRC / "analysis" / "group_features.py",
    group_features_helpers_source: Path = (
        SRC / "analysis" / "group_features_helpers.py"
    ),
    group_collusion_rate_source: Path = SRC / "analysis" / "group_collusion_rate.py",
    group_collusion_rate_helpers_source: Path = (
        SRC / "analysis" / "group_collusion_rate_helpers.py"
    ),
    produces: Path = BLD / "data" / "heatmap_data.pickle",
) -> None:
    """Runs 100 simulations and collect group-level data for final figures."""
    _ = (
        auction_framework_source,
        create_firms_and_issuers_source,
        co_bidding_network_source,
        group_detection_source,
        group_detection_helpers_source,
        group_features_source,
        group_features_helpers_source,
        group_collusion_rate_source,
        group_collusion_rate_helpers_source,
    )

    all_rows: list[pd.DataFrame] = []

    for simulation_id in range(N_SIMULATIONS):
        firms_df = create_firms(
            n_firms=N_FIRMS,
            seed=FIRMS_SEED_BASE + simulation_id,
        )
        issuers_df = create_issuers(
            n_issuers=N_ISSUERS,
            seed=ISSUERS_SEED_BASE + simulation_id,
        )

        state = SimulationState(firms_df=firms_df, issuers_df=issuers_df)

        state = run_simulation(
            n_rounds=N_ROUNDS,
            state=state,
            seed=SIMULATION_SEED_BASE + simulation_id,
            burn_in_rounds=BURN_IN_ROUNDS,
        )

        network_df = build_co_bidding_network(state)
        groups_df = detect_groups(network_df)

        if groups_df.empty:
            continue

        features_df = compute_group_features(network_df, groups_df)
        collusion_df = compute_group_collusion_rates(groups_df, state.round_log)

        merged_df = features_df.merge(collusion_df, on="group_id", how="left")
        merged_df["simulation_id"] = simulation_id

        all_rows.append(merged_df)

    if all_rows:
        heatmap_data = pd.concat(all_rows, ignore_index=True)
    else:
        heatmap_data = pd.DataFrame(
            columns=[
                "group_id",
                "coherence",
                "exclusivity",
                "collusion_rate",
                "simulation_id",
            ]
        )

    produces.parent.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(heatmap_data, produces)

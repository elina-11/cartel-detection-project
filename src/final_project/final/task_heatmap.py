from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD, SRC
from final_project.final.heatmap import generate_figure_a, generate_figure_b


def task_generate_figure_a(
    group_data: Path = BLD / "data" / "heatmap_data.pickle",
    figure_source: Path = SRC / "final" / "heatmap.py",
    heatmap_helpers_source: Path = SRC / "final" / "heatmap_helpers.py",
    produces: Path = BLD / "figures" / "figure_a.png",
) -> None:
    """Generates Figure A."""
    _ = figure_source, heatmap_helpers_source

    df = pd.read_pickle(group_data)
    fig = generate_figure_a(df)

    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=300, bbox_inches="tight")
    plt.close(fig)


def task_generate_figure_b(
    group_data: Path = BLD / "data" / "heatmap_data.pickle",
    figure_source: Path = SRC / "final" / "heatmap.py",
    heatmap_helpers_source: Path = SRC / "final" / "heatmap_helpers.py",
    produces: Path = BLD / "figures" / "figure_b.png",
) -> None:
    """Generate Figure B."""
    _ = figure_source, heatmap_helpers_source

    df = pd.read_pickle(group_data)
    fig = generate_figure_b(df)

    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=300, bbox_inches="tight")
    plt.close(fig)

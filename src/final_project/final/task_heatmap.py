from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD, SRC
from final_project.final.heatmap import generate_figure


def task_generate_figure_3a(
    group_features: Path = BLD / "data" / "group_features.pickle",
    figure_3_source: Path = SRC / "final" / "heatmap.py",
    figure_3_helpers_source: Path = SRC / "final" / "heatmap_helpers.py",
    produces: Path = BLD / "figures" / "figure_3a.png",
) -> None:
    """Generate Figure 3A heatmap."""
    _ = figure_3_source, figure_3_helpers_source

    df = pd.read_pickle(group_features)
    fig = generate_figure(df)

    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=300, bbox_inches="tight")

    plt.close(fig)

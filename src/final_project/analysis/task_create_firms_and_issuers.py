from pathlib import Path

from final_project.analysis.create_firms_and_issuers import create_firms, create_issuers
from final_project.config import BLD, SRC

N_FIRMS: int = 50
N_ISSUERS: int = 75
FIRMS_SEED: int = 42
ISSUERS_SEED: int = 24


def task_create_firms(
    script: Path = SRC / "analysis" / "create_firms_and_issuers.py",
    produces: Path = BLD / "data" / "firms.pickle",
) -> None:
    """Create firms and save them to build folder."""
    firms = create_firms(n_firms=N_FIRMS, seed=FIRMS_SEED)
    firms.to_pickle(produces)


def task_create_issuers(
    script: Path = SRC / "analysis" / "create_firms_and_issuers.py",
    produces: Path = BLD / "data" / "issuers.pickle",
) -> None:
    """Create issuers and save them to the build folder."""
    issuers = create_issuers(n_issuers=N_ISSUERS, seed=ISSUERS_SEED)
    issuers.to_pickle(produces)

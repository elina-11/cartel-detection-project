"""All the general configuration of the project."""

from pathlib import Path

SRC: Path = Path(__file__).parent.resolve()
ROOT: Path = SRC.joinpath("..", "..").resolve()

BLD: Path = ROOT.joinpath("bld").resolve()


DOCUMENTS: Path = ROOT.joinpath("documents").resolve()

TEMPLATE_GROUPS: tuple[str, ...] = ("marital_status", "highest_qualification")

# Simulation structure
N_FIRMS: int = 50
N_ISSUERS: int = 75
N_ROUNDS: int = 2000
BURN_IN_ROUNDS: int = 1000
N_SIMULATIONS: int = 100

# Fixed seeds for deterministic generation
FIRMS_SEED: int = 42
ISSUERS_SEED: int = 24

# Seeds used for simulation loops
FIRMS_SEED_BASE: int = 1000
ISSUERS_SEED_BASE: int = 2000
SIMULATION_SEED_BASE: int = 3000

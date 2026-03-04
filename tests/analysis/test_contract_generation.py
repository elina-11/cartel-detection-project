import numpy as np

from final_project.analysis.contract_generation import generate_contract_near_issuer
from final_project.analysis.create_firms_and_issuers import create_issuers

N_ISSUERS = 5
ISSUER_SEED = 42
RNG_SEED = 246


def test_contract_generation_structure() -> None:
    """The function checks if the returned object has the correct structure."""

    issuers_df = create_issuers(n_issuers=N_ISSUERS, seed=ISSUER_SEED)
    rng = np.random.default_rng(RNG_SEED)

    contract = generate_contract_near_issuer(issuers_df, rng)

    assert isinstance(contract, dict)
    assert set(contract.keys()) == {"issuer_id", "contract_x", "contract_y"}


def test_contract_coordinates_within_unit_square() -> None:
    """The function checks if contract coordinates lie within [0,1] range."""

    issuers_df = create_issuers(n_issuers=N_ISSUERS, seed=ISSUER_SEED)
    rng = np.random.default_rng(RNG_SEED)

    contract = generate_contract_near_issuer(issuers_df, rng)

    assert 0 <= contract["contract_x"] <= 1
    assert 0 <= contract["contract_y"] <= 1


def test_contract_generation_reproducibility() -> None:
    """The function checks if the function is reproducible with the same RNG seed."""

    issuers_df = create_issuers(n_issuers=N_ISSUERS, seed=ISSUER_SEED)

    rng1 = np.random.default_rng(RNG_SEED)
    rng2 = np.random.default_rng(RNG_SEED)

    contract1 = generate_contract_near_issuer(issuers_df, rng1)
    contract2 = generate_contract_near_issuer(issuers_df, rng2)

    assert contract1 == contract2

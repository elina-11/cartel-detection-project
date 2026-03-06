import pandas as pd
import pytest

from final_project.analysis.firm_participation import (
    _compute_firm_distances,
    select_participating_firms,
)

@pytest.fixture
def firms_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "firm_id": [0, 1, 2],
            "x": [0.0, 0.3, 0.9],
            "y": [0.0, 0.4, 0.9],
        }
    )

def test_compute_firm_distances_structure(firms_df: pd.DataFrame) -> None:
    distances = _compute_firm_distances(
        firms_df=firms_df,
        contract_x=0.0,
        contract_y=0.0,
    )

    assert isinstance(distances, pd.Series)
    assert distances.index.tolist() == [0, 1, 2]


def test_compute_firm_distances_values(firms_df: pd.DataFrame) -> None:
    distances = _compute_firm_distances(
        firms_df=firms_df,
        contract_x=0.0,
        contract_y=0.0,
    )

    assert distances.loc[0] == pytest.approx(0.0)
    assert distances.loc[1] == pytest.approx(0.5)
    assert distances.loc[2] == pytest.approx((0.9**2 + 0.9**2) ** 0.5)


def test_select_participating_firms_without_radius_expansion(
    firms_df: pd.DataFrame,
) -> None:
    result = select_participating_firms(
        firms_df=firms_df,
        contract_x=0.0,
        contract_y=0.0,
        initial_radius=0.5,
        radius_increment=0.1,
    )

    assert isinstance(result, dict)
    assert set(result.keys()) == {"participating_firms", "radius_used"}
    assert result["participating_firms"] == [0, 1]
    assert result["radius_used"] == pytest.approx(0.5)


def test_select_participating_firms_with_radius_expansion(
    firms_df: pd.DataFrame,
) -> None:
    result = select_participating_firms(
        firms_df=firms_df,
        contract_x=0.6,
        contract_y=0.6,
        initial_radius=0.1,
        radius_increment=0.1,
    )

    assert isinstance(result, dict)
    assert len(result["participating_firms"]) >= 1
    assert result["radius_used"] > 0.1


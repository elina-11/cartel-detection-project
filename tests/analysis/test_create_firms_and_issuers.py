import pandas as pd
import pytest

from final_project.analysis.create_firms_and_issuers import create_firms, create_issuers


@pytest.fixture
def firms_df() -> pd.DataFrame:
    """This function creates a reusable firms DataFrame."""
    return create_firms(n_firms=50, seed=42)


@pytest.fixture
def issuers_df() -> pd.DataFrame:
    """This function creates a reusable issuers DataFrame."""
    return create_issuers(n_issuers=30, seed=24)


def test_create_firm_structure(firms_df: pd.Dataframe) -> None:
    assert firms_df.shape == (50, 3)
    assert list(firms_df.columns) == ["firm_id", "x", "y"]
    assert firms_df["firm_id"].tolist() == list(range(50))


def test_create_firms_coordinates_range(firms_df: pd.DataFrame) -> None:
    assert firms_df["x"].between(0, 1).all()
    assert firms_df["y"].between(0, 1).all()


def test_create_issuers_structures(issuers_df: pd.DataFrame) -> None:
    assert issuers_df.shape == (30, 3)
    assert list(issuers_df.columns) == ["issuer_id", "x", "y"]
    assert issuers_df["issuer_id"].tolist() == list(range(30))


def test_create_issuers_coordinats_range(issuers_df: pd.DataFrame) -> None:
    assert issuers_df["x"].between(0, 1).all()
    assert issuers_df["y"].between(0, 1).all()

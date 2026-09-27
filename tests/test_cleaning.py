import numpy as np
import pandas as pd

from data.cleaning import (
    add_missing_indicators,
    duplicate_combination_summary,
    duplicate_transaction_id_count,
    exact_duplicate_count,
    log1p_feature,
    missingness_summary,
    numeric_outlier_summary,
    replace_empty_strings_with_na,
    row_missingness_summary,
)


def test_missingness_summary():
    df = pd.DataFrame(
        {
            "a": [1, np.nan, 3],
            "b": ["x", "y", "z"],
        }
    )

    result = missingness_summary(df)

    assert result.loc["a", "missing_count"] == 1
    assert result.loc["a", "missing_rate"] == 1 / 3
    assert result.loc["b", "missing_count"] == 0


def test_row_missingness_summary():
    df = pd.DataFrame(
        {
            "a": [1, np.nan],
            "b": [np.nan, "x"],
        }
    )

    result = row_missingness_summary(df)

    assert result.loc[0, "missing_count"] == 1
    assert result.loc[1, "missing_count"] == 1


def test_add_missing_indicators():
    df = pd.DataFrame(
        {
            "amount": [100, np.nan, 300],
        }
    )

    result = add_missing_indicators(
        df,
        ["amount"],
    )

    assert result["amount_missing"].tolist() == [0, 1, 0]
    assert result["amount"].isna().sum() == 1


def test_exact_duplicate_count():
    df = pd.DataFrame(
        {
            "x": [1, 1, 2],
            "y": ["a", "a", "b"],
        }
    )

    assert exact_duplicate_count(df) == 1


def test_duplicate_transaction_id_count():
    df = pd.DataFrame(
        {
            "TransactionID": [1, 2, 2, 3],
        }
    )

    assert duplicate_transaction_id_count(df) == 1


def test_numeric_outlier_summary():
    df = pd.DataFrame(
        {
            "amount": [10, 11, 12, 13, 14, 1000],
        }
    )

    result = numeric_outlier_summary(
        df,
        "amount",
    )

    assert result["outlier_count"] >= 1
    assert 0 < result["outlier_rate"] <= 1


def test_log1p_feature():
    df = pd.DataFrame(
        {
            "amount": [0, 1, 9],
        }
    )

    result = log1p_feature(
        df,
        "amount",
    )

    expected = np.log1p([0, 1, 9])

    assert np.allclose(
        result["amount_log1p"],
        expected,
    )

    assert result["amount"].tolist() == [0, 1, 9]


def test_replace_empty_strings_with_na():
    df = pd.DataFrame(
        {
            "category": ["A", "", "B"],
        }
    )

    result = replace_empty_strings_with_na(df)

    assert result["category"].isna().sum() == 1


def test_duplicate_combination_summary():
    df = pd.DataFrame(
        {
            "card1": [100, 100, 100, 200],
            "addr1": [10, 10, 10, 20],
            "amount": [50, 70, 90, 100],
        }
    )

    result = duplicate_combination_summary(
        df,
        ["card1", "addr1"],
    )

    assert result["duplicated_rows"] == 3
    assert result["duplicated_groups"] == 1
    assert result["largest_group_size"] == 3

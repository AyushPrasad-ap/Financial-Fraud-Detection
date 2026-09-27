from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


def missingness_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return column-level missing-value statistics.

    The returned table contains:
    - missing_count
    - missing_rate
    """
    missing_count = df.isna().sum()

    summary = pd.DataFrame(
        {
            "missing_count": missing_count,
            "missing_rate": df.isna().mean(),
        }
    )

    return summary.sort_values("missing_rate", ascending=False)


def row_missingness_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return per-row missing-value counts and rates.
    """
    result = pd.DataFrame(index=df.index)

    result["missing_count"] = df.isna().sum(axis=1)
    result["missing_rate"] = df.isna().mean(axis=1)

    return result


def add_missing_indicators(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """
    Add binary missing-value indicators for selected columns.

    The original columns are left unchanged.
    """
    result = df.copy()

    for column in columns:
        if column not in result.columns:
            raise KeyError(f"Column not found: {column}")

        result[f"{column}_missing"] = result[column].isna().astype("int8")

    return result


def exact_duplicate_count(df: pd.DataFrame) -> int:
    """Return the number of exact duplicate rows."""
    return int(df.duplicated().sum())


def duplicate_transaction_id_count(
    df: pd.DataFrame,
) -> int:
    """Return the number of duplicate TransactionID rows."""
    if "TransactionID" not in df.columns:
        raise KeyError("TransactionID column not found.")

    return int(df["TransactionID"].duplicated().sum())


def numeric_outlier_summary(
    df: pd.DataFrame,
    column: str,
) -> dict[str, float]:
    """
    Summarize a numeric feature using the IQR rule.

    This function identifies potential outliers for investigation.
    It does NOT remove them.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    series = pd.to_numeric(df[column], errors="coerce").dropna()

    if series.empty:
        raise ValueError(f"No valid numeric values found for column: {column}")

    q1 = float(series.quantile(0.25))
    q3 = float(series.quantile(0.75))
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outlier_mask = (series < lower_bound) | (series > upper_bound)

    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": int(outlier_mask.sum()),
        "outlier_rate": float(outlier_mask.mean()),
    }


def log1p_feature(
    df: pd.DataFrame,
    source_column: str,
    output_column: str | None = None,
) -> pd.DataFrame:
    """
    Create a log1p-transformed copy of a non-negative numeric feature.

    This is an explicit transformation utility; it does not overwrite
    the original feature.
    """
    if source_column not in df.columns:
        raise KeyError(f"Column not found: {source_column}")

    values = pd.to_numeric(df[source_column], errors="coerce")

    if (values.dropna() < 0).any():
        raise ValueError(
            f"{source_column} contains negative values; "
            "log1p transformation is not valid."
        )

    result = df.copy()

    if output_column is None:
        output_column = f"{source_column}_log1p"

    result[output_column] = np.log1p(values)

    return result


def replace_empty_strings_with_na(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Replace truly empty strings in object/string columns with missing values.

    Whitespace-only strings are intentionally not changed automatically;
    their treatment should be established from the audit.
    """
    result = df.copy()

    object_columns = result.select_dtypes(include=["object", "string"]).columns

    for column in object_columns:
        result[column] = result[column].replace("", pd.NA)

    return result


def duplicate_combination_summary(
    df: pd.DataFrame,
    columns: list[str],
) -> dict[str, object]:
    """
    Analyze repeated combinations of selected columns.

    The target column should generally not be included in `columns`.
    The function reports how many rows belong to repeated combinations
    and how many distinct duplicated groups exist.
    """
    missing_columns = [column for column in columns if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Columns not found: {missing_columns}")

    duplicated_mask = df.duplicated(
        subset=columns,
        keep=False,
    )

    duplicated_rows = df.loc[duplicated_mask, columns]

    if duplicated_rows.empty:
        return {
            "columns": columns,
            "duplicated_rows": 0,
            "duplicated_row_rate": 0.0,
            "duplicated_groups": 0,
            "largest_group_size": 0,
        }

    group_sizes = duplicated_rows.groupby(columns, dropna=False).size()

    return {
        "columns": columns,
        "duplicated_rows": int(duplicated_mask.sum()),
        "duplicated_row_rate": float(duplicated_mask.mean()),
        "duplicated_groups": len(group_sizes),
        "largest_group_size": int(group_sizes.max()),
    }

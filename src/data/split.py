from pathlib import Path
from textwrap import dedent

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
REPORTS_DIR = PROJECT_ROOT / "reports"

INPUT_PATH = INTERIM_DIR / "train_merged.csv"
REPORT_PATH = REPORTS_DIR / "split_strategy.md"


TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


def validate_ratios() -> None:
    """Ensure the split ratios sum to 1."""
    total = TRAIN_RATIO + VALIDATION_RATIO + TEST_RATIO

    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Split ratios must sum to 1.0, got {total:.6f}")


def create_temporal_split() -> None:
    """Create and document a chronological train/validation/test split."""

    validate_ratios()

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing merged dataset: {INPUT_PATH}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading merged dataset...")
    df = pd.read_csv(INPUT_PATH)

    required_columns = {"TransactionID", "TransactionDT", "isFraud"}

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if df["TransactionDT"].isna().any():
        raise ValueError("TransactionDT contains missing values.")

    if df["TransactionID"].duplicated().any():
        raise ValueError("TransactionID is not unique.")

    print("Sorting chronologically...")
    df = df.sort_values("TransactionDT").reset_index(drop=True)

    n_rows = len(df)

    train_end = int(n_rows * TRAIN_RATIO)
    validation_end = int(n_rows * (TRAIN_RATIO + VALIDATION_RATIO))

    train = df.iloc[:train_end]
    validation = df.iloc[train_end:validation_end]
    test = df.iloc[validation_end:]

    splits = {
        "train": train,
        "validation": validation,
        "test": test,
    }

    summary = []

    for name, split_df in splits.items():
        summary.append(
            {
                "split": name,
                "rows": len(split_df),
                "percentage": len(split_df) / n_rows * 100,
                "transaction_dt_min": split_df["TransactionDT"].min(),
                "transaction_dt_max": split_df["TransactionDT"].max(),
                "fraud_count": int(split_df["isFraud"].sum()),
                "fraud_rate": split_df["isFraud"].mean() * 100,
            }
        )

    summary_df = pd.DataFrame(summary)

    report = dedent("""
        # Train / Validation / Test Split Strategy

        ## 1. Objective

        The dataset is divided chronologically using `TransactionDT` rather than using a random train/test split.

        This prevents information from future transaction periods from entering the training data and better reflects the time-dependent nature of fraud detection.

        ## 2. Split Ratios

        The project uses the following initial chronological split:

        - Train: 70%
        - Validation: 15%
        - Final Test: 15%

        The data is sorted by `TransactionDT` in ascending order before the split.

        ## 3. Split Definition

        | Split | Rows | Percentage | TransactionDT Min | TransactionDT Max | Fraud Count | Fraud Rate |
        |---|---:|---:|---:|---:|---:|---:|
    """).lstrip()

    for row in summary:
        report += (
            f"| {row['split']} | "
            f"{row['rows']:,} | "
            f"{row['percentage']:.2f}% | "
            f"{row['transaction_dt_min']:,} | "
            f"{row['transaction_dt_max']:,} | "
            f"{row['fraud_count']:,} | "
            f"{row['fraud_rate']:.4f}% |\n"
        )

    report += (
        dedent("""
        
        ## 4. Validation Strategy

        The project uses two evaluation layers:

        1. A final chronological holdout consisting of the last 15% of transactions.
        2. Temporal cross-validation performed inside the training period.

        The final test set must remain untouched during:

        - feature selection
        - model selection
        - hyperparameter tuning
        - threshold selection
        - preprocessing design decisions

        ## 5. Temporal Cross-Validation

        After the final holdout is established, temporal cross-validation will be performed within the training period using expanding historical windows.

        Conceptually:

        ```text
        Fold 1:
        TRAIN ───────────────► VALID

        Fold 2:
        TRAIN ─────────────────────► VALID

        Fold 3:
        TRAIN ───────────────────────────────► VALID

        Fold 4:
        TRAIN ───────────────────────────────────────► VALID
        ```

        This allows the project to evaluate whether model performance remains stable as the temporal horizon moves forward.

        ## 6. Leakage Prevention

        All learned preprocessing and feature statistics must be fitted only using the historical data available to the corresponding training portion.

        Examples include:

        - imputation statistics
        - scaling parameters
        - category mappings
        - frequency encoding
        - target encoding
        - historical behavioral features
        - resampling

        Future observations and labels must not influence earlier predictions.

        ## 7. Advanced Robustness Check

        Because IEEE-CIS does not provide a clean customer identifier, a later optional experiment may construct a proxy entity key from selected card, address, and email-related fields.

        This experiment is intended to measure entity overlap across temporal splits.

        It must not be interpreted as true customer-level generalization because the original dataset does not provide a clean customer identifier.

        ## 8. Conclusion

        The final evaluation design is intentionally chronological:

        ```text
        PAST                                              FUTURE

        |---------------- TRAIN ----------------|-- VAL --|-- TEST --|
                         70%                       15%        15%
        ```

        The final test set represents the latest transaction period and will be reserved for the final unseen evaluation.
    """).strip()
        + "\n"
    )

    REPORT_PATH.write_text(report, encoding="utf-8")

    print("\nTemporal split created successfully.")
    print(summary_df.to_string(index=False))
    print(f"\nReport written to: {REPORT_PATH}")


if __name__ == "__main__":
    create_temporal_split()

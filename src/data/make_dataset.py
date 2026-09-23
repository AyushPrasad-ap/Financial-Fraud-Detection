from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"

TRANSACTION_PATH = RAW_DIR / "train_transaction.csv"
IDENTITY_PATH = RAW_DIR / "train_identity.csv"

OUTPUT_PATH = INTERIM_DIR / "train_merged.csv"


def make_dataset() -> None:
    """Create the reproducible interim transaction-level dataset."""

    if not TRANSACTION_PATH.exists():
        raise FileNotFoundError(f"Missing transaction dataset: {TRANSACTION_PATH}")

    if not IDENTITY_PATH.exists():
        raise FileNotFoundError(f"Missing identity dataset: {IDENTITY_PATH}")

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading transaction data...")
    transactions = pd.read_csv(TRANSACTION_PATH)

    print("Loading identity data...")
    identity = pd.read_csv(IDENTITY_PATH)

    print("Joining datasets...")
    merged = transactions.merge(
        identity,
        on="TransactionID",
        how="left",
    )

    print(f"Transaction rows: {len(transactions):,}")
    print(f"Identity rows: {len(identity):,}")
    print(f"Merged rows: {len(merged):,}")
    print(f"Merged columns: {len(merged.columns):,}")

    merged.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved interim dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    make_dataset()

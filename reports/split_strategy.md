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
| train | 413,378 | 70.00% | 86,400 | 10,437,996 | 14,538 | 3.5169% |
| validation | 88,581 | 15.00% | 10,438,003 | 13,151,840 | 3,042 | 3.4341% |
| test | 88,581 | 15.00% | 13,151,880 | 15,811,131 | 3,083 | 3.4804% |
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

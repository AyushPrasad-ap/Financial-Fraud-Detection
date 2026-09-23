# Data Audit — IEEE-CIS Fraud Detection

## 1. Dataset Overview

The project uses the IEEE-CIS Fraud Detection training data, consisting of two related tables:

- `train_transaction.csv`
- `train_identity.csv`

The two tables were loaded independently and joined on `TransactionID` using a left join. The transaction table contains the target variable `isFraud`.

The audit was performed on the resulting transaction-level dataset without applying preprocessing, imputation, encoding, scaling, outlier removal, or feature engineering.

---

## 2. Dataset Size

### Source tables

| Dataset | Rows | Columns |
|---|---:|---:|
| `train_transaction.csv` | 590,540 | 394 |
| `train_identity.csv` | 144,233 | 41 |

### Joined dataset

| Attribute | Result |
|---|---:|
| Rows | 590,540 |
| Columns | 434 |
| Total cells | 256,294,360 |

The left join preserves all 590,540 transactions.

The identity table contains 144,233 unique `TransactionID` values. Relative to the 590,540 transactions, this corresponds to approximately **24.42%** of transactions having a matching identity record, leaving approximately **75.58%** without a corresponding identity row.

---

## 3. Schema and Data Types

### Joined dataset

The joined dataset contains:

| Data type | Count |
|---|---:|
| `float64` | 399 |
| `int64` | 4 |
| `str` | 31 |
| **Total** | **434** |

From semantic column groups identified during the audit:

| Feature group | Count |
|---|---:|
| Numeric columns | 403 |
| Categorical/string columns | 31 |

The numerical columns include the transaction target and ordering variables (`isFraud`, `TransactionDT`), transaction amount, card/address variables, the `C*`, `D*`, and `V*` feature groups, and numerical identity variables.

The categorical columns include transaction-level categorical variables as well as identity/device information.

### Categorical columns

The audit identified the following 31 categorical/string columns:

```text
ProductCD
card4
card6
P_emaildomain
R_emaildomain
M1
M2
M3
M4
M5
M6
M7
M8
M9
id_12
id_15
id_16
id_23
id_27
id_28
id_29
id_30
id_31
id_33
id_34
id_35
id_36
id_37
id_38
DeviceType
DeviceInfo
```

---

## 4. Missingness

Missingness is substantial in the joined dataset.

| Missingness statistic | Result |
|---|---:|
| Columns containing missing values | 414 / 434 |
| Total missing values | 115,523,073 |
| Total cells | 256,294,360 |
| Overall missing-cell percentage | 45.07% |

This means that nearly half of all cells in the joined dataset are missing.

### Top 30 columns by missing percentage

| Rank | Column | Missing % |
|---:|---|---:|
| 1 | `id_24` | 99.1962% |
| 2 | `id_25` | 99.1310% |
| 3 | `id_07` | 99.1271% |
| 4 | `id_08` | 99.1271% |
| 5 | `id_21` | 99.1264% |
| 6 | `id_26` | 99.1257% |
| 7 | `id_27` | 99.1247% |
| 8 | `id_23` | 99.1247% |
| 9 | `id_22` | 99.1247% |
| 10 | `dist2` | 93.6284% |
| 11 | `D7` | 93.4099% |
| 12 | `id_18` | 92.3607% |
| 13 | `D13` | 89.5093% |
| 14 | `D14` | 89.4695% |
| 15 | `D12` | 89.0410% |
| 16 | `id_04` | 88.7689% |
| 17 | `id_03` | 88.7689% |
| 18 | `D6` | 87.6068% |
| 19 | `id_33` | 87.5895% |
| 20 | `id_09` | 87.3123% |
| 21 | `D8` | 87.3123% |
| 22 | `id_10` | 87.3123% |
| 23 | `D9` | 87.3123% |
| 24 | `id_30` | 86.8654% |
| 25 | `id_32` | 86.8619% |
| 26 | `id_34` | 86.8248% |
| 27 | `id_14` | 86.4456% |
| 28 | `V138` | 86.1237% |
| 29 | `V139` | 86.1237% |
| 30 | `V148` | 86.1237% |

Missing values are therefore not a minor cleanup issue. Their distribution will need to be investigated by feature group, class, and time period in later phases.

The identity table's incomplete coverage is also relevant: the presence or absence of identity information may itself become a useful feature later.

**No missing values were imputed or removed during this audit.**

---

## 5. Cardinality

The number of distinct values was calculated for every column, including missing values as a distinct state (`dropna=False`).

### Cardinality summary

| Statistic | Unique-value count |
|---|---:|
| Number of audited columns | 434 |
| Minimum | 2 |
| 25th percentile | 10 |
| Median | 42.5 |
| 75th percentile | 827.25 |
| Maximum | 590,540 |

### Highest-cardinality columns

| Rank | Column | Unique values |
|---:|---|---:|
| 1 | `TransactionID` | 590,540 |
| 2 | `TransactionDT` | 573,349 |
| 3 | `id_02` | 115,656 |
| 4 | `V307` | 37,368 |
| 5 | `V127` | 24,415 |
| 6 | `V308` | 23,065 |
| 7 | `TransactionAmt` | 20,902 |
| 8 | `V310` | 19,137 |
| 9 | `V306` | 16,211 |
| 10 | `V317` | 15,185 |
| 11 | `V203` | 14,952 |
| 12 | `V128` | 14,508 |
| 13 | `card1` | 13,553 |
| 14 | `V264` | 13,359 |
| 15 | `V204` | 12,859 |
| 16 | `D8` | 12,354 |
| 17 | `V130` | 12,333 |
| 18 | `V318` | 12,310 |
| 19 | `V265` | 11,758 |
| 20 | `V314` | 11,378 |

`TransactionID` is uniquely identified for every transaction and is therefore an obvious identifier candidate rather than a normal predictive feature.

`TransactionDT` also has very high cardinality and represents elapsed time, making it a temporal variable rather than a conventional categorical feature.

Other high-cardinality variables will require further investigation before deciding how they should be represented in subsequent modeling phases.

---

## 6. Target Distribution

The target variable is `isFraud`.

### Class counts

| `isFraud` | Transactions | Proportion |
|---:|---:|---:|
| 0 | 569,877 | 96.5010% |
| 1 | 20,663 | 3.4990% |
| **Total** | **590,540** | **100.0000%** |

The observed fraud rate is:

**3.4990%**

The dataset is therefore strongly imbalanced, with legitimate transactions representing the large majority of observations.

This confirms that ordinary accuracy cannot be treated as the sole indicator of model quality. Later phases will explicitly investigate precision, recall, F1, ROC-AUC, Average Precision / PR-AUC, false-positive behavior, and operational threshold performance.

---

## 7. Duplicate Analysis

### TransactionID duplicates

| Dataset | Duplicate `TransactionID` values |
|---|---:|
| `train_transaction` | 0 |
| `train_identity` | 0 |

Both source tables therefore have unique `TransactionID` values.

### Exact duplicate rows

In the joined dataset:

| Check | Result |
|---|---:|
| Exact duplicate rows | 0 |

No exact duplicate rows were observed during the audit.

This does not imply that all repeated feature combinations are duplicates. Entity-level or feature-level repetitions require separate investigation in later phases.

---

## 8. Numerical Statistics

Selected summary statistics from the joined dataset include:

| Feature | Mean | Median | Std. Dev. | Min | Max |
|---|---:|---:|---:|---:|---:|
| `TransactionAmt` | 135.0272 | 68.7690 | 239.1625 | 0.2510 | 31,937.3910 |
| `TransactionDT` | 7,372,311.31 | 7,306,527.50 | 4,617,223.65 | 86,400 | 15,811,131 |
| `card1` | 9,898.73 | 9,678.00 | 4,901.17 | 1,000 | 18,396 |
| `card2` | 362.56 | 361.00 | 157.79 | 100 | 600 |
| `card3` | 153.19 | 150.00 | 11.34 | 100 | 231 |
| `card5` | 199.28 | 226.00 | 41.24 | 100 | 237 |

`TransactionAmt` has a substantially higher mean than median and a large maximum relative to its central tendency, indicating substantial dispersion and a likely right-skewed distribution. This will be investigated more carefully during EDA rather than assuming a transformation at this stage.

---

## 9. Categorical Features

The audit identified 31 categorical/string features.

Examples include:

- `ProductCD`
- `card4`
- `card6`
- `P_emaildomain`
- `R_emaildomain`
- `DeviceType`
- `DeviceInfo`
- identity categorical variables such as `id_30`, `id_31`, `id_33`, and `id_34`
- binary/match-style variables such as `M1`–`M9` and several `id_*` fields

These variables will require different treatment depending on cardinality and semantic role. Low-cardinality variables may be suitable for one-hot encoding, while high-cardinality variables may require frequency encoding or carefully implemented target encoding in later phases.

No encoding was performed during this audit.

---

## 10. Potential Identifier Columns

### `TransactionID`

`TransactionID` has:

```text
590,540 unique values
590,540 total rows
```

and therefore uniquely identifies every transaction in the training data.

It should be treated as an identifier candidate rather than a normal predictive feature unless a later analysis establishes a documented reason to retain it.

### `TransactionDT`

`TransactionDT` has 573,349 unique values and represents elapsed time from a reference point.

It should be treated primarily as a temporal variable. It must not be interpreted as a real calendar timestamp without an appropriate reference.

### Other high-cardinality variables

Columns such as `id_02`, `V307`, `V127`, `V308`, and several other `V*` variables have substantial cardinality. High cardinality alone does not establish that a column is an identifier, so these variables require further analysis rather than automatic removal.

---

## 11. Potential Leakage Considerations

No explicit target leakage was established during this audit.

However, several areas require careful treatment in later phases:

1. Statistics used for frequency encoding must be fitted using training/history available before the observations being transformed.
2. Historical behavioral features must use only past information.
3. Target encoding must not use validation or test labels to construct model inputs.
4. The final test set must remain untouched during feature selection, hyperparameter tuning, threshold selection, and model selection.
5. Any resampling must occur only within the training process.

`TransactionID` is also a potential identifier feature and should not be included automatically simply because it is present in the raw data.

---

## 12. Temporal Structure

`TransactionDT` provides the primary temporal ordering variable used in this project.

Observed range:

| Statistic | Value |
|---|---:|
| Minimum `TransactionDT` | 86,400 |
| 25th percentile | 3,027,057.75 |
| Median | 7,306,527.50 |
| 75th percentile | 11,246,620 |
| Maximum | 15,811,131 |

The first ten observed transactions show increasing `TransactionDT` values, confirming that the variable provides a meaningful ordering of observations.

The project will therefore use time-aware validation rather than relying on a random split. A detailed chronological train/validation/test strategy belongs to the next phases.

No calendar conversion was applied during this audit.

---

## 13. Class Imbalance

The observed fraud rate is **3.4990%**, meaning approximately 96.5% of transactions are legitimate and 3.5% are fraudulent.

This confirms severe class imbalance for the purposes of this project.

The imbalance has several implications:

- Accuracy can be misleading.
- False negatives and false positives have different operational consequences.
- Precision and recall must both be evaluated.
- Average Precision / PR-AUC will be emphasized for ranking quality.
- Threshold selection will need to be treated as a separate operational decision.
- Class-weighting and resampling strategies will be experimentally evaluated later.

No imbalance treatment was applied during Phase 2.

---

## 14. Initial Findings

The completed audit establishes the following key characteristics:

1. The transaction dataset contains **590,540 observations and 394 columns** before joining.
2. The identity dataset contains **144,233 observations and 41 columns**.
3. The joined transaction-level dataset contains **590,540 rows and 434 columns**.
4. The join is performed on unique `TransactionID` values.
5. There are **no exact duplicate rows** in the joined dataset.
6. Missingness is extensive: **414 of 434 columns** contain missing values, accounting for **45.07% of all cells**.
7. The dataset contains **403 numeric** and **31 categorical/string** columns under the audit's dtype classification.
8. `TransactionID` is fully unique and is therefore an obvious identifier candidate.
9. `TransactionDT` provides the temporal ordering and should be preserved for time-aware analysis.
10. The target is strongly imbalanced, with **20,663 fraud cases (3.4990%)**.
11. `TransactionAmt` shows substantial dispersion and a likely right-skewed distribution.
12. The incomplete identity-table coverage is itself an important property to investigate as part of missingness analysis.

These findings provide the basis for the data-cleaning, EDA, temporal validation, feature-engineering, and leakage-prevention decisions in subsequent phases.

---

## 15. Phase 2 Conclusions

Phase 2 establishes the structure and quality characteristics of the raw IEEE-CIS training data without modifying it.

The dataset is large, heterogeneous, highly incomplete, strongly imbalanced, and temporally structured. It contains both low- and high-cardinality variables and an explicit transaction identifier.

The most important implications for subsequent phases are:

```text
High missingness
        ↓
Investigate missingness patterns
        ↓
Design leakage-safe imputation + missing indicators

High cardinality
        ↓
Investigate encoding strategies
        ↓
Use train-only statistics

Strong class imbalance
        ↓
Use appropriate fraud metrics
        ↓
Evaluate class-weighting/resampling experimentally

Temporal structure
        ↓
Chronological splitting
        ↓
Time-aware validation

Potential identifiers / leakage
        ↓
Explicit feature-role analysis
        ↓
Avoid future information
```

No preprocessing or modeling decisions are finalized from this audit alone. They will be tested experimentally in later phases.

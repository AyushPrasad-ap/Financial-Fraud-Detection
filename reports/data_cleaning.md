# Data Cleaning Report

## Phase 5 — Data Cleaning

This report documents the data-cleaning analysis.

---

# 1. Phase 5.1 — Missing Values

## 1.1 Objective

The objective of this analysis was to understand the missing-data structure of the IEEE-CIS Fraud Detection dataset before deciding how missing values should be handled.

The analysis examined missingness at multiple levels:

- column
- row
- fraud class
- identity availability
- time period
- feature group
- individual feature

No rows were dropped and no imputation was performed during this analysis.

---

## 1.2 Overall Missingness

The joined dataset contains:

| Attribute | Result |
|---|---:|
| Rows | 590,540 |
| Columns | 434 |
| Columns containing missing values | 414 |
| Columns without missing values | 20 |
| Total missing cells | 115,523,073 |
| Overall missing-cell rate | 45.07% |

Approximately 45% of all cells in the dataset are missing.

This establishes that missingness is a fundamental characteristic of the dataset rather than a small number of isolated data-quality issues.

### Decision

A blanket `dropna()` strategy is not appropriate for this dataset because it would discard a substantial amount of transaction information.

---

## 1.3 Column-Level Missingness

The most incomplete features identified during the audit were:

| Feature | Missing Count | Missing Rate |
|---|---:|---:|
| `id_24` | 585,793 | 99.1962% |
| `id_25` | 585,408 | 99.1310% |
| `id_07` | 585,385 | 99.1271% |
| `id_08` | 585,385 | 99.1271% |
| `id_21` | 585,381 | 99.1264% |
| `id_26` | 585,377 | 99.1257% |
| `id_27` | 585,371 | 99.1247% |
| `id_23` | 585,371 | 99.1247% |
| `id_22` | 585,371 | 99.1247% |
| `dist2` | 552,913 | 93.6284% |
| `D7` | 551,623 | 93.4099% |
| `id_18` | 545,427 | 92.3607% |
| `D13` | 528,588 | 89.5093% |
| `D14` | 528,353 | 89.4695% |
| `D12` | 525,823 | 89.0410% |

The full analysis identified **9 features with at least 95% missingness**:

```text
id_24
id_25
id_07
id_08
id_21
id_26
id_27
id_23
id_22
```

### Decision

These features are considered **extremely sparse candidates for later investigation**, but they are not automatically removed at this stage.

High missingness alone is not sufficient evidence that a feature is useless.

---

## 1.4 Row-Level Missingness

Row-level missingness was also analyzed.

| Statistic | Missing values per row | Missing-rate per row |
|---|---:|---:|
| Mean | 195.62 | 45.07% |
| Minimum | 24 | 5.53% |
| 25th percentile | 208 | 47.93% |
| Median | 211 | 48.62% |
| 75th percentile | 229 | 52.77% |
| Maximum | 340 | 78.34% |

This shows that missingness is widespread across individual transactions as well. It is not confined to a small set of anomalous rows.

### Decision

Rows will not be removed simply because they contain many missing values.

---

## 1.5 Missingness by Fraud Class

Average missingness differs between the two target classes:

| Class | Average missingness |
|---|---:|
| Legitimate (`isFraud = 0`) | 45.4626% |
| Fraudulent (`isFraud = 1`) | 37.3436% |

The difference is approximately **8.12 percentage points**.

This demonstrates that the pattern of missing information is associated with the target class in this dataset.

This is an observational relationship and should not be interpreted as evidence that missingness causes fraud.

### Decision

Missingness should not automatically be treated as meaningless noise. Missingness patterns are potential predictive information and should be preserved for later modeling experiments.

---

## 1.6 Identity Availability

The identity table does not contain information for every transaction. To examine the effect of this explicitly, an `identity_available` indicator was defined as whether at least one `id_*` feature is non-missing.

| Identity information | Transactions | Fraud Count | Fraud Rate |
|---|---:|---:|---:|
| Unavailable | 446,307 | 9,345 | 2.0939% |
| Available | 144,233 | 11,318 | 7.8470% |

The observed fraud rate is therefore substantially different depending on whether identity information is available.

### Decision

`identity_available` is retained as a **candidate engineered feature** for later experimentation.

It is not yet declared part of the final feature set.

---

## 1.7 Missingness Over Time

The dataset was divided into four temporal quartiles using `TransactionDT` to investigate whether overall missingness changes across the transaction timeline.

| Time period | Overall missingness | Fraud rate |
|---|---:|---:|
| Q1 — Earliest | 42.14% | 2.63% |
| Q2 | 46.55% | 4.07% |
| Q3 | 45.80% | 3.84% |
| Q4 — Latest | 45.39% | 3.45% |

Missingness is therefore not perfectly constant over time.

The earliest quarter has noticeably lower overall missingness than the later periods.

### Decision

Missingness should be evaluated with the project's temporal structure in mind. A feature or missingness pattern should not be assumed to be equally stable across all periods without validation.

---

## 1.8 Missingness by Feature Group

Missingness was aggregated across the main feature families.

| Feature Group | Feature Count | Mean Missingness | Median Missingness | Maximum Missingness |
|---|---:|---:|---:|---:|
| Identity | 38 | 84.82% | 82.44% | 99.20% |
| `D*` features | 17 | 60.49% | 76.16% | 93.41% |
| `M*` features | 9 | 49.92% | 47.66% | 59.35% |
| `V*` features | 339 | 43.04% | 47.29% | 86.12% |
| Other | 11 | 22.37% | 0.00% | 93.63% |
| Address | 2 | 11.13% | 11.13% | 11.13% |
| Card | 6 | 0.51% | 0.27% | 1.51% |
| `C*` features | 14 | 0.00% | 0.00% | 0.00% |

Missingness is therefore strongly heterogeneous across feature families.

Identity features are especially sparse, while the card and `C*` feature groups have very little missingness.

### Decision

A single universal missing-value treatment should **not** be applied to every feature. Missing-value handling should depend on feature type, sparsity, and the role of the feature.

---

## 1.9 Feature-Level Missingness Differences Between Fraud and Legitimate Transactions

Missingness was compared independently for every feature between legitimate and fraudulent transactions.

The largest absolute differences were:

| Feature | Legitimate Missing | Fraud Missing | Absolute Difference |
|---|---:|---:|---:|
| `R_emaildomain` | 77.8787% | 45.6662% | 32.2126 pp |
| `id_02` | 77.2495% | 45.6904% | 31.5591 pp |
| `id_36` | 77.2296% | 45.6904% | 31.5393 pp |
| `id_37` | 77.2296% | 45.6904% | 31.5393 pp |
| `id_35` | 77.2296% | 45.6904% | 31.5393 pp |
| `id_38` | 77.2296% | 45.6904% | 31.5393 pp |
| `id_15` | 77.2296% | 45.6904% | 31.5393 pp |
| `id_11` | 77.2302% | 45.7097% | 31.5205 pp |
| `id_29` | 77.2302% | 45.7097% | 31.5205 pp |
| `id_28` | 77.2302% | 45.7097% | 31.5205 pp |
| `DeviceType` | 77.2584% | 45.7436% | 31.5148 pp |
| `id_12` | 76.6765% | 45.2258% | 31.4508 pp |
| `id_01` | 76.6765% | 45.2258% | 31.4508 pp |
| `id_31` | 77.3441% | 45.9372% | 31.4069 pp |
| `id_06` | 77.9105% | 46.8519% | 31.0586 pp |

These differences further support the conclusion that missingness carries information related to the target distribution.

### Decision

Missingness indicators should remain a candidate component of later feature engineering and preprocessing experiments.

They will be implemented only where justified rather than automatically generated for every column.

---

# 2. Missing-Value Handling Policy

Based on the completed Phase 5.1 analysis, the current policy is:

| Decision | Status |
|---|---|
| Drop rows with missing values | **No** |
| Globally fill all missing values immediately | **No** |
| Treat missingness as potentially informative | **Yes** |
| Preserve identity availability information | **Yes — candidate feature** |
| Automatically remove ≥95%-missing features | **No** |
| Use missingness indicators | **Candidate — to be evaluated later** |
| Final imputation strategy | **Not finalized yet** |

The final imputation strategy will be implemented later in the leakage-safe preprocessing pipeline, after the temporal split and feature-role decisions have been established.

---

# 3. Key Conclusions from Phase 5.1

The missing-value analysis establishes the following:

1. Missingness is extensive, affecting **45.07% of all cells**.
2. Missingness is widespread across individual transactions, with a median of **211 missing values per transaction**.
3. Missingness patterns differ between legitimate and fraudulent transactions.
4. Identity availability is strongly associated with the observed fraud rate.
5. Missingness varies substantially across feature groups.
6. Missingness also changes across temporal periods.
7. Several features are extremely sparse, including nine features with at least 95% missingness.
8. The results support preserving missingness information rather than treating every missing value as a simple data-quality defect.
9. No rows or columns have been removed as a result of Phase 5.1.
10. No final imputation strategy has been applied yet.

---

# 4. Phase 5.1 Completion Status

```text
Phase 5.1 — Missing Values

Column-level analysis          ✅
Row-level analysis             ✅
Missingness vs fraud class     ✅
Identity availability          ✅
Temporal missingness analysis  ✅
Feature-group analysis         ✅
Feature-level class comparison ✅
Cleaning policy defined        ✅
```

**Phase 5.1 — Missing Values is complete.**

The report has been extended with the results and decisions from:

- Phase 5.2 — Duplicates
- Phase 5.3 — Outliers
- Phase 5.4 — Inconsistent Data (pending)

---

# 5. Phase 5.2 — Duplicate Analysis

## 5.1 Objective

The objective of the duplicate analysis was to distinguish genuine duplicate records from legitimate repeated transactions that share the same observable entity or feature attributes.

The analysis examined:

- exact duplicate rows
- duplicate `TransactionID` values
- repeated `card1` values
- repeated `card1 + addr1` combinations
- repeated `card1 + P_emaildomain` combinations
- repeated `DeviceType + DeviceInfo + ProductCD` combinations
- whether repeated `card1 + addr1` groups contain both legitimate and fraudulent transactions

The project outline explicitly cautions against automatically removing repeated entity/feature combinations because multiple legitimate transactions can share the same observable attributes.

## 5.2 Exact Duplicate Rows

The joined dataset contains:

| Check | Result |
|---|---:|
| Exact duplicate rows | 0 |
| Duplicate `TransactionID` values | 0 |

No evidence of ordinary row-level duplication or duplicate transaction identifiers was found.

### Decision

No rows are removed on the basis of exact duplication or duplicate `TransactionID`.

## 5.3 Repeated Entity / Feature Combinations

Repeated combinations were investigated because repetition alone does not establish that transactions are duplicates.

| Feature combination | Repeated rows | Repeated-row rate | Repeated groups | Largest group size |
|---|---:|---:|---:|---:|
| `card1` | 587,096 | 99.4168% | 10,109 | 14,932 |
| `card1 + addr1` | 574,788 | 97.3326% | 24,222 | 9,928 |
| `card1 + P_emaildomain` | 572,869 | 97.0077% | 25,810 | 7,041 |
| `DeviceType + DeviceInfo + ProductCD` | 589,677 | 99.8539% | 1,809 | 439,670 |

The extremely high repetition rates demonstrate that repeated feature combinations are a normal characteristic of the dataset rather than evidence of duplicate records.

## 5.4 `card1 + addr1` Analysis

There are **24,222** repeated `card1 + addr1` groups.

Among these, **2,666 groups contain both legitimate and fraudulent transactions**.

This is an important distinction:

```text
same card + same address
          ≠
duplicate transaction
```

For example, the largest repeated `card1 + addr1` groups include multiple transactions with different fraud outcomes. Therefore, collapsing these rows would remove legitimate observations and destroy potentially useful behavioral information.

### Decision

Repeated `card1 + addr1` combinations are retained and are **not treated as duplicate records**.

## 5.5 `card1 + P_emaildomain` Analysis

Repeated `card1 + P_emaildomain` combinations are also extremely common, with **25,810 repeated groups** covering **572,869 rows**.

Examples of large repeated groups include combinations such as:

| `card1` | `P_emaildomain` | Transactions | Fraud Count | Fraud Rate |
|---:|---|---:|---:|---:|
| 7,919 | `gmail.com` | 7,041 | 54 | 0.7669% |
| 9,500 | `gmail.com` | 5,605 | 184 | 3.2828% |
| 7,919 | missing | 4,465 | 45 | 1.0078% |
| 15,885 | `hotmail.com` | 4,196 | 84 | 2.0019% |
| 17,188 | `gmail.com` | 4,034 | 66 | 1.6361% |
| 15,885 | `gmail.com` | 3,988 | 284 | 7.1214% |

These groups demonstrate that repeated card/email-domain combinations can contain multiple transactions and can exhibit different fraud outcomes.

### Decision

Repeated `card1 + P_emaildomain` combinations are retained and are **not treated as duplicate records**.

## 5.6 Device / Product Combination Analysis

The combination of `DeviceType + DeviceInfo + ProductCD` is also highly repetitive.

The largest group observed was:

```text
DeviceType = missing
DeviceInfo = missing
ProductCD  = W

Transactions = 439,670
Fraud Count  = 8,969
Fraud Rate   = 2.0399%
```

This group requires careful interpretation. It does **not** mean that a single known device generated 439,670 transactions. Rather, all observations with missing `DeviceType`, missing `DeviceInfo`, and `ProductCD = W` collapse into the same observable combination.

This finding also reinforces the missingness conclusions from Phase 5.1: missingness can affect entity-style groupings and should not be interpreted as a unique entity identifier.

### Decision

Repeated device/product combinations are retained. They are not removed as duplicate transactions.

## 5.7 Overall Duplicate-Handling Decision

The duplicate analysis supports the following policy:

| Situation | Finding | Action |
|---|---|---|
| Exact duplicate rows | 0 | Keep all observations |
| Duplicate `TransactionID` | 0 | Keep all observations |
| Repeated entity/feature combinations | Very common | Do not remove |
| Repeated combinations with mixed fraud labels | Confirmed | Treat as valid repeated observations |
| Missing device/entity attributes forming large groups | Present | Do not interpret as true duplicate entities |

The analysis therefore establishes that **duplicate-like feature repetition should not be handled by dropping rows**.

Repeated entity combinations may instead become useful inputs for later behavioral and historical feature engineering, provided that such features are constructed using only information available before the transaction and in a leakage-safe manner.

## 5.8 Phase 5.2 Completion Status

```text
Phase 5.2 — Duplicates

Exact duplicate analysis             ✅
TransactionID duplicate analysis     ✅
Repeated entity combinations         ✅
Mixed-label group analysis            ✅
Duplicate-handling policy             ✅
```

**Phase 5.2 — Duplicate Analysis is complete.**

The report has now been extended with **Phase 5.3 — Outlier Analysis** and **Phase 5.4 — Inconsistent Data**.

---


# 6. Phase 5.3 — Outlier Analysis

## 6.1 Objective

The objective of the outlier analysis was to identify unusually large or unusual numerical observations and determine whether they represent data-quality problems, legitimate extreme transactions, or potentially useful fraud-related signal.

The analysis focused first on `TransactionAmt`, followed by an IQR-based screening of other numeric features. The project outline explicitly states that outliers should not be automatically removed because an unusually large transaction may be a legitimate outlier or a fraud signal.

## 6.2 `TransactionAmt` Distribution

The observed distribution of `TransactionAmt` was:

| Statistic | Value |
|---|---:|
| Count | 590,540 |
| Mean | 135.027176 |
| Standard deviation | 239.162522 |
| Minimum | 0.251 |
| 25th percentile | 43.321 |
| Median | 68.769 |
| 75th percentile | 125.000 |
| Maximum | 31,937.391 |

`TransactionAmt` is strongly right-skewed, with a skewness of **14.3745**.

Selected upper-tail quantiles were:

| Quantile | TransactionAmt |
|---|---:|
| 90% | 275.293 |
| 95% | 445.000 |
| 99% | 1,104.000 |
| 99.5% | 1,656.110 |
| 99.9% | 2,769.807 |
| 100% | 31,937.391 |

This shows a long upper tail rather than a small number of isolated malformed values.

## 6.3 Validity Checks for `TransactionAmt`

The following checks were performed:

| Check | Result |
|---|---:|
| Negative transaction amounts | 0 |
| Zero transaction amounts | 0 |
| Missing transaction amounts | 0 |

No clearly invalid `TransactionAmt` values were identified by these checks.

## 6.4 IQR-Based Outlier Screening

The reusable `numeric_outlier_summary()` utility from `src/data/cleaning.py` was used to calculate the IQR bounds for `TransactionAmt`.

| Statistic | Result |
|---|---:|
| Q1 | 43.321 |
| Q3 | 125.000 |
| IQR | 81.679 |
| Lower bound | -79.1975 |
| Upper bound | 247.5185 |
| Potential outlier observations | 66,482 |
| Potential outlier rate | 11.2578% |

Because the upper IQR boundary is 247.52 while the transaction amount distribution is heavily right-skewed, the IQR rule flags a substantial portion of legitimate-looking upper-tail observations as potential outliers.

### Decision

The IQR flag is treated as an **investigation mechanism**, not as evidence that these 66,482 observations are erroneous. No rows are removed and no transaction amounts are clipped.

## 6.5 Transaction Amount by Fraud Class

`TransactionAmt` was compared between legitimate and fraudulent transactions:

| Class | Mean | Median | 75% | 95% | 99% | 99.9% | Maximum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Legitimate (`isFraud = 0`) | 134.512 | 68.5 | 120.0 | 435.0 | 1,104.0 | 2,775.381 | 31,937.391 |
| Fraudulent (`isFraud = 1`) | 149.245 | 75.0 | 161.0 | 500.0 | 994.0 | 2,680.334 | 5,191.000 |

The distributions overlap substantially, although fraudulent transactions show somewhat higher mean, median, 75th percentile, and 95th percentile values in this dataset.

## 6.6 Fraud Rate: IQR Outliers vs Non-Outliers

Using the IQR rule for `TransactionAmt`:

| Group | Transactions | Fraud Count | Fraud Rate |
|---|---:|---:|---:|
| Non-outlier | 524,058 | 17,291 | 3.2994% |
| IQR outlier | 66,482 | 3,372 | 5.0721% |

The observed fraud rate among IQR-flagged transaction amounts is higher than among non-flagged amounts.

This is an observational difference and does not by itself imply that an IQR outlier is fraudulent.

### Decision

Outlier status is retained as an analytical observation rather than used as a deletion rule. Large transaction amounts may contain predictive information and should remain available for later modeling experiments.

## 6.7 Extreme Transaction Inspection

The largest observed transaction amount was **31,937.391**. Inspection of the largest transactions showed that most extreme values were legitimate (`isFraud = 0`), while at least one transaction with an amount of **5,191.000** was fraudulent.

This confirms that very large transaction amounts cannot be assumed to be erroneous or fraudulent solely because they are extreme.

### Decision

Extreme transactions are retained. No manual deletion or clipping is performed.

## 6.8 Log Transformation Analysis

Because `TransactionAmt` is strongly right-skewed, a `log1p` transformation was evaluated:

| Measure | Raw | `log1p` |
|---|---:|---:|
| Skewness | 14.3745 | 0.4883 |
| Median | 68.769 | 4.2452 |
| 75th percentile | 125.000 | 4.8363 |
| 90th percentile | 275.293 | 5.6215 |
| 95th percentile | 445.000 | 6.1003 |
| 99th percentile | 1,104.000 | 7.0076 |
| 99.9th percentile | 2,769.807 | 7.9269 |
| Maximum | 31,937.391 | 10.3716 |

The transformation substantially reduces skewness and compresses the upper tail.

### Decision

The raw `TransactionAmt` column is preserved. A `log1p(TransactionAmt)` representation remains a **candidate feature transformation** for later modeling/preprocessing experiments rather than a permanent replacement at this stage.

## 6.9 Screening of Other Numeric Features

The `numeric_outlier_summary()` utility was also applied as a screening mechanism across other numeric columns.

Several features produced high IQR-based outlier rates, including `V222`, `V221`, `id_13`, `id_25`, and several `V*` features. Some of these features produced degenerate IQR bounds where the lower and upper bounds were identical, demonstrating an important limitation of applying a generic IQR rule mechanically to highly discrete or sparse features.

### Decision

The IQR screening results for other numeric columns are treated as **diagnostic flags only**. No blanket removal, clipping, or transformation is applied based solely on IQR statistics.

## 6.10 Overall Outlier-Handling Policy

| Decision | Status |
|---|---|
| Automatically remove IQR outliers | **No** |
| Remove large transactions | **No** |
| Clip `TransactionAmt` | **No** |
| Treat all extreme numeric values as errors | **No** |
| Preserve raw `TransactionAmt` | **Yes** |
| Evaluate `log1p(TransactionAmt)` later | **Yes — candidate transformation** |
| Use generic IQR screening as an investigation tool | **Yes** |

## 6.11 Phase 5.3 Completion Status

```text
Phase 5.3 — Outliers

TransactionAmt distribution analysis     ✅
Invalid amount checks                   ✅
IQR outlier analysis                    ✅
Fraud vs. outlier comparison            ✅
Extreme transaction inspection          ✅
log1p transformation analysis           ✅
Numeric feature outlier screening       ✅
Outlier-handling policy                 ✅
```

**Phase 5.3 — Outlier Analysis is complete.**

# 7. Phase 5.4 — Inconsistent Data

## 7.1 Objective

The objective of the inconsistent-data analysis was to identify malformed categorical values, inconsistent textual representations, sentinel values, and potentially impossible numerical values without applying arbitrary transformations to anonymized features.

The analysis examined:

- empty strings
- whitespace-only strings
- casing differences
- sentinel-like categorical values
- negative numerical values
- zero numerical values
- infinite numerical values
- target-value consistency

The project outline specifically recommends these checks and cautions against arbitrarily normalizing anonymized categories simply to make them appear cleaner.

## 7.2 Empty Strings and Whitespace

All object/string columns were checked after stripping surrounding whitespace.

| Check | Result |
|---|---:|
| Columns containing empty/whitespace-only strings | 0 |
| Empty/whitespace-only values requiring replacement | 0 |

No empty-string or whitespace-only categorical values were detected.

### Decision

No categorical values are modified on the basis of empty-string or whitespace checks.

## 7.3 Casing Inconsistencies

Case-normalization analysis identified collisions only in the `DeviceInfo` feature.

The lowercase groups containing multiple distinct observed values were:

```text
alcatel
 dash
 ilium
 mi
 moto
 stellar
 vivo
```

Each of these groups contained two distinct observed variants that differ only in casing.

### Decision

`DeviceInfo` is **not globally lowercased or otherwise normalized** at this stage. The feature is anonymized and categorical, so changing its representation without establishing semantic equivalence could alter the observed categories unnecessarily.

Any categorical normalization required later will be handled deliberately as part of the preprocessing/encoding strategy.

## 7.4 Sentinel-Like Values

The sentinel-value scan identified:

| Feature | Value | Count |
|---|---|---:|
| `id_15` | `Unknown` | 11,645 |

The observed `Unknown` value is recorded as a distinct categorical value rather than automatically converted to missing data.

### Decision

`id_15 = "Unknown"` is retained for now. Whether it should be treated as a separate category or mapped to missingness will be evaluated later according to the feature's modeling role and preprocessing design.

## 7.5 Negative Numerical Values

Negative values were observed in the following numeric features:

| Feature | Negative Count | Minimum |
|---|---:|---:|
| `id_01` | 124,678 | -100.0 |
| `id_14` | 79,113 | -660.0 |
| `id_06` | 45,540 | -100.0 |
| `id_05` | 6,097 | -72.0 |
| `id_08` | 4,894 | -100.0 |
| `id_10` | 2,047 | -100.0 |
| `id_04` | 585 | -28.0 |
| `id_09` | 463 | -36.0 |
| `id_07` | 347 | -46.0 |
| `id_03` | 187 | -13.0 |
| `D15` | 15 | -83.0 |
| `D4` | 15 | -122.0 |
| `D11` | 7 | -53.0 |
| `D6` | 3 | -83.0 |
| `D14` | 3 | -193.0 |
| `D12` | 2 | -83.0 |

Negative values were **not automatically classified as invalid**. The anonymized nature of the `id_*` and `D*` features means that a generic non-negative constraint cannot be imposed safely without feature-specific semantic evidence.

### Decision

No negative values are removed or clipped as part of Phase 5.4.

## 7.6 Zero Numerical Values

Zero values were widespread across the numerical feature set, particularly within the `C*`, `D*`, and `V*` feature families.

Examples include:

- `C3`: 588,111 zeros
- `C4`: 451,883 zeros
- `D1`: 280,130 zeros
- `D4`: 166,571 zeros
- `V15`: 452,075 zeros
- `V98`: 558,622 zeros

`isFraud = 0` also occurs 569,877 times, as expected for the legitimate class.

### Decision

Zeros are **not globally treated as invalid or missing values**. Their interpretation depends on the individual feature and will be handled later during feature engineering and preprocessing.

## 7.7 Transaction Amount Consistency

`TransactionAmt` was separately checked for values that would clearly violate the expected numeric representation used in this project.

| Check | Result |
|---|---:|
| Negative amounts | 0 |
| Zero amounts | 0 |
| Missing amounts | 0 |

No inconsistent transaction-amount values were detected through these checks.

## 7.8 Infinite Values

All numeric columns were checked for positive or negative infinity.

| Check | Result |
|---|---:|
| Infinite numeric values | 0 |

No infinite values were found.

## 7.9 Target Consistency

The target `isFraud` contains only the expected binary values:

| `isFraud` | Count |
|---:|---:|
| 0 | 569,877 |
| 1 | 20,663 |

No unexpected target categories were observed.

## 7.10 Overall Inconsistent-Data Handling Policy

| Situation | Finding | Action |
|---|---|---|
| Empty/whitespace-only strings | None detected | No change |
| Casing collisions | `DeviceInfo` only | Retain original categories |
| Sentinel-like categorical values | `id_15 = "Unknown"` | Retain for later evaluation |
| Negative numeric values | Present in several `id_*` and `D*` features | Do not remove automatically |
| Zero numeric values | Widespread | Do not treat as globally invalid |
| Negative/zero `TransactionAmt` | None | No correction required |
| Infinite numeric values | None | No correction required |
| Unexpected `isFraud` values | None | No correction required |

## 7.11 Phase 5.4 Completion Status

```text
Phase 5.4 — Inconsistent Data

Empty/whitespace string analysis       ✅
Casing inconsistency analysis          ✅
Sentinel-value analysis                ✅
Negative-value analysis                ✅
Zero-value analysis                    ✅
TransactionAmt validity checks         ✅
Infinite-value analysis                ✅
Target consistency check               ✅
Handling policy defined                ✅
```

**Phase 5.4 — Inconsistent Data is complete.**

# 8. Phase 5 — Data Cleaning Completion Status

```text
Phase 5 — Data Cleaning

5.1 Missing Values                    ✅
5.2 Duplicates                        ✅
5.3 Outliers                          ✅
5.4 Inconsistent Data                 ✅
```

**Phase 5 — Data Cleaning is complete.**

The analyses in this phase intentionally distinguish between **observations that require cleaning** and **observations that are unusual but potentially informative**. No broad deletion rule, blanket imputation rule, arbitrary categorical normalization, or automatic outlier-removal rule has been applied merely because a value appears unusual.

Final preprocessing decisions will be implemented later in the leakage-safe preprocessing and feature-engineering stages, using the chronological split established in Phase 4.

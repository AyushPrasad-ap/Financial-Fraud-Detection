# Financial Fraud Detection — Problem Definition

## 1. Business Problem

Financial transaction fraud is a binary classification problem in which each transaction must be assessed for the likelihood that it is fraudulent.

The objective is not simply to classify transactions as fraud or legitimate. The system should estimate a fraud-risk probability for each transaction and convert that probability into an operational decision using a decision threshold.

The intended downstream use is a fraud-review workflow in which transactions with sufficiently high estimated fraud risk can be flagged for further investigation.

---

## 2. ML Objective

Given the information available for a transaction at time `t`, estimate the probability that the transaction is fraudulent while:

- avoiding future-information and target leakage,
- handling severe class imbalance,
- accounting for the time-dependent nature of fraud,
- and producing predictions that can support a downstream fraud-review decision.

Formally:

`y ∈ {0, 1}`

where:

- `0` → legitimate transaction
- `1` → fraudulent transaction

The model should produce:

`P(fraud | transaction information)`

rather than treating the final classification as the primary output.

---

## 3. Prediction Target

The prediction target is the binary `isFraud` label.

```text
0 → legitimate
1 → fraudulent
````

The model will estimate the probability that the target class is `1`.

---

## 4. Unit of Prediction

The unit of prediction is an individual transaction.

Each transaction represents one observation for which the fraud-risk probability is estimated.

---

## 5. Input Available at Prediction Time

The model should use only information that would be available at the time the transaction is evaluated.

The primary dataset contains transaction and, where available, identity-related information. The transaction data contains a mixture of numerical and categorical variables, including card-related, address, email-domain, match, device, and identity features.

`TransactionDT` represents elapsed time from a reference point and provides the temporal ordering of transactions; it should not automatically be interpreted as a real-world calendar timestamp.

Future transaction information, future labels, and statistics derived using future observations must not be used when generating a prediction.

---

## 6. Output

For each transaction, the system will produce:

1. A fraud-risk probability.
2. An operational decision derived from that probability using a configurable threshold.

Example:

```text
P(fraud) = 0.87
        ↓
threshold policy
        ↓
FLAG FOR REVIEW
```

The threshold is treated as an operational policy rather than as an intrinsic property of the model.

---

## 7. Success Metrics

Because fraud is a highly imbalanced problem, accuracy will not be used as the primary success criterion.

The primary ranking-oriented metric will be:

* Average Precision (AP / PR-AUC)

Additional evaluation metrics will include:

* Precision
* Recall
* F1-score
* ROC-AUC
* False Positive Rate (FPR)

Operationally relevant metrics such as top-k performance and threshold-dependent alert behavior may also be considered.

The final evaluation will consider not only predictive performance but also temporal stability and the operational trade-off between false positives and false negatives.

---

## 8. Constraints

The project has the following constraints:

* Fraud is a minority class, creating severe class imbalance.
* Fraud detection is cost-sensitive: false positives and false negatives have different consequences.
* Model decisions are threshold-dependent.
* Fraud behavior can change over time, making temporal validation important.
* Preprocessing, feature engineering, encoding, frequency statistics, and resampling must be designed to prevent data leakage.
* The dataset is anonymized, so the semantic meaning of every feature cannot be assumed.
* The raw dataset must not be committed to GitHub due to the competition's terms.

---

## 9. Assumptions

The project assumes that:

* Each observation represents a transaction.
* The target label indicates whether the transaction is fraudulent.
* Only information available at transaction evaluation time can be used to generate a prediction.
* A downstream fraud-review process can consume a probability score and apply an operational threshold.
* Temporal ordering can be established using `TransactionDT`.
* Evaluation should reflect the time-dependent nature of the fraud problem.

---

## 10. Known Limitations

The primary dataset is anonymized and contains engineered or derived variables from the original fraud-detection system. Therefore, the semantic meaning of every anonymized feature is not necessarily known.

The dataset also does not provide a clean customer identifier. Consequently, customer-level generalization cannot be directly measured without constructing a proxy entity key, and any such proxy-based analysis must not be interpreted as true customer-level evaluation.

The dataset is a competition dataset and may not perfectly represent a live production fraud-detection environment.

The project therefore focuses on demonstrating leakage-safe machine learning methodology, temporal evaluation, fraud-risk estimation, and production-oriented engineering rather than claiming direct real-world production performance.

---

## 11. Project Objective Summary

The project will build a reproducible fraud-risk decision system that:

```
Transaction
    ↓
Fraud-risk model
    ↓
P(fraud)
    ↓
Threshold policy
    ↓
Operational decision
```

The system will be evaluated using leakage-safe, time-aware methodology and will emphasize Average Precision, precision, recall, false-positive behavior, temporal stability, and probability quality rather than raw classification accuracy.




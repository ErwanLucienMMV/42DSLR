# Data investigation worksheet

**Current evidence:** both provided CSVs are present in `datasets/`. They have
1,600 training rows and 400 test rows with the same 19-column schema. The training
target is complete; every test target is blank. The measured data dictionary,
missingness, statistics, correlations, and file fingerprints are recorded in
[dataset findings](08-dataset-findings.md).

## Verified inventory

| Fact | Training file | Test file |
| --- | --- | --- |
| Source and inspection date | Provided by user; inspected 10 Nov 2026 | Provided by user; inspected 10 Nov 2026 |
| SHA-256 fingerprint | Recorded in dataset findings | Recorded in dataset findings |
| Encoding, delimiter, quoting | ASCII-compatible UTF-8; comma-separated; parsed as CSV | Same |
| Data rows and columns | 1,600 rows, 19 columns | 400 rows, 19 columns |
| Exact header names and order | Listed in dataset findings | Identical to training |
| Identifier column and uniqueness | `Index`, unique, 0-1599 in order | `Index`, unique, 0-399 in order |
| Target presence / missingness | Four valid houses; 0 missing | Target column present; all 400 blank |
| Duplicate full rows / identifiers | 0 / 0 | 0 / 0 |
| Missing-value representations | Empty cells in 11 course columns | Empty cells in 11 course columns and target |
| Non-finite or malformed numeric values | None among populated numeric cells | None among populated numeric cells |

Treat commas inside quoted fields correctly. Distinguish blank cells from zero;
negative scores must not automatically be rejected. Do not silently convert a
bad numeric token to a missing value or zero. Record the row and column concerned.
Validate the expected house labels in labeled data; reject or explain unexpected
labels rather than silently relabeling them.

## Use the data dictionary

The [verified data dictionary](08-dataset-findings.md) lists every observed column,
its role, numeric ranges, and missing counts. Keep it synchronized if the source
files change, and record the final modeling decision for each candidate feature.

Separate these roles:

- **Target:** the house label; used to train and evaluate, never as an input feature.
- **Identifier:** a numeric identifier can belong in the descriptive table while
  being excluded from the classifier. Numeric storage does not make it predictive.
- **Candidate feature:** a measured numeric course score, subject to inspection.
- **Metadata:** names, dates, or other non-course fields if they actually exist.
  Start by excluding personal metadata from modeling and explain that decision.

The subject does not enumerate actual CSV columns. The dictionary in these notes
was checked against both provided files, rather than inferred from the subject.

## Keep three data treatments distinct

1. **Descriptive statistics:** use observed valid values independently per numeric
   column. Count can therefore differ across columns. Do not impute first, as this
   would conceal missingness and change the reported distribution.
2. **Exploratory plots:** omit missing values only for the feature(s) shown. A scatter
   plot must retain only rows where both coordinates exist, preserving their pairing.
   Record retained counts by house. Do not discard every row with any missing field
   just to draw a single course's histogram.
3. **Model input:** choose and persist a deterministic imputation and scaling policy
   so every valid test row can receive a prediction.

## Proposed modeling baseline

Use a fixed, stratified training/validation split of labeled training data, for
example 80% / 20%, with every house represented on both sides. Record the seed
and counts. The ratio is a recommendation, not a subject requirement.

For each selected feature, fill missing values with a median learned from the
training partition only. Compute that median manually. Standardize with a mean
and nonzero scale learned from that same partition; see the [model guide](05-logistic-regression.md).
Apply those saved values unchanged to validation data.

Never impute using the true house: that label will be unavailable at prediction
time. Do not fit separate preprocessing to the test file or let validation/test
rows influence training medians, means, scales, or hyperparameters. Formal feature
comparisons should also use training-only exploration; reserve validation for
assessing the resulting choices.

An all-missing training feature has no learnable median: exclude it and document
why. A constant feature has no useful scale: exclude it or use a documented unit
scale. Reject non-finite transformed values rather than carrying them into training.

After selecting the approach, refit preprocessing and the four classifiers on
all labeled training rows. Save that final preprocessing with the final weights.
Do not report the earlier validation score as a measured score on the official
test set. Without true test labels, that score cannot be calculated locally.

## Evidence log

Initial evidence is available; these entries distinguish it from future outputs:

| Decision / finding | Evidence to attach | Current result |
| --- | --- | --- |
| Course with homogeneous distributions | Per-house histogram, shared bins, counts | Care of Magical Creatures is supported by similar house summaries; required histogram pending |
| Similar feature pair | Paired scatter plot and explanation of relationship | Astronomy / Defense Against the Dark Arts: r = -1 on 1,537 paired observations; required scatter plot pending |
| Retained modeling features | Pair plot, missingness, ablation on validation data | Pending |
| Excluded columns | Role, redundancy, missingness, or constant-value evidence | Identifier / target / metadata roles verified; course exclusions require validation |
| Imputation / scaling | Training-only fitted values and edge-case handling | Pending |
| Chosen learning settings | Convergence trace and validation results | Pending |

No particular feature set has yet been trained or shown to reach 98%.

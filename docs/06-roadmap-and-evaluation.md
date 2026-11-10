# Implementation roadmap and evaluation checklist

**Preparation only:** the datasets have been inventoried and descriptive evidence
recorded. No required program or trained model has been implemented. This is an
ordered plan for later work, following the subject's analysis-to-model sequence.

## Milestones

| Order | Work to do later | Evidence of completion |
| --- | --- | --- |
| 1 | Use the inventoried CSVs; choose a language and supporting libraries | Inventory is complete; language / supporting tools remain to be selected |
| 2 | Parse and validate CSVs; identify numerical columns and their roles | Readable errors for malformed data; documented schema and missing tokens |
| 3 | Implement manual statistics and `describe.[extension]` | Eight-row table for every numeric column; hand examples match |
| 4 | Produce histogram, scatter, and pair-plot entry points | All three questions answered with saved evidence and explanations |
| 5 | Select a candidate feature set and a fixed validation protocol | Split counts, seed, feature rationale, and training-only preprocessing rules |
| 6 | Implement stable binary logistic regression and four one-vs-rest models | Loss behavior, small gradient check, finite coefficients |
| 7 | Compare features / learning settings; investigate errors | Validation accuracy and per-house confusion counts; documented settings |
| 8 | Refit on all labeled training data and save a complete artifact | Reproducible preprocessing and all four parameter vectors on disk |
| 9 | Implement standalone prediction and `houses.csv` export | Fresh-process prediction, exact header, correct row count and labels |
| 10 | Review the mandatory requirements and prepare the defense | Reproducible run instructions and explanations of every major choice |

Choose plotting CLI arguments and the model filename consistently and document
them when implemented. The only explicitly specified dataset arguments are the
ones recorded in the [requirements table](01-requirements.md). This documentation
does not introduce a build system or dependency lockfile prematurely.

## Accuracy and diagnostic measurements

For m labeled examples:

**accuracy = number of exact house matches / m**.

The subject's target is **accuracy >= 0.98** on the evaluator's test data, not
merely on the training rows. On a validation sample of m rows, the allowed number
of mistakes for 98% is floor(0.02m); for 200 rows that is at most 4 mistakes.

A confusion table should count true house on one axis and predicted house on the
other. It reveals whether one house is consistently mistaken for another even
when total accuracy looks good. Record the total and per-house sample counts.
Validation results are estimates; a small split may vary substantially with the
seed. If configuration choices become sensitive to the split, consider additional
stratified folds with preprocessing refitted inside each training fold.

The supplied test file may have no usable house labels. Predictions can still be
checked structurally, but measured test accuracy requires ground truth. Do not
fabricate test labels, optimize against assumed labels, or claim the 98% target
has been met before it has been measured.

## Focused checks to run after implementation

| Area | Meaningful checks |
| --- | --- |
| Statistics | Known four-value example; missing cells; one value; all missing; constant column; negative values; repeated quartiles |
| CSV handling | Quoted delimiters; blank cells; malformed numeric input; duplicate headers; expected target values |
| Preprocessing | No training/validation leakage; saved fills/scales reused; zero-scale and all-missing cases |
| Gradient descent | Zero-weight loss; correct update direction; finite-difference agreement on a tiny case; finite extreme-logit behavior |
| One-vs-rest | Correct binary targets; one model per house; deterministic argmax and ties |
| Model persistence | Predictions agree before and after saving/loading; malformed or incomplete artifacts rejected |
| Prediction CSV | Exact `Index,Hogwarts House` header; one row per input; valid spellings; preserved input order; no extra index column |
| Full workflow | Fresh train process writes artifact; fresh predict process reads it and writes `houses.csv` |

These checks are planned validation tasks. They are not an assertion that tests
exist or have run. Do not use a forbidden statistics or model library as a shortcut
in the submitted implementation, including through a wrapper.

## If accuracy falls short

First check target mapping, feature ordering, row alignment, missing-value handling,
and whether preprocessing was reused correctly. Then inspect scaling, convergence,
learning rate, and per-house errors. Compare the selected feature subset with all
eligible numeric course features. Correct the baseline before adding bonus work.

Do not improve a score by dropping hard validation/test rows, including the label
as an input, or fitting transformations to validation/test data. Preserve honest
measurements and explain the limits of each result.

## Mandatory completion checklist

- [ ] All six required entry points have the exact base names.
- [ ] `describe` covers every numerical feature with manually calculated results.
- [ ] Each visualization answers its stated question with defensible evidence.
- [ ] Four binary logistic regressions implement one-vs-rest classification.
- [ ] Mandatory training uses explicitly implemented gradient descent.
- [ ] Prediction loads the saved training artifact and writes the exact CSV format.
- [ ] The classifier meets the subject's 98% evaluation target when ground truth is available.
- [ ] No forbidden heavy-lifting statistics or model-fitting functions are used.
- [ ] The repository contains the complete, reproducible submission.
- [ ] The choices and mathematics can be explained during peer evaluation.

## Defense prompts

Explain why logistic regression solves classification despite its name; why
sigmoid and cross-entropy are paired; how the gradient leads to the update; why
four binary classifiers are needed; why their outputs need not sum to one; how
missing values and scales are learned without leakage; how the three plots
justify the features; and why a high training score does not establish test
performance. Be ready to trace one student's row from CSV fields to saved
preprocessing, four scores, one house label, and its output CSV line.

Bonus work can follow only after the mandatory baseline is complete and reliable.

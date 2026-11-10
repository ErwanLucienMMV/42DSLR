# DSLR study and implementation guide

Preparation for **Data Science x Logistic Regression**, subject version 5.
This repository contains study documentation, aggregate findings, and the supplied
fictional Hogwarts datasets in `datasets/`, and a commented learning POC. No main
DSLR programs, trained Hogwarts model, or house predictions have been produced.

The goal is to explore student data and build a Hogwarts house classifier using
four one-vs-rest logistic regressions trained with gradient descent. The subject
requires a minimum accuracy of **98%** during evaluation.

## Reading order

| Document | What you can retrieve from it |
| --- | --- |
| [Requirements](docs/01-requirements.md) | Required filenames, restrictions, outputs, and subject page references |
| [Data investigation](docs/02-data-investigation.md) | What to collect from the CSVs, missing-data decisions, and leakage prevention |
| [Manual statistics](docs/03-manual-statistics.md) | Formulas, conventions, and small hand-checkable examples |
| [Exploratory plots](docs/04-exploratory-plots.md) | How to answer the three visualization questions and justify features |
| [Logistic regression](docs/05-logistic-regression.md) | One-vs-rest mathematics, training, numerical stability, and saved-model requirements |
| [Roadmap and evaluation](docs/06-roadmap-and-evaluation.md) | Ordered implementation milestones, acceptance checks, and defense questions |
| [Sources](docs/07-sources.md) | Subject provenance, verified learning resources, and unresolved choices |
| [Dataset findings](docs/08-dataset-findings.md) | Verified schema, missing values, class counts, reference statistics, and feature relationships |

## Start here

1. Read the requirements and manual statistics notes.
2. Read the [dataset findings](docs/08-dataset-findings.md): the supplied files are
   tracked in [datasets](datasets/), with 1,600 labeled training rows and 400
   unlabeled test rows.
3. Use the data inventory and exploration notes to plan which features to compare.
4. Try the [commented AND/OR learning POC](getting%20feets%20wet/README.md) to
   practice the core calculation, then use the roadmap for the main DSLR project.

## Learning POC

The [getting feets wet](getting%20feets%20wet/README.md) folder contains a
standard-library Python example of one sigmoid neuron learning AND and OR, plus
an XOR comparison illustrating its limits. The code includes detailed explanatory
comments, visible loss traces, and mathematical checks. See that folder's README
for run commands and a guided reading order.

The notes distinguish **subject requirements** from **recommended design choices**.
The data inspection identifies Care of Magical Creatures as a histogram candidate
and Astronomy / Defense Against the Dark Arts as the similar-feature pair.
The required plots, final feature selection, training, and achieved accuracy are
still pending.
The example statistics and plots in the subject are illustrations, not evidence
about the supplied Hogwarts dataset.

## Source of truth

The attached version 5 subject was visually reviewed in full. The page references
in these notes use its **printed page numbers**: printed page 6 is PDF page 7.
See [source provenance](docs/07-sources.md) for the original file fingerprint.
These notes summarize the assignment and provide study material; the subject
remains authoritative if a summary is ambiguous.

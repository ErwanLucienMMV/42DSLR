# Sources and open decisions

Prepared on **10 November 2026** from the user-supplied subject and the primary
references below. The project requirements come from the subject, not from
third-party solutions or assumptions about another version of DSLR.

## Subject provenance

- Title: **Data Science x Logistic Regression - Harry Potter and the Data Scientist**.
- Version: **5**, as printed on the cover.
- Original file: `C:\Users\erwan\Downloads\DSLR Subject.pdf`.
- Length: 14 PDF pages; cover is unnumbered and remaining pages are printed 1-13.
- SHA-256: `8E25AEFA5B09D7E6FD171BAE0E3FAB8E71B5D566E0CCD63D95ED26052904419D`.
- Method: every page was rendered and visually inspected. Text extraction returned
  no readable content, so these notes are a curated summary rather than an OCR transcript.
- The original PDF remains at the user-supplied location; it is not duplicated in
  the repository. The fingerprint identifies exactly which version was reviewed.

| Subject section | Printed pages | PDF page positions, starting at 1 |
| --- | --- | --- |
| Objectives | 4 | 5 |
| General instructions | 5 | 6 |
| Data analysis and statistics restrictions | 6-7 | 7-8 |
| Visualization requirements | 7 | 8 |
| Logistic regression and output CSV | 8 | 9 |
| Bonus conditions | 9 | 10 |
| Submission, defense, and 98% threshold | 10 | 11 |
| Mathematics | 11 | 12 |
| Plot examples | 12-13 | 13-14 |

The foreword and fictional introduction provide background rather than extra
implementation requirements. Instructions inside the assignment were treated as
content to document; the user's current scope authorizes preparation and Git
delivery only, with no project implementation yet.

## Primary learning references

These links were opened and checked while preparing the notes. Their purpose is
to explain concepts and supporting tools. They do not expand the APIs allowed by
the subject.

| Reference | What to read for this project |
| --- | --- |
| [Stanford CS229 lecture notes](https://cs229.stanford.edu/notes2022fall/main_notes.pdf) | Part I, section 2, classification and logistic regression; deepen the explanation of the subject's equations |
| [NumPy percentile reference](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html) | Compare percentile conventions, especially linear interpolation; implement it manually, do not call this function |
| [Matplotlib histogram reference](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html) | Understand shared bins and density normalization for house distributions |
| [Matplotlib scatter reference](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html) | Understand scatter coordinates and visual encodings |

No project solution repositories were used. Dataset-specific observations in
these notes come from the supplied CSVs, not the illustrative examples in the PDF.

## Dataset provenance

The user supplied `datasets/dataset_train.csv` and `datasets/dataset_test.csv`
after the initial subject review. Both were inspected on 10 November 2026.
They remain unchanged and are excluded from Git; only aggregate findings are
published. Exact fingerprints, schema, row counts, and analysis
conventions are in [dataset findings](08-dataset-findings.md). An upstream download
URL was not provided, so none is claimed.

## Decisions to settle when implementation starts

| Question | Proposed starting point | Evidence / action needed |
| --- | --- | --- |
| Where are the provided CSV files? | `datasets/dataset_train.csv` and `datasets/dataset_test.csv` | Inventory and fingerprints recorded |
| Which language and support libraries? | A language with convenient CSV parsing and plotting | Choose explicitly; audit statistical/model helpers |
| What do actual columns contain? | Verified 19-column schema, with 13 course scores | Dictionary recorded; choose model inputs next |
| How are invalid and missing values represented? | Empty cells; no malformed populated numeric values found | Choose explicit handling; test targets remain unknown |
| Which std and quartile definitions? | Sample std for describe; type-7 quartiles | Check any supplied evaluator examples and document conventions |
| Which inputs should the classifier use? | Eligible numeric course scores, excluding identifiers and target | Plots and fixed-protocol validation |
| How to impute and scale? | Training-fitted medians and population-standard-deviation scaling | Check missingness, constants, and all-missing columns |
| How to select learning settings? | Full-batch GD with tracked loss and a finite iteration limit | Convergence and validation evidence |
| How to store the model? | Versioned human-readable artifact with preprocessing and weights | Choose filename and validate a fresh-process round trip |
| How to handle row identifiers? | Preserve input order and existing identifiers | Verify official CSV/evaluation convention beyond the sequential example |

Completed work includes subject review, research, dataset inspection, and
documentation. Required program implementation, plot generation, model training,
and performance evaluation remain for the next phase.

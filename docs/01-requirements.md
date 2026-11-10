# Requirements from subject version 5

Source: the supplied `DSLR Subject.pdf`, chapters III-VIII. Page references below
use printed pages, not the PDF viewer's page counter.

## Mandatory deliverables

The subject permits any programming language. `[extension]` means the extension
for the language eventually selected; Python is a possible choice, not a requirement.

| Deliverable | Input / output contract | Purpose | Subject |
| --- | --- | --- | --- |
| `describe.[extension]` | Takes a dataset path; displays a table for all numerical features | Show Count, Mean, Std, Min, 25%, 50%, 75%, Max as in the example | V.1, pp. 6-7 |
| `histogram.[extension]` | Displays a histogram; argument syntax is not specified | Identify a course whose score distribution is homogeneous across all four houses | V.2.1, p. 7 |
| `scatter_plot.[extension]` | Displays a scatter plot; argument syntax is not specified | Identify two similar features | V.2.2, p. 7 |
| `pair_plot.[extension]` | Displays a pair plot or scatter matrix | Support the choice of logistic-regression features | V.2.3, p. 7 |
| `logreg_train.[extension]` | Takes `dataset_train.csv`; writes a file containing learned weights | Train a one-vs-rest multiclass logistic-regression model using gradient descent | V.3, p. 8 |
| `logreg_predict.[extension]` | Takes `dataset_test.csv` and the learned-weights file; writes `houses.csv` | Predict each student's house | V.3, p. 8 |

The eight statistics are the rows shown in the required example. The subject
does not define the standard-deviation denominator or percentile interpolation
method; proposed conventions are in [manual statistics](03-manual-statistics.md).

## Rules that affect the implementation

- **Write the core calculations yourself.** Chapter IV, p. 5 rejects methods that
  do the heavy lifting, explicitly including a DataFrame's `describe` method.
- **Do not call built-in or library statistics that calculate the requested
  results.** V.1, p. 7 explicitly lists count, mean, std, min, max, percentile,
  and equivalents in any language or library.
- **Use logistic regression with one-vs-all / one-vs-rest.** V.3, p. 8 specifies
  this multiclass strategy. A different classifier or softmax model would not
  satisfy that requirement.
- **Use gradient descent for the mandatory training.** V.3, p. 8 requires it.
  Do not delegate fitting, loss, gradients, or updates to a model library.
- **Be able to explain and justify the work.** Chapter VII, p. 10 evaluates the
  submitted implementation and the reasoning behind the choices.

Practical interpretation: implement statistics, preprocessing calculations, loss,
gradients, updates, and prediction decisions explicitly. CSV parsing, sorting,
elementary arithmetic/transcendental operations, and plotting primitives are
reasonable supporting tools; the subject is not an exhaustive API whitelist.
Review any helper that might hide an assessed calculation. A statistics reference
linked in these docs is for understanding conventions, not permission to call it.

## Prediction file

The subject requires `houses.csv` with this exact header and two-column layout:

```csv
Index,Hogwarts House
0,Gryffindor
1,Hufflepuff
2,Ravenclaw
3,Hufflepuff
4,Slytherin
```

These rows are illustrative, not labels to reuse. Produce one prediction per
input row. Preserve input order and the dataset's row identifiers when present;
inspect the official dataset and evaluation convention before deciding how to
handle nonsequential identifiers. Do not introduce an extra CSV index column.

The four label spellings shown by the subject are `Gryffindor`, `Hufflepuff`,
`Ravenclaw`, and `Slytherin`.

## Evaluation and bonus

- Chapter VII, p. 10 sets a **minimum accuracy of 98%** on `dataset_test.csv`,
  evaluated using Scikit-Learn's accuracy score. This is an evaluator tool, not
  an instruction to use Scikit-Learn to implement the classifier.
- Only work in the submitted Git repository is evaluated. Verify names and paths.
- Chapter V recommends analysis, visualization, then classification, in that order.
- Chapter VI, p. 9 suggests additional descriptive fields, stochastic gradient
  descent, and other optimization variants including batch and mini-batch GD.
- Bonus is assessed only when every mandatory requirement is fully satisfied.

There is an ambiguity in the bonus wording: batch GD is listed there even though
mandatory training already requires gradient descent. A sensible baseline is
ordinary full-batch gradient descent; do not claim it as an extra bonus by itself.

## Choices not fixed by this PDF

Language; dataset download location; exact CSV schema; missing-value policy;
features; split protocol; scaling convention; learning rate; stopping rule;
weight-file name and format; plotting CLI syntax; and tie-breaking behavior are
not specified. Choose them explicitly and document the reasons. The following
guides propose a starting point without presenting those choices as requirements.

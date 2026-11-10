# Manual descriptive statistics

Subject basis: V.1, printed pp. 6-7. Implement the calculations yourself. Library
`describe`, count, mean, standard deviation, min/max, percentile, and equivalent
shortcuts are expressly forbidden. The formulas below are mathematical study
notes, not an implementation.

## Definitions and proposed conventions

For a numeric column, let the valid observed values be x_1, ..., x_n. Missing
values are omitted independently per column. Sorting below means ascending order
and does not remove repeated values.

| Row | Calculation | Meaning |
| --- | --- | --- |
| Count | n, obtained by explicitly counting valid entries | Number of observed values, not number of CSV rows |
| Mean | mu = (x_1 + ... + x_n) / n | Arithmetic center |
| Std | s = sqrt(S / (n - 1)), where S = sum of (x_i - mu)^2 | Sample standard deviation |
| Min | Smallest value found by comparison | Lower observed extreme |
| 25% | Q(0.25) | First quartile |
| 50% | Q(0.50) | Median |
| 75% | Q(0.75) | Third quartile |
| Max | Largest value found by comparison | Upper observed extreme |

The sample denominator n - 1 is a proposed convention; the subject does not
explicitly specify it. Do not confuse it with population standard deviation,
which divides by n. Use adequate internal precision and round only for display.

For numerical robustness, the following incremental identity is useful: when a
new value arrives, increase n by one, let delta be its difference from the old
mean, update the mean by delta / n, then increase the running squared-deviation
total by delta times the difference from the new mean. This is Welford's update;
it avoids subtracting two large nearly equal squared totals. A two-pass method
using deviations from the mean is also suitable for a small dataset.

## Quartiles by linear interpolation

The PDF does not fix a percentile method. Proposed convention: linear
interpolation on sorted values with zero-based positions, the type-7 convention
described in the [NumPy percentile reference](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html).
That link explains the convention; calling its percentile function remains
forbidden for the project.

For q between 0 and 1 and sorted observations a_0, ..., a_(n-1):

1. Compute r = (n - 1)q.
2. Let lo = floor(r), hi = ceil(r), and t = r - lo.
3. Q(q) = (1 - t)a_lo + t a_hi.

Different quartile definitions can give different answers on small samples.
Record this convention and check any evaluator examples before treating a
disagreement as a bug.

## Hand-checkable examples

For observed values **1, 2, 3, 4**, plus one blank cell:

| Statistic | Expected under the conventions above |
| --- | --- |
| Count | 4 |
| Mean | 2.5 |
| Std | sqrt(5 / 3), approximately 1.290994449 |
| Min / Max | 1 / 4 |
| 25% / 50% / 75% | 1.75 / 2.5 / 3.25 |

The blank is not a zero and does not increase Count. As a second check, the
sorted values **2, 2, 9** have median 2, Q(0.25) = 2, and Q(0.75) = 5.5.

## Edge cases and output

- **No valid values:** Count is 0; mean, std, extrema, and quartiles are undefined.
  Display an explicit marker such as `NaN`, consistently.
- **One valid value:** mean, extrema, and all quartiles equal that value; sample
  standard deviation is undefined because n - 1 is zero.
- **Constant column, n > 1:** standard deviation is 0.
- **Negative or repeated values:** preserve them; they are valid observations
  unless dataset-specific evidence establishes otherwise.
- **NaN, infinity, malformed tokens:** explicitly identify or reject them according
  to the documented parsing policy; do not let infinity contaminate a mean.

Describe all numerical columns, including an identifier if it is genuinely
numeric. The classifier can exclude that identifier separately. Display clear
column names, the eight row labels, consistent decimal precision, and readable
alignment. Never replace long names with ambiguous labels without a mapping.

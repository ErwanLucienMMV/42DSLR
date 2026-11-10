# Answering the visualization questions

Subject basis: V.2, printed p. 7; illustrative charts are in VIII.2, pp. 12-13.
The subject says there need not be a unique answer. Your evidence and explanation
matter. Inspection of the supplied CSVs gives useful starting points in the
[dataset findings](08-dataset-findings.md): Care of Magical Creatures for the
histogram, and Astronomy / Defense Against the Dark Arts for the similar pair.
The required plots themselves have not been implemented or generated.

## Histogram: homogeneous distributions across houses

Interpret homogeneous as similar score distributions between the four houses,
rather than simply a small variance within one house.

For every numeric course candidate, compare the four house distributions using
the same bin boundaries and horizontal range. Use consistent colors, a legend,
axis labels, and enough transparency or separate panels to reveal overlap.
Record how many valid observations each house contributes. Inspect shape,
location, spread, tails, and outliers rather than comparing only averages.

If class sizes differ, normalized distributions can make shapes easier to compare;
state whether the vertical axis represents raw counts, proportions, or density.
Density is not the height of an individual observation: the areas of the bars
sum to one for each normalized distribution. A raw-count companion plot can
still show sample-size differences.

Use [Matplotlib's histogram documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html)
to understand bins and density. The subject permits plotting support. If there
is doubt about a plotting helper's internal statistics, explicitly compute bin
counts and let the plotting library draw them.

Record a conclusion in this form: course name; plot path; retained observations
by house; how the distributions overlap; and any missingness caveat. A course
that looks alike across houses may be a weak discriminator by itself, which is
useful evidence when choosing model inputs.

## Scatter plot: two similar features

Compare plausible numeric feature pairs, using rows where both values are valid.
Color points by house. Similarity can appear as a tight linear relationship with
positive or negative slope; two features need not have the same units or ranges.

Distinguish a strong global relationship from one caused only by separation
between house clusters. If useful, inspect within-house relationships too.
Check whether outliers or a tiny retained sample dominate the picture. A strong
correlation indicates association, not causation or identical information.

As optional supporting mathematics, Pearson correlation is:

**r = sum[(x_i - mean_x)(y_i - mean_y)] /
sqrt(sum[(x_i - mean_x)^2] sum[(y_i - mean_y)^2]).**

All terms must use the same paired observations, and constant inputs make this
quantity undefined. If included, calculate the statistic manually; it is not a
required substitute for the scatter plot. The
[Matplotlib scatter reference](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html)
explains the underlying plotting primitive.

Record the pair, direction and strength of the visible relationship, paired
sample counts, and whether keeping both features appears redundant.

## Pair plot: select classifier inputs

A pair plot places a univariate distribution on each diagonal and feature-pair
scatter plots off the diagonal. Use a consistent house legend throughout. A
scatter matrix assembled from basic plotting primitives is acceptable; a specific
high-level pair-plot library is not required by the subject.

Inspect which courses separate each house, which pairs are redundant, and which
features appear almost constant or uninformative. Keep full names readable. For
many columns, generate a readable broad overview and focused subsets rather than
shrinking every panel until it is illegible. Preserve enough coverage to justify
the exclusions.

Plots guide a candidate feature set; they do not prove which set generalizes best.
Compare a reasoned subset with a baseline containing all eligible course scores
using the same split and preprocessing. Change one decision at a time and log
validation accuracy and per-house errors. Highly correlated features are not
automatically forbidden, and individual weak features may help in combination.

## Evidence to preserve

| Artifact | Explanation to write beside it |
| --- | --- |
| Histogram answering V.2.1 | Why this course has comparable distributions for all four houses |
| Scatter plot answering V.2.2 | Why these two features are similar, including sign and possible redundancy |
| Pair plot answering V.2.3 | Which features to retain or exclude and why |
| Feature comparison log | Which validation measurements support the final choice |

For every plot, record the dataset fingerprint, missing-value policy, features,
normalization if any, and observation counts. The example figures in the PDF do
not identify the correct courses or pairs for the actual project data.

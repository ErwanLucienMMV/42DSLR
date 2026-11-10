# Findings from the provided datasets

Inspected on **10 November 2026**. Sources: local files
`datasets/dataset_train.csv` and `datasets/dataset_test.csv`, provided by the user.
The original files have not been edited and are excluded from Git. Place them at
those paths separately when using another checkout. This is reference analysis for planning
the project, not output from an implemented `describe` program or trained model.

## File inventory

| Property | Training | Test |
| --- | --- | --- |
| Filename | `dataset_train.csv` | `dataset_test.csv` |
| Bytes | 396,455 | 93,731 |
| Data rows, excluding header | 1,600 | 400 |
| Columns | 19 | 19, identical names and order |
| Populated house labels | 1,600 | 0 |
| Index values | Unique, sequential 0-1599 | Unique, sequential 0-399 |
| Rows with all 13 course scores present | 1,251 | 310 |
| Rows missing at least one course score | 349 | 90 |
| Duplicate full rows / duplicate indices | 0 / 0 | 0 / 0 |
| Malformed row widths | 0 | 0 |
| Malformed or non-finite populated numeric cells | 0 | 0 |

Both files are ASCII-compatible UTF-8 with comma delimiters and LF line endings.
Missing data are empty cells. The indices restart in the test file, so `Index`
is not a globally unique key across both files. There are no identical 13-course
row tuples shared between the two files, including their missing-value positions.

SHA-256 fingerprints:

- Training: `4C5D5707412273C6F37886D07CA462EEC880C4DF50C589C76C7BE0FAAE0AE81F`
- Test: `EEC9C7AA259FE1AD6C1FA95CB4F286D3DCFC378B3176DAC53491F3D85F49DB88`

## Schema in exact CSV order

The first six columns are:

| Position | Exact header | Observed type / values | Proposed role |
| --- | --- | --- | --- |
| 1 | Index | Integer, complete in both files | Row identifier; describe numerically, exclude from classifier |
| 2 | Hogwarts House | Four labels in training; entirely blank in test | Target; never an input feature |
| 3 | First Name | Text, complete | Metadata; exclude from initial model |
| 4 | Last Name | Text, complete | Metadata; exclude from initial model |
| 5 | Birthday | Date strings in year-month-day form, complete | Metadata; exclude from initial model |
| 6 | Best Hand | `Left` or `Right`, complete | Metadata; exclude from initial course-score baseline |

The next 13 columns are numeric course scores, in the exact order below. Valid
counts equal the file's row count minus missing count. No course is all-missing
or constant in either file. Rounded training ranges are shown; negative scores
are genuinely present and must not be rejected just because of their sign.

| Position | Course | Train missing | Test missing | Training min | Training max |
| --- | --- | --- | --- | --- | --- |
| 7 | Arithmancy | 34 | 13 | -24370.000 | 104956.000 |
| 8 | Astronomy | 32 | 13 | -966.741 | 1016.212 |
| 9 | Herbology | 33 | 11 | -10.296 | 11.613 |
| 10 | Defense Against the Dark Arts | 31 | 8 | -10.162 | 9.667 |
| 11 | Divination | 39 | 6 | -8.727 | 10.032 |
| 12 | Muggle Studies | 35 | 10 | -1086.497 | 1092.389 |
| 13 | Ancient Runes | 35 | 8 | 283.870 | 745.396 |
| 14 | History of Magic | 43 | 11 | -8.859 | 11.890 |
| 15 | Transfiguration | 34 | 11 | 906.627 | 1098.958 |
| 16 | Potions | 30 | 10 | -4.697 | 13.537 |
| 17 | Care of Magical Creatures | 40 | 8 | -3.314 | 3.057 |
| 18 | Charms | 0 | 0 | -261.049 | -225.428 |
| 19 | Flying | 0 | 0 | -181.470 | 279.070 |

The different score scales support standardizing model inputs. Dropping rows with
any missing course would discard 349 training students (21.8125%) and 90 test
students (22.5%). Test rows must receive predictions, so plan deterministic
training-fitted imputation rather than complete-case filtering for the model.

## Training class balance

| House | Rows | Share |
| --- | --- | --- |
| Gryffindor | 327 | 20.4375% |
| Hufflepuff | 529 | 33.0625% |
| Ravenclaw | 443 | 27.6875% |
| Slytherin | 301 | 18.8125% |
| Total | 1,600 | 100% |

The majority-class baseline is 33.0625%, far below the subject's 98% requirement.
Use stratification when constructing a validation split. All 400 test house
cells are blank: official test accuracy cannot be measured from these files alone.
For this actual test file, `houses.csv` should contain 400 predictions, with
indices 0-399 in input order and the exact required header.

## Reference descriptive statistics for training data

Each column is summarized independently from its observed values, without
imputation. Std uses the sample denominator n - 1. Quartiles use zero-based
linear interpolation at position (n - 1)q. Values are rounded to six decimal
places. These are proposed conventions explained in
[manual statistics](03-manual-statistics.md), not additional subject requirements.

This transposed table is a reference for checking the future program. The
subject's sample display instead places features across columns and statistics
down rows. `Index` is included because it is numeric, despite being excluded
from the proposed classifier inputs.

| Feature | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Index | 1600 | 799.500000 | 462.024530 | 0.000000 | 399.750000 | 799.500000 | 1199.250000 | 1599.000000 |
| Arithmancy | 1566 | 49634.570243 | 16679.806036 | -24370.000000 | 38511.500000 | 49013.500000 | 60811.250000 | 104956.000000 |
| Astronomy | 1568 | 39.797131 | 520.298268 | -966.740546 | -489.551387 | 260.289446 | 524.771949 | 1016.211940 |
| Herbology | 1567 | 1.141020 | 5.219682 | -10.295663 | -4.308182 | 3.469012 | 5.419183 | 11.612895 |
| Defense Against the Dark Arts | 1569 | -0.387863 | 5.212794 | -10.162119 | -5.259095 | -2.589342 | 4.904680 | 9.667405 |
| Divination | 1561 | 3.153910 | 4.155301 | -8.727000 | 3.099000 | 4.624000 | 5.667000 | 10.032000 |
| Muggle Studies | 1565 | -224.589915 | 486.344840 | -1086.496835 | -577.580096 | -419.164294 | 254.994857 | 1092.388611 |
| Ancient Runes | 1565 | 495.747970 | 106.285165 | 283.869609 | 397.511047 | 463.918305 | 597.492230 | 745.396220 |
| History of Magic | 1557 | 2.963095 | 4.425775 | -8.858993 | 2.218653 | 4.378176 | 5.825242 | 11.889713 |
| Transfiguration | 1566 | 1030.096946 | 44.125116 | 906.627320 | 1026.209993 | 1045.506996 | 1058.436410 | 1098.958201 |
| Potions | 1570 | 5.950373 | 3.147854 | -4.697484 | 3.646785 | 5.874837 | 8.248173 | 13.536762 |
| Care of Magical Creatures | 1560 | -0.053427 | 0.971457 | -3.313676 | -0.671606 | -0.044811 | 0.589919 | 3.056546 |
| Charms | 1600 | -243.374409 | 8.783640 | -261.048920 | -250.652600 | -244.867765 | -232.552305 | -225.428140 |
| Flying | 1600 | 21.958012 | 97.631602 | -181.470000 | -41.870000 | -2.515000 | 50.560000 | 279.070000 |

## Histogram candidate: Care of Magical Creatures

This course has similar per-house centers and spreads. It is a strong candidate
for the question about homogeneous score distributions, pending a shared-bin
histogram to inspect the full shapes.

| House | Observed values | Mean | Sample std | 25% | Median | 75% |
| --- | --- | --- | --- | --- | --- | --- |
| Gryffindor | 323 | -0.139186 | 0.988395 | -0.737608 | -0.115513 | 0.532913 |
| Hufflepuff | 515 | -0.028449 | 0.976197 | -0.593520 | 0.018346 | 0.620742 |
| Ravenclaw | 431 | 0.003899 | 0.973625 | -0.713612 | 0.006862 | 0.672262 |
| Slytherin | 291 | -0.087348 | 0.937378 | -0.674072 | -0.098988 | 0.521009 |

Arithmancy also has similar house means, roughly 49,122-50,249, but differing
spreads. Compare both visually rather than asserting that similar means prove
identical distributions. Use normalized house distributions to account for the
unequal sample counts.

## Similar pair: Astronomy and Defense Against the Dark Arts

There are **1,537** training rows with both values present. Pearson correlation
is **-1.000000** at displayed precision. More directly, the observed relationship is:

**Astronomy = -100 x Defense Against the Dark Arts.**

Across all paired training rows, the maximum absolute residual of
Astronomy + 100 x Defense Against the Dark Arts is about **4.55e-13**, consistent
with floating-point rounding. A scatter plot should therefore show an almost
exact straight line with negative slope. Similarity here means redundant
information after rescaling, not similar raw numeric values.

The missing-value masks differ, so redundancy in observed values does not mean
the two columns have identical completeness. Initially compare retaining one
column against retaining both with independent imputation. Any plan to reconstruct
one from the other should be separately justified and validated.

Other notable paired training correlations:

| Pair | Paired rows | Pearson r |
| --- | --- | --- |
| History of Magic / Flying | 1,557 | -0.896283 |
| Transfiguration / Flying | 1,566 | -0.873673 |
| History of Magic / Transfiguration | 1,523 | 0.849203 |
| Muggle Studies / Charms | 1,565 | 0.847607 |
| Herbology / Charms | 1,567 | 0.746614 |

Correlations use only rows with both values present, without imputation.

## Feature-selection clues, not a final model choice

House-specific observed means below help identify promising panels for the pair
plot. They are descriptive summaries over the full labeled training file, not a
validation experiment or proof that a feature subset reaches 98%.

| Course | Gryffindor | Hufflepuff | Ravenclaw | Slytherin |
| --- | --- | --- | --- | --- |
| Astronomy | 493.337 | 497.708 | -480.043 | -496.334 |
| Herbology | -4.784 | 4.919 | 5.022 | -4.776 |
| Divination | 4.901 | 5.022 | 4.988 | -4.814 |
| Muggle Studies | -501.483 | -498.351 | 489.112 | -478.732 |
| Ancient Runes | 596.934 | 400.147 | 597.750 | 401.814 |
| History of Magic | -4.815 | 5.010 | 4.916 | 4.968 |
| Transfiguration | 951.135 | 1049.562 | 1050.334 | 1051.899 |
| Potions | 2.938 | 4.961 | 6.972 | 9.471 |
| Charms | -252.731 | -244.347 | -231.081 | -249.593 |
| Flying | 189.025 | -7.086 | -3.980 | -70.322 |

Start by comparing all 13 course scores with a reasoned subset. Candidates for
ablation include Arithmancy and Care of Magical Creatures, whose house summaries
are similar, and one of Astronomy / Defense Against the Dark Arts, whose observed
values are redundant. Do not eliminate courses based only on these tables.
Inspect the actual pair plot and measure performance under a fixed validation
protocol. Full-file exploration has already informed these hypotheses, so do not
present a later split from the same file as a completely untouched blind test.

## Analysis method and limits

The CSVs were parsed locally without changing them. Counts, sums of deviations,
sample standard deviations, sorted-value interpolation, and paired correlations
were evaluated explicitly for this reference report. No project source files,
required entry points, plot scripts, model-fitting routines, weights, or prediction
files were created. Future project code must implement the assessed calculations
itself and follow the subject's restrictions.

Required visualizations, imputation/scaling fitted for an actual run, final
features, optimizer settings, validation accuracy, and official test accuracy
remain unmeasured or unimplemented.

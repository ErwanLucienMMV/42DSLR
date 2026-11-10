# Logistic regression reference

Subject basis: V.3, printed p. 8 and VIII.1, p. 11. These notes unpack the
subject's equations and propose practical conventions. They contain no code.
For additional background, see the classification chapter in the
[Stanford CS229 lecture notes](https://cs229.stanford.edu/notes2022fall/main_notes.pdf).

## One binary problem per house

Let m be the number of training students and d the number of retained numeric
features. For each house k, define a binary target y_(i,k): 1 when student i
belongs to k, 0 otherwise. Train four separate parameter vectors.

For a student with processed features x_1, ..., x_d, include an intercept x_0 = 1:

**z_k = theta_(k,0) + theta_(k,1)x_1 + ... + theta_(k,d)x_d**

**p_k = sigmoid(z_k) = 1 / (1 + exp(-z_k))**

Each classifier estimates membership in its house against the other three.
One-vs-rest probabilities need not sum to one. For prediction, choose the house
with the largest p_k; do not independently apply a 0.5 threshold and risk several
houses or no house. Because sigmoid is increasing, comparing finite logits z_k
gives the same ranking. Persist a fixed class order to break exact ties.

Shape checks: the processed feature matrix is m by d; with the intercept it is
m by (d + 1). Each classifier has d + 1 parameters; all four together have
4(d + 1) weights. Every feature name and position must match at prediction time.

## Binary cross-entropy and gradient

For a single house, with p_i = sigmoid(theta dot x_i):

**J(theta) = -(1/m) sum_i [y_i ln(p_i) + (1 - y_i) ln(1 - p_i)]**

The subject's partial derivative for component j is:

**g_j = (1/m) sum_i [(p_i - y_i)x_(i,j)]**

The intercept follows the same expression with x_(i,0) = 1. There is no extra
sigmoid derivative factor in this combined cross-entropy gradient.

For learning rate alpha > 0, perform the simultaneous update:

**theta_j(new) = theta_j(old) - alpha g_j(theta(old)).**

Compute all gradient components from the same old parameter vector, then update
them together. Use all m training examples in an ordinary full-batch update.
For a simple baseline, zero initialization is sufficient for this linear model.
Keep regularization and alternative optimizers out of the initial baseline.

## Numerical stability

Large magnitude logits can overflow a naive exponential. A stable sigmoid uses
1 / (1 + exp(-z)) for nonnegative z, and exp(z) / (1 + exp(z)) for negative z.
The exponent is nonpositive in each branch.

An equivalent stable per-observation loss expressed in logits is:

**loss(z, y) = max(z, 0) - y z + ln(1 + exp(-abs(z))).**

Here `max` denotes an elementary two-value comparison in a mathematical identity,
not a shortcut for the forbidden descriptive maximum calculation. A numerically
accurate elementary logarithm-of-one-plus operation can evaluate the last term.
The gradient remains (p - y)x. Reject non-finite data and parameters explicitly.

## Scaling and missing values

Recommended baseline: training-fitted median imputation followed by standardization
of each retained numeric feature. For this scaling convention:

**x_scaled = (x_imputed - mu_train) / sigma_train**, where
**sigma_train = sqrt(sum_i (x_imputed_i - mu_train)^2 / m).**

This uses population standard deviation for scaling. It is a separate explicit
choice from the proposed sample standard deviation in `describe`. Both statistics
must be implemented manually. Do not scale the constant intercept.

Compute these parameters using only training-partition data during validation;
use the same saved parameters for all subsequent rows. Handle a zero scale or
all-missing feature as described in the [data investigation guide](02-data-investigation.md).
Scaling helps keep gradient descent from progressing at very different rates
along features with different numerical ranges.

## Convergence and correctness checks

Track the loss of each binary classifier, not just final accuracy. Record the
learning rate, iteration limit, stopping rule, and whether the run converged.
If loss explodes or oscillates, inspect the gradient, scaling, and learning rate.
Slow improvement may indicate a rate that is too small. Training accuracy alone
cannot select a reliable configuration.

The subject does not prescribe a tolerance or iteration budget. Choose them after
observing convergence. A finite limit and a clearly reported stopping reason
prevent an endless run. Relative loss improvement or gradient size can support
a stopping rule; do not silently declare success after a single small change.

Useful future hand checks:

- At zero weights, every sigmoid is 0.5 and binary loss is ln(2), about 0.693147.
- With one intercept-only example labeled 1, the initial gradient is -0.5.
  A descent update must increase the intercept and lower the loss.
- For a tiny synthetic case, compare an analytic gradient component to
  [J(theta + epsilon e_j) - J(theta - epsilon e_j)] / (2 epsilon).
  A small epsilon, such as 0.00001, is a starting point; compare with a tolerance
  because floating-point arithmetic is approximate.

## Saved model: more than weights

The subject requires a file containing learned weights but leaves its format open.
A self-contained model artifact should also contain:

| Field | Why prediction needs it |
| --- | --- |
| Format version | Detect incompatible future layouts |
| Ordered house labels | Map classifier outputs back to exact house names |
| Ordered selected feature names | Align CSV columns with learned coefficients |
| Intercept and coefficients for all four houses | Evaluate the learned linear scores |
| Missing-value rules and per-feature fill values | Reproduce training imputation |
| Per-feature mean and scale, plus constant-feature policy | Reproduce training normalization |
| Training settings and dataset fingerprint | Explain and reproduce the training run |

A simple human-readable format such as JSON is a reasonable future choice, not
a mandated filename or format. Prediction must load the artifact without fitting
anything again. Validate dimensions, required fields, label uniqueness, and finite
numeric values. Reordered CSV columns can be aligned by saved names; a missing
required column needs an explicit error.

Preserve every valid test row and its order, choose one allowed label, then write
`houses.csv` using the [required layout](01-requirements.md). A separate prediction
process must be sufficient: it must not depend on an in-memory training session.

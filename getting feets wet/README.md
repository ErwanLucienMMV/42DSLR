# Getting feet wet: one neuron learns logic gates

This small proof of concept practices the binary logistic-regression calculation
needed for DSLR. It learns **AND** and **OR**, then tries **XOR** to demonstrate
the limits of a linear decision boundary. The code is heavily commented so you
can follow the reasons behind the calculations.

It uses two weights, one bias, a sigmoid, binary cross-entropy, and full-batch
gradient descent. Everything is calculated explicitly using Python's standard
library. There are no dependencies to install, no hidden layers, and no Hogwarts
data are read or changed. The main DSLR programs remain unimplemented.

## Run it

Use Python 3.10 or newer. From the repository root:

```powershell
python "getting feets wet/demo.py"
```

The default runs all three experiments, each starting from fresh zero parameters
and taking 10,000 updates at learning rate 1.0. You can run one experiment and
adjust the training settings:

```powershell
python "getting feets wet/demo.py" --gate and
python "getting feets wet/demo.py" --gate or --iterations 1000
python "getting feets wet/demo.py" --gate xor
python "getting feets wet/demo.py" --gate and --learning-rate 0.1 --iterations 100
python "getting feets wet/demo.py" --help
```

The output shows loss at selected updates, final weights and bias, and each row's
target, predicted probability, and binary prediction. Probabilities are displayed
to six decimal places, so a printed 0.000000 or 1.000000 can be a rounded value.

## Read the code in this order

1. [demo.py](demo.py): inspect `INPUTS` and `TARGETS`. The labels tell the algorithm
   the desired answers; the algorithm does not know the gate's logical rule.
2. [logistic_regression.py](logistic_regression.py): read `Neuron.score`,
   `probability`, and `predict` to follow one forward prediction.
3. In that same file, read `loss_and_gradient`: it measures prediction quality
   and calculates how changing each parameter would affect the loss.
4. Read `train`: each iteration uses those gradients to update all parameters.
5. [test_logistic_regression.py](test_logistic_regression.py): read the one-step
   example and finite-difference check to see how to verify the mathematics.

## What the neuron calculates

For inputs x0 and x1:

**score z = w0*x0 + w1*x1 + bias**

**probability p = sigmoid(z) = 1 / (1 + exp(-z))**

The hard prediction is 1 when p >= 0.5, otherwise 0. The boundary occurs at
w0*x0 + w1*x1 + bias = 0, a straight line in the input plane. The bias lets that
line move away from the origin. A sigmoid changes the score into a probability
but does not make this boundary curved.

Training minimizes average binary cross-entropy:

**J = average of -[y*ln(p) + (1-y)*ln(1-p)].**

The implementation evaluates an equivalent expression in terms of z to avoid
logarithms of rounded zero probabilities. Its stable sigmoid also avoids
overflowing exponentials. Those branches are numerical precautions; they leave
the mathematical model unchanged.

## Why the updates look this way

For one training row, the derivative of loss with respect to the score simplifies
to **p - y**. Multiplying by an input gives the corresponding weight derivative:

- dJ/dw0 = average of (p-y)*x0.
- dJ/dw1 = average of (p-y)*x1.
- dJ/dbias = average of (p-y), because the bias's input is effectively 1.

The gradient points toward increasing loss. Therefore gradient descent subtracts
it: **new parameter = old parameter - learning_rate*gradient**. Every derivative
in a step must use the same old parameters, which is why the implementation
creates a new immutable `Neuron` only after all gradients have been calculated.

One concrete step: train on just input (1, 2) with target 1, initially using zero
parameters. The initial probability is 0.5, so p-y = -0.5. The gradients are
(-0.5, -1.0) for the weights and -0.5 for the bias. A learning rate of 1 gives new
weights (0.5, 1.0) and bias 0.5. The new score is 3 and the probability is about
0.952574, moving toward the desired answer. A test checks this known result.

## Expected results with the defaults

| Gate | Initial loss | Final loss, approximately | Truth-table accuracy |
| --- | --- | --- | --- |
| AND | 0.693147 | 0.001713 | 4/4, 100% |
| OR | 0.693147 | 0.000906 | 4/4, 100% |
| XOR | 0.693147 | 0.693147 | 2/4, 50% in this setup |

AND and OR are linearly separable: one line can separate their positive and
negative examples. A model can classify all four cases correctly before its
probabilities become particularly confident, so accuracy may reach 100% while
loss keeps decreasing. For separable data without regularization, weights can
continue growing as loss approaches zero; there need not be a finite best set
of weights. A fixed iteration budget keeps this teaching example simple.

For XOR, the positive corners (0,1) and (1,0) alternate with negative corners
(0,0) and (1,1). No single straight line can separate all four. In addition,
zero initialization gives p=0.5 everywhere, and the positive and negative
gradient contributions cancel exactly. Training therefore stays at zero weights
and zero bias. The explicit tie rule assigns every row to 1, giving 50%.

That 50% describes this initialization and full-batch experiment. Some linear
boundaries can classify three XOR rows correctly, but none can classify all four.
A nonlinear hidden layer or engineered interaction feature would change the
model's expressive power; neither is needed for this logistic-regression POC.

These accuracies are measured on the same four rows used for training. This is
a check that a truth table can be fitted, not a measurement of generalization
or evidence toward DSLR's 98% evaluation target.

## Run the checks

```powershell
python -m unittest discover -s "getting feets wet" -p "test_*.py" -v
```

The checks cover the initial loss, a known update, finite-difference agreement
for all three gradients, extreme-score stability, learning AND/OR, the stationary
XOR case, reproducibility, and invalid inputs/settings. Finite differences
approximate a derivative by perturbing one parameter in each direction; agreement
with the analytic derivative helps detect sign mistakes and missing factors.

## Experiments to understand the behavior

- Reduce the learning rate while keeping the update count fixed. Compare how far
  the loss falls and whether every hard prediction is already correct.
- Run AND for 1, 10, 100, and 1,000 updates. Watch the bias move before the weights
  start responding, and distinguish improving probabilities from improving accuracy.
- Increase the rate gradually. A larger step can overshoot; convergence is not
  guaranteed for an arbitrary learning rate.
- Compare AND's and OR's final bias. Think about where a straight line must sit
  to isolate only (1,1), or only (0,0), respectively.

## Connection to DSLR

DSLR extends this binary calculation to many selected course scores and trains
four separate classifiers, one per house against the others. It then chooses the
house with the highest score. That extension also needs CSV handling, missing-data
imputation, scaling, feature selection, validation, and model persistence.

This POC deliberately keeps only two tiny inputs so the loss and gradient steps
are easy to inspect before introducing those additional responsibilities.

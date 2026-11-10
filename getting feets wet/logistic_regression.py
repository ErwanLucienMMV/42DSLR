"""A two-input sigmoid neuron, trained with explicitly calculated gradients.

This is binary logistic regression: two weights, one bias, and no hidden layer.
Only Python's standard library is used. In particular, no library computes the
loss, differentiates it, or fits the parameters for us.

Start reading at Neuron, then loss_and_gradient, then train. The demo supplies
truth tables separately so the learning algorithm never needs to know gate rules.
"""

from dataclasses import dataclass
import math


# One example contains two numeric inputs and the expected binary answer.
# The answer is a target used during training, never an extra input to the neuron.
Example = tuple[tuple[float, float], int]


def sigmoid(z: float) -> float:
    """Convert a linear score into a number between zero and one."""
    # The usual formula is 1 / (1 + exp(-z)). If z is very negative, exp(-z)
    # can overflow. These equivalent branches only exponentiate nonpositive
    # numbers, so even large finite scores can be evaluated safely.
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    exponential = math.exp(z)
    return exponential / (1.0 + exponential)


@dataclass(frozen=True)
class Neuron:
    """The learned model: a straight boundary followed by a sigmoid.

    'Frozen' means a model cannot be changed in place. Each training step creates
    a new model, making it clear that all gradients use the OLD parameters.
    """

    weights: tuple[float, float] = (0.0, 0.0)
    bias: float = 0.0

    def score(self, inputs: tuple[float, float]) -> float:
        # Each weight measures how its input changes the linear score.
        # The bias shifts the boundary, allowing it to move away from the origin.
        return self.weights[0] * inputs[0] + self.weights[1] * inputs[1] + self.bias

    def probability(self, inputs: tuple[float, float]) -> float:
        return sigmoid(self.score(inputs))

    def predict(self, inputs: tuple[float, float]) -> int:
        # Training uses continuous probabilities, which have useful derivatives.
        # We turn them into a hard 0/1 answer only when making a prediction.
        # Exactly 0.5 is deliberately assigned to class 1 for deterministic ties.
        return 1 if self.probability(inputs) >= 0.5 else 0


def loss_and_gradient(
    model: Neuron, examples: tuple[Example, ...]
) -> tuple[float, tuple[float, float], float]:
    """Return mean binary cross-entropy and its weight and bias derivatives."""
    if not examples:
        raise ValueError("At least one training example is required.")

    total_loss = 0.0
    weight_gradient_0 = 0.0
    weight_gradient_1 = 0.0
    bias_gradient = 0.0

    for inputs, target in examples:
        score = model.score(inputs)
        probability = sigmoid(score)

        # Binary cross-entropy is -[y*log(p) + (1-y)*log(1-p)].
        # A confident wrong prediction has a large loss. A confident correct
        # prediction has a small loss. Lower average loss is the training goal.
        #
        # Directly taking log(p) is unsafe: floating-point sigmoid can round
        # to exactly 0 or 1. This equivalent expression works on the score:
        #   max(score, 0) - target*score + log(1 + exp(-abs(score))).
        # log1p computes log(1 + a) accurately when a is very small.
        positive_score = score if score > 0.0 else 0.0
        total_loss += (
            positive_score
            - target * score
            + math.log1p(math.exp(-abs(score)))
        )

        # Combining sigmoid with cross-entropy gives the simple derivative
        # d(loss)/d(score) = p - y. The sigmoid derivative has ALREADY been
        # accounted for in this simplification; do not multiply by it again.
        error = probability - target

        # Chain rule: score = w0*x0 + w1*x1 + bias.
        # Its derivatives with respect to w0, w1, bias are x0, x1, and 1.
        weight_gradient_0 += error * inputs[0]
        weight_gradient_1 += error * inputs[1]
        bias_gradient += error

    # Average over the full truth table: this is FULL-BATCH gradient descent.
    # Averaging also makes the learning rate less dependent on dataset size.
    count = len(examples)
    return (
        total_loss / count,
        (weight_gradient_0 / count, weight_gradient_1 / count),
        bias_gradient / count,
    )


@dataclass(frozen=True)
class TrainingResult:
    model: Neuron
    # losses[0] is before any update; losses[t] is after t updates.
    # Retaining the trace is cheap here: there are only four training examples.
    losses: tuple[float, ...]


def train(
    examples: tuple[Example, ...],
    learning_rate: float = 1.0,
    iterations: int = 10_000,
) -> TrainingResult:
    """Learn two weights and a bias; keep the loss trace for inspection."""
    if not math.isfinite(learning_rate) or learning_rate <= 0.0:
        raise ValueError("Learning rate must be finite and greater than zero.")
    if not isinstance(iterations, int) or iterations <= 0:
        raise ValueError("Iterations must be a positive integer.")
    if not examples:
        raise ValueError("At least one training example is required.")
    for inputs, target in examples:
        if len(inputs) != 2 or not all(math.isfinite(value) for value in inputs):
            raise ValueError("Each example needs two finite input values.")
        if target not in (0, 1):
            raise ValueError("Targets must be 0 or 1.")

    # Zero initialization is fine for one logistic-regression neuron. There are
    # no hidden neurons whose symmetry would need to be broken randomly.
    # It also makes runs deterministic and easy to reproduce while learning.
    model = Neuron()
    losses = []

    for _ in range(iterations):
        loss, weight_gradient, bias_gradient = loss_and_gradient(model, examples)
        losses.append(loss)

        # A gradient points uphill. Subtracting it takes a step downhill:
        #   parameter_new = parameter_old - learning_rate * gradient.
        # Both weights and the bias use the SAME old model's gradients.
        model = Neuron(
            weights=(
                model.weights[0] - learning_rate * weight_gradient[0],
                model.weights[1] - learning_rate * weight_gradient[1],
            ),
            bias=model.bias - learning_rate * bias_gradient,
        )
        if not all(math.isfinite(value) for value in (*model.weights, model.bias)):
            raise ValueError("Training produced non-finite parameters; lower the learning rate.")

    # There is no early stopping in this teaching example. A fixed iteration
    # budget makes the sequence easy to follow; convergence is inspected through
    # the trace. Separable gates can keep lowering loss after reaching 100%.
    final_loss, _, _ = loss_and_gradient(model, examples)
    losses.append(final_loss)
    return TrainingResult(model=model, losses=tuple(losses))

"""Run small truth-table experiments using the same learning algorithm.

From the repository root:
    python "getting feets wet/demo.py"
    python "getting feets wet/demo.py" --gate and --iterations 1000
"""

import argparse

from logistic_regression import Example, train


# The algorithm sees only inputs and labels. Keeping the truth tables here makes
# it clear that train() does not contain a hand-written AND, OR, or XOR solution.
# The four rows always appear in this order: 00, 01, 10, 11.
INPUTS = ((0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0))
TARGETS = {
    "and": (0, 0, 0, 1),
    "or": (0, 1, 1, 1),
    "xor": (0, 1, 1, 0),
}


def gate_examples(gate: str) -> tuple[Example, ...]:
    """Attach each input pair to its known answer for the requested experiment."""
    return tuple(zip(INPUTS, TARGETS[gate]))


def run_experiment(gate: str, learning_rate: float, iterations: int) -> None:
    examples = gate_examples(gate)
    result = train(examples, learning_rate=learning_rate, iterations=iterations)
    model = result.model

    print(f"\n{gate.upper()} - one sigmoid neuron, no hidden layer")
    print(f"Learning rate: {learning_rate:g}; full-batch updates: {iterations}")
    print("Loss trace (binary cross-entropy):")

    # A few checkpoints show the scale of improvement without printing 10,001
    # lines. Include the user's final iteration even if it is not a power of ten.
    checkpoints = sorted({0, 1, 10, 100, 1000, iterations})
    for step in checkpoints:
        if step <= iterations:
            print(f"  after {step:>6} updates: {result.losses[step]:.6f}")

    print(f"Weights: ({model.weights[0]:.6f}, {model.weights[1]:.6f})")
    print(f"Bias: {model.bias:.6f}")
    print(" x0  x1 | target | probability | prediction")
    print("--------+--------+-------------+-----------")

    correct = 0
    for inputs, target in examples:
        probability = model.probability(inputs)
        prediction = model.predict(inputs)
        if prediction == target:
            correct += 1
        print(
            f" {inputs[0]:.0f}   {inputs[1]:.0f} |    {target}   |"
            f"    {probability:.6f} |     {prediction}"
        )

    # These are the SAME four rows used for learning. This checks that the model
    # can fit a truth table; it is not an estimate of unseen-data performance.
    print(f"Truth-table accuracy: {correct}/{len(examples)} ({correct / len(examples):.0%})")

    if gate == "xor":
        print("XOR cannot be perfectly separated by this model's straight boundary.")
        print("With this balanced table and zero initialization, the gradient is zero:")
        print("every probability stays at 0.5, and the fixed tie rule predicts 1.")
        print("The resulting 50% is expected here, not a training implementation failure.")
    else:
        print("This gate is linearly separable, so the neuron can learn all four rows.")
        print("Loss can keep improving after every hard prediction becomes correct.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Learn AND/OR and inspect why raw-input logistic regression cannot solve XOR."
    )
    parser.add_argument("--gate", choices=("and", "or", "xor", "all"), default="all")
    parser.add_argument("--learning-rate", type=float, default=1.0)
    parser.add_argument("--iterations", type=int, default=10_000)
    args = parser.parse_args()

    # Report invalid user settings as concise CLI errors, rather than a traceback.
    # The core validates them too, so direct callers get the same protections.
    gates = tuple(TARGETS) if args.gate == "all" else (args.gate,)
    try:
        for gate in gates:
            run_experiment(gate, args.learning_rate, args.iterations)
    except ValueError as error:
        parser.error(str(error))


# Importing gate_examples in tests must not run the demonstration automatically.
if __name__ == "__main__":
    main()

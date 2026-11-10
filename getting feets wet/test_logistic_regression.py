"""Small mathematical checks, so a plausible demo is not our only evidence.

Run from the repository root:
    python -m unittest discover -s "getting feets wet" -p "test_*.py" -v

These tests use known answers and numerical differentiation to independently
check the learning calculations. They do not use a machine-learning library.
"""

import math
import unittest

from demo import gate_examples
from logistic_regression import Neuron, loss_and_gradient, sigmoid, train


class LogisticRegressionTests(unittest.TestCase):
    def test_zero_parameters_give_half_probability_and_log_two_loss(self):
        # This is a useful reference point before any training: a score of zero
        # gives p=0.5, and either binary label then incurs loss -log(0.5).
        model = Neuron()
        for inputs, _ in gate_examples("and"):
            self.assertEqual(model.probability(inputs), 0.5)
        loss, _, _ = loss_and_gradient(model, gate_examples("and"))
        self.assertAlmostEqual(loss, math.log(2.0))

    def test_one_step_moves_all_parameters_from_the_same_old_prediction(self):
        # At zero parameters, p-y = -0.5 for this positive example.
        # Therefore gradients are (-0.5*1, -0.5*2) and bias gradient -0.5.
        # With rate 1, subtracting them gives weights (0.5, 1) and bias 0.5.
        # Updating parameters prematurely within a step would change this answer.
        examples = (((1.0, 2.0), 1),)
        result = train(examples, learning_rate=1.0, iterations=1)
        self.assertEqual(result.model.weights, (0.5, 1.0))
        self.assertEqual(result.model.bias, 0.5)
        self.assertLess(result.losses[-1], result.losses[0])

    def test_gradient_matches_numerical_differentiation(self):
        examples = gate_examples("or")
        parameters = (0.3, -0.7, 0.2)
        model = Neuron(weights=parameters[:2], bias=parameters[2])
        _, weight_gradient, bias_gradient = loss_and_gradient(model, examples)
        analytic_gradient = (*weight_gradient, bias_gradient)
        epsilon = 0.000001

        # Numerical differentiation asks: how much does the loss change if ONE
        # parameter moves a tiny amount? It checks our analytic derivative via
        # a separate route: [J(theta+e) - J(theta-e)] / (2e).
        for position in range(3):
            with self.subTest(parameter=position):
                above = list(parameters)
                below = list(parameters)
                above[position] += epsilon
                below[position] -= epsilon
                high_loss, _, _ = loss_and_gradient(
                    Neuron(weights=tuple(above[:2]), bias=above[2]), examples
                )
                low_loss, _, _ = loss_and_gradient(
                    Neuron(weights=tuple(below[:2]), bias=below[2]), examples
                )
                numerical_gradient = (high_loss - low_loss) / (2.0 * epsilon)
                self.assertAlmostEqual(
                    analytic_gradient[position], numerical_gradient, places=7
                )

    def test_extreme_scores_have_finite_loss_and_gradient(self):
        # Naive exp(1000) overflows, and naive log(0) fails. Confident WRONG
        # predictions should instead give a large but finite loss of about 1000.
        self.assertEqual(sigmoid(-1000.0), 0.0)
        self.assertEqual(sigmoid(1000.0), 1.0)
        model = Neuron(weights=(1000.0, 0.0))
        examples = (((1.0, 0.0), 0), ((-1.0, 0.0), 1))
        loss, weights, bias = loss_and_gradient(model, examples)
        self.assertAlmostEqual(loss, 1000.0)
        for value in (loss, *weights, bias):
            self.assertTrue(math.isfinite(value))

    def test_and_and_or_are_learned_with_decreasing_loss(self):
        for gate in ("and", "or"):
            with self.subTest(gate=gate):
                examples = gate_examples(gate)
                result = train(examples, iterations=1000)
                self.assertEqual(len(result.losses), 1001)
                for inputs, expected in examples:
                    self.assertEqual(result.model.predict(inputs), expected)
                self.assertLess(result.losses[-1], 0.03)
                # This monotonic behavior is expected for THESE small examples
                # with rate 1; gradient descent is not stable at every rate.
                for earlier, later in zip(result.losses, result.losses[1:]):
                    self.assertLessEqual(later, earlier + 1e-12)

    def test_balanced_xor_is_stationary_at_zero_initialization(self):
        examples = gate_examples("xor")
        _, weight_gradient, bias_gradient = loss_and_gradient(Neuron(), examples)
        self.assertEqual(weight_gradient, (0.0, 0.0))
        self.assertEqual(bias_gradient, 0.0)
        result = train(examples, iterations=100)
        self.assertEqual(result.model, Neuron())
        self.assertAlmostEqual(result.losses[-1], math.log(2.0))
        correct = 0
        for inputs, expected in examples:
            if result.model.predict(inputs) == expected:
                correct += 1
        self.assertEqual(correct, 2)

    def test_training_is_reproducible(self):
        # There is no random initialization or shuffled mini-batch order.
        examples = gate_examples("and")
        self.assertEqual(train(examples, iterations=10), train(examples, iterations=10))

    def test_invalid_training_settings_are_rejected(self):
        examples = gate_examples("and")
        for rate in (0.0, -1.0, math.inf, math.nan):
            with self.subTest(learning_rate=rate), self.assertRaises(ValueError):
                train(examples, learning_rate=rate)
        for iterations in (0, -1, 1.5):
            with self.subTest(iterations=iterations), self.assertRaises(ValueError):
                train(examples, iterations=iterations)

    def test_invalid_examples_are_rejected(self):
        invalid_tables = (
            (),
            (((1.0, 0.0), 2),),
            (((math.nan, 0.0), 1),),
            (((math.inf, 0.0), 1),),
            (((1.0,), 1),),
        )
        for examples in invalid_tables:
            with self.subTest(examples=examples), self.assertRaises(ValueError):
                train(examples)


if __name__ == "__main__":
    unittest.main()

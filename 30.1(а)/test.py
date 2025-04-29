import  unittest
from function import function
from math import log
import random


class TestFunction(unittest.TestCase):

    def test_01_equal(self):
        x = 0
        eps = 0.1
        expected_value = 0
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value)

    def test_02_equal(self):
        x = 0.5
        eps = 1e-3
        expected_value = log(1 + x)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=0.001)

    def test_03_equal(self):
        with self.assertRaises(AssertionError):
            function(0.5, 0)

    def test_04_equal(self):
        x = 0.999
        eps = 1e-5
        expected_value = log(1 + x)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=eps)

    def test_05_equal(self):
        x = -0.5
        eps = 1e-4
        expected_value = log(1 + x)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=eps)

    def test_06_equal(self):
        x = 0.3
        eps = 1e-6
        expected_value = log(1 + x)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=eps)

    def test_07_equal(self):
        x = random.uniform(-0.1, 0.1)
        eps = 1e-7
        expected_value = log(1 + x)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=eps)

    def test_08_equal(self):
        x = 0.6
        for eps in [1e-2, 1e-4, 1e-6]:
            with self.subTest(eps=eps):
                expected_value = log(1 + x)
                value = function(x, eps)
                self.assertAlmostEqual(expected_value, value, delta=eps)

    def test_09_equal(self):
        x1 = 0.8888
        x2 = 0.9999
        eps = 1e-6
        value1 = function(x1, eps)
        value2 = function(x2, eps)
        self.assertLess(value1, value2)

    def test_10_equal(self):
        with self.assertRaises(AssertionError):
            function(-1, 0.1)  # abs(x) >= 1 → виняток
        with self.assertRaises(AssertionError):
            function(0, 0)  # eps == 0 → виняток
        with self.assertRaises(AssertionError):
            function(20, -20)  # abs(x) >= 1 і eps < 0 → виняток


if __name__ == "__main__":
    unittest.main(verbosity=2)

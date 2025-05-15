import unittest
from T30_1ж import f_sum
from math import sqrt

class TestSqrtSeries(unittest.TestCase):
    def test_1_domain_x(self):
        _, err = f_sum(1.0, 1e-6)
        self.assertEqual(err, 1)

    def test_2_domain_eps(self):

        _, err = f_sum(0.5, 0)
        self.assertEqual(err, 2)

    def test_3_zero(self):
        y, err = f_sum(0, 1e-6)
        self.assertTrue(err == 0 and abs(y - 1) < 1e-6)

    def test_4_accuracy(self):
        x = 0.3
        eps = 1e-8
        expected = 1 / sqrt(1 + x)
        result, err = f_sum(x, eps)
        self.assertTrue(err == 0 and abs(result - expected) < eps)

    def test_5_multiple_eps(self):
        x = 0.7
        for eps in [1e-2, 1e-4, 1e-6]:
            with self.subTest(eps=eps):
                result, err = f_sum(x, eps)
                expected = 1 / sqrt(1 + x)
                self.assertTrue(err == 0 and abs(result - expected) < eps)

if __name__ == "__main__":
    unittest.main()

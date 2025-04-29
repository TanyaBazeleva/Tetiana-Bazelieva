import unittest
from T30_1a import *
from math import log1p

class Test_log1p(unittest.TestCase):
    """Клас містить тести для перевірки функції f_ln(x, eps)."""

    def test_1_isx1(self):
        """1 - перевірити, що abs(x) ≥ 1 → помилка"""
        _, Er = f_ln(2, 1e-6)
        self.assertEqual(Er, 1, "значення abs(x) ≥ 1")

    def test_2_iseps(self):
        """2 - перевірити, що eps ∉ (0,1) → помилка"""
        _, Er = f_ln(0.2, 2)
        self.assertEqual(Er, 2, "значення eps ∉ (0,1)")

    def test_3_iszero(self):
        """3 - перевірити, що f_ln(0, eps) = 0"""
        x = 0
        eps = 1e-6
        f, Er = f_ln(x, eps)
        self.assertTrue(Er == 0 and abs(f) < eps, f"f_ln(0, eps) = {f}")

    def test_4_islog1p(self):
        """4 - перевірити, що f_ln(x, eps) ≈ log1p(x)"""
        x = 0.4346
        eps = 1e-12
        f, Er = f_ln(x, eps)
        self.assertTrue(Er == 0 and abs(f - log1p(x)) < eps,
                        f"abs(f_ln(x, eps) - log1p(x)) = {abs(f - log1p(x))}")

if __name__ == "__main__":
    unittest.main()

import unittest
import os
import shutil
from T30_14 import *

class TestCompareDirectories(unittest.TestCase):
    def setUp(self):
        os.makedirs("test_dir1", exist_ok=True)
        os.makedirs("test_dir2", exist_ok=True)
        with open("test_dir1/a.txt", "w"): pass
        with open("test_dir1/b.txt", "w"): pass
        with open("test_dir2/b.txt", "w"): pass
        with open("test_dir2/c.txt", "w"): pass

    def test_2_compare_diff(self):
        diff = compare_directories("test_dir1", "test_dir2")
        self.assertEqual(set(diff), {"a.txt", "c.txt"})

    def test_3_write_result(self):
        diff = compare_directories("test_dir1", "test_dir2")
        output_file = "diff_result.txt"
        write_result(diff, output_file)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read().strip().split("\n")
        self.assertEqual(set(content), {"a.txt", "c.txt"})

    def tearDown(self):
        shutil.rmtree("test_dir1", ignore_errors=True)
        shutil.rmtree("test_dir2", ignore_errors=True)
        if os.path.exists("diff_result.txt"):
            os.remove("diff_result.txt")

if __name__ == "__main__":
    unittest.main()

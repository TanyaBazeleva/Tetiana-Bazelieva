import unittest
from T30.5 import *

class Test_log1p(unittest.TestCase):
    def setUp(self):
        self.createEmptyFile("1.txt")
        self.createOneLineFile("2.txt")
        self.createMultLineFile("3.txt")
        self.createErrorLineFile("4.txt")
    def createEmptyFile(self, fname):
        f = open(fname, "w")
        f.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
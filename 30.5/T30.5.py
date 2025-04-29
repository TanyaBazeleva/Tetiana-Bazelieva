import sys
import os

INPUT_FILE = "test1.txt"
def max_file_number(fname):
    try:
        list_number = []
        f = open(fname)
        for line in f.readline():
            numbers = line.split()
            for x_str in numbers:
                try:
                    x = float(x_str)
                    list_number.append(x)
                except ValueError as e:
                    raise e
                except Exception as e:
                    raise e
        return max(list_number)
    except Exception as e:
        raise e
if __name__ == "__main__":
    m = max_file_number(INPUT_FILE)
    print("max=", m)
import os

def compare_directories(dir1, dir2):
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1
    return sorted(only_in_dir1.union(only_in_dir2))

def write_result(diff_list, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for filename in diff_list:
            f.write(filename + "\n")

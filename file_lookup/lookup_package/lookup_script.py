import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--tolerance", "-t", type=float, help="Tolerance for size difference with similar sizes", default=0.1, required=False)

pattern = '*.pdf'
similar_size = "ER-27"
remove_dot_folders = True
tol = 0.2


def match_exists(pattern, string) -> bool:
    return len([m.start() for m in re.finditer(pattern=pattern, string=string)]) > 0

os.system(f"cd ~/ && find -iname '{pattern}' > lookup_files.txt")

with open("lookup_files.txt", "r") as f:
    files = f.readlines()

files = [file.replace("\n", "") for file in files]

if remove_dot_folders:
    files = [file for file in files if not match_exists(r"[^a-zA-Z0-9]\.[a-zA-Z0-9]+", file)]

similar_size_files = [file for file in files if similar_size in file]

sizes = [os.path.getsize(file) for file in files]

similar_size_files_sizes = [os.path.getsize(file) for file in similar_size_files]

size_filtered_files = [file for file, size in zip(files, sizes) if any(abs(size/similar_size - 1) <= tol for similar_size in similar_size_files_sizes)]

for file in size_filtered_files:
    print(file)
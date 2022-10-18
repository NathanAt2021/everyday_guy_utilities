import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--tolerance",
    "-t",
    type=float,
    help="Tolerance for relative size difference with similar files' sizes. Must be a float between 0 and 1. Defaults to 0.1 (10%).",
    default=0.1,
    required=False,
)
parser.add_argument(
    "--pattern",
    "-p",
    type=str,
    help="Pattern to search with. Must be similar to patterns used with the 'find -iname' command line.",
    required=True,
)
parser.add_argument(
    "--similar-file-filter",
    "-s",
    type=str,
    help="A substring that is contained in reference file used for size filtering. If not used, will return all files that match the pattern.",
    required=False,
    default=None,
)
parser.add_argument(
    "--remove-dot-folders",
    "-d",
    type=bool,
    help="Whether to remove dot folders that are often used in packages and OS config files. Defaults to True.",
    required=False,
    default=True,
)
parser.add_argument(
    "--lookup-file-file-name",
    "-l",
    type=str,
    help="Name under which to store the results of the 'find -iname' command line before filtering with Python. Defaults to 'lookupFilez.txt'. If you have a file under this name, change this argument to a file name you don't have in your root folder.",
    required=False,
    default="lookupFilez.txt",
)
args = parser.parse_args()

pattern: str = args.pattern
similar_size: str = args.similar_file_filter
tol: float = args.tolerance
remove_dot_folders: bool = args.remove_dot_folders
lookup_file: str = args.lookup_file_file_name


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

size_filtered_files = [
    file
    for file, size in zip(files, sizes)
    if any(abs(size / similar_size - 1) <= tol for similar_size in similar_size_files_sizes)
]

for file in size_filtered_files:
    print(file)

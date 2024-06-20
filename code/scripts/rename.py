"""Rename files to shorter names.
Files are read from "../../data/mfa_data/corpus/" unless specified otherwise (see usage below).

Usage:
    python rename.py --in_path <path>
"""

import os

import argparse
from tqdm.auto import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_path", type=str, default="../../data/mfa_data/corpus/", required=False)
    args = parser.parse_args()

    in_path = args.in_path

    for file in tqdm(os.listdir(args.in_path)):
        name = file.split("_")
        #if file.endswith(".TextGrid"):
        if name[2]=="A.TextGrid" or name[2]=="B.TextGrid":
            os.remove(f"{args.in_path}{file}")
        os.rename(f"{args.in_path}{file}", f"{args.in_path}{name[2]}")
        #if file.endswith(".wav"):
            #os.rename(f"{in_path}{file}", f"{in_path}{name[3]}")

"""Rename files to shorter names.

Usage:
    python rename.py
"""

import os
from collections import Counter

import tgt
from tqdm.auto import tqdm

if __name__ == "__main__":
    in_path = "../../data/mfa_data/corpus/"

    for file in tqdm(os.listdir(in_path)):
        name = file.split("_")
        if file.endswith(".TextGrid"):
            os.rename(f"{in_path}{file}", f"{in_path}{name[2]}")
        if file.endswith(".wav"):
            os.rename(f"{in_path}{file}", f"{in_path}{name[3]}")

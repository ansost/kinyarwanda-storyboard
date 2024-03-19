"""Util script to change the original tg file names to a shorter format.
Presupposes that the textgrids are stored in "../../data/textgrids/".

Usage:
    python change_filenames.py
"""

import os

if __name__ == "__main__":
    path = "../../data/textgrids"
    for file in os.listdir(path):
        name = file.split("_")
        os.rename(f"{path}/{file}", f"{path}/grid_{name[2][:-9]}.tg")

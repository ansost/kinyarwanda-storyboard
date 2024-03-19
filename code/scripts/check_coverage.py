"""Check coverage of fleurs words and the textgrids.

Usage:
    python check_coverage.py
"""

import os

import pandas as pd
import tgt

if __name__ == "__main__":
    data_path = "../../data/"
    df = pd.read_csv(
        f"{data_path}epifleur_pronunciation_dict.tsv", sep="\t", header=None
    )
    fleurs_words = set(df[df.columns[0]].unique())

    tg_words = set()
    for file in os.listdir(f"{data_path}textgrids"):
        tg = tgt.io.read_textgrid("../../data/textgrids/grid_011.tg")
        intervals = tg.tiers[1].intervals
        texts = [i.text.split() for i in intervals]
        words = [word for sublist in texts for word in sublist]
        tg_words.update(words)

    print(f"Number of fleurs words: {len(fleurs_words)}")  # 10825
    print(f"Number of words in textgrids: {len(tg_words)}")  # 129
    print(f"Number of words in both: {len(fleurs_words & tg_words)}")  # 69

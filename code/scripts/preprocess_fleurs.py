"""Add column names to the Fleurs dataset for kinyarwanda.
Data from: https://huggingface.co/datasets/mbazaNLP/fleurs-kinyarwanda
For a detailed column description, see the README of the dataset on huggingface.

Usage:
    python get_preprocess_fleurs.py
"""

import pandas as pd


if __name__ == "__main__":
    fleurs = ["train", "test", "dev"]
    col_names = [
        "id",
        "audio",
        "raw_orthographic_transcription",
        "orthographic_transcription",
        "phonetic_transcription",
        "n_samples",
        "gender",
    ]

    for dataset in fleurs:
        df = pd.read_csv(f"../../data/fleurs/{dataset}.tsv", sep="\t")
        df.columns = col_names
        df.to_csv(f"../../data/fleurs/{dataset}.tsv", index=False, sep="\t")

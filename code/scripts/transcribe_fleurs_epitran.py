"""Transcibe the words in the fleurs dataset using the Epitran library.
Saves the transcription in a new column and saves the word to transcription dictionary in a tsv file.

NOTE: The kinyarwanda g2p dictionary has to be copied into the epitran data directory manually (See README).

Usage:
    python transcribe_fleurs_epitran.py
"""

from typing import List, Tuple, Any

import epitran.vector
import pandas as pd
from tqdm.auto import tqdm

tqdm.pandas()


def transcribe_word(words: str) -> List[List[Any]]:
    """Transcribe a word to segments using epitran."""
    word_list = words.split()
    transcriptions = [epi.word_to_segs(x) for x in word_list]
    return transcriptions


if __name__ == "__main__":
    epi = epitran.vector.VectorsWithIPASpace("kin-Latn", ["kin-Latn"])

    fleurs = ["train", "test", "dev"]

    for dataset in fleurs:
        df = pd.read_csv(
            f"../../data/fleurs/{dataset}.tsv",
            sep="\t",
            usecols=["orthographic_transcription"],
        )
        df["epitran_transcription"] = df["orthographic_transcription"].progress_apply(
            transcribe_word
        )
        df.to_csv(f"../../data/fleurs/{dataset}.csv", index=False)

        pronunciation_dict = dict(
            zip(df["orthographic_transcription"], df["epitran_transcription"])
        )
        with open("../../data/epifleur_pronunciation_dict.tsv", "w") as f:
            for key in pronunciation_dict.keys():
                f.write("%s\t%s\n" % (key, pronunciation_dict[key]))

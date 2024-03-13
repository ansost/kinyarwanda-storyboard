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


def transcribe_word(word: str) -> List[str]:
    """Transcribe a word to segments using epitran."""
    transcriptions = epi.word_to_segs(word)
    ipa = [tuples[3] for tuples in transcriptions]
    return ipa


def clean_word(word: str) -> str:
    """Clean the word to remove punctuation."""
    cleaned_word = []
    for character in word:
        if character.isalpha():
            cleaned_word.append(character)
    word = "".join(cleaned_word)
    return word


def generate_dict_entry(orthrographic_transcription, pronunciation_dict) -> None:
    """Get the ipa representation of the transcriptions."""
    word_list = orthrographic_transcription.split()
    for word in word_list:
        word = clean_word(word)
        ipa = transcribe_word(word)
        pronunciation_dict[word] = ipa


if __name__ == "__main__":
    epi = epitran.vector.VectorsWithIPASpace("kin-Latn", ["kin-Latn"])
    fleurs = ["train", "test", "dev"]

    all_pronunciations = {}
    for dataset in fleurs:
        df = pd.read_csv(
            f"../../data/fleurs/{dataset}.tsv",
            sep="\t",
            usecols=["orthographic_transcription"],
        )
        for transcription in tqdm(df["orthographic_transcription"]):
            generate_dict_entry(transcription, all_pronunciations)

    with open("../../data/epifleur_pronunciation_dict.tsv", "w") as f:
        for key, value in all_pronunciations.items():
            if value:
                f.write("%s\t%s\n" % (key, " ".join(value)))

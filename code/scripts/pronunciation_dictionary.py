"""Transcibe the words in fleurs and the textgrids using the Epitran library.
Saves the transcription in a new column and saves the word to transcription dictionary in a tsv file.

NOTE: The kinyarwanda g2p dictionary has to be copied into the epitran data directory manually (See README).

Usage:
    python pronunciation_dictionary.py
"""

from typing import List

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
        if word in pronunciation_dict:
            continue
        word = clean_word(word)
        ipa = transcribe_word(word)
        pronunciation_dict[word] = ipa


if __name__ == "__main__":
    data_path = "../../data/"
    epi = epitran.vector.VectorsWithIPASpace("kin-Latn", ["kin-Latn"])
    fleurs = ["train", "test", "dev"]

    words = set()

    all_pronunciations = {}
    for dataset in fleurs:
        df = pd.read_csv(
            f"{data_path}fleurs/{dataset}.tsv",
            sep="\t",
            usecols=["orthographic_transcription"],
        )
        words.update(df["orthographic_transcription"].unique())

    with open(f"{data_path}tg_wordlist.txt") as f:
        wordlist = f.readlines()
    wordlist = [word.strip() for word in wordlist]

    words.update(wordlist)

    for word in tqdm(words):
        generate_dict_entry(word, all_pronunciations)

    with open("../../data/fleurtg_pronunciation_dict.tsv", "w+") as f:
        for key, value in all_pronunciations.items():
            if value and value != [""]:
                f.write("%s\t%s\n" % (key, " ".join(value)))

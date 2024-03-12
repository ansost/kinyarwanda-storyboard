"""Downloads and preprocesses the Fleurs dataset for kinyarwanda.
Creates:
    - fleurs_train/test/dev_preprocessed.tsv --> dataset with column names
    - pronunciation_dict.tsv --> dictionary of {ort. word: phon. transcription}
    - phone_set.txt --> set of all phonetic symbols in the dataset

NOTES: For a detailed column description, see the README of the dataset on huggingface.

WIP NOTES:
    - get pronunciation dictionary for words from dataset.
    - get phone set from dataset
    - is the data duplicated in the train set?

Usage:
    python get_preprocess_fleurs.py
"""

import string
from typing import Dict, List, Tuple

import pandas as pd


def clean(word: str, transcription: str, to_replace: List[str]) -> Tuple[str, str]:
    """Remove unwanted characters from strings."""
    for item in to_replace:
        word = word.replace(item, "")
        transcription = transcription.replace(item, "")
    return word, transcription


def get_entry(words: str, transcriptions: str, to_replace: List[str]) -> Dict[str, str]:
    """Produce dictionary entries from df cells.

    returns:
        entries: dictionary of {ort. word: phon. transcription}
    """
    entries = {}
    word_list = words.split()
    transcription_list = transcriptions.strip().split("|")
    assert len(word_list) == len(
        transcription_list
    ), f"Number of words and transcriptions don't match up for {words}\n{transcriptions}."

    for index, word in enumerate(word_list):
        word, transcription = clean(word, transcription_list[index], to_replace)
        entries[word] = transcription
    return entries


if __name__ == "__main__":
    fleurs = ["train", "test", "dev"]

    to_replace = ["“", "”", "¥", "¾", "8", "9", "7", "5", "2", "0"]
    for item in string.punctuation:
        to_replace.append(item)

    # Adding column names to all datasets.
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
        df.to_csv(
            f"../../data/fleurs/{dataset}_preprocessed.tsv", index=False, sep="\t"
        )
    # TODO: If data not redundant, merge is possible.

    # Get pronunciation dictionary.
    pronunciation_dict = {}

    for dataset in fleurs:
        df = pd.read_csv(
            f"../../data/fleurs/{dataset}_preprocessed.tsv",
            sep="\t",
            usecols=["orthographic_transcription", "phonetic_transcription"],
        )
        ort_transcriptions = df["orthographic_transcription"].to_list()
        phon_transcriptions = df["phonetic_transcription"].to_list()

        # TODO: parallelize?
        for i in range(0, len(df.phonetic_transcription)):
            pronunciation_dict.update(
                get_entry(ort_transcriptions[i], phon_transcriptions[i], to_replace)
            )
    with open("../../data/fleurs_pronunciation_dict.tsv", "w") as f:
        for key in pronunciation_dict.keys():
            f.write("%s\t%s\n" % (key, pronunciation_dict[key]))

    # Get phone set.
    phone_set = set()
    for transcription in pronunciation_dict.values():
        phone_set.update(transcription.split())
    with open("../../data/fleurs_phone_set.txt", "w") as f:
        for phone in phone_set:
            f.write("%s\n" % phone)

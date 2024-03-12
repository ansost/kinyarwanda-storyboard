"""Downloads and preprocesses the Fleurs dataset for kinyarwanda.
Preprocessing consists of ...

NOTES: You need to be logged in via the huggingface cli to download the dataset. For a detailed column description, see the README of the dataset on huggingface.

WIP NOTES:
    - get pronunciation dictionary for words from dataset.
    - get phone set from dataset
    - is the data duplicated in the train set?

Usage:
    python get_preprocess_fleurs.py
"""
import pandas as pd


def get_entry(words: List[str], transcripions: List[str]) -> Dict[str : List[str]]:
    """Produce dictionary entries from df cells.

    returns:
        entries: dictionary of {ort. word: phon. transcription}
    """
    entries = {}
    words = words.split()
    transcriptions = transcriptions.split("|")
    assert len(words) == len(
        transcriptions
    ), f"number of words and transcriptions don't match up for {words}\n{transcriptions}"

    for index, word in enumerate(words):
        entries["word"] = transcriptions[index]
    return entries


if __name__ == "__main__":
    fleurs = ["train", "test", "dev"]

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
        df.to_csv(f"../../data/fleurs/{dataset}_preprocessed.tsv", index=False)
    # TODO: If data not redundant, merge is possible.

    # Get pronunciation dictionary.
    cols = ["orthrographic_transcription", "phonetic_transcription"]
    pronunciation_dictionary = {}
    ort_transcriptions = df["orthographic_transcriptions"].to_list()
    phon_transcriptions = df["phonetic_transcriptions"].to_list()

    for dataset in fleurs:
        df = pd.read_csv(f"../../data/fleurs/{dataset}.tsv", sep="\t", usecols=cols)

        # TODO: parallelize?
        for i in range(0, len(df.phonetic_transcription)):
            pronunciation_dict.update(
                get_entry(ort_transcriptions(i), phonetic_transcriptions(i))
            )

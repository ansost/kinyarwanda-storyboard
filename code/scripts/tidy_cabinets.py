"""Util script to preprocess textgrid and wav data.
Removes unused files and renames the files to shorter names.
Then removes the 'sentence' tier from the soundfiles and creates a frequency list from the transcriptions.
Everything is saved in an mfa compatible format.

NOTE: Download the "KinyarwandaStoryboardRecordings2023" folder from the cloud and move the folder to "data/".
You need to unzip the folder before running the script.

Usage:
    python tidy_cabinets.py
"""

import os
from collections import Counter

import tgt
from tqdm.auto import tqdm

if __name__ == "__main__":
    in_path = "../../data/KinyarwandaStoryboardRecordings2023/"
    out_path = "../../data/mfa_data/corpus/"
    raus = [
        "Kinyarwanda_recording_22:10:23.wav",
        "Kinyarwanda_recording_22:10:23b.wav",
        "Kinyarwanda_recording_12:10:23.wav",
        "Kinyarwanda_recording_12:10:23b.wav",
        "bantuLiterature",
    ]

    # Remove the files that are not needed.
    for file in raus:
        if os.path.isdir(f"{in_path}{file}"):
            os.rmdir(f"{in_path}{file}")
        else:
            os.remove(f"{in_path}{file}")

    # Rename the files to shorter names.
    for file in tqdm(os.listdir(f"{in_path}annotatedTextGrids/")):
        name = file.split("_")
        if not file.endswith("A.TextGrid") or file.endswith("B.TextGrid"):
            os.rename(f"{out_path}{file}", f"{out_path}{name[2]}")

    # Remove 'sentence' tier from soundfiles and make wordlist.
    wordlist = []
    for file in tqdm(os.listdir(out_path)):
        tg = tgt.read_textgrid(f"{out_path}{file}")
        intervals = tg.tiers[1].intervals
        texts = [i.text.split() for i in intervals]
        words = [word for sublist in texts for word in sublist]
        wordlist.extend(words)

        tg.delete_tier("Sentences")
        tgt.write_to_file(tg, f"{out_path}{file}", format="long")

    # Create frequency dictionary from wordlist.
    frequency_dict = Counter(wordlist)
    with open("../../data/tg_word_freq.tsv", "w") as f:
        for word, freq in frequency_dict.items():
            f.write(f"{word}\t{freq}\n")

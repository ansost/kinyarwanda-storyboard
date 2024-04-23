"""Re-format textgrids after MFA.

Usage:
    python postprocessing.py
"""

import os

import tgt
from tqdm.auto import tqdm


def reorder(t: tgt.core.TextGrid, new_tiers: list[str]) -> tgt.TextGrid:
    """Reorder tiers in a textgrid.
    Returns a new textgrid with the tiers in the order "utterances", "words", "phones".
    """
    t_new = tgt.core.TextGrid()
    for tier in new_tiers:
        t_new.add_tier(t.get_tier_by_name(tier))
    return t_new


if __name__ == "__main__":
    in_path = "../../data/alignments/kinyarwanda_model/"
    files = os.listdir(in_path)
    new_tiers = ["utterances", "words", "phones"]

    for tier in tqdm(files):
        original_textgrid = tgt.io.read_textgrid(os.path.join(in_path, tier))
        tiers = original_textgrid.get_tier_names()
        t_new = reorder(original_textgrid, new_tiers)
        tgt.io.write_to_file(t_new, os.path.join(in_path, tier), format="long")

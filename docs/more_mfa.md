# Using MFA without Docker

Alternatively to the Docker image you can install MFA via **Conda**, or **source**. Instructions can be found in the [MFA docs](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html). After installing MFA, come back to the instructions below.

## Generate alignments

The sections below describe how to generate alignments (+ the necessary preprocessing) for Kinyarwanda using different methods:

1. Train a **new model for Kinyarwanda** using the Fleurs corpus.
2. Use a **pre-trained Hausa model + a Hausa dictionary** (the model does not know Kinyarwanda orthography or phonology).
3. Use a **pre-trained Hausa model** + **g2p Hausa model** to generate a pronunciation dictionary for the Kinyarwanda data.
4. **Adapt the Hausa model** to Kinyarwanda.

Sections repeat steps like downloading the pre-trained models. You can skip these steps if you have already done them in the same docker instance. **Re-starting the docker instance will remove everything you do not have on your local machine**.

If you try multiple methods, make sure to use the `--clean` flag to remove files from previous runs.

### New Kinyarwanda model

Run all scripts from within `code/scripts`. All scripts contain detailed documentation on their usage and what they do. You may need to change the paths to files and folders according to your folder structure.

**In your terminal:**

1. Copy the Kinyarwanda g2p data to your Epitran directory:

```sh
wget https://raw.githubusercontent.com/dmort27/epitran/master/epitran/data/map/kin-Latn.csv
cp kin-Latn.csv <path to your venv>/<your venv name>/lib/python3.11/site-packages/epitran/data/space
```

2. Download the Fleurs corpus from: [https://huggingface.co/datasets/mbazaNLP/fleurs-kinyarwanda](https://huggingface.co/datasets/mbazaNLP/fleurs-kinyarwanda) and put it in `data/fleurs/`.
3. Preprocess the data using `preprocess_fleurs.py`.
4. Generate a pronunciation dictionary for fleurs and the textgrids using `pronunciation_dictionary_epitran.py`.
5. Train the model: `mfa corpus fleurtg_pronunciation_dict.txt model --single_speaker --include_original_text`.
6. Align the files: `mfa align corpus fleurtg_pronunciation_dict.txt model.zip kinyarwanda_model --single_speaker --include_original_text`.

### Hausa pre-trained model with Hausa dictionary

**In your terminal:**

1. Download the hausa mfa dictionary: `mfa model download dictionary hausa_mfa`.
2. Download the hausa mfa acoustic model: `mfa model download acoustic hausa_mfa`.
3. Generate alignments using: `mfa align corpus mfa/pretrained_models/dictionary/hausa_mfa.dict mfa/pretrained_models/acoustic/hausa_mfa.zip hausa_dict --single_speaker --include_original_text`.

### Hausa pre-trained model and Hausa g2p transcribed Kinyarwanda words

**In your terminal:**

1. Download the hausa mfa dictionary: `mfa model download dictionary hausa_mfa`.
2. Train a new g2p model based on the mfa hausa pronunciation dictionary: `mfa train_g2p mfa/pretrained_models/dictionary/hausa_mfa.dict trained_g2p_hausa`.
3. Validate the textgrids to generate an oov word list: `mfa validate corpus mfa/pretrained_models/dictionary/hausa_mfa.dict`.
4. Generate pronunciations for the oov words (all tg words): `mfa g2p /mfa/corpus/oovs_found_hausa_mfa.txt trained_g2p_hausa.zip oov_pronunciations.dict`.
5. Align using the transcriptions: `mfa align corpus oov_pronunciations.dict mfa/pretrained_models/acoustic/hausa_mfa.zip hausa_g2p --single_speaker --include_original_text`.

### Adapted the Hausa model to Kinyarwanda

**In your terminal:**

1. Download the hausa mfa dictionary: `mfa model download dictionary hausa_mfa`.
2. Download the hausa mfa acoustic model: `mfa model download acoustic hausa_mfa`.
3. Adapt the Hausa model to Kinyarwanda and generate alignments: `mfa adapt corpus hausa_mfa.dict mfa/pretrained_models/acoustic/hausa_mfa.zip model --single_speaker --include_original_text`.
4. Generate alignments: `mfa align corpus/ mfa/pretrained_models/dictionary/hausa_mfa.dict mfa/pretrained_models/acoustic/model.zip hausa_adapted --single_speaker --include_original_text`.

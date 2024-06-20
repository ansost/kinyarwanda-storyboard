# Kinyarwanda ASR for storyboard recordings

The goal of work package 2-DataSet is to create a data set containing nouns and verbs of spoken Kinyarwanda that will serve as basis for our modeling and experiments.

## Pre-requisites
>
> This code is tested on Manjaro 6.5.13-7 with 16×MD Ryzen 7 7730U and 22,4 GiB RAM.
> With these specifications, all individual computations take max. 10 minutes.

This tutorial uses the Docker version of MFA. To use MFA without Docker, see the file in the docs folder: [more_mfa.md](docs/more_mfa.md).

1. Get a copy of the repository via [git](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or the [zip archive](https://github.com/ansost/kinyarwanda-storyboard/archive/refs/heads/main.zip).
2. Install [Docker](https://docs.docker.com/get-docker/)
3. Pull the forced aligner image. In you terminal: `docker pull mmcauliffe/montreal-forced-aligner:v2.2.16`.
4. Install [Python 3.11.6](https://www.python.org/downloads/release/python-3116/).
5. Make a virtual environment to install the Python requirements from the root of the repository:

    ```sh
    python -m venv <name_of_venv>
    source <name_of_venv>/bin/activate
    pip install -r requirements.txt
    ```

    If you want to specify the version of Python, you can do so with:

    ```sh
    python3.11 -m venv <name_of_venv>
    source <name_of_venv>/bin/activate
    pip install -r requirements.txt
    ```

6. Download the textgrids and wav files from the PhilCloud, place them in `data/mfa_data/corpus` and rename them using `rename.py`.

## Generate alignments

The sections below describe how to generate alignments (+ the necessary preprocessing) for Kinyarwanda using different methods:

1. Train a **new model for Kinyarwanda** using the Fleurs corpus.
2. Use a **pre-trained Hausa model + a Hausa dictionary** (the model does not know Kinyarwanda orthography or phonology).
3. Use a **pre-trained Hausa model** + **g2p Hausa model** to generate a pronunciation dictionary for the Kinyarwanda data.
4. **Adapt the Hausa model** to Kinyarwanda.

Sections repeat steps like downloading the pre-trained models. You can skip these steps if you have already done them in the same docker instance. **Re-starting the docker instance will remove everything you do not have on your local machine**.

If you try multiple methods, make sure to use the `--clean` flag to remove files from previous runs.

### New Kinyarwanda model

Run all scripts from within `code/scripts`. All scripts contain detailed documentation on their usage and what they do.

**In your terminal:**

1. Copy the Kinyarwanda g2p data to your Epitran directory:

```sh
wget https://raw.githubusercontent.com/dmort27/epitran/master/epitran/data/map/kin-Latn.csv
cp kin-Latn.csv <path to your venv>/<your venv name>/lib/python3.11/site-packages/epitran/data/space
```

2. Download the Fleurs corpus from: [https://huggingface.co/datasets/mbazaNLP/fleurs-kinyarwanda](https://huggingface.co/datasets/mbazaNLP/fleurs-kinyarwanda) and put it in `data/fleurs/`.
3. Preprocess the data using `preprocess_fleurs.py`.
4. Generate a pronunciation dictionary for fleurs and the textgrids using `pronunciation_dictionary_epitran.py`.
5. Start the mfa container and mount the data directory: `docker run -it -v <path to repo>/kinyarwanda-storyboard/data:/data mmcauliffe/montreal-forced-aligner:v2.2.16`.
6. Train the model: `mfa train data/mfa_data/corpus data/fleurtg_pronunciation_dict.txt home/mfauser/model --single_speaker --include_original_text`.
7. Align the files: `mfa align data/mfa_data/corpus/ data/fleurtg_pronunciation_dict.txt home/mfauser/model.zip home/mfauser/kinyarwanda_model --single_speaker --include_original_text`.
8. **In a new terminal:** Copy the output back to your local machine: `docker cp <container id>:/<path to data> data/` (Obtain the `docker id` by running `docker ps`).

### Hausa pre-trained model with Hausa dictionary

**In your terminal:**

1. Start the mfa container and mount the data directory: `docker run -it -v <path to repo>/kinyarwanda-storyboard/data:/data mmcauliffe/montreal-forced-aligner:v2.2.16`.
2. Download the hausa mfa dictionary: `mfa model download dictionary hausa_mfa`.
3. Download the hausa mfa acoustic model: `mfa model download acoustic hausa_mfa`.
4. Generate alignments using: `mfa align data/mfa_data/corpus/ mfa/pretrained_models/dictionary/hausa_mfa.dict mfa/pretrained_models/acoustic/hausa_mfa.zip home/mfauser/hausa_dict --single_speaker --include_original_text`.
5. **In a new terminal:** Copy the output back to your local machine: `docker cp <container id>:/<path to data> data/` (Obtain the `docker id` by running `docker ps`).

### Hausa pre-trained model and Hausa g2p transcribed Kinyarwanda words

**In your terminal:**

1. Start the mfa container and mount the data directory: `docker run -it -v <path to repo>/kinyarwanda-storyboard/data:/data mmcauliffe/montreal-forced-aligner:v2.2.16`.
2. Download the hausa mfa dictionary: `mfa model download dictionary hausa_mfa`.
3. Train a new g2p model based on the mfa hausa pronunciation dictionary: `mfa train_g2p mfa/pretrained_models/dictionary/hausa_mfa.dict home/mfauser/trained_g2p_hausa`.
4. Validate the textgrids to generate an oov word list: `mfa validate data/mfa_data/corpus mfa/pretrained_models/dictionary/hausa_mfa.dict`.
5. Generate pronunciations for the oov words (all tg words): `mfa g2p /mfa/corpus/oovs_found_hausa_mfa.txt home/mfauser/trained_g2p_hausa.zip home/mfauser/oov_pronunciations.dict`.
6. Align using the transcriptions: `mfa align data/mfa_data/corpus/ data/oov_pronunciations.dict mfa/pretrained_models/acoustic/hausa_mfa.zip home/mfauser/hausa_g2p --single_speaker --include_original_text`.
7. **In a new terminal:** Copy the output to you local machine: `docker cp <container id>:/<path to data> data/` (Obtain the `docker id` by running `docker ps`).
8. Copy the oov word transcriptions to your local machine: `docker cp <container id>:/home/mfauser/oov_pronunciations.dict data/` (Obtain the `docker id` by running `docker ps`).

### Adapted the Hausa model to Kinyarwanda

**In your terminal:**

1. Start the mfa container and mount the data directory: `docker run -it -v <path to repo>/kinyarwanda-storyboard/data:/data mmcauliffe/montreal-forced-aligner:v2.2.16`.
2. Download the hausa mfa dictionary: `mfa model download dictionary hausa_mfa`.
3. Download the hausa mfa acoustic model: `mfa model download acoustic hausa_mfa`.
4. Adapt the Hausa model to Kinyarwanda and generate alignments: `mfa adapt data/mfa_data/corpus mfa/pretrained_models/dictionary/hausa_mfa.dict mfa/pretrained_models/acoustic/hausa_mfa.zip home/mfauser/model --single_speaker --include_original_text`.
5. Generate alignments: `mfa align data/mfa_data/corpus/ mfa/pretrained_models/dictionary/hausa_mfa.dict mfa/pretrained_models/acoustic/model.zip home/mfauser/hausa_adapted --single_speaker --include_original_text`.
6. **In a new terminal:** Copy the output to you local machine: `docker cp <container id>:/<path to data> data/` (Obtain the `docker id` by running `docker ps`).

## Postprocessing

After aligning with MFA the textgrid tiers can be re-ordered using the script `postprocessing.py`.

### License

???

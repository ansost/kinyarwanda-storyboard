# Kinyarwanda ASR for storyboard recordings

The goal of work package 2-DataSet is to create a data set containing nouns and verbs of spoken Kinyarwanda that will serve as basis for our modeling and experiments.

# Pre-requisites
1. Get a copy of the repository via [git](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or the [zip archive](https://github.com/ansost/kinyarwanda-storyboard/archive/refs/heads/main.zip).
2. Install [Docker](https://docs.docker.com/get-docker/) and pull the forced aligner image [Montreal-Forced-Aligner v3.0.0a](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html#docker-installation).
3. Install [Python 3.11.6](https://www.python.org/downloads/release/python-3116/) (or make a [virtual environment](https://docs.python.org/3/tutorial/venv.html) with the same version).
4. Make a virtual environment to install the Python requirements. the requirements file is in the root of the repository.
    ```sh
    python3 -m venv <name_of_venv>
    source <name_of_venv>/bin/activate
    pip install -r requirements.txt
    ```
    If you want to specifcy the version of Python, you can do so with:
    ```sh
    python3.11 -m venv <name_of_venv>
    source <name_of_venv>/bin/activate
    pip install -r requirements.txt
    ```
5. Download the folder `KinyarwandaStoryboardRecordings2023` from OwnCloud and place it in the `data/` directory of the repository.
6. Copy the Kinyarwanda g2p data to your Epitran directory:
```sh
cp kin-Latn.csv <path to your venv>/<your venv name>/lib/python3.11/site-packages/epitran/data/space
```

## Generate alignments
Run all scripts from within `code/scripts` in the commandline. All scripts contain detailed documentation on their usage and what they do.

1. Prepare the Text grids and delete unnecessary data using `tidy_cabinets.py`.
2. Generate a pronunciation dictionary using `pronunciation_dictionary.py`.
3. Start the mfa container:
```sh
docker run -it mmcauliffe/montreal-forced-aligner
```
4. In your shell (not the container shell), obtain the containr ID by running `docker ps` and then selecting it in the first column of the output. Then copy your data over with:
```sh
docker cp <path to data> <container id>:/<path to data>
```
5. In the container shell, train the and generate alignments in the container using. Do not change the output directory.
```sh
mfa train [OPTIONS] CORPUS_DIRECTORY DICTIONARY_PATH /home/mfauser/output/
```
6. In your shell, copy the output back to your local machine:
```sh
docker cp <container id>:/<path to data> <path to data>
```

### License

???

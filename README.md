# Kinyarwanda ASR for storyboard recordings

**Project description:**

The goal of work package 2-DataSet is to create a data set containing nouns and verbs of spoken Kinyarwanda that will serve as basis for our modeling and experiments.

## Getting the code

Either clone the [git](https://git-scm.com/) repository:

```sh
git clone git@github.com:ansost/NoClu.git
```

Or [download a zip archive](https://github.com/ansost/kinyarwanda-storyboard/archive/refs/heads/main.zip).

### Requirements

See `requirements.txt` for a full list of requirements.
The fastest way to install the requirements is using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing) and a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (like [venv](https://docs.python.org/3/library/venv.html)).
> Make sure to substitute <name_of_vev> with an actual name for your environment.
> Choose `kinV` as a name for the environment to be ignore automatically by the .gitignore.

```sh
python3 -m venv <name_of_venv>
source <name_of_venv>/bin/activate
pip install -r requirements.txt
```

## Software implementation

All source code used to generate the results and figures in this paper are in `code/scripts/`.
The calculations and figure generation are run in [Python](https://www.python.org/) scripts with [Python 3.11.6](https://www.python.org/downloads/release/python-3116/).

This repository uses pre-commit hooks. Learn more about them and how to install/use them here: [https://pre-commit.com/](https://pre-commit.com/).

NOTE: The kinyarwanda g2p data has to be copied manually using
```sh
 cp kin-Latn.csv <path to your venv>/<your venv name>/lib/python3.11/site-packages/epitran/data/space
```

### Data

text

#### Preprocessing

description

```sh
python3 scriptname.py
```

### License

text

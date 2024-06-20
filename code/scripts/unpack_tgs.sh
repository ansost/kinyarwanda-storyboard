#!/bin/bash
# This script is meant to be run from code/scripts. 

unzip -d ../../data/mfa_data/corpus/ ../../data/mfa_data/corpus/annotatedTextGrids.zip
rm -r ../../data/mfa_data/corpus/annotatedTextGrids.zip
mv ../../data/mfa_data/corpus/annotatedTextGrids/* ../../data/mfa_data/corpus/
rm -r ../../data/mfa_data/corpus/annotatedTextGrids
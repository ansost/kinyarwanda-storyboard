#!/bin/bash
sudo systemctl start docker
docker run -it mmcauliffe/montreal-forced-aligner:latest
docker cp ../data/fleurtg_pronunciation_dict.tsv mmcauliffe/montreal-forced-aligner:latest:/

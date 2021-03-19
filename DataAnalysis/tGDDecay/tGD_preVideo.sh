#!/bin/bash

# argv1: User
# argv2: AOI
# argv3: Experiment

# ./STP_preVideo.sh dsk3 HLT E_01_100_01
python tGD_preVideo.py $1 $2 $3
python tGD_ffmpeg.py $1 $2 $3

#!/bin/bash

# argv1: User
# argv2: Drive

python tGD_pstHeatmap.py $1 $2 HLT
python tGD_pstHeatmap.py $1 $2 WLD
python tGD_pstHeatmap.py $1 $2 TRS
# python tGD_pstHeatmap.py $1 $2 CST


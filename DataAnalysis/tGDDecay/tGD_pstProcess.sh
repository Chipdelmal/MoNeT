#!/bin/bash

# argv1: User
# argv2: Drive

python tGD_pstFraction.py $1 $2 ECO
python tGD_pstFraction.py $1 $2 HLT
python tGD_pstFraction.py $1 $2 TRS
python tGD_pstFraction.py $1 $2 WLD

python tGD_pstProcess.py $1 $2 ECO
python tGD_pstProcess.py $1 $2 HLT
python tGD_pstProcess.py $1 $2 TRS
python tGD_pstProcess.py $1 $2 WLD

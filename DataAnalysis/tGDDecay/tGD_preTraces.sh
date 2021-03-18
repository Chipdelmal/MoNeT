#!/bin/bash

python tGD_preTraces.py $1 $2 HLT
python tGD_preTraces.py $1 $2 TRS
python tGD_preTraces.py $1 $2 WLD
python tGD_preTraces.py $1 $2 ECO
python tGD_preTraces.py $1 $2 CST

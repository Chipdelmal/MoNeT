#!/bin/bash

# scp -r lab:/RAID5/marshallShare/tGD/video/tGD/000/PREPROCESS/ '/home/chipdelmal/Documents/WorkSims/tGD/video/tGD'

bash ./tGD_preVideo.sh dsk3 $1 E_01_100_01
bash ./tGD_preVideo.sh dsk3 $1 E_01_100_02
bash ./tGD_preVideo.sh dsk3 $1 E_01_200_01
bash ./tGD_preVideo.sh dsk3 $1 E_01_200_02
bash ./tGD_preVideo.sh dsk3 $1 E_04_100_01
bash ./tGD_preVideo.sh dsk3 $1 E_04_100_02
bash ./tGD_preVideo.sh dsk3 $1 E_04_200_01
bash ./tGD_preVideo.sh dsk3 $1 E_04_200_02
bash ./tGD_preVideo.sh dsk3 $1 E_08_100_01
bash ./tGD_preVideo.sh dsk3 $1 E_08_100_02
bash ./tGD_preVideo.sh dsk3 $1 E_08_200_01
bash ./tGD_preVideo.sh dsk3 $1 E_08_200_02
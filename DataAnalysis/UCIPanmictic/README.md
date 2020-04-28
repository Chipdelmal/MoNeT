# UCI Panmictic Population Paper

* [uciPan_aux.py](./uciPan_aux.py): Colors and constants for scripts.
* [uciPan_drive.py](./uciPan_drive.py): Drive parameters for the experiments.
* [uciPan_fun.py](./uciPan_fun.py): Auxiliary functions for the scripts.
* [uciPan_plot.py](./uciPan_plot.py): Plot-related auxiliary functions for scripts.
* [uciPan_main.py](./uciPan_main.py): Script to export the summary CSV for the mean-response analyses.
* [uciPan_reps.py](./uciPan_reps.py): Script to export the summaries CSVs for the traces-responses analyses.
* [uciPan_rsCrv.py](./uciPan_rsCrv.py): Response time-series (constant release number, variable ratio).
* [uciPan_rtCrv.py](./uciPan_rtCrv.py): Response time-series (constant ratio, variable release number).
* [uciPan_paper.nb](./uciPan_paper.nb): Response surfaces plots for the paper.


## Running scripts

### Exporting plots and factorial summaries (needs nano toggle)

```bash
python uciPan_main.py RAID5 tParams island
python uciPan_main.py RAID5 tParams islandMixed
python uciPan_main.py RAID5 tParams islandGravidFemales
```
### Images from PDF to PNG

```bash
mogrify -verbose -density 250 -resize 600 -background white -alpha remove -alpha off -format png ./*.pdf
```

## Copy Files from server

### Copy images

```bash
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/islandGravidFemales/img/ /home/chipdelmal/Desktop/Panmictic/tParams/islandGravidFemales/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/islandMixed/img/ /home/chipdelmal/Desktop/Panmictic/tParams/islandMixed/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/island/img/ /home/chipdelmal/Desktop/Panmictic/tParams/island/;

scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/yParams/islandGravidFemales/img/ /home/chipdelmal/Desktop/Panmictic/yParams/islandGravidFemales/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/yParams/islandMixed/img/ /home/chipdelmal/Desktop/Panmictic/yParams/islandMixed/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/yParams/island/img/ /home/chipdelmal/Desktop/Panmictic/yParams/island/;
```

### Copy summaries

```bash
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/islandGravidFemales/thresholdCrosses.csv /home/chipdelmal/Desktop/Panmictic/tParams/islandGravidFemales/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/islandMixed/thresholdCrosses.csv /home/chipdelmal/Desktop/Panmictic/tParams/islandMixed/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/island/thresholdCrosses.csv /home/chipdelmal/Desktop/Panmictic/tParams/island/

scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/yParams/islandGravidFemales/thresholdCrosses.csv /home/chipdelmal/Desktop/Panmictic/yParams/islandGravidFemales/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/yParams/islandMixed/thresholdCrosses.csv /home/chipdelmal/Desktop/Panmictic/yParams/islandMixed/;\
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/yParams/island/thresholdCrosses.csv /home/chipdelmal/Desktop/Panmictic/yParams/island/
```

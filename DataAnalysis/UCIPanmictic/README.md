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

Convert all

```bash
mogrify -verbose -density 300 -resize 1000 -background white -alpha remove -alpha off -format png ./*.pdf
```

```bash
rm *-OVR.pdf;
mogrify -verbose -density 1000 -resize 5000 -background white -alpha remove -alpha off -format png ./*.pdf;
rm *.pdf;
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

Copy all dynamics plots:

```bash
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/img/ /media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/
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

### Copy Experiments

#### Analyzed data

```bash
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/island/out/LDR/ANALYZED/ /home/chipdelmal/Desktop/Panmictic/tParams/island/out/LDR/ANALYZED/
```

#### Preprocessed data

```bash
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/island/out/LDR/PREPROCESS/*.lzma /media/chipdelmal/cache/Sims/Panmictic/tParams/island/out/LDR/PREPROCESS

scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/islandMixed/out/LDR/PREPROCESS/*.lzma /media/chipdelmal/cache/Sims/Panmictic/tParams/islandMixed/out/LDR/PREPROCESS

scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/islandGravidFemales/out/LDR/PREPROCESS/*.lzma /media/chipdelmal/cache/Sims/Panmictic/tParams/islandGravidFemales/out/LDR/PREPROCESS
```

#### Postprocessed data

```bash
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/tParams/island/out/LDR/POSTPROCESS/ /media/chipdelmal/cache/Sims/Panmictic/tParams/island/out/LDR/
```

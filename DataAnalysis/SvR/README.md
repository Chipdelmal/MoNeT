#   Suppression Versus Replacement

Scripts to run the analyses for the BioEssay paper comparing population suppression and replacement.


## Workflow

```bash
python svr_preProcess.py USR AOI
python svr_preTraces.py USR AOI
python svr_pstProcess.py USR HLT
python svr_pstTraces.py USR AOI
python svr_pstHeatmap.py USR AOI
```

## Copy Experiments Results

Whole set:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/ /media/chipdelmal/cache/Sims/SvR/
```

Preprocessed Data:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/replacement/out/LDR/PREPROCESS/ /media/chipdelmal/cache/Sims/SvR/sim/replacement/out/LDR/
```

Postprocessed Data:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/HX/POSTPROCESS/ /media/chipdelmal/cache/Sims/SvR/sim/HX/
```

Heatmaps:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/HX/img/H* /media/chipdelmal/cache/Sims/SvR/sim/HX/

scp -rp  lab:/RAID5/marshallShare/SvR/sim/HY/img/H* /media/chipdelmal/cache/Sims/SvR/sim/HY/
```

Traces:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/HX/img/E* /media/chipdelmal/cache/Sims/SvR/sim/HX/img/

scp -rp  lab:/RAID5/marshallShare/SvR/sim/HY/img/E* /media/chipdelmal/cache/Sims/SvR/sim/HY/img/
```

Traces Full:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/HX/img/Full/E* /media/chipdelmal/cache/Sims/SvR/sim/HX/imgFull/

scp -rp  lab:/RAID5/marshallShare/SvR/sim/HY/img/Full/E* /media/chipdelmal/cache/Sims/SvR/sim/HY/imgFull/
```


Compress data:

```bash
tar c ./ANALYZED | lbzip2 -n 16 > ANALYZED.tar.bz2
tar c ./GARBAGE | lbzip2 -n 16 > GARBAGE.tar.bz2
tar c ./RAW | lbzip2 -n 16 > RAW.tar.bz2
```

#   Suppression Versus Replacement

Scripts to run the analyses for the BioEssay paper comparing population suppression and replacement.


## Workflow

```bash
python svr_preProcess.py
python svr_preTraces.py
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

Traces Plots:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/replacement/out/LDR/img/ /media/chipdelmal/cache/Sims/SvR/sim/replacement/out/LDR/
```

Heatmaps:

```bash
scp -rp  lab:/RAID5/marshallShare/SvR/sim/replacement/out/LDR/img/htm/ /media/chipdelmal/cache/Sims/SvR/sim/replacement/out/LDR/img
```

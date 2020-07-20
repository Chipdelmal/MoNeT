# UCI São Tomé and Príncipe

This is an extension of the [UCIPanmictic](https://github.com/Chipdelmal/MoNeT/tree/master/DataAnalysis/UCIPanmictic) workflow, as it covers both one/multi node analyses.

## Running scripts

### Exporting plots and factorial summaries (needs nano srv toggle)

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
```

### Copy summaries

```bash
```

### Copy Experiments

#### Analyzed data

```bash
```

#### Preprocessed data

```bash
```

#### Postprocessed data

```bash
scp -rp  lab:/RAID5/marshallShare/UCI/Yoosook/gravidReleases/islandnonGravid/out/LDR/POSTPROCESS/ /media/chipdelmal/cache/Sims/Panmictic/gravidDev/islandnonGravid/out/LDR/
```

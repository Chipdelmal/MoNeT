# tGD Drive-out

Scripts for the new idea for tGD

```bash
scp -rp lab:/RAID5/marshallShare/tGD/images/ '~/Desktop/tGD/images/'
```

## DOWNLOAD

Download PREPROCESS folders:

```bash
python tGD_dwdDta.py linkedDrive PREPROCESS *HLT*_rep.bz
python tGD_dwdDta.py splitDrive PREPROCESS *HLT*_rep.bz
python tGD_dwdDta.py tGD PREPROCESS *HLT*_rep.bz
```

Download POSTPROCESS folders:

```bash
python tGD_dwdDta.py linkedDrive POSTPROCESS *.csv
python tGD_dwdDta.py splitDrive POSTPROCESS *csv
python tGD_dwdDta.py tGD POSTPROCESS *.csv
```

Download IMAGES folders:

```bash
python tGD_dwdDta.py linkedDrive imgPst *Q90.png
python tGD_dwdDta.py splitDrive imgPst *Q90.png
python tGD_dwdDta.py tGD imgPst *Q90.png
```

Download HEATMAPS:

```bash
python tGD_dwdDta.py linkedDrive imgPst/ren_hnf None
python tGD_dwdDta.py splitDrive imgPst/ren_hnf None
python tGD_dwdDta.py tGD imgPst/ren_hnf None
```


## WIPE

Wipe PREPROCESS folders:

```bash
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/000/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/001/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/005/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/010/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/100/PREPROCESS;

rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/000/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/001/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/005/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/010/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/100/PREPROCESS;

rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/000/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/001/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/005/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/010/PREPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/100/PREPROCESS;
```

Wipe img folders:

```bash
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/000/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/001/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/005/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/010/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/100/img;

rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/000/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/001/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/005/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/010/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/100/img;

rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/000/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/001/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/005/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/010/img;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/100/img;
```

Wipe PostProcess folders:

```bash
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/000/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/001/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/005/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/010/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/linkedDrive/100/POSTPROCESS;

rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/000/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/001/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/005/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/010/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/splitDrive/100/POSTPROCESS;

rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/000/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/001/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/005/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/010/POSTPROCESS;
rm -R /RAID5/marshallShare/tGD/fullSweep/tGD/100/POSTPROCESS;
```

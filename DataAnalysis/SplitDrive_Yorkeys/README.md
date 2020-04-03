# Split Drive: _Yorkeys Knob_

These routines are created for the experiments in the future paper to test the _split drive_ performance in comparison to other drives.

##  Files

* [SDY_clstSort.nb](./SDY_clstSort.nb): Clusters the nodes into two groups so that we can separate _Yorkeys Knob_ from _Trinity Park_ and process them easily in the following routines.
* [SDY_selAgg.py](./SDY_selAgg.py): Performs the "different resolution" aggregation of the landscape (agglomerates all _Trinity Park_ into one node, leaving _Yorkeys Knob_ untouched).
* [SDY_clstAux.py](./SDY_clstAux.py):
* [SDY_selAgg.py](./SDY_selAgg.py):
* [SDY_select.py](./SDY_select.py):
* [SDY_validation.py](./SDY_validation):

## Paths

### Validation

* `/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated`
* `/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/unAggregated`


## Bash


```bash
scp -rp\
  hector@marshall-lab-cal.berkeley.edu:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/img/*.pdf\
  /home/chipdelmal/shared/SDY/img/;
scp -rp\
    hector@marshall-lab-cal.berkeley.edu:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/err/*.csv\
    /home/chipdelmal/shared/SDY/err/;
scp -rp\
    hector@marshall-lab-cal.berkeley.edu:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/err/img/*\
    /home/chipdelmal/shared/SDY/err/img/;
```


```bash
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated/ANALYZED/E_15_20_050/ '~/Desktop/SplitDrive_Yorkeys/geoProof/Aggregated/ANALYZED'

scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated/GARBAGE/E_15_20_050/ '~/Desktop/SplitDrive_Yorkeys/geoProof/Aggregated/GARBAGE'
```

```bash
scp -rp lab:'/RAID5/marshallShare/SplitDrive_Yorkeys/video/' '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/'
```

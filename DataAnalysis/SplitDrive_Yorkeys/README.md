# Split Drive: _Yorkeys Knob_

These routines are created for the experiments in the future paper to test the _split drive_ performance in comparison to other drives.

##  Files

* [SDY_clstSort.nb](./SDY_clstSort.nb): Clusters the nodes into two groups so that we can separate _Yorkeys Knob_ from _Trinity Park_ and process them easily in the following routines.
* [SDY_selAgg.py](./SDY_selAgg.py): Performs the "different resolution" aggregation of the landscape (agglomerates all _Trinity Park_ into one node, leaving _Yorkeys Knob_ untouched).
* [SDY_clstAux.py](./SDY_clstAux.py): Clustering auxiliary functions.
* [SDY_selAgg.py](./SDY_selAgg.py): Selective aggregation routine for one-node Trinity.
* [SDY_select.py](./SDY_select.py): Genotypes selectors for dictionaries.
* [SDY_validation.py](./SDY_validation.py): Export the validation plots
* [SDY_video.py](./SDY_video.py): Exports frames and compiles video for SDY validation.
* [SDY_looper.py](./SDY_looper.py): Batch-exports videos in parallel for the aggregation validation.

## Paths

### Validation

* `/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated`
* `/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/unAggregated`


## Bash

Copy analyses plots to desktop:

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
Copy an experiment to desktop for debugging:

```bash
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated/ANALYZED/E_15_20_050/ '~/Desktop/SplitDrive_Yorkeys/geoProof/Aggregated/ANALYZED'

scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated/GARBAGE/E_15_20_050/ '~/Desktop/SplitDrive_Yorkeys/geoProof/Aggregated/GARBAGE'
```

Copy videos from server to desktop:

```bash
scp -rp lab:'/RAID5/marshallShare/SplitDrive_Yorkeys/video/Aggregated/*.mp4' '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/video/Aggregated/'

scp -rp lab:'/RAID5/marshallShare/SplitDrive_Yorkeys/video/unAggregated/*.mp4' '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/video/unAggregated/'
```

## Videos Checklist

All the experiments names:

```python
[
    ['E_05_10_025', 'E_05_20_025', 'E_05_30_025', 'E_15_10_025'],
    ['E_15_20_025', 'E_15_30_025', 'E_30_10_025', 'E_30_20_025'],
    ['E_30_30_025', 'E_05_10_050', 'E_05_20_050', 'E_05_30_050'],
    ['E_15_10_050', 'E_15_20_050', 'E_15_30_050', 'E_30_10_050'],
    ['E_30_20_050', 'E_30_30_050', 'E_05_10_075', 'E_05_20_075'],
    ['E_05_30_075', 'E_15_10_075', 'E_15_20_075', 'E_15_30_075'],
    ['E_30_10_075', 'E_30_20_075', 'E_30_30_075', 'E_05_10_100'],
    ['E_05_20_100', 'E_05_30_100', 'E_15_10_100', 'E_15_20_100'],
    ['E_30_30_100', 'E_15_30_100', 'E_30_10_100', 'E_30_20_100']
]
```
Run a single video experiment:

```bash
python SDY_video.py 'srv' 'agg' 'hlt' 'E_05_10_025'
python SDY_video.py 'dsk' 'nag' 'eco' 'E_30_20_075'
```

Run the experiment in batch:

```bash
python SDY_looper.py
```

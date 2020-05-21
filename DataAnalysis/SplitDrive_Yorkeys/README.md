# Split Drive: _Yorkeys Knob_

These routines are created for the experiments in the future paper to test the _split drive_ performance in comparison to other drives.

##  Files

* [SDY_clstSort.nb](./SDY_clstSort.nb): Clusters the nodes into two groups so that we can separate _Yorkeys Knob_ from _Trinity Park_ and process them easily in the following routines.
* [SDY_selAgg.py](./SDY_selAgg.py): Performs the "different resolution" aggregation of the landscape (agglomerates all _Trinity Park_ into one node, leaving _Yorkeys Knob_ untouched).
* [SDY_clstAux.py](./SDY_clstAux.py): Clustering auxiliary functions.
* [SDY_selAgg.py](./SDY_selAgg.py): Selective aggregation routine for one-node Trinity.
* [SDY_select.py](./SDY_select.py): Genotypes selectors for dictionaries.
* [SDY_validation.py](./SDY_validation.py): Generate the validation CSV files and traces plots.
* [SDY_video.py](./SDY_video.py): Exports frames and compiles video for SDY validation.
* [SDY_looper.py](./SDY_looper.py): Batch-exports videos in parallel for the aggregation validation.
* [SDY_ix.py](./SDY_ix.py): Indices for the TP and YK sections of the landscapes for validation.


## Scripts Order

### Errors:

```bash
python SDY_validation.py
python SDY_error.py
python SDY_errorPlot.py
```

### Videos

```bash
python
```

## Paths

### Validation

* `/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated`
* `/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/unAggregated`
* `/RAID5/marshallShare/SplitDrive_Yorkeys/idCheck/`


## Bash

Copy analyses plots to desktop:

```bash
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/img/*.pdf /home/chipdelmal/Desktop/SplitDrive_Yorkeys/img/;
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/err/*.csv /media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/err/;
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/err/img/* /media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/err/img;
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/Landscapes/LandSorted/* /media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/LandSorted/;

```

Copy landscapes to server:

```bash
scp -rp /media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/Landscapes/LandAggregated/Filtered/* lab:/RAID5/marshallShare/SplitDrive_Yorkeys/Landscapes/LandAggregated/Filtered/

```

```bash
mogrify -verbose -density 1000 -resize 2000 -background white -alpha remove -alpha off -format png ./*.pdf
```

Copy an experiment to desktop for debugging:

```bash
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated/ANALYZED/E_15_20_050/ '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/geoProof/Aggregated/ANALYZED'
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/Aggregated/GARBAGE/E_15_20_050/ '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/geoProof/Aggregated/GARBAGE'

scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/unAggregated/ANALYZED/E_30_30_100_c1/ '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/geoProof/unAggregated/ANALYZED'
scp -rp lab:/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/unAggregated/GARBAGE/E_30_30_100_c1/ '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/geoProof/unAggregated/GARBAGE'
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

Run the experiment in batch. Change the parameters with *nano* and then run:

```bash
python SDY_looper.py
```

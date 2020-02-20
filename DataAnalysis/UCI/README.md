# UCI Scripts (Winter 2020)

##  Main Scripts

* [mainYoosook](./mainYoosook.py): Contains the routine for the short paper in fixation speeds for _Saõ Tomé & Principe_ sims.
* [mainPanmictic](./mainPanmictic): Creates the traces plots for the STP analyses as a panmictic population.
* [mainSTP](./mainSTP.py): Is a heavily modified script to generate the plots needed for the annual meeting.
* [clusterAndAggregate](./clusterAndAggregate.py): Variation of Gillian's original code used for video-clustering.
* [mapClusters](./mapClusters.py): Generates the background layer for the videos.


##  Auxiliaries

* [fun](./fun.py): Functions definitions for analyses.
* [aux](./aux.py): Definitions for auxiliary code on plotting and analyzing routines.
* [plot](./plot.py): Auxiliary code for the labels and lines on the timings.
* [drive](./drive.py): Drive selection routines.
* [auxVideo](./auxVideo.py): Video-related code.
* [auxCluster](./auxCluster.py): Cluster-related code.
* [checkArrays](./checkArrays.py): Unknown
* [normalizeKernel](./normalizeKernel.py): Auxiliary script to make sure the kernel runs from 0 to 1.

```
ffmpeg -r 30 -f image2 -s 4096x2160 -i c_%06d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p video.mp4
```

import glob
import MoNeT_MGDrivE as monet
import subprocess

#######
# STATIC GLOBALS
####### 3rd , "#6898ff"
colors = ["#090446", "#f20060", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ["W", "H", "R", "B"]

folder = '/Volumes/marshallShare/Riverside_Alt_Kernels/output/Fine2/'
coordFileLocation = '/Volumes/marshallShare/Riverside_Alt_Kernels/'
coordFileName = coordFileLocation+'barkersfiel3_LatLongs_clustered.csv'
clusterFileName = coordFileLocation+'clusteringResult.csv'
patchFilePattern = {'males':'/M_*', 'females':'/F_*'}
subfolder = folder+'/images/clustercharts2/'
vlocation = folder+'videos/'
imagePattern = '/c_%06d.png'

coordinates = monet.getClusters(clusterFileName)

for expPath in sorted(glob.glob(folder+'ANALYZED/E_05*')):
    experiment = expPath.split("/")[-1]
    vname = vlocation+experiment+'_cdots.mp4'
    background = coordFileName.replace('.csv','.png')
    imageLocation = subfolder+experiment

    print(experiment)

    subprocess.Popen(['mkdir', subfolder+experiment])

    clusters = monet.populateClusters(
                        len(coordinates[0]),
                        coordFileName, expPath,
                        patchFilePattern)

    genotypes = monet.getGenotypes(clusters[0]['male'][0])
    aggDict = monet.autoGenerateGenotypesDictionary(groups, genotypes)
    aggList = monet.aggregateClusters(clusters, aggDict)
    monet.generateClusterGraphs(aggList, [coordinates[1],coordinates[0]], imageLocation, colors)
    video = monet.generateVideo(vname,background, imageLocation, imagePattern)

wait(video)

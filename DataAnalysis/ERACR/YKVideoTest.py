import glob
import MoNeT_MGDrivE as monet
import subprocess

#######
# STATIC GLOBALS
####### 3rd , "#6898ff"
colors = ["#090446", "#f20060", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ["W", "H", "R", "B", "E"]

folder = '/Volumes/marshallShare/ERACR/Yorkeys4/Experiment4/'
extras = '/Volumes/marshallShare/ERACR/Yorkeys4/Clustered/'
patchFilePattern = {'males':'/M_*', 'females':'/F_*'}
imagePattern = '/c_%06d.png'

def get_corners(fileName):
    lats = []
    longs = []
    clusterData = open(fileName,'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        lat = float(tokens[1])
        long = float(tokens[0])
        lats.append(lat)
        longs.append(long)

    minLat = min(lats)
    minLong  = min(longs)
    maxLat = max(lats)
    maxLong = max(longs)
    return [[minLong,maxLong],[minLat,maxLat]]


expFolder = '/Volumes/marshallShare/ERACR/Yorkeys4/Experiment4/Yorkeys_AGG_1_00001'
expBaseName = expFolder.split('/')[-1]
clusteringNum = int(expBaseName.split('_')[-1])
bgName  = expBaseName.replace('_AGG_','_VBG_')
clusterName = bgName.replace('VBG_','AGCV_')
background = extras+bgName+'.png'
background
originalCoordFile = extras+expBaseName.replace('_AGG_','_CLS_')+'.csv'
original_corners = get_corners(originalCoordFile)
expPath = sorted(glob.glob(expFolder+'/ANALYZED/E_*'))[0]
vname = expPath.replace('ANALYZED','videos')+'_cdots.mp4'
coordinates = monet.getClusters(extras+clusterName+'.csv')
imageLocation = expPath.replace('ANALYZED','images/clustercharts')
subprocess.Popen(['mkdir', imageLocation])
clusters = monet.populateClusters(
                        len(coordinates[0]),
                        '', expPath,
                        patchFilePattern)
genotypes = monet.getGenotypes(clusters[0]['male'][0])
aggDict = monet.autoGenerateGenotypesDictionary(groups, genotypes)
aggList = monet.aggregateClusters(clusters, aggDict)
monet.generateClusterGraphs(aggList, coordinates, imageLocation, colors, original_corners, 0.002, 512, skip=True)
video = monet.generateVideo(vname,background, imageLocation, imagePattern)

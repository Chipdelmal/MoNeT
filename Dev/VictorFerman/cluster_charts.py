import glob
import math
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import subprocess

def getClusters(fileLocation):
    coordinates = [[],[]]
    clusterFile = open(fileLocation,'r')

    for line in clusterFile:
        tokens = line.split(',')
        coordinates[0].append(float(tokens[1]))
        coordinates[1].append(float(tokens[0]))

    return coordinates

def populateClusters(clusterNum, cFileName, pFileLocation, pFilePattern={}):

    clusters = []
    for i in range(clusterNum):
        clusters.append({'male':[],'female':[]})
    patchCluster =[]
    coordFile = open(cFileName,'r')

    for line in coordFile:
        patchCluster.append(int(line.split(',')[2].strip()))

    if 'male' in pFilePattern:
        patchFileList = sorted(glob.glob(pFileLocation+pFilePattern['male']))
    else:
        patchFileList = sorted(glob.glob(pFileLocation+'/ADM_*'))
        if not patchFileList:
            patchFileList = sorted(glob.glob(pFileLocation+'/M_*'))

    for index,patchFileN in enumerate(patchFileList):
        clusters[patchCluster[index]]['male'].append(patchFileN)

    if 'female' in pFilePattern:
        patchFileList = sorted(glob.glob(pFileLocation+pFilePattern['female']))
    else:
        patchFileList = sorted(glob.glob(pFileLocation+'/AF1_*'))
        if not patchFileList:
            patchFileList = sorted(glob.glob(pFileLocation+'/F_*'))

    for index,patchFileN in enumerate(patchFileList):
        clusters[patchCluster[index]]['female'].append(patchFileN)

    return clusters


def aggregateClusters(clusters,aggDict):
    aggList = []
    for fileList in clusters:
        aggPatches = monet.loadAndAggregateLandscapeData(
            {'male':fileList['male'], 'female':fileList['female']},aggDict, male=True, female=True
        )["landscape"]
        res = np.zeros_like(aggPatches[0])
        for patch in aggPatches:
            res += patch
        aggList.append(res)
    return aggList


def getGenotypes(fileName):
    f = open(fileName, 'r')
    header = next(f).split(',')[1:]
    f.close()
    return header


def createFig(coordinates):
    fig=None
    ax=None
    m = None
    minLat = min(coordinates[1])
    maxLat = max(coordinates[1])
    minLong = min(coordinates[0])
    maxLong = max(coordinates[0])
    fig,ax = plt.subplots(figsize=(5, 5))
    ax.tick_params(
    axis='both',          # changes apply to the both
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    right=False,
    labelbottom=False, # labels along the bottom edge are off
    labelleft=False)
    m = Basemap(projection='merc',llcrnrlat=minLat-0.001,urcrnrlat=maxLat+0.001,llcrnrlon=minLong-0.001,urcrnrlon=maxLong+0.001,lat_ts=20,resolution='i', ax=ax)
    m.drawcounties(linewidth=0.3)
    return (fig,ax,m)

def getAlphas(popList):
    total = np.sum(popList)
    return ([float(x)/total for x in popList],total)


def draw_dots(m, alphas, colorList, long=0, lat=0, size=60):
    start = 0.0
    for idx,value in ennumerate(alphas):
        m.scatter([long],[lat], latlon=True, marker=(6,0), s=max(9, 0.15*size), facecolor=colorsList[idx], alpha= value)

def generateClusterGraphs(aggList, coordinates, destination, colorList):
    time = len(aggList[0])
    fig,ax,m = createFig(coordinates)
    for tick in range(time):
        for idx,cData in enumerate(aggList):
            pops = []
            try:
                pops = cData[tick]
                alphas,size = getAlphas(pops)
                if alphas:
                    draw_dots(m, alphas, colorList, coordinates[0][idx], coordinates[1][idx], size)
                else:
                    continue
            except Exception as e:
                return
        else:
            fig.savefig(destination+'/c_'+str(tick).zfill(6)+".png",
                    dpi=512, orientation='portrait', papertype=None,
                    transparent=True, format="png",
                    bbox_inches='tight', pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            fig,ax,m = createFig(coordinates)
    return

def generateVideo(name, background, imageLocation, imagePattern):
    video = subprocess.Popen(['ffmpeg','-i', background, '-r', '24', '-f',
    'image2', '-s', '1920x1080', '-i', imageLocation+imagePattern,
    '-vcodec', 'libx264', '-crf', '25', '-filter_complex',
    '[0:v][1:v]overlay=0:0[bg]; [bg]pad=ceil(iw/2)*2:ceil(ih/2)*2, ' +
    'format=yuv420p[outv]', '-map', '[outv]', name])
    print(video.pid)
    return video


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
subfolder = folder+'/images/clustercharts/'
vlocation = folder+'videos/'
imagePattern = '/c_%06d.png'

coordinates = getClusters(clusterFileName)

for expPath in sorted(glob.glob(folder+'ANALYZED/E_05*')):
    experiment = expPath.split("/")[-1]

    print(experiment)
    subprocess.Popen(['mkdir', subfolder+experiment])

    clusters = populateClusters(len(coordinates[0]), coordFileName, expPath,
                    patchFilePattern)

    genotypes = getGenotypes(clusters[0][0])
    aggDict = monet.autoGenerateGenotypesDictionary(groups, genotypes)
    aggList = aggregateClusters(clusters, aggDict)
    imageLocation = subfolder+experiment
    generateClusterGraphs(aggList, coordinates, imageLocation, colors)
    vname = vlocation+experiment+'_cdots.mp4'
    background = coordFileName.replace('.csv','.png')
    video = generateVideo(vname,background, imageLocation, imagePattern)

video.wait()

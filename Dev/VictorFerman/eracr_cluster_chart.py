import glob
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import subprocess

def getLines(fileName):
    f = open(fileName, 'r')
    lines = len(f.readlines())-1
    f.close()
    return lines

def createFig():
    fig=None
    ax=None
    m = None

    fig,ax = plt.subplots(figsize=(10, 10))
    ax.tick_params(
    axis='both',          # changes apply to the both
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    right=False,
    labelbottom=False, # labels along the bottom edge are off
    labelleft=False)
    m = Basemap(projection='merc',llcrnrlat=minLat-0.002,urcrnrlat=maxLat+0.002,llcrnrlon=minLong-0.002,urcrnrlon=maxLong+0.002,lat_ts=20,resolution='i', ax=ax)
    m.drawcounties(linewidth=0.3)
    return (fig,ax,m)

def getAlphas(header, fileList, weights, miss=False):
    total = 0
    res= [0]*len(weights)
    headerLen = len(header)
    for patchFile in fileList:
        line = next(patchFile)
        data = line.split(',')
        if miss:
            continue
        elif len(data) == headerLen:
            for i in range(1,len(data)):
                for j in range(len(weights)):
                    num = float(data[i])*weights[j][i-1]
                    res[j]+= num
                    total += num
        else:
            miss=True

    if miss:
        return []
    else:
        return [float(x)/total for x in res]


def draw_dots(m,alphas, X=0, Y=0):
    N = len(alphas)
    start = 0.0
    for i in range(N):
        alphaValue = alphas[i]
        m.scatter([X],[Y], latlon=True, marker='o', s=80, facecolor=colors[i], alpha= alphaValue)

#######
# STATIC GLOBALS
#######
colors = ["#090446", "#f20060", "#6898ff", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ["W", "H", "E", "R", "B"]
weights = [[],[],[],[],[]]

folder = '/Volumes/marshallShare/ERACR/Bakersfield/Riverside/Experiment/MultipleRelease8/'
coordFileLocation = '/Volumes/marshallShare/ERACR/Bakersfield/Riverside/clean/'
coordFileName = 'full2_clustered.csv'
clusterFileName = 'clusterResult.csv'
patchFilePattern = '/ADM_*'
subfolder = folder+'clustercharts/'

clusters = {}

cNum=0
lats = []
longs =[]
clusterFile = open(coordFileLocation+clusterFileName,'r')
for line in clusterFile:
    tokens = line.split(',')
    lats.append(float(tokens[1]))
    longs.append(float(tokens[0]))
    clusters[str(cNum)]=[]
    cNum+=1

minLat = min(lats)
minLong = min(longs)
maxLat = max(lats)
maxLong = max(longs)

patchCluster =[]
coordFile = open(coordFileLocation+coordFileName,'r')
for line in coordFile:
    patchCluster.append(line.split(',')[2].strip())

for expPath in sorted(glob.glob(folder+'ANALYZED/E_*')):
    experiment = expPath.split("/")[-1]
    patchFileList = sorted(glob.glob(expPath+patchFilePattern))
    print(experiment)
    subprocess.Popen(['mkdir', subfolder+experiment])
    header = []
    lines = getLines(patchFileList[0])
    for index,patchFileN in enumerate(patchFileList):
        patchFile = open(patchFileN, 'r')
        headerLine = next(patchFile)
        clusters[patchCluster[index]].append(patchFile)
    else:
        header = headerLine.split(',')
        patchFile = None
        for genotype in header[1:]:
            for j in range(len(groups)):
                weights[j].append(genotype.count(groups[j]))

    fig,ax,m = createFig()

    for time in range(lines):
        miss = False
        for k,pFileList in clusters.items():
            idx = int(k)
            alphas = getAlphas(header,pFileList,weights,miss)
            if alphas:
                draw_dots(m, alphas, longs[idx], lats[idx])
            else:
                miss=True
                continue

        else:
            fig.savefig(subfolder+experiment+'/c_'+str(time).zfill(6)+".png",
                    dpi=512, orientation='portrait', papertype=None,
                    facecolor='w', edgecolor='w', format="png",
                    bbox_inches='tight', pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            fig,ax,m = createFig()

    for pFileList in clusters:
        for patchFile in pFileList:
            patchFile.close()

    vname = experiment+'_cdots.mp4'
    video = subprocess.Popen(['ffmpeg', '-r', '24', '-f', 'image2', '-s', '1920x1080', '-i', subfolder+experiment+'/c_%06d.png', '-vcodec', 'libx264', '-crf', '25','-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-pix_fmt', 'yuv420p',folder+'videos/'+vname])
    print(video.pid)

video.wait()

import glob
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import subprocess

#########
# AUX functions
#########
def getCoordInfo(fileName):
    x = []
    y = []
    patchNum = 0
    coordFile= open(fileName, 'r')
    for line in coordFile:
        coord = line.split(',')
        x.append(float(coord[2]))
        y.append(float(coord[3]))
        patchNum = len(x)

    return(x,y,patchNum)

def getLines(fileName):
    f = open(fileName, 'r')
    lines = len(f.readlines())-1
    f.close()
    return lines

def getSizes(line, weights):
    total = 0
    res = [0]*len(weights)
    for i in range(len(line)):
        for j in range(len(weights)):
            num = float(line[i])*weights[j][i]
            res[j]+= num
            total += num

    return [float(x)/total for x in res]

def draw_pie(ax,ratios, X=0, Y=0):
    N = len(ratios)
    start = 0.0
    for i in range(N):
        ratio = ratios[i]
        if ratio >= 0.005:
            x = [0] + np.cos( np.linspace(2*math.pi*start, 2*math.pi*(start+ratio)) ).tolist()
            y = [0] + np.sin( np.linspace(2*math.pi*start, 2*math.pi*(start+ratio)) ).tolist()
            xy1 = np.column_stack([x, y])
            s1 = np.abs(xy1).max()
            ax.scatter([X],[Y] , marker=(xy1), s=12*s1**2, facecolor=colors[i])
            start += ratio

#######
# STATIC GLOBALS
#######
colors = ["#090446", "#f20060", "#6898ff", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ["W", "H", "E", "R", "B"]
weights = [[],[],[],[],[]]

folder = '/Volumes/marshallShare/ERACR/Bakersfield/Riverside/Experiment/MultipleRelease8/'
coordFileLocation = '/Volumes/marshallShare/ERACR/Bakersfield/Riverside/clean/Full.csv'
patchFilePattern = '/ADM_*'
subfolder = folder+'piecharts/'


########
# Per landscape GLOBALS
########
lines = 0
video = None
(longs,lats,patches) = getCoordInfo(coordFileLocation)
minLat = min(lats)
minLong = min(longs)
maxLat = max(lats)
maxLong = max(longs)


for expPath in sorted(glob.glob(folder+'ANALYZED/E_*')):
    experiment = expPath.split("/")[-1]
    patchFileList = sorted(glob.glob(expPath+patchFilePattern))
    print(experiment)
    subprocess.Popen(['mkdir', subfolder+experiment])
    patchFiles =[]
    lines = getLines(patchFileList[0])
    for i in patchFileList:
        patchFile = open(i, 'r')
        headerLine = next(patchFile)
        patchFiles.append(patchFile)
    else:
        header = headerLine.split(',')
        for genotype in header[1:]:
            for j in range(len(groups)):
                weights[j].append(genotype.count(groups[j]))

    fig, ax = plt.subplots(figsize=(5, 5))
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
    for time in range(lines):
        for i in range(patches):
            line = next(patchFiles[i])
            data = line.split(',')
            if len(data) != len(header):
                continue
            sizes = getSizes(data[1:],weights)
            px,py = m(longs[i],lats[i])
            draw_pie(ax, sizes, px, py)

        else:
            m.drawcounties(linewidth=0.3)
            plt.savefig(subfolder+experiment+'/'+str(time).zfill(6)+".png",
                        dpi=1024, facecolor='w',
                        edgecolor='w', orientation='portrait', papertype=None,
                        format="png", transparent=False, bbox_inches='tight',
                        pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            fig, ax= plt.subplots(figsize=(5, 5))
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


    for patchfile in patchFiles:
        patchfile.close()
    vname = experiment+'.mp4'
    video = subprocess.Popen(['ffmpeg', '-r', '24', '-f', 'image2', '-s', '1920x1080', '-i', subfolder+experiment+'/%06d.png', '-vcodec', 'libx264', '-crf', '25','-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-pix_fmt', 'yuv420p',folder+'videos/'+vname])
    print(video.pid)

video.wait()

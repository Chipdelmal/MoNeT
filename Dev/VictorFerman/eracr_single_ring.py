import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import subprocess


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
            ax.scatter([X],[Y] , marker=(xy1), s=500*s1**2, facecolor=colors[i])
            start += ratio


colors = ['#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ['W', 'H', 'R', 'B', 'E']
weights = [[],[],[],[],[]]
patches = 10
radius = 50

folder = '/Volumes/marshallShare/vic/eRACRfact16/'
video = None
coordFile = open(str(patches)+'_'+str(radius)+'_ring_coords.csv')
xList = []
yList = []
for line in coordFile:
    coord = line.split(',')
    xList.append(float(coord[0]))
    yList.append(float(coord[1]))
for interval in range(100, 275, 25):
    for releases in range (20,32,2):
        experiment='E_'+str(interval).zfill(4)+'_02_'+str(releases).zfill(5)
        print(experiment)
        maleFile = open(folder+experiment+'/ADM_Run001.csv', 'r')
        #maleFile = open('/Users/vferman/Desktop/HOLD/MGDrivE2/ADM_Run001.csv', 'r')
        first = next(maleFile)
        header = first.split(',')

        for genotype in header[2:]:
            for i in range(len(groups)):
                weights[i].append(genotype.count(groups[i]))
        time= 0
        fig, ax = plt.subplots(figsize=(3, 3))
        for line in maleFile:
            data = line.split(',')
            currentPatch = int(data[1])
            if currentPatch != (patches-1):
                if len(data) != len(header):
                    continue
                sizes = getSizes(data[2:],weights)
                draw_pie(ax, sizes, xList[currentPatch], yList[currentPatch])
            else:
                if len(data) != len(header):
                    pass
                else:
                    sizes = getSizes(data[2:],weights)
                    draw_pie(ax, sizes, xList[currentPatch], yList[currentPatch])
                    ax.set_ylim((-radius-10), (radius+10))
                    ax.set_xlim((-radius-10), (radius+10))
                plt.savefig(folder+experiment+'/'+str(time).zfill(5)+".png",
                            dpi=1024, facecolor='w',
                            edgecolor='w', orientation='portrait', papertype=None,
                            format="png", transparent=False, bbox_inches='tight',
                            pad_inches=0.05, frameon=None)
                plt.close(fig)
                plt.close('all')
                time+=1
                fig, ax= plt.subplots(figsize=(3, 3))
        maleFile.close()
        video = subprocess.Popen(['ffmpeg', '-r', '24', '-f', 'image2', '-s', '1920x1080', '-i', folder+experiment+'/%05d.png', '-vcodec', 'libx264', '-crf', '25','-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-pix_fmt', 'yuv420p',folder+'videos/'+experiment+'.mp4'])
        print(video.pid)

video.wait()

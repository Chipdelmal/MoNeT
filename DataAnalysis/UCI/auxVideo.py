#!/usr/bin/python
# -*- coding: utf-8 -*-

# ############################################################################
# Aux
#   Non-critical functions to help on the analyses
# ############################################################################
import os
import fun
import subprocess
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


PAD = .1
COLORS = [
        fun.rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        fun.rescaleRGBA((255, 0, 152, 255/1)),      # 1: Magenta
        fun.rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        fun.rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        fun.rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        fun.rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]


def get_corners(fileName):
    lats = []
    longs = []
    clusterData = open(fileName, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (lat, long) = (float(tokens[1]), float(tokens[2]))
        lats.append(lat)
        longs.append(long)

    minLat = min(lats)
    minLong = min(longs)
    maxLat = max(lats)
    maxLong = max(longs)
    return [[minLong, maxLong], [minLat, maxLat]]


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


def createBasemapInstance(minLat, maxLat, minLon, maxLon, pad=1.5):
    base = Basemap(
            projection='merc',
            lat_0=(maxLat - minLat)/2, lon_0=(maxLon - minLon)/2,
            resolution='h', area_thresh=0.1,
            llcrnrlon=minLon - pad, llcrnrlat=minLat - pad,
            urcrnrlon=maxLon + pad, urcrnrlat=maxLat + pad,
            epsg=4269
        )
    return base


def generateClusterGraphs(
            clstFile,
            aggList, coordinates, destination, colorList, original_corners,
            padding, dpi, countries=False, skip=False, refPopSize=1,
            verbose=True, background=False, timeLocation=(.5, .5)
        ):
    time = len(aggList[0])
    # if original_corners:
    #     fig, ax, m = monet.createFig(original_corners, padding, countries)
    # else:
    #     fig, ax, m = monet.createFig(coordinates, padding, countries)

    timeMax = list(range(time))
    for tick in timeMax:
        imgFileName = destination+'/c_'+str(tick).zfill(6)+".png"
        if skip and os.path.isfile(imgFileName):
            continue

        for idx, cData in enumerate(aggList):
            if idx == 0:
                (fig, ax, m) = createMap(clstFile, COLORS, pad=.025)
            pops = []
            try:
                pops = cData[tick]
                alphas, size = monet.getAlphas(pops)
                if alphas:
                    draw_dots(
                            m, alphas, colorList,
                            coordinates[1][idx], coordinates[0][idx],
                            size/refPopSize
                        )
                else:
                    continue
            except Exception as e:
                return e
        else:
            ax.axis('off')
            plt.text(
                    timeLocation[0], timeLocation[1], str(tick+1).zfill(4),
                    ha='left', va='top',
                    transform=fig.transFigure
                )
            fig.savefig(imgFileName,
                        dpi=dpi, orientation='portrait', papertype=None,
                        transparent=False, format="png",
                        bbox_inches='tight', pad_inches=0.05, frameon=None)
            plt.close(fig)
            plt.close('all')
            if original_corners:
                fig, ax, m = monet.createFig(
                        original_corners, padding, countries
                    )
            else:
                fig, ax, m = monet.createFig(coordinates, padding, countries)
        if verbose:
            print(
                    'Exporting frame: ({}/{})'.format(
                            str(tick+1).zfill(4), str(time).zfill(4)
                    ), end='\r'
                )
    return


def generateVideo(name, background, imageLocation, imagePattern):
    video = subprocess.Popen([
            'ffmpeg', '-i', background, '-r', '24', '-f',
            'image2', '-s', '1920x1080', '-i', imageLocation+imagePattern,
            '-vcodec', 'libx264', '-crf', '25', '-filter_complex',
            '[0:v][1:v]overlay=0:0[bg]; [bg]pad=ceil(iw/2)*2:ceil(ih/2)*2, '
            + 'format=yuv420p[outv]', '-map', '[outv]', name]
        )
    return video


def createMap(clusterFile, COLORS, pad=.025):
    (minLat, maxLat, minLong, maxLong) = (0, 0, 0, 0)
    (lats, longs, clusters) = ([], [], [])
    clusterData = open(clusterFile, 'r')
    next(clusterData)
    for line in clusterData:
        tokens = line.split(',')
        (lat, long, cluster) = (
                float(tokens[1]), float(tokens[2]), int(tokens[3])
            )
        lats.append(lat)
        longs.append(long)
        clusters.append(cluster)

    (minLat, maxLat, minLong, maxLong) = (
            min(lats), max(lats), min(longs), max(longs)
        )
    (minCluster, maxCluster) = (min(clusters), max(clusters))

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, label="1")
    m = Basemap(
            projection='merc',
            llcrnrlat=minLat-pad, urcrnrlat=maxLat+pad,
            llcrnrlon=minLong-pad, urcrnrlon=maxLong+pad,
            lat_ts=20, resolution='i', ax=ax
        )
    m.drawcoastlines(color=COLORS[4], linewidth=5, zorder=-1)
    m.drawcoastlines(color=COLORS[0], linewidth=2, zorder=-1)
    m.drawcoastlines(color=COLORS[4], linewidth=.5, zorder=-1)
    # m.fillcontinents(color=COLORS[3], lake_color='aqua')
    m.scatter(
            longs, lats, latlon=True, alpha=.1, marker='x', s=1,
            cmap=plt.get_cmap('winter'), c=clusters,
            vmin=minCluster, vmax=maxCluster
        )
    ax.tick_params(
            axis='both',       # changes apply to the both
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            right=False,
            labelbottom=False,  # labels along the bottom edge are off
            labelleft=False
        )
    ax.axis('off')
    return (fig, ax, m)


def callffmpeg(folder, pattern, rate, resolution, outFile):
    calling = [
            'ffmpeg', '-r', str(rate), '-f', 'image2',  '-s',
            '{}x{}'.format(str(resolution[0]), str(resolution[1])),
            '-i', folder + pattern, '-vcodec', 'libx264', '-crf', '25',
            '-pix_fmt', 'yuv420p', outFile
        ]
    video = subprocess.Popen(calling)
    print(calling)
    return video


def draw_dots(m, alphas, colorList, long=0, lat=0, size=60):
    # start = 0.0
    for idx, value in enumerate(alphas):
        m.scatter(
                [long], [lat], latlon=True, marker=(6, 0),
                s=max(6, 0.11 * size), facecolor=colorList[idx],
                alpha=value, linewidths=.2, edgecolors='White'
            )


import math
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


COLORS = [
        rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        rescaleRGBA((255, 0, 152, 255/1)),      # 1: Magenta
        rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]


def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='', vLines=[0, 0], hLines=[0]):
    figArr = monet.plotNodeTraces(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.axes.xaxis.set_visible(False)
    axTemp.axes.yaxis.set_visible(False)
    axTemp.xaxis.set_tick_params(width=1)
    axTemp.yaxis.set_tick_params(width=1)
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))

    if vLines[0] > 0:
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.2, facecolor='#3687ff', zorder=0)
    axTemp.axhline(
            hLines, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000'
        )
    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000')
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=0.05
        )
    plt.close('all')
    return True


def plotMap(fig, ax, pts, BLAT, BLNG, drawCoasts=True):
    # Hi-Res Basemap ----------------------------------------------------------
    mH = Basemap(
        projection='merc', ax=ax, lat_ts=20, resolution='h',
        llcrnrlat=BLAT[0], urcrnrlat=BLAT[1],
        llcrnrlon=BLNG[0], urcrnrlon=BLNG[1],
    )
    mL = Basemap(
        projection='merc', ax=ax, lat_ts=20, resolution='i',
        llcrnrlat=BLAT[0], urcrnrlat=BLAT[1],
        llcrnrlon=BLNG[0], urcrnrlon=BLNG[1],
    )
    if drawCoasts:
        mH.drawcoastlines(color=COLORS[0], linewidth=2, zorder=1)
        mH.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=2)
        mL.drawcoastlines(color=COLORS[4], linewidth=10, zorder=0)
    # Lo-Res Basemap ----------------------------------------------------------
    mH.scatter(
        list(pts['lon']), list(pts['lat']), latlon=True,
        alpha=.2, marker='.', s=[10 * math.log(i) for i in list(pts['pop'])],
        color='#E048B8', zorder=3
    )
    # Ax parameters -----------------------------------------------------------
    ax.tick_params(
        axis='both', which='both',
        bottom=True, top=False, left=True, right=False,
        labelbottom=True, labelleft=True
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # Return values -----------------------------------------------------------
    return (fig, ax)
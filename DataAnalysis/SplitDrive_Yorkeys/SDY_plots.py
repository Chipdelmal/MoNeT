
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


# #############################################################################
# Videos
# #############################################################################
def plotMap(
        fig, ax, pts, BLAT, BLNG, 
        drawCoasts=True, ptColor='#66ff00'
):
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
        mH.drawcoastlines(color=COLORS[0], linewidth=0, zorder=1)
        mH.drawcoastlines(color=COLORS[3], linewidth=0, zorder=2)
        mL.drawcoastlines(color=COLORS[4], linewidth=0, zorder=0)
    # Lo-Res Basemap ----------------------------------------------------------
    mH.scatter(
        list(pts['Lat']), list(pts['Lon']), latlon=True,
        alpha=.15, marker='.', 
        s=popsToPtSize(list(pts['Pop']), offset=10, amplitude=10),
        color=ptColor, zorder=2
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
    return (fig, ax, mL)


def floatToHex(a, minVal=0, maxVal=1):
    intVal = round(np.interp(a, (minVal, maxVal), (0, 255)))
    return intVal


def popsToPtSize(pops, offset=10, amplitude=10):
    return [max(offset, amplitude * math.sqrt(i)) for i in pops]


def plotPopsOnMap(
    fig, ax, mapR, 
    lngs, lats, fractions, pops, 
    color='#ed174b', marker=(6, 0),
    offset=10, amplitude=10, lw=5, ec=(0, 0, 0, .5)
):
    colors = [color + '%02x' % floatToHex(i) for i in fractions]
    mapR.scatter(
        lngs, lats, 
        latlon=True, marker=marker,
        s=popsToPtSize(pops, offset=offset, amplitude=amplitude),
        c=colors, ax=ax, lw=lw, ec=ec, zorder=5
    )
    return (fig, ax, mapR)


def plotGenePopsOnMap(
    fig, ax, mapR,
    lngs, lats, colors, 
    GC_FRA, time, alphaScaler=.5,
    marker=(6, 0), offset=10, amplitude=10, lw=2, ec=(0, 0, 0, .5)
):
    geneFraSlice = np.asarray([i[time] for i in GC_FRA]).T
    geneFraSlice = np.asarray([i * alphaScaler for i in geneFraSlice])
    for gIx in range(geneFraSlice.shape[0]-1):
        (fig, ax, mapR) = plotPopsOnMap(
            fig, ax, mapR, 
            lats, lngs, geneFraSlice[gIx], geneFraSlice[-1],
            color=colors[gIx], marker=marker,
            offset=offset, amplitude=amplitude, lw=lw, ec=ec
        )
    return (fig, ax, mapR)
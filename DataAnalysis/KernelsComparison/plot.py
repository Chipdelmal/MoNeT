#!/usr/bin/python
# -*- coding: utf-8 -*-

(SUP_COL, MIN_COL) = ('gray', 'red')


def setAxesColor(axTemp, color):
    axTemp.tick_params(color=color)
    for spine in axTemp.spines.values():
        spine.set_edgecolor(color)
    return axTemp


def removeTicksAndLabels(axTemp):
    axTemp.set_xticklabels([])
    axTemp.set_yticklabels([])
    axTemp.set_xticks([])
    axTemp.set_yticks([])
    return axTemp


def printHAxisNumbers(
            ax, numbers, xRange, top=True,
            color='Black', relStr=0, fntSz=4, alpha=.5
        ):
    (yPos, vAlign) = (-.02, 'top')
    if top:
        (yPos, vAlign) = (1.01, 'bottom')
    # Plot text if the list is longer than one
    if len(numbers) > 0:
        for i in numbers:
            ax.text(
                    i/xRange, yPos, str(i-relStr), color=color, fontsize=fntSz,
                    alpha=.5, verticalalignment=vAlign,
                    horizontalalignment='center', transform=ax.transAxes
                )
    return ax


def printHAxisNumbersAlt(
            ax, numbers, xRange,
            color='Black', relStr=0, fntSz=4, alpha=.5
        ):
    if len(numbers) > 0:
        for (ix, i) in enumerate(numbers):
            (yPos, vAlign) = (-.05, 'top')
            # Alternate based on open/close of the threshold cross
            if ix < len(numbers) / 2:
                if (ix % 2 == 0):
                    (yPos, vAlign) = (1.01, 'bottom')
            else:
                if (ix % 2 != 0):
                    (yPos, vAlign) = (1.01, 'bottom')
            # Plot text
            ax.text(
                    i/xRange, yPos, str(i-relStr), color=color, fontsize=fntSz,
                    alpha=.5, verticalalignment=vAlign,
                    horizontalalignment='center', transform=ax.transAxes
                )
    return ax


def printVAxisNumbers(ax, numbers, yRange, color='Black', left=True, rnd=True):
    (xPos, hAlign) = (-.004, 'right')
    #
    if len(numbers) > 0:
        for i in numbers:
            if rnd:
                val = str(int(i))
            else:
                val = round(i, 2)
            #####
            ax.text(
                    xPos, i/yRange, val, color=color, fontsize=2,
                    alpha=.5, verticalalignment='center',
                    horizontalalignment=hAlign, transform=ax.transAxes
                )
    return ax


def parseTitle(thresholds, prtcDays):
    title = '  '.join(['[{}: {}]'.format(
                str(round(x[0], 2)).ljust(4, '0'),
                str(x[1]).zfill(4)
            ) for x in zip(thresholds, prtcDays)]
        )
    return title


def parseMinTitle(minTuple, SSPOP, thrs=.05, relStr=0):
    if(1 - minTuple[1] / SSPOP >= thrs):
        title = "MIN: [{}: {}]".format(
                int(minTuple[0] - relStr),
                round(1 - minTuple[1]/SSPOP, 2)
            )
    else:
        title = "MIN: [0: 0]"
    return title


def printTitle(ax, title, pos=(.999, .5), fntSz=10, alpha=.75):
    ax.text(
            pos[0], pos[1], title, color=SUP_COL,
            fontsize=fntSz, alpha=alpha,
            verticalalignment='top', horizontalalignment='right',
            transform=ax.transAxes
        )
    return ax


def printMinTitle(ax, title):
    ax.text(
            .999, .45, title + ' ', color=MIN_COL, fontsize=2, alpha=.5,
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes
        )
    return ax


def printVLines(ax, chngDays):
    for vLine in chngDays:
        ax.axvline(
                x=vLine, linewidth=.1,
                linestyle='--', color=SUP_COL, alpha=.75
            )
    return ax


def printMinLines(ax, minTuple, style, SSPOP, thrs=.05):
    (width, alpha) = (.3, .5)
    if(1 - minTuple[1] / SSPOP >= thrs):
        ax.axhline(
                y=minTuple[1], xmin=0, xmax=minTuple[0]/style['xRange'][1],
                linewidth=width, linestyle='--', color=MIN_COL, alpha=alpha
            )
        ax.axvline(
                x=minTuple[0], ymin=0, ymax=1,
                linewidth=width, linestyle='--', color=MIN_COL, alpha=alpha
            )
    return ax


def setRange(ax, style):
    ax.set_xlim(style['xRange'][0], style['xRange'][1])
    ax.set_ylim(style['yRange'][0], style['yRange'][1])
    return ax

#!/usr/bin/python
# -*- coding: utf-8 -*-

import SDY_functions as fun
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt

(VOL, SIG, PRB) = ('RAID5', 'unAggregated', ('Aggregated',))
PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
pthOut = PATH + 'err/'
pthImg = pthOut + 'img/'
###############################################################################
# Setting up colors and style
###############################################################################
COLORS = [
        "#090446A0", "#f20060A0", "#c6d8ffA0",
        "#7692ffA0", "#29339bA0", "#7fff3aA0"
    ]
STYLE = {
        "width": 1, "alpha": .15, "dpi": 2 * 300,
        "legend": False, "aspect": .5, "colors": COLORS,
        "xRange": [0, 1825], "yRange": [-1.25, +1.25]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
###############################################################################
# Main Routine
###############################################################################
# Loading the signal files ----------------------------------------------------
pth = PATH + 'pre/' + SIG + '/'
sigFiles = fun.getPreProcessedExperiments(pth, 'sum')
# Loading the paths for the probes --------------------------------------------
prbExpPths = [PATH + 'pre/' + st + '/' for st in PRB]
prbFiles = fun.getPreProcessedExperiments(prbExpPths[0], 'sum')
# Cycling through file pairs --------------------------------------------------
for i in range(0, len(sigFiles)):
    (namS, pthS) = sigFiles[i]
    (namP, pthP) = prbFiles[i]
    # Load data
    (dataS, dataP) = (pkl.load(pthS), pkl.load(pthP))
    (genes, popS) = (dataS['genotypes'], dataS['population'])
    (genes, popP) = (dataP['genotypes'], dataP['population'])
    # Calculate error
    err = fun.rpd(popS, popP)
    # Plot
    pop = {'genotypes': genes, 'population': err}
    plot = monet.plotMeanGenotypeTrace(pop, STYLE)
    axTemp = plot.get_axes()[0]
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    # Write to disk
    monet.writeListToCSV(pthOut+namP+'.csv', err, genes)
    plot.savefig(
            "{}/{}.pdf".format(pthImg, namP),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='pdf',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')

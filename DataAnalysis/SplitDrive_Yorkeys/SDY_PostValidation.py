#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import SDY_functions as fun
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt

(VOL, SIG, PRB) = (
        'RAID5', 'C001303',
        (
            'C000001', 'C000010', 'C000050', 'C000100',
            'C000150', 'C000200', 'C001303'
        )
    )
PATH = '/RAID5/marshallShare/SplitDrive_Yorkeys/batchProof/'
# PATH = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
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
        "xRange": [0, 1825], "yRange": [-1, +1]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH, pthImg, pthOut)
###############################################################################
# Main Routine
###############################################################################
# Loading the signal files ----------------------------------------------------
pth = PATH + 'pre/' + SIG + '/'
sigFiles = fun.getPreProcessedExperiments(pth, 'sum')
# Loading the paths for the probes --------------------------------------------
for j in range(0, len(PRB)):
    strInt = str(j+1).zfill(len(str(len(PRB))))
    print('* Analyzing ({}/{})       '.format(strInt, str(len(PRB))), end='\r')
    prbExpPths = PATH + 'pre/' + PRB[j] + '/'
    prbFiles = fun.getPreProcessedExperiments(prbExpPths, 'sum')
    oPth = pthOut + PRB[j] + '/'
    iPth = oPth + '/img/'
    monet.makeFolder(oPth)
    monet.makeFolder(iPth)
    # Cycling through file pairs ---------------------------------------------
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
        for yix in (-1, -.75, -.5, -.25, .25, .5, .75, 1):
            axTemp.axhline(y=yix, color=(0,0,0,.25), linewidth=.2, ls='dashed')
        axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
        axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
        # Write to disk
        monet.writeListToCSV(oPth+namP+'.csv', err, genes)
        plot.savefig(
                "{}/{}-{}.png".format(iPth, PRB[j], namP),
                dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
                orientation='portrait', papertype=None, format='png',
                transparent=True, bbox_inches='tight', pad_inches=.01
            )
        plt.close('all')
tE = datetime.datetime.now()
print('* Analyzed ({}/{})         '.format(strInt, str(len(PRB))), end='\n')
# fun.printExperimentTail(str(tE-tS), 'Plotting')

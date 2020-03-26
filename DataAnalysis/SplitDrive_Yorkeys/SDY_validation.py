
import sys
import datetime
import numpy as np
import SDY_aux as aux
import SDY_functions as fun
# import SDY_select as sel
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(VOL, SETS, PLOTS, ERROR) = (
        'RAID5', ('unAggregated', 'Aggregated'), True, True
    )
###############################################################################
# Setting up colors and style
###############################################################################
(MALE, FEMALE) = (True, True)
COLORS = [
        "#09044620", "#f2006020", "#c6d8ff20",
        "#7692ff20", "#29339b20", "#7fff3a20"
    ]
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300,
        "legend": True, "aspect": .5, "colors": COLORS,
        "xRange": [0, 1825], "yRange": [0, 150000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
# PATH = '/{}/marshallShare/SplitDrive_Yorkeys/geoProof/'.format(VOL)
PATH = '/home/chipdelmal/Desktop/SD/'
GDICT = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
###############################################################################
# Get paths and create output folders
###############################################################################
# Input paths
(sig, prb) = (
        fun.getValidationExperiments(PATH, SETS[0]),
        fun.getValidationExperiments(PATH, SETS[1])
    )
# Shallow validation
(xpTest, xpNumb) = (len(sig) == len(prb), len(sig))
(PATH_ERR, PATH_IMG) = (PATH + 'err/', PATH + 'img/')
fun.createFolders([PATH_ERR, PATH_IMG])
###############################################################################
# Print terminal message
###############################################################################
tSrt = datetime.datetime.now()
aux.printExperimentHead(PATH, PATH_IMG, PATH_ERR, str(tSrt), 'GeoValidation ')
if xpTest is False:
    print(aux.CRED+'ERROR: Missmatch in number of experiments!'+CEND)
    sys.exit()
###############################################################################
# Main analyses
###############################################################################
for i in range(xpNumb):
    # Load data ---------------------------------------------------------------
    aux.printProggress(i, xpNumb, sig)
    (nS, mS, tS) = fun.loadAndCalcResponse(sig[i], GDICT, MALE, FEMALE)
    # (nP, mP, tP) = fun.loadAndCalcResponse(prb[i], GDICT, MALE, FEMALE)
    # Calculate and save error  -----------------------------------------------
    # err = fun.rpd(mS['landscape'], mP['landscape'])
    # np.savetxt(
    #         '{}/{}.csv'.format(PATH_ERR, nS), err,
    #         fmt='%.4e', delimiter=',', header=','.join(mS['genotypes'])
    #     )
    # Plots  ------------------------------------------------------------------
    figArr = monet.plotLandscapeDataRepetitions(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.set_xticks(range(0, STYLE["xRange"][1], 150))
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}.pdf".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='pdf',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished! ')

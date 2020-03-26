
import sys
import datetime
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
COLORS = ["#090446", "#f20060", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300,
        "legend": True, "aspect": .5, "colors": COLORS,
        "xRange": [0, 1825], "yRange": [0, 7000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
# PATH = '/{}/marshallShare/SplitDrive_Yorkeys/geoProof/'.format(VOL)
PATH = '/home/chipdelmal/Desktop/SD/'
GDICT = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
###############################################################################
# Get paths and create output folders
###############################################################################
# Input paths
sig = fun.getValidationExperiments(PATH, SETS[0])
prb = fun.getValidationExperiments(PATH, SETS[1])
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
    print(aux.CRED+'ERROR: Missmatch in number of experiments!'+ CEND)
    sys.exit()
###############################################################################
# Main analyses
###############################################################################
i = 0
aux.printProggress(i, xpNumb, sig)
(nS, mS, tS) = fun.loadAndCalcResponse(sig[i], GDICT, MALE, FEMALE)
(nP, mP, tP) = fun.loadAndCalcResponse(prb[i], GDICT, MALE, FEMALE)
err = fun.rpd(mS['landscape'], mP['landscape'])
print(err)
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished!')

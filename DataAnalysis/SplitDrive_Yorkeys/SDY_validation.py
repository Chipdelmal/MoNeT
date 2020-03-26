
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
sig = fun.getValidationExperiments(PATH, SETS[0]) # (xpSN, xpSAP, xpSGP)
prb = fun.getValidationExperiments(PATH, SETS[1]) # (xpPN, xpPAP, xpPGP)
# Shallow validation
(xpTest, xpNumb) = (len(sig[0]) == len(prb[0]), len(sig[0]))
# for i in range(xpNumb):
#     print('{}-{}::{}-{}'.format(xpSN[i], xpPN[i], xpSAP[i], xpPAP[i]))
# Outputs paths
(PATH_ERR, PATH_IMG) = (PATH + 'err/', PATH + 'img/')
monet.makeFolder(PATH_ERR)
monet.makeFolder(PATH_IMG)
###############################################################################
# Print terminal message
###############################################################################
tSrt = datetime.datetime.now()
aux.printExperimentHead(PATH, PATH_IMG, PATH_ERR, str(tSrt), 'GeoValidation ')
print('{}* Experiments test passed: {}{}'.format(aux.CYEL, xpTest, aux.CEND))
###############################################################################
# Main analyses
###############################################################################
(i, dtSet) = (0, prb)
# Loop starts here!
(name, aPath, gPath) = dtSet[i]
(aFiles, gFiles) = (
        monet.readExperimentFilenames(aPath),
        monet.listDirectoriesWithPathWithinAPath(gPath+'/')
    )
# Mean response
print(aux.CBBL, end='\r')
print('* Loading mean response...', end='\r')
landData = monet.loadLandscapeData(aFiles, male=True, female=True)
print('* Aggregating mean response...', end='\r')
aggData = monet.aggregateGenotypesInLandscape(landData, GDICT)
aggData['landscape'] = sum(aggData['landscape'])
print(aux.CEND, end='\r')
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished!')

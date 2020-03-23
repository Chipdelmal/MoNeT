import SDY_aux as aux
# import SDY_select as sel
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(VOL, SETS) = ('RAID5', ('unAggregated', 'Aggregated'))
###############################################################################
COLORS = ["#090446", "#f20060", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300,
        "legend": True, "aspect": .5, "colors": COLORS,
        "xRange": [0, 1825], "yRange": [0, 7000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
PATH = '/{}/marshallShare/SplitDrive_Yorkeys/geoProof/'.format(VOL)
GDICT = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
###############################################################################
(EXPsT, EXPsP) = [
		sorted(monet.listDirectoriesInPath(PATH+exp+'/ANALYZED/')) 
		for exp in SETS
	]
for i in zip(EXPsT, EXPsP):
    print('{} : {}'.format(i[0], i[1]))
###############################################################################
# for DRIVE in [1]:
#     pathsRoot, aggregationDictionary, prepend, pathO = aux.driveSelector(
#         DRIVE, HEALTH, pathRoot
#     )
#     pathExport = pathOut + pathO + '/'
#     ###########################################################################
#     num = len(pathsRoot)
#     for i in range(480, num, 1):
#         pathSample = pathsRoot[i]
#         experimentString = pathSample.split("/")[-1]
#         paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
#         landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
#                 paths, aggregationDictionary,
#                 male=False, female=True, dataType=float
#             )
#         landscapeReps = funcs.normalizeLandscapeDataRepetitions(
#                 landscapeReps, totalPopIx=-1
#             )
#         figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
#         for j in range(0, len(figsArray)):
#             figsArray[j].get_axes()[0].set_xlim(0,style['xRange'][1])
#             figsArray[j].get_axes()[0].set_ylim(0,style['yRange'][1])
#             expOutStr = pathExport + prepend + experimentString
#             monet.quickSaveFigure(
#                 figsArray[j], expOutStr+"_N"+str(j)+".png", dpi=style['dpi']
#             )
#         plt.close('all')
#         print('\tExported ' + str(i + 1).rjust(4, '0') + '/' + str(num) + ': ' + expOutStr)
# ###############################################################################
# print('******************************************************************')
# print('* Finished all drives correctly')
# print('******************************************************************')

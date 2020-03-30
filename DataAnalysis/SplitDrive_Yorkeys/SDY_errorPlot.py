
import glob
import sys
import datetime
import numpy as np
import SDY_aux as aux
import SDY_functions as fun
# import SDY_select as sel
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


###############################################################################
# Setting up colors and style
###############################################################################
VOL = 'RAID5'
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
PATH = '/{}/marshallShare/SplitDrive_Yorkeys/geoProof/err/'.format(VOL)
# PATH = '/home/chipdelmal/shared/SDY/err/'
GDICT = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
###############################################################################
# Get paths and create output folders
###############################################################################
# I/O paths
(filePaths, PATH_IMG) = (glob.glob(PATH + '*.csv'), PATH+'img/')
fun.createFolders([PATH_IMG])
# ###############################################################################
# # Print terminal message
# ###############################################################################
tSrt = datetime.datetime.now()
aux.printExperimentHead(PATH, PATH_IMG, PATH, str(tSrt), 'GeoValidation ')
# ###############################################################################
# # Main analyses
# ###############################################################################
for (i, file) in enumerate(filePaths):
    # Print Progress
    (curr, total) = (str(i+1).zfill(3), str(len(filePaths)).zfill(3))
    print('Working on: {}/{}'.format(curr, total), end='\r')
    # Plot
    name = file.split('/')[-1].split('.')[0]
    pop = {
            'genotypes': GDICT['genotypes'],
            'population': np.loadtxt(file, skiprows=1, delimiter=',')
        }
    plot = monet.plotMeanGenotypeTrace(pop, STYLE)
    axTemp = plot.get_axes()[0]
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    plot.savefig(
            "{}/{}-{}.pdf".format(PATH_IMG, name, 'E'),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='pdf',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
    plt.close('all')
print('Finished exporting all the plots!')
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished! ')

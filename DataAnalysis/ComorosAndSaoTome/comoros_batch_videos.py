import glob
import MoNeT_MGDrivE as monet
import subprocess

#######
# STATIC GLOBALS
####### 3rd , "#6898ff"
colors = ["#090446", "#f20060", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ["W", "H", "R", "B", "E"]

folder = '/Volumes/marshallShare/Comoros_STP/STP/output/'
patchFilePattern = {'males':'/M_*', 'females':'/F_*'}
imagePattern = '/c_%06d.png'
bgname  = '/Volumes/marshallShare/Comoros_STP/STP/STP_all_sites2.png'
clusterName = '/Volumes/marshallShare/Comoros_STP/STP/STP_all_sites2.csv'


for expFolder in sorted(glob.glob(folder+'*')):
    expBaseName = expFolder.split('/')[-1]
    print(expBaseName)
    for expPath in sorted(glob.glob(expFolder+'/ANALYZED/E_*')):
        vname = expPath.replace('ANALYZED','videos')+'_cdots.mp4'
        coordinates = monet.getClusters(clusterName)

        imageLocation = expPath.replace('ANALYZED','images/clustercharts')
        subprocess.Popen(['mkdir', imageLocation])
        clusters = monet.populateClusters(
                            len(coordinates[0]),
                            '', expPath,
                            patchFilePattern)
        genotypes = monet.getGenotypes(clusters[0]['male'][0])
        aggDict = monet.autoGenerateGenotypesDictionary(groups, genotypes)
        aggList = monet.aggregateClusters(clusters, aggDict)
        monet.generateClusterGraphs(aggList, coordinates, imageLocation, colors, 0.1, 512)
        video = monet.generateVideo(vname,bgname, imageLocation, imagePattern)

video.wait()

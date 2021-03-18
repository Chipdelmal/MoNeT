
import sys
import subprocess
from datetime import datetime
import MoNeT_MGDrivE as monet

###############################################################################
# Define inputs
###############################################################################
if monet.isNotebook():
    (USR, AOI, EXP) = ('dsk', 'HLT', 'E_01_100_01')
else:
    (USR, AOI, EXP) = (sys.argv[1], sys.argv[2], sys.argv[3])
id = "{}-{}".format(EXP, AOI)
rate = 25
###############################################################################
# User select
###############################################################################
basePath = '/home/chipdelmal/Documents/WorkSims/tGD/video/tGD/video/'
###############################################################################
# Define paths
###############################################################################
outName = id
outPath = basePath + outName + '.mp4'
inPath = basePath + id + '/%04d.png'
tS = datetime.now()
monet.printExperimentHead(basePath, outPath, tS, 'tGD ffmpeg '+AOI)
###############################################################################
# Launch process
###############################################################################
sp = subprocess.Popen([
    'ffmpeg',
    '-y', 
    '-loglevel', 'quiet',
    '-start_number', '1',
    '-r', str(rate),
    '-f', 'image2',
    '-s', '1920x1080',
    '-i', inPath,
    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
    '-vcodec', 'libx264',
    '-preset', 'veryslow',
    '-crf', '15',
    # '-report',
    '-pix_fmt', 'yuv420p',
    outPath
])
sp.wait()
print("I: " + inPath +"\n" + "O: " + outPath)

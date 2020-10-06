

import sys
import subprocess
import MoNeT_MGDrivE as monet


(drive, download, pattern) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (drive, download) = ('linkedDrive', 'img')

# Experiments names (folders)
EXPS = ('000', )#'001', '005', '010', '100')
# Experiments paths
(LAB_BASE, DSK_BASE) = (
        # 'lab:/RAID5/marshallShare/tGD/fullSweep/',
        'lab:/RAID5/marshallShare/tGD/figure2/',
        '/home/chipdelmal/Documents/WorkSims/tGD/figure2/'
        # '/media/hdd/WorkExperiments/tGD/fS/',
        # '/media/hdd/WorkExperiments/tGD/figure2/'
	    # '/media/hdd/WorkExperiments/tGDMLFull/'
    )
monet.makeFolder(DSK_BASE+drive)
# Download loop
for (i, exp) in enumerate(EXPS):
    (fm, to) = [pth+drive+'/'+exp+'/' for pth in (LAB_BASE, DSK_BASE)]
    fullTo = to+download+'/'
    monet.makeFolder(to)
    monet.makeFolder(fullTo)
    if pattern == 'None':
        cmd = 'scp -rp '+fm+download+'*'+' '+fullTo
    else:
        cmd = 'scp -rp '+fm+download+'/'+pattern+' '+fullTo
    print('* Downloading {} part {}/{}... '.format(drive, i+1, len(EXPS)))
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

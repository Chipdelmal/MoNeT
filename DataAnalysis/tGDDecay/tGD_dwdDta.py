

import sys
import subprocess
import MoNeT_MGDrivE as monet


(drive, download, pattern) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (drive, download) = ('linkedDrive', 'img')

# Experiments names (folders)
EXPS = ('050', '100', '400', '800') #'001', '005', '010', '100')
# EXPS = ('000', )
# Experiments paths
(LAB_BASE, DSK_BASE) = (
        'lab:/RAID5/marshallShare/tGD/figure3/',
        '/home/chipdelmal/Documents/WorkSims/tGD/figure3/'
    )
monet.makeFolder(DSK_BASE+drive)
# Download loop
for (i, exp) in enumerate(EXPS):
    (fm, to) = [pth+drive+'/'+exp+'/' for pth in (LAB_BASE, DSK_BASE)]
    fullTo = to+download+'/'
    fullNone = to+'/'
    monet.makeFolder(to)
    monet.makeFolder(to+'img/')
    monet.makeFolder(fullTo)
    if pattern == 'None':
        cmd = 'scp -rp '+fm+download+'*'+' '+fullNone
    else:
        cmd = 'scp -rp '+fm+download+'/'+pattern+' '+fullTo
    print('* Downloading {} part {}/{}... '.format(drive, i+1, len(EXPS)))
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

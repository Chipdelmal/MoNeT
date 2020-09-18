
import sys
import subprocess
import MoNeT_MGDrivE as monet


(drive, download) = (sys.argv[1], sys.argv[2])
# (drive, download) = ('PAN', 'img')

# Experiments names (folders)
EXPS = ('mixed', 'gravidFemale', 'nonGravidFemale')
# Experiments paths
(LAB_BASE, DSK_BASE) = (
        'lab:/RAID5/marshallShare/STP/',
        '/media/hdd/WorkExperiments/STP/'
        # '/home/chipdelmal/Documents/WorkSims/STP/PAN/sim/'
    )
monet.makeFolder(DSK_BASE+drive)
# Download loop
for (i, exp) in enumerate(EXPS):
    (fm, to) = [pth + drive + '/sim/' + exp+'/' for pth in (LAB_BASE, DSK_BASE)]
    monet.makeFolder(to)
    cmd = 'scp -rp '+fm+download+' '+to
    print('* Downloading...')
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    print('Finished!')

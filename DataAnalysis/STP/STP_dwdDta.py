import sys
import subprocess
import MoNeT_MGDrivE as monet


(drive, download) = (sys.argv[1], sys.argv[2])
# (drive, download) = ('linkedDrive', 'img')

# Experiments paths
(LAB_BASE, DSK_BASE) = (
        'lab:/RAID5/marshallShare/STP/sim/',
        '/media/chipdelmal/cache/Sims/STP/sim/'
    )
monet.makeFolder(DSK_BASE+drive)
# Download loop
(fm, to) = [pth+drive+'/' for pth in (LAB_BASE, DSK_BASE)]
monet.makeFolder(to)
cmd = 'scp -rp '+fm+download+' '+to
print('* Downloading...')
print('\t'+cmd)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()
print('Finished!')

import sys
import subprocess


(drive, download, ext) = (sys.argv[1], sys.argv[2], sys.argv[3])
# (drive, download, ext) = ('linkedDrive', 'img', '*.bz2')

# Experiments names (folders)
EXPS = ('000', '001', '005', '010', '100')
# Experiments paths
LAB_BASE = 'lab:/RAID5/marshallShare/tGD/fullSweep/'
# Download loop
for (i, exp) in enumerate(EXPS):
    cmd = 'rm '+LAB_BASE+drive+'/'+exp+'/'+download+'/'+ext
    print('* Deleting {} part {}/{}... '.format(drive, i+1, len(EXPS)))
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
print('Finished!')

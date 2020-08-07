import sys
import subprocess


(drive, download) = (sys.argv[1], sys.argv[2])
# (drive, download) = ('linkedDrive', 'img')

# Experiments names (folders)
EXPS = ('000', '001', '005', '010', '100')
# Experiments paths
(LAB_BASE, DSK_BASE) = (
        'lab:/RAID5/marshallShare/tGD/fullSweep/',
        '/media/chipdelmal/cache/Sims/tGD/fS/'
    )
# Download loop
for (i, exp) in enumerate(EXPS):
    (fm, to) = [pth+drive+'/'+exp+'/' for pth in (LAB_BASE, DSK_BASE)]
    cmd = 'scp -rp '+fm+download+' '+to
    print('* Downloading {} part {}/{}... '.format(drive, i+1, len(EXPS)))
    print('\t'+cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
print('Finished!')

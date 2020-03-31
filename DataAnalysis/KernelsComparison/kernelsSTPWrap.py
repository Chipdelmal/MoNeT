
import os
import datetime
import subprocess
import k_aux as aux
import k_fun as fun


(VOL, expName) = ('RAID5', 'R12_con')
fldrsPath = '/{}/marshallShare/UCI/{}/'.format(VOL, expName)
tStr = datetime.datetime.now()
###############################################################################
# Hello Message
###############################################################################
print(aux.PAD)
fun.printExperimentHead(fldrsPath, '', '', str(tStr))
###############################################################################
# Main Cycle
###############################################################################
subfolders = [f.path for f in os.scandir(fldrsPath) if f.is_dir()]
# Launch subprocesses
sp = []
for (i, kernel) in enumerate(subfolders):
    spLst = ['python', 'kernelsSTP.py', 'RAID5', expName, kernel]
    sp.append(subprocess.Popen(spLst, shell=True, stderr=subprocess.STDOUT))
    print('Subprocess launched ({}/{})'.format(i+1, len(subfolders)), end='\r')
# Wait for the processes to finish
print('All subprocesses launched ({}). Please wait!'.format(len(subfolders)))
exit_codes = [p.wait() for p in sp]
print('* Finished!')
###############################################################################
# Goodbye Message
###############################################################################
tEnd = datetime.datetime.now()
print(aux.PADL)
print(aux.CWHT+'UCI Experiments Analysis [{}]'.format(str(tEnd-tStr))+aux.CEND)
print(aux.PAD)

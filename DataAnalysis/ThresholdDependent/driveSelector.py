import glob
import numpy as np


def driveGenesSelector(driveID):
    if (driveID == 'T' or driveID == 'U'):
        # Translocations and UDMel
        wildsList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
        homingList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
    else:
        # Wolbachia
        wildsList = [1]
        homingList = [0]
    return (wildsList, homingList)



def compileFactorialCSVFromFiles(pathFiles, outPath):
    """
    Description:
        * Takes all the CSV files from factorial experiments slots
            (starting with 'E_'), and compiles it into a flattened file. The
            file is written directly to directory.
    In:
        * path: Experiment path containing the files.
        * outFilename: (avoid the filename beginning with 'E_').
    Out:
        * NA
    Notes:
        * This function writes to HDD.
    """
    # files = os.listdir(path)
    # filenames = [
    #     path + name for name in files if fnmatch.fnmatch(name, 'E_*.csv')
    # ]
    filenames = glob.glob(pathFiles+'E_*.csv')
    f = open(outPath, 'wb')
    for file in filenames:
        fileData = np.genfromtxt(file, skip_header=1, delimiter=",")
        np.savetxt(f, fileData, fmt='%2.5f', delimiter=",")
    f.close()

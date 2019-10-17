patches = 10
folder = '/Volumes/marshallShare/vic/eRACRfact19/'
for interval in range(100, 275, 25):
    for releases in range (20,42,2):
        experiment='E_'+str(interval).zfill(4)+'_02_'+str(releases).zfill(5)
        print(experiment)
        maleFile = open(folder+experiment+'/ADM_Run001.csv', 'r')
        fileList = []
        first = next(maleFile)
        for i in range(patches):
            fileList.append(open(folder + experiment + '/ADM_Run1_Patch' + str(i).zfill(4) + '.csv', 'w'))
            fileList[i].write(first)

        for line in maleFile:
            data = line.split(',')
            currentPatch = int(data[1])
            fileList[currentPatch].write(line)
        maleFile.close()
        for i in range(patches):
            fileList[i].close()

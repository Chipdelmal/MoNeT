fileName = '/Volumes/marshallShare/ERACR/Yorkeys_MINI/mgdrive_timing_copy.txt'
result = fileName.replace('.txt', '.csv')

timingFile = open(fileName, 'r')
next(timingFile)
next(timingFile)
next(timingFile)

resultFile = open(result, 'w')
resultFile.write('Clustering, Start, End, Difference(Seconds)\n')
for line in timingFile:
    tokens = line.split()
    if tokens[0] == '##' or (len(tokens) <=1):
        continue
    elif tokens[0] == '#':
        cluster = tokens[1]
        start = int(tokens[2])
        end = int(tokens[3])
    else:
        cluster = tokens[0]
        start = int(tokens[1])
        end = int(tokens[2])
    resultFile.write('{0},{1},{2},{3}\n'.format(cluster,start,end,(end-start)))

timingFile.close()
resultFile.close()

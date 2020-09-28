import compress_pickle as pkl
import MoNeT_MGDrivE as monet


def readExperimentFilenamesV2(
    experimentPath,
    sexFilenameID={"m": ["M_"], "fS": ["FS_"], "fE": ["FE_"], "fI": ["FI_"]}
        ):

    maleFiles = []
    if 'm' in sexFilenameID:
        for i in sexFilenameID['m']:
            fileList = monet.getFileExperimentList(experimentPath, i)
            maleFiles.extend(fileList)

    femaleSFiles = []
    if 'fS' in sexFilenameID:
        for i in sexFilenameID['fS']:
            fileList = monet.getFileExperimentList(experimentPath, i)
            femaleSFiles.extend(fileList)

    femaleEFiles = []
    if 'fE' in sexFilenameID:
        for i in sexFilenameID['fE']:
            fileList = monet.getFileExperimentList(experimentPath, i)
            femaleEFiles.extend(fileList)

    femaleIFiles = []
    if 'fI' in sexFilenameID:
        for i in sexFilenameID['fI']:
            fileList = monet.getFileExperimentList(experimentPath, i)
            femaleIFiles.extend(fileList)

    filesDict = {
            "m": maleFiles,
            "fS": femaleSFiles, "fE": femaleEFiles, "fI": femaleIFiles
        }

    return filesDict


def filterFilesByIndex(
            files, ix,
            m=True, fS=True, fE=True, fI=True
        ):
    mL = [files['m'][z] for z in ix] if m else []
    fSL = [files['fS'][z] for z in ix] if fS else []
    fEL = [files['fE'][z] for z in ix] if fE else []
    fIL = [files['fI'][z] for z in ix] if fI else []
    ffiles = {'m': mL, 'fS': fSL, 'fE': fEL, 'fI': fIL}
    return ffiles


def preProcessSubLandscapeV2(
            pop, landReps, fName, drive,
            nodesAggLst, nodeAggIx,
            MF=(True, True), cmpr='bz2',
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True
        ):
    if SUM:
        sumData = monet.sumLandscapePopulationsFromFiles(pop, MF[0], MF[1])
        sumAgg = monet.aggregateGenotypesInNode(sumData, drive)
        pkl.dump(sumAgg, fName+'_sum', compression=cmpr)
    if AGG:
        aggData = monet.loadAndAggregateLandscapeData(pop, drive, MF[0], MF[1])
        pkl.dump(aggData, fName+'_agg', compression=cmpr)
    if SPA:
        geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
        pkl.dump(geneSpaTemp, fName+'_spa', compression=cmpr)
    if REP or SRP:
        fLandReps = monet.filterAggregateGarbageByIndex(
                landReps, nodesAggLst[nodeAggIx]
            )
        if REP:
            pkl.dump(fLandReps, fName+'_rep', compression=cmpr)
    if SRP:
        fRepsSum = [sum(i) for i in fLandReps['landscapes']]
        fRepsDict = {
                'genotypes': fLandReps['genotypes'],
                'landscapes': fRepsSum
            }
        pkl.dump(fRepsDict, fName+'_srp', compression=cmpr)
    return None


def preProcessLandscapeV2(
            pathMean, pathTraces, expName, drive, prePath='./',
            nodesAggLst=[[0]], analysisOI='HLT', fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True,
            sexFilenameID={"male": ["M_"], "female": ["FS_", "FE_", "FI_"]}
        ):
    dirsTraces = monet.listDirectoriesWithPathWithinAPath(pathTraces)
    files = readExperimentFilenamesV2(pathMean)
    filesList = [monet.filterFilesByIndex(files, ix) for ix in nodesAggLst]
    landReps = None
    if REP or SRP:
        landReps = monet.loadAndAggregateLandscapeDataRepetitions(
                dirsTraces, drive, MF[0], MF[1]
            )
    for (nodeAggIx, pop) in enumerate(filesList):
        fName = fNameFmt + str(nodeAggIx).zfill(nodeDigits)
        preProcessSubLandscapeV2(
                    pop, landReps, fName, drive,
                    nodesAggLst, nodeAggIx,
                    MF=MF, cmpr=cmpr,
                    SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
                )
    return None


def preProcessV2(
            exIx, expNum, expDirsMean, expDirsTrac,
            drive, analysisOI='HLT', prePath='./',
            nodesAggLst=[[0]], outExpNames={},
            fNameFmt='{}/{}-{}_', OVW=True,
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True,
            sexFilenameID={"male": ["M_"], "female": ["FS_", "FE_", "FI_"]}
        ):
    # Setup paths -------------------------------------------------------------
    strInt = str(exIx+1).zfill(len(str(expNum)))
    print('* Analyzing ({}/{})'.format(strInt, str(expNum)), end='\r')
    (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx]+'/')
    expName = pathMean.split('/')[-1]
    if not((expName in outExpNames) and (OVW)):
        fNameFmt = '{}/{}-{}_'.format(prePath, expName, analysisOI)
        preProcessLandscapeV2(
                    pathMean, pathTraces, expName, drive, prePath,
                    analysisOI=analysisOI, nodesAggLst=nodesAggLst,
                    fNameFmt=fNameFmt, MF=MF, cmpr=cmpr, nodeDigits=nodeDigits,
                    SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
                )
    return None

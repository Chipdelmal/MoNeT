import MoNeT_MGDrivE as monet

def driveSelector(DRIVE, HEALTH, pathRoot):
    if DRIVE == 1:
        (pathExt, pathO) = ("CRISPR/2019_10_04_GARBAGE/", 'CRISPR')
        if HEALTH is True:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [1, 4, 5, 6],
                    [0, 2, 3, 7, 8, 9],
                    [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]
                ]
            )
        else:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["W", "Other", "Total"],
                [
                    [0, 0, 1, 2, 3],
                    [1, 4, 4, 5, 6, 3, 6, 8, 9, 9, 5, 7, 7, 8, 2],
                    [0, 0, 1, 2, 3, 1, 4, 4, 5, 6, 3, 6, 8, 9, 9, 5, 7, 7, 8, 2]
                ]
            )
    if DRIVE == 2:
        (pathExt, pathO) = ("InundativeRelease/2019_10_04_GARBAGE/", 'IR')
        if HEALTH is True:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [1, 2],
                    [0],
                    [0, 1, 2]
                ]
            )
        else:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["W", "Other", "Total"],
                [
                    [0, 0, 1],
                    [1, 2, 2],
                    [0, 0, 1, 1, 2, 2]
                ]
            )
    if DRIVE == 3:
        (pathExt, pathO) = ("SplitDrive/2019_10_04_GARBAGE/", 'SD')
        if HEALTH is True:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26],
                    [0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18, 19, 20, 22, 23, 27, 28, 29],
                    [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26, 0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18, 19, 20, 22, 23, 27, 28, 29]
                ]
            )
        else:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["W", "Other", "Total"],
                [
                    [0, 0, 1, 2, 3, 10, 10, 11, 12, 13, 20, 20, 21, 22, 23],
                    [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26, 3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29, 2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28],
                    [0, 0, 1, 2, 3, 10, 10, 11, 12, 13, 20, 20, 21, 22, 23, 1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26, 3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29, 2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28]
                ]
            )
    if HEALTH is True:
        prepend = "H"
    else:
        prepend = "E"
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(pathRoot+pathExt)
    return [pathsRoot, aggregationDictionary, prepend, pathO]

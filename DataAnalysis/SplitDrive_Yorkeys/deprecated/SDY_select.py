import MoNeT_MGDrivE as monet


def driveSelector(DRIVE, HEALTH, pathRoot):
    if DRIVE == 1:
        (pathExt, pathO) = ("SplitDrive/2019_10_12_GARBAGE/", 'SD')
        if HEALTH is True:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "Other", "Total"],
                [
                    [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26],
                    [
                        0, 1, 2, 3, 7, 8, 9, 10, 12, 13,
                        17, 18, 19, 20, 22, 23, 27, 28, 29
                        ],
                    [
                        4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26,
                        0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18,
                        19, 20, 22, 23, 27, 28, 29
                        ]
                    ]
                )
        else:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "B", "R", "W", "C", "Total"],
                [
                    [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26],
                    [3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29],
                    [2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28],
                    [
                        0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5,
                        6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12,
                        13, 13, 14, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23
                        ],
                    [
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20,
                        21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26,
                        27, 27, 28, 28, 29, 29
                        ],
                    [
                        1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24,
                        25, 26, 3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23,
                        26, 28, 29, 29, 2, 5, 7, 7, 8, 12, 15, 17, 17,
                        18, 22, 25, 27, 27, 28, 0, 0, 0, 0, 1, 1, 1,
                        2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8,
                        9, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14,
                        15, 16, 17, 18, 19, 20, 20, 21, 22, 23, 10,
                        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20,
                        21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26,
                        27, 27, 28, 28, 29, 29
                        ]
                    ]
                )
    if HEALTH is True:
        prepend = "H"
    else:
        prepend = "E"
    if pathRoot != '':
        pathsRoot = monet.listDirectoriesWithPathWithinAPath(pathRoot+pathExt)
    else:
        pathsRoot = ''
    return [pathsRoot, aggregationDictionary, prepend, pathO]


def driveSelectorVideo(DRIVE, HEALTH, pathRoot):
    if DRIVE == 1:
        (pathExt, pathO) = ("SplitDrive/2019_10_12_GARBAGE/", 'SD')
        if HEALTH is True:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "Other"],
                [
                    [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26],
                    [
                        0, 1, 2, 3, 7, 8, 9, 10, 12, 13,
                        17, 18, 19, 20, 22, 23, 27, 28, 29
                        ]
                ])
            colors = ["#f20060A0", "#b0a9fc00"]
        else:
            aggregationDictionary = monet.generateAggregationDictionary(
                ["H", "B", "R", "W", "C"],
                [
                    [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26],
                    [3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29],
                    [2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28],
                    [
                        0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5,
                        6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12,
                        13, 13, 14, 15, 16, 17, 18, 19, 20, 20, 21, 22, 23
                        ],
                    [
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20,
                        21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26,
                        27, 27, 28, 28, 29, 29
                        ]
                    ]
                )
            colors = [
                    "#09044620", "#f2006020", "#c6d8ff20",
                    "#7692ff20", "#29339b20", "#7fff3a20"
                ]
    if HEALTH is True:
        prepend = "H"
    else:
        prepend = "E"
    if pathRoot != '':
        pathsRoot = monet.listDirectoriesWithPathWithinAPath(pathRoot+pathExt)
    else:
        pathsRoot = ''
    return [pathsRoot, aggregationDictionary, colors, pathO]

import MoNeT_MGDrivE as monet

###############################################################################
# Colors
###############################################################################
# Health ----------------------------------------------------------------------
COLHN = [
        "#09044620", "#f2006020", "#c6d8ff20",
        "#7692ff20", "#29339b20", "#7fff3a20"
    ]
COLHO = [i[:-2]+'FF' for i in COLHN]
COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
# Ecology ---------------------------------------------------------------------
COLEN = [
        "#09044620", "#f2006020", "#c6d8ff20",
        "#7692ff20", "#29339b20", "#7fff3a20"
    ]
COLEO = [i[:-2]+'FF' for i in COLEN]
COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)
###############################################################################
# Gene-Dictionaries
###############################################################################
# Linked Drive Replacement ----------------------------------------------------
drive_LDR = {
        'id': 'Replacement', 'folder': 'LDR', 'loc': 1,
        'HLT': {
            'gDict': monet.generateAggregationDictionary(
                    ["H", "Other", "Total"],
                    [
                        [1, 4, 5, 6],
                        [0, 2, 3, 7, 8, 9],
                        [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]
                    ]
                ),
            'color': [COLHN, COLHO, COLHM]
        },
        'ECO': {
            'gDict': monet.generateAggregationDictionary(
                    ["H", "B", "R", "W", "Total"],
                    [
                        [1, 4, 4, 5, 6],
                        [3, 6, 8, 9, 9],
                        [2, 5, 7, 7, 8],
                        [0, 0, 1, 2, 3],
                        [
                            1, 4, 4, 5, 6, 3, 6, 8, 9, 9,
                            2, 5, 7, 7, 8, 0, 0, 1, 2, 3
                        ]
                    ]
                ),
            'color': [COLEN, COLEO, COLEM]
        }
    }
# Linked Drive Suppression ----------------------------------------------------
drive_LDS = {
        'id': 'LDS', 'folder': 'LDS', 'loc': 1,
        'HLT': {
            'gDict': monet.generateAggregationDictionary(
                    ["H", "Other", "Total"],
                    [
                        [1, 4, 5, 6],
                        [0, 2, 3, 7, 8, 9],
                        [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]
                    ]
                ),
            'color': [COLHN, COLHO, COLHM]
        },
        'ECO': {
            'gDict': monet.generateAggregationDictionary(
                    ["H", "B", "R", "W", "Total"],
                    [
                        [1, 4, 4, 5, 6],
                        [3, 6, 8, 9, 9],
                        [2, 5, 7, 7, 8],
                        [0, 0, 1, 2, 3],
                        [
                            1, 4, 4, 5, 6, 3, 6, 8, 9, 9,
                            2, 5, 7, 7, 8, 0, 0, 1, 2, 3
                        ]
                    ]
                ),
            'color': [COLEN, COLEO, COLEM]
        }
    }


# Selector --------------------------------------------------------------------
def driveSelector(dID):
    drive = drive_LDR
    if dID == 'LDS':
        drive = drive_LDS
    return drive

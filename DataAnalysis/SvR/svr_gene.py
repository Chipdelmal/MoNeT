import MoNeT_MGDrivE as monet

###############################################################################
# Colors
###############################################################################
# Health ----------------------------------------------------------------------
COLHN = [
        "#f2006020", "#c6d8ff20", "#09044620"
    ]
COLHO = [i[:-2]+'FF' for i in COLHN]
COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
# Ecology ---------------------------------------------------------------------
COLEN = [
        "#ff004d10", "#FFFB2810", "#66FF0010",
        "#c6d8ff10", "#09044610", "#7fff3a10"
    ]
COLEO = [i[:-2]+'FF' for i in COLEN]
COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)
###############################################################################
# Gene-Dictionaries
###############################################################################
# Linked Drive Replacement ----------------------------------------------------
# 0: WW, 1: WH, 2: WR, 3: WB, 4: HH,
# 5: HR, 6: HB, 7: RR, 8: RB, 9: BB
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
                            0, 0, 1, 1, 2, 2, 3, 3, 4, 4,
                            5, 5, 6, 6, 7, 7, 8, 8, 9, 9
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
                        [1, 4, 5, 6, 0, 2, 3, 7, 8, 9]
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

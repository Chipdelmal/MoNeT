import MoNeT_MGDrivE as monet
import tGD_gene_tGD as gtGd
import tGD_gene_linked as gld


def driveSelector(DRIVE, TYPE):
    # Linked Drive ------------------------------------------------------------
    if DRIVE == 'linkedDrive':
        if TYPE == 'ECO':
            aggregationDictionary = monet.generateAggregationDictionary(
                    ["W", "H", "R", "B"], gld.ld_ECO
                )
            yRange = 11000
        elif TYPE == 'HLT':
            aggregationDictionary = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gld.ld_HLT
                )
            yRange = 11000
    # Split Drive -------------------------------------------------------------
    if DRIVE == 'splitDrive':
        if TYPE == 'ECO':
            aggregationDictionary = monet.generateAggregationDictionary(
                    ["W", "H", "R", "B", "Y"],
                    [
                        [0, 0, 1, 2, 3, 4, 4, 8, 11, 13],
                        [1, 5, 5, 6, 7, 8],
                        [2, 6, 9, 9, 10, 11],
                        [3, 7, 10, 12, 12, 13],
                        []
                    ]
                )
            yRange = 11000
        elif TYPE == 'HLT':
            aggregationDictionary = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"],
                    [
                        [0, 0, 1, 2, 3, 4, 4, 8, 11, 13],
                        [1, 5, 5, 6, 7, 8],
                        [2, 6, 9, 9, 10, 11],
                        [3, 7, 10, 12, 12, 13],
                        []
                    ]
                )
            yRange = 11000
    # tGD Drive ---------------------------------------------------------------
    if DRIVE == 'tGD':
        if TYPE == 'ECO':
            aggregationDictionary = monet.generateAggregationDictionary(
                    ["WA+WB", "H", "RA", "RB", "G"], gtGd.tGD_ECO
                )
            yRange = 11000
        elif TYPE == 'HLT':
            aggregationDictionary = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gtGd.tGD_HLT
                )
            yRange = 11000
    return {'gDict': aggregationDictionary, 'yRange': yRange}


driveSelector('tGD')

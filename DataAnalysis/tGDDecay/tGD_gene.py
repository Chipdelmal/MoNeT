
import tGD_gene_tGD as gtGd
import tGD_gene_split as gsd
import tGD_gene_linked as gld
import MoNeT_MGDrivE as monet


def driveSelector(DRIVE, TYPE):
    ###########################################################################
    # Linked Drive
    ###########################################################################
    if DRIVE == 'linkedDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(["W", "H", "R", "B"], gld.LD_ECO)
            yRange = 11000
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(["H*", "O-", "Total"], gld.LD_HLT)
            yRange = 11000
    ###########################################################################
    # Split Drive
    ###########################################################################
    if DRIVE == 'splitDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(["W", "H", "R", "B", "Y"], gsd.SD_ECO)
            yRange = 11000
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(["H*", "O-", "Total"], gsd.SD_HLT)
            yRange = 11000
    ###########################################################################
    # tGD Drive
    ###########################################################################
    if DRIVE == 'tGD':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(["WA+WB", "H", "RA", "RB", "G"], gtGd.TGD_ECO)
            yRange = 11000
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(["H*", "O-", "Total"], gtGd.TGD_HLT)
            yRange = 11000
    ###########################################################################
    # Return values
    ###########################################################################
    return {'gDict': aggD, 'yRange': yRange}

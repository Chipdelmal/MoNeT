
import tGD_gene_tGD as gtGd
import tGD_gene_split as gsd
import tGD_gene_linked as gld
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
###############################################################################
# Ecology ---------------------------------------------------------------------
COLEN = [
        "#2614ed", "#FF006E", "#45d40c",
        "#8338EC", "#1888e3", "#0003ff"
    ]
COLEN = [c+'2A' for c in COLEN]
COLEO = [i[:-2]+'FF' for i in COLEN]
COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)
# Health ----------------------------------------------------------------------
COLHN = ["#FF006E", "#8338EC", "#0C4887"]
COLHN = [c+'2A' for c in COLHN]
COLHO = [i[:-2]+'FF' for i in COLHN]
COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
###############################################################################
# Drive
###############################################################################


def driveSelector(DRIVE, TYPE):
    # Linked Drive -###########################################################
    if DRIVE == 'linkedDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["W", "H", "R", "B"], gld.LD_ECO
                )
            yRange = 11000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gld.LD_HLT
                )
            yRange = 11000/2
            colors = COLHN
    # Split Drive #############################################################
    if DRIVE == 'splitDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["W", "H", "R", "B", "C"], gsd.SD_ECO
                )
            yRange = 21000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gsd.SD_HLT
                )
            yRange = 11000/2
            colors = COLHN
    # tGD Drive ###############################################################
    if DRIVE == 'tGD':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA+WB", "H", "RA", "RB", "G"], gtGd.TGD_ECO
                )
            yRange = 21000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gtGd.TGD_HLT
                )
            yRange = 11000/2
            colors = COLHN
    # Return values ###########################################################
    return {'gDict': aggD, 'yRange': yRange, 'colors': colors}


import sys

sys.path.append('C:/Users/prisc/Documents/GitHub/MoNeT2/DataAnalysis/tGDDecay/')
import tGD_gene_tGD as gtgd
import tGD_gene_split as gsd
import tGD_gene_linked as gld
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
###############################################################################
# Ecology ---------------------------------------------------------------------
COLEN = [
        "#2614ed", "#FF006E", "#45d40c",
        "#8338EC", "#1888e3", "#BC1097"
    ]
COLEN = [c+'1A' for c in COLEN]
COLEO = [i[:-2]+'FF' for i in COLEN]
COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)
# Health ----------------------------------------------------------------------
COLHN = ["#FF006E", "#8338EC", "#0C4887"]
COLHN = [c+'1A' for c in COLHN]
COLHO = [i[:-2]+'FF' for i in COLHN]
COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
# Trash ----------------------------------------------------------------------
COLTN = ["#00a2fe", "#8338EC", "#0C4887"]
COLTN = [c+'1A' for c in COLTN]
COLTO = [i[:-2]+'FF' for i in COLTN]
COLTM = monet.generateAlphaColorMapFromColorArray(COLTO)
###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE):
    # Linked Drive -###########################################################
    # aggD = 0
    # yRange = 0
    # colors = 0
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
        elif TYPE == 'TRS':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gld.LD_HLT
                )
            yRange = 11000/2
            colors = COLTN
    # Split Drive #############################################################
    if DRIVE == 'splitDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA", "H", "R", "B", "C", "WB"], gsd.SD_ECO
                )
            yRange = 11000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gsd.SD_HLT
                )
            yRange = 11000/2
            colors = COLHN
        elif TYPE == 'TRS':
            aggD = monet.generateAggregationDictionary(
                    ["C*", "O-", "Total"], gsd.SD_TRS
                )
            yRange = 11000/2
            colors = COLTN
    # tGD Drive ###############################################################
    if DRIVE == 'tGD':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA", "H", "RA", "RB", "G", "WB"], gtgd.TGD_ECO
                )
            yRange = 11000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gtgd.TGD_HLT
                )
            yRange = 11000/2
            colors = COLHN
        elif TYPE == 'TRS':
            aggD = monet.generateAggregationDictionary(
                    ["G*", "O-", "Total"], gtgd.TGD_TRS
                )
            yRange = 11000/2
            colors = COLTN
    # Return values ###########################################################

    return {'gDict': aggD, 'yRange': yRange, 'colors': colors}

# test = driveSelector('tGD', 'HLT')
# print(test)

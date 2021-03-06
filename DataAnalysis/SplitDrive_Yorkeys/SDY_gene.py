
import SDY_gene_split as gsd
import SDY_aux as aux
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
COLTN = ["#00a2fe", "#8337ec", "#0C4887"]
COLTN = [c+'1A' for c in COLTN]
COLTO = [i[:-2]+'FF' for i in COLTN]
COLTM = monet.generateAlphaColorMapFromColorArray(COLTO)
# Wild ----------------------------------------------------------------------
COLWN = ["#04df06", "#8337ec", "#0C4887"]
COLWN = [c+'1A' for c in COLWN]
COLWO = [i[:-2]+'FF' for i in COLWN]
COLWM = monet.generateAlphaColorMapFromColorArray(COLWO)


###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE):
    # Split Drive #############################################################
    if DRIVE == 'SD':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA", "H", "R", "B", "C", "WB"], gsd.SD_ECO
                )
            yRange = 12500 * 2
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gsd.SD_HLT
                )
            yRange = 12500
            colors = COLHN
        elif TYPE == 'TRS':
            aggD = monet.generateAggregationDictionary(
                    ["C*", "O-", "Total"], gsd.SD_TRS
                )
            yRange = 12500
            colors = COLTN
        elif TYPE == 'WLD':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], gsd.SD_WLD
                )
            yRange = 12500
            colors = COLWN
    # Return values ###########################################################
    return {'gDict': aggD, 'yRange': yRange, 'colors': colors}

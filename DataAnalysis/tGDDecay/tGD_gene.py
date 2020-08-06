
import tGD_gene_tGD as gtGd
import tGD_gene_split as gsd
import tGD_gene_linked as gld
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
###############################################################################
# Health ----------------------------------------------------------------------
COLHN = ["#FF006E0A", "#8338EC0A", "#0C48870A"]
COLHO = [i[:-2]+'FF' for i in COLHN]
COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
# Ecology ---------------------------------------------------------------------
COLEN = [
        "#ff004d0A", "#C7FF030A", "#66FF000A",
        "#8338EC0A", "#0904460A", "#7fff3a0A"
    ]
COLEO = [i[:-2]+'FF' for i in COLEN]
COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)


###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE):
    # Linked Drive -###########################################################
    if DRIVE == 'linkedDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(["W", "H", "R", "B"], gld.LD_ECO)
            yRange = 11000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(["H*", "O-", "Total"], gld.LD_HLT)
            yRange = 11000/2
            colors = COLHN
    # Split Drive #############################################################
    if DRIVE == 'splitDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(["W", "H", "R", "B", "C"], gsd.SD_ECO)
            yRange = 11000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(["H*", "O-", "Total"], gsd.SD_HLT)
            yRange = 11000/2
            colors = COLHN
    # tGD Drive ###############################################################
    if DRIVE == 'tGD':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(["WA+WB", "H", "RA", "RB", "G"], gtGd.TGD_ECO)
            yRange = 11000
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(["H*", "O-", "Total"], gtGd.TGD_HLT)
            yRange = 11000/2
            colors = COLHN
    # Return values ###########################################################
    return {'gDict': aggD, 'yRange': yRange, 'colors': colors}

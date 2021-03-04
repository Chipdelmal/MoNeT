
import tGD_gene_tGD as gtgd
import tGD_gene_split as gsd
import tGD_gene_linked as gld
import tGD_gene_clvr as clv
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
COLTN = ["#0eeb10", "#8337ec", "#0C4887"]
COLTN = [c+'1A' for c in COLTN]
COLTO = [i[:-2]+'FF' for i in COLTN]
COLTM = monet.generateAlphaColorMapFromColorArray(COLTO)
# Wild ----------------------------------------------------------------------
COLWN = ["#8337ec", "#00a2fe", "#0C4887"]
COLWN = [c+'1A' for c in COLWN]
COLWO = [i[:-2]+'FF' for i in COLWN]
COLWM = monet.generateAlphaColorMapFromColorArray(COLWO)
# CLS ----------------------------------------------------------------------
COLCN = ["#0eeb10", "#FF006E", "#ffffff"]
COLCN = [c+'AA' for c in COLCN]
COLCO = [i[:-2]+'FF' for i in COLCN]
COLCM = monet.generateAlphaColorMapFromColorArray(COLCO)


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
            yRange = 11000*2
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gld.LD_HLT
                )
            yRange = 11000/2
            colors = COLHN
        elif TYPE == 'TRS':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], gld.LD_TRS
                )
            yRange = 11000
            colors = COLTN
        elif TYPE == 'WLD':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], gld.LD_WLD
                )
            yRange = 11000
            colors = COLWN
        elif TYPE == 'CST':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], gld.LD_CST
                )
            yRange = 11000
            colors = COLCN
    # Split Drive #############################################################
    if DRIVE == 'splitDrive':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA", "H", "R", "B", "C", "WB"], gsd.SD_ECO
                )
            yRange = 11000*2
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
            yRange = 11000
            colors = COLTN
        elif TYPE == 'WLD':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], gsd.SD_WLD
                )
            yRange = 11000
            colors = COLWN
        elif TYPE == 'CST':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], gsd.SD_CST
                )
            yRange = 11000
            colors = COLCN
    # tGD Drive ###############################################################
    if DRIVE == 'tGD':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA", "H", "RA", "RB", "G", "WB"], gtgd.TGD_ECO
                )
            yRange = 11000*2
            colors = COLEN
        elif TYPE == 'CAS':
            aggD = monet.generateAggregationDictionary(
                    ["W", "H", "R", "B", "Total"], gtgd.TGD_CAS
                )
            yRange = 11000
            colors = ['#8338ec1A', '#45d40c1A', '#1888e31A', '#bc10971A', '#0C48871A']
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
            yRange = 11000
            colors = COLTN
        elif TYPE == 'WLD':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], gtgd.TGD_WLD
                )
            yRange = 11000
            colors = COLWN
        elif TYPE == 'CST':
            aggD = monet.generateAggregationDictionary(
                    ["C", "G", "Total"], gtgd.TGD_CST
                )
            yRange = 11000
            colors = COLCN
    # ClvR Drive ###############################################################
    if DRIVE == 'ClvR':
        if TYPE == 'ECO':
            aggD = monet.generateAggregationDictionary(
                    ["WA", "H", "RA", "RB", "G", "WB"], clv.TGD_ECO
                )
            yRange = 11000*2
            colors = COLEN
        elif TYPE == 'HLT':
            aggD = monet.generateAggregationDictionary(
                    ["H*", "O-", "Total"], clv.TGD_HLT
                )
            yRange = 11000/2
            colors = COLHN
        elif TYPE == 'TRS':
            aggD = monet.generateAggregationDictionary(
                    ["G*", "O-", "Total"], clv.TGD_TRS
                )
            yRange = 11000
            colors = COLTN
        elif TYPE == 'WLD':
            aggD = monet.generateAggregationDictionary(
                    ["O-", "W*", "Total"], clv.TGD_WLD
                )
            yRange = 11000
            colors = COLWN
        elif TYPE == 'CST':
            aggD = monet.generateAggregationDictionary(
                    ["C", "G", "Total"], clv.TGD_CST
                )
            yRange = 11000
            colors = COLCN
    # Return values ###########################################################
    return {'gDict': aggD, 'yRange': yRange, 'colors': colors}

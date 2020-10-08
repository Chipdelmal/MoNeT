
import MoNeT_MGDrivE as monet


genotypes = [
        'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR', 'WWRB',
        'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR', 'WCHB', 'WCRR',
        'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB', 'CCHH', 'CCHR', 'CCHB',
        'CCRR', 'CCRB', 'CCBB'
    ]
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
# WA --------------------------------------------------------------------------
wAGenes = (('W', (0, 1)), )
wAPos = monet.aggregateGeneAppearances(genotypes, wAGenes)
# H ---------------------------------------------------------------------------
hGenes = (('H', allGeneIx), )
hPos = monet.aggregateGeneAppearances(genotypes, hGenes)
# RA --------------------------------------------------------------------------
rGenes = (('R', allGeneIx), )
rPos = monet.aggregateGeneAppearances(genotypes, rGenes)
# RB --------------------------------------------------------------------------
bGenes = (('B', allGeneIx), )
bPos = monet.aggregateGeneAppearances(genotypes, bGenes)
# G ---------------------------------------------------------------------------
cGenes = (('C', allGeneIx), )
cPos = monet.aggregateGeneAppearances(genotypes, cGenes)
# WB --------------------------------------------------------------------------
wBGenes = (('W', (2, 3)), )
wBPos = monet.aggregateGeneAppearances(genotypes, wBGenes)
# Full set --------------------------------------------------------------------
SD_ECO = (wAPos, hPos, rPos, bPos, cPos, wBPos)

###############################################################################
# Health genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', allGeneIx), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', allGeneIx), ('R', allGeneIx), ('B', allGeneIx), ('C', allGeneIx))
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('C', allGeneIx), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', allGeneIx), ('R', allGeneIx), ('B', allGeneIx), ('H', allGeneIx))
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', allGeneIx), ('R', allGeneIx), ('B', allGeneIx), ('C', allGeneIx))
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', allGeneIx), )
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_WLD = [list(i) for i in (hPos - wPos, wPos, wPos | hPos)]

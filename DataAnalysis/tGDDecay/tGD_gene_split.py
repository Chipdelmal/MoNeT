
import tGD_aux as aux


genotypes = (
    'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR', 'WWRB',
    'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR', 'WCHB', 'WCRR',
    'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB', 'CCHH', 'CCHR', 'CCHB',
    'CCRR', 'CCRB', 'CCBB'
)
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
# WA --------------------------------------------------------------------------
wAGenes = (('W', (0, 1)), )
wAPos = aux.aggregateGeneAppearances(genotypes, wAGenes)
# H ---------------------------------------------------------------------------
hGenes = (('H', allGeneIx), )
hPos = aux.aggregateGeneAppearances(genotypes, hGenes)
# RA --------------------------------------------------------------------------
rGenes = (('R', allGeneIx), )
rPos = aux.aggregateGeneAppearances(genotypes, rGenes)
# RB --------------------------------------------------------------------------
bGenes = (('B', allGeneIx), )
bPos = aux.aggregateGeneAppearances(genotypes, bGenes)
# G ---------------------------------------------------------------------------
cGenes = (('C', allGeneIx), )
cPos = aux.aggregateGeneAppearances(genotypes, cGenes)
# WB --------------------------------------------------------------------------
wBGenes = (('W', (2, 3)), )
wBPos = aux.aggregateGeneAppearances(genotypes, wBGenes)
# Full set --------------------------------------------------------------------
SD_ECO = (wAPos, hPos, rPos, bPos, cPos, wBPos)

###############################################################################
# Health genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', (2, 3)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (2, 3)), ('R', (2, 3)), ('B', (2, 3)), ('C', (2, 3)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('C', (0, 1)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 1)), ('R', (0, 1)), ('B', (0, 1)), ('H', (0, 1)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', (0, 1)), ('R', (0, 1)), ('B', (0, 1)), ('C', (0, 1)))
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 1)), )
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_WLD = [list(i) for i in (hPos - wPos, wPos, wPos | hPos)]

###############################################################################
# Custom genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('C', (0, 1)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('H', (2, 3)), )
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_CST = [list(i) for i in (hPos - wPos, wPos, wPos | hPos)]
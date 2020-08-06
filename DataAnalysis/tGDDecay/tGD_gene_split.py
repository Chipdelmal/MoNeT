
import tGD_aux as aux


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
hGenes = (('H', allGeneIx), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', allGeneIx), ('R', allGeneIx), ('B', allGeneIx), ('C', allGeneIx))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Trash genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('C', allGeneIx), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', allGeneIx), ('R', allGeneIx), ('B', allGeneIx), ('H', allGeneIx))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
SD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

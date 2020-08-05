
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
# W ---------------------------------------------------------------------------
wGenes = (('W', allGeneIx), )
wPos = aux.aggregateGeneAppearances(genotypes, wGenes)
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
# Full set --------------------------------------------------------------------
SD_ECO = (wPos, hPos, rPos, bPos, cPos)

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
SD_HLT = (hPos, wPos - hPos, wPos | hPos)


import tGD_aux as aux


genotypes = [
        'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR', 'WWRB',
        'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR', 'WCHB', 'WCRR',
        'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB', 'CCHH', 'CCHR', 'CCHB',
        'CCRR', 'CCRB', 'CCBB'
    ]


###############################################################################
# Ecology genotype counts
###############################################################################
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 2)), ('W', (1, 3)))
wPos = aux.aggregateGeneAppearances(genotypes, wGenes)
# H ---------------------------------------------------------------------------
hGenes = (('P', (0, 2)), ('M', (0, 2)))
hPos = aux.aggregateGeneAppearances(genotypes, hGenes)
# RA --------------------------------------------------------------------------
rAGenes = (('R', (0, 2)), ('B', (0, 2)))
rAPos = aux.aggregateGeneAppearances(genotypes, rAGenes)
# RB --------------------------------------------------------------------------
rBGenes = (('R', (1, 3)), ('B', (1, 3)))
rBPos = aux.aggregateGeneAppearances(genotypes, rBGenes)
# G ---------------------------------------------------------------------------
gGenes = (('G', (1, 3)), )
gPos = aux.aggregateGeneAppearances(genotypes, gGenes)
# Full set --------------------------------------------------------------------
sd_ECO = (wPos, hPos, rAPos, rBPos, gPos)


###############################################################################
# Health genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('P', (0, 2)), ('M', (0, 2)))
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 2)), ('R', (0, 2)), ('B', (0, 2)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
sd_HLT = (hPos, wPos - hPos, wPos | hPos)

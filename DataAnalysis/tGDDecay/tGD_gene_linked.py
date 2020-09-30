
import tGD_aux as aux


genotypes = ['WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB']
allGeneIx = range(len(genotypes))

###############################################################################
# Ecology genotype counts
###############################################################################
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 1)), )
wPos = aux.aggregateGeneAppearances(genotypes, wGenes)
# H ---------------------------------------------------------------------------
hGenes = (('H', (0, 1)), )
hPos = aux.aggregateGeneAppearances(genotypes, hGenes)
# RA --------------------------------------------------------------------------
rGenes = (('R', (0, 1)), )
rPos = aux.aggregateGeneAppearances(genotypes, rGenes)
# RB --------------------------------------------------------------------------
bGenes = (('B', (0, 1)), )
bPos = aux.aggregateGeneAppearances(genotypes, bGenes)
# Full set --------------------------------------------------------------------
LD_ECO = (wPos, hPos, rPos, bPos)

###############################################################################
# Health genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', (0, 1)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 1)), ('R', (0, 1)), ('B', (0, 1)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
LD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', (0, 1)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 1)), ('R', (0, 1)), ('B', (0, 1)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
LD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('H', (0, 1)), ('R', (0, 1)), ('B', (0, 1)))
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 1)), )
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
LD_WLD = [list(i) for i in (hPos - wPos, wPos, wPos | hPos)]

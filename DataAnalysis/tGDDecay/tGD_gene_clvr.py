import tGD_aux as aux

genotypes = (
    'WWWWWW', 'WWWWRW', 'WWWWBW', 'WWWWRR', 'WWWWBR', 'WWWWBB',
    'CWWWWW', 'CWWWRW', 'CWWWBW', 'CWWWRR', 'CWWWBR', 'CWWWBB',
    'WGWWWW', 'WGWWRW', 'WGWWBW', 'WGWWRR', 'WGWWBR', 'WGWWBB',
    'CGWWWW', 'CGWWRW', 'CGWWBW', 'CGWWRR', 'CGWWBR', 'CGWWBB',
    'CWCWWW', 'CWCWRW', 'CWCWBW', 'CWCWRR', 'CWCWBR', 'CWCWBB',
    'CWWGWW', 'CWWGRW', 'CWWGBW', 'CWWGRR', 'CWWGBR', 'CWWGBB',
    'CGCWWW', 'CGCWRW', 'CGCWBW', 'CGCWRR', 'CGCWBR', 'CGCWBB',
    'WGWGWW', 'WGWGRW', 'WGWGBW', 'WGWGRR', 'WGWGBR', 'WGWGBB',
    'CGWGWW', 'CGWGRW', 'CGWGBW', 'CGWGRR', 'CGWGBR', 'CGWGBB',
    'CGCGWW', 'CGCGRW', 'CGCGBW', 'CGCGRR', 'CGCGBR', 'CGCGBB'
)

###############################################################################
# Ecology genotype counts
###############################################################################
# WA --------------------------------------------------------------------------
wAGenes = (('W', (0, 2)), )
wAPos = aux.aggregateGeneAppearances(genotypes, wAGenes)
# H ---------------------------------------------------------------------------
hGenes = (('G', (1, 3)), )
hPos = aux.aggregateGeneAppearances(genotypes, hGenes)
# RA --------------------------------------------------------------------------
rAGenes = (('R', (0, 2)), ('B', (0, 2)))
rAPos = aux.aggregateGeneAppearances(genotypes, rAGenes)
# RB --------------------------------------------------------------------------
rBGenes = (('R', (1, 3)), ('B', (1, 3)))
rBPos = aux.aggregateGeneAppearances(genotypes, rBGenes)
# G ---------------------------------------------------------------------------
gGenes = (('C', (0, 2)), )
gPos = aux.aggregateGeneAppearances(genotypes, gGenes)
# WB --------------------------------------------------------------------------
wBGenes = (('W', (1, 3)), )
wBPos = aux.aggregateGeneAppearances(genotypes, wBGenes)
# Full set --------------------------------------------------------------------
TGD_ECO = (wAPos, hPos, rAPos, rBPos, gPos, wBPos)


###############################################################################
# Health genotype counts
###############################################################################
# H* --------------------------------------------------------------------------
hGenes = (('G', (1, 3)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# O- --------------------------------------------------------------------------
wGenes = (('W', (1, 3)), ('R', (1, 3)), ('B', (1, 3)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
TGD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Trash genotype counts
###############################################################################
# C* --------------------------------------------------------------------------
hGenes = (('C', (0, 2)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# O* --------------------------------------------------------------------------
wGenes = (('W', (0, 2)), ('R', (0, 2)), ('B', (0, 2)))
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
TGD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Wild genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('C', (0, 2)), ('R', (0, 2)), ('B', (0, 2)))
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W* --------------------------------------------------------------------------
wGenes = (('W', (0, 2)), )
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
TGD_WLD = [list(i) for i in (hPos - wPos, wPos, hPos | wPos)]


###############################################################################
# Custom genotype counts
###############################################################################
# H ---------------------------------------------------------------------------
hGenes = (('C', (0, 2)), )
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W* --------------------------------------------------------------------------
wGenes = (('G', (1, 3)), )
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
TGD_CST = [list(i) for i in (hPos - wPos, wPos, hPos | wPos)]

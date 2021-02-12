
import tGD_aux as aux


genotypes = (
    "WWWW", "PWWW", "MWWW", "RWWW", "BWWW", "WGWW", "PGWW", "MGWW", "RGWW",
    "BGWW", "WRWW", "PRWW", "MRWW", "RRWW", "BRWW", "WBWW", "PBWW", "MBWW",
    "RBWW", "BBWW", "PWPW", "MWPW", "PWRW", "BWPW", "PWWG", "PGPW", "MGPW",
    "PWRG", "BGPW", "PWWR", "PRPW", "MRPW", "PWRR", "BRPW", "PWWB", "PBPW",
    "MBPW", "PWRB", "BBPW", "MWMW", "MWRW", "BWMW", "MWWG", "MWPG", "MGMW",
    "MWRG", "BGMW", "MWWR", "MWPR", "MRMW", "MWRR", "BRMW", "MWWB", "MWPB",
    "MBMW", "MWRB", "BBMW", "RWRW", "BWRW", "RWWG", "PGRW", "MGRW", "RGRW",
    "BGRW", "RWWR", "PRRW", "MRRW", "RRRW", "BRRW", "RWWB", "PBRW", "MBRW",
    "RBRW", "BBRW", "BWBW", "BWWG", "BWPG", "BWMG", "BWRG", "BGBW", "BWWR",
    "BWPR", "BWMR", "BWRR", "BRBW", "BWWB", "BWPB", "BWMB", "BWRB", "BBBW",
    "WGWG", "PGWG", "MGWG", "RGWG", "BGWG", "WGWR", "PRWG", "MRWG", "RRWG",
    "BRWG", "WBWG", "PBWG", "MBWG", "RBWG", "BBWG", "PGPG", "MGPG", "PGRG",
    "BGPG", "PGWR", "PGPR", "MRPG", "PGRR", "BRPG", "PGWB", "PBPG", "MBPG",
    "PGRB", "BBPG", "MGMG", "MGRG", "BGMG", "MGWR", "MGPR", "MGMR", "MGRR",
    "BRMG", "MGWB", "MGPB", "MBMG", "MGRB", "BBMG", "RGRG", "BGRG", "RGWR",
    "PRRG", "MRRG", "RGRR", "BRRG", "RGWB", "PBRG", "MBRG", "RBRG", "BBRG",
    "BGBG", "BGWR", "BGPR", "BGMR", "BGRR", "BGBR", "BGWB", "BGPB", "BGMB",
    "BGRB", "BBBG", "WRWR", "PRWR", "MRWR", "RRWR", "BRWR", "WBWR", "PBWR",
    "MBWR", "RBWR", "BBWR", "PRPR", "MRPR", "PRRR", "BRPR", "PRWB", "PBPR",
    "MBPR", "PRRB", "BBPR", "MRMR", "MRRR", "BRMR", "MRWB", "MRPB", "MBMR",
    "MRRB", "BBMR", "RRRR", "BRRR", "RRWB", "PBRR", "MBRR", "RBRR", "BBRR",
    "BRBR", "BRWB", "BRPB", "BRMB", "BRRB", "BBBR", "WBWB", "PBWB", "MBWB",
    "RBWB", "BBWB", "PBPB", "MBPB", "PBRB", "BBPB", "MBMB", "MBRB", "BBMB",
    "RBRB", "BBRB", "BBBB"
)


###############################################################################
# Ecology genotype counts
###############################################################################
# WA --------------------------------------------------------------------------
wAGenes = (('W', (0, 2)), )
wAPos = aux.aggregateGeneAppearances(genotypes, wAGenes)
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
# WB --------------------------------------------------------------------------
wBGenes = (('W', (1, 3)), )
wBPos = aux.aggregateGeneAppearances(genotypes, wBGenes)
# Full set --------------------------------------------------------------------
TGD_ECO = (wAPos, hPos, rAPos, rBPos, gPos, wBPos)

###############################################################################
# Cas genotype counts
###############################################################################
# WA --------------------------------------------------------------------------
wAGenes = (('W', (0, 2)), )
wAPos = set(aux.aggregateGeneAppearances(genotypes, wAGenes))
# H ---------------------------------------------------------------------------
hGenes = (('P', (0, 2)), ('M', (0, 2)))
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# RA --------------------------------------------------------------------------
rAGenes = (('R', (0, 2)), )
rAPos = set(aux.aggregateGeneAppearances(genotypes, rAGenes))
# BA --------------------------------------------------------------------------
bAGenes = (('B', (0, 2)), )
bAPos = set(aux.aggregateGeneAppearances(genotypes, bAGenes))
# Full set --------------------------------------------------------------------
TGD_CAS = [list(i) for i in (wAPos, hPos, rAPos, bAPos, wAPos | hPos | rAPos | bAPos)]


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
hGenes = (('P', (0, 2)), ('M', (0, 2)))
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
hGenes = (('P', (0, 2)), ('M', (0, 2)), ('R', (0, 2)), ('B', (0, 2)))
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
hGenes = (('P', (0, 2)), ('M', (0, 2)))
hPos = set(aux.aggregateGeneAppearances(genotypes, hGenes))
# W* --------------------------------------------------------------------------
wGenes = (('G', (1, 3)), )
wPos = set(aux.aggregateGeneAppearances(genotypes, wGenes))
# Full set --------------------------------------------------------------------
TGD_CST = [list(i) for i in (hPos - wPos, wPos, hPos | wPos)]

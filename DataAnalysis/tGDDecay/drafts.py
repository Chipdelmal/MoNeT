import re


def countGeneAppearances(genotypes, gene, pos):
    # Split genotypes
    splitGenotypes = [list(genes) for genes in genotypes]
    # Count
    appearances = []
    for p in pos:
        slot = [gene[p] for gene in splitGenotypes]
        matches = re.finditer(gene, ''.join(slot))
        appearances.extend([match.start() for match in matches])
    appearances.sort()
    return appearances


flatten = lambda l: [item for sublist in l for item in sublist]


def aggregateGeneAppearances(genotypes, genes):
    gcnt = [countGeneAppearances(genotypes, gn[0], gn[1]) for gn in genes]
    return sorted(flatten(gcnt))



genotypes = ["WWWW","PWWW","MWWW","RWWW","BWWW","WGWW","PGWW","MGWW","RGWW",
                 "BGWW","WRWW","PRWW","MRWW","RRWW","BRWW","WBWW","PBWW","MBWW",
                 "RBWW","BBWW","PWPW","MWPW","PWRW","BWPW","PWWG","PGPW","MGPW",
                 "PWRG","BGPW","PWWR","PRPW","MRPW","PWRR","BRPW","PWWB","PBPW",
                 "MBPW","PWRB","BBPW","MWMW","MWRW","BWMW","MWWG","MWPG","MGMW",
                 "MWRG","BGMW","MWWR","MWPR","MRMW","MWRR","BRMW","MWWB","MWPB",
                 "MBMW","MWRB","BBMW","RWRW","BWRW","RWWG","PGRW","MGRW","RGRW",
                 "BGRW","RWWR","PRRW","MRRW","RRRW","BRRW","RWWB","PBRW","MBRW",
                 "RBRW","BBRW","BWBW","BWWG","BWPG","BWMG","BWRG","BGBW","BWWR",
                 "BWPR","BWMR","BWRR","BRBW","BWWB","BWPB","BWMB","BWRB","BBBW",
                 "WGWG","PGWG","MGWG","RGWG","BGWG","WGWR","PRWG","MRWG","RRWG",
                 "BRWG","WBWG","PBWG","MBWG","RBWG","BBWG","PGPG","MGPG","PGRG",
                 "BGPG","PGWR","PGPR","MRPG","PGRR","BRPG","PGWB","PBPG","MBPG",
                 "PGRB","BBPG","MGMG","MGRG","BGMG","MGWR","MGPR","MGMR","MGRR",
                 "BRMG","MGWB","MGPB","MBMG","MGRB","BBMG","RGRG","BGRG","RGWR",
                 "PRRG","MRRG","RGRR","BRRG","RGWB","PBRG","MBRG","RBRG","BBRG",
                 "BGBG","BGWR","BGPR","BGMR","BGRR","BGBR","BGWB","BGPB","BGMB",
                 "BGRB","BBBG","WRWR","PRWR","MRWR","RRWR","BRWR","WBWR","PBWR",
                 "MBWR","RBWR","BBWR","PRPR","MRPR","PRRR","BRPR","PRWB","PBPR",
                 "MBPR","PRRB","BBPR","MRMR","MRRR","BRMR","MRWB","MRPB","MBMR",
                 "MRRB","BBMR","RRRR","BRRR","RRWB","PBRR","MBRR","RBRR","BBRR",
                 "BRBR","BRWB","BRPB","BRMB","BRRB","BBBR","WBWB","PBWB","MBWB",
                 "RBWB","BBWB","PBPB","MBPB","PBRB","BBPB","MBMB","MBRB","BBMB",
                 "RBRB","BBRB","BBBB"]


# W ---------------------------------------------------------------------------
wGenes = (('W', (0, 2)), ('W', (1, 3)))
wPos = aggregateGeneAppearances(genotypes, wGenes)
# H ---------------------------------------------------------------------------
hGenes = (('P', (0, 2)), ('M', (0, 2)))
hPos = aggregateGeneAppearances(genotypes, hGenes)
# RA --------------------------------------------------------------------------
rAGenes = (('R', (0, 2)), ('B', (0, 2)))
rAPos = aggregateGeneAppearances(genotypes, rAGenes)
# RB --------------------------------------------------------------------------
rBGenes = (('R', (1, 3)), ('B', (1, 3)))
rBPos = aggregateGeneAppearances(genotypes, rBGenes)
# G ---------------------------------------------------------------------------
gGenes = (('G', (1, 3)), )
gPos = aggregateGeneAppearances(genotypes, gGenes)

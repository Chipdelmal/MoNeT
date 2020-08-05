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


genes = (('R', 'B'), ('R'))

prb = 'RBWR'
(lA, lB) = (prb[:2], prb[2:])
(lAs, lBs) = (
        sum([lA.count(i) for i in genes[0]]),
        sum([lB.count(i) for i in genes[1]])
    )
lociiCount = lAs + lBs


# def lociCountGenes(genotype, genesList):
#     (lA, lB) = (genotype[:2], genotype[2:])
#     (lAs, lBs) = (
#             sum([lA.count(i) for i in genesList[0]]),
#             sum([lB.count(i) for i in genesList[1]])
#         )
#     lociCount = lAs + lBs
#     return lociCount

list(prb)


def lociCountGenes(genotype, genesList):
    alleles = list(genotype)
    lociCount = []
    for (i, gene) in enumerate(genesList):
        lociCount.extend(alleles[i].count(gene))
    return lociCount


lociCountGenes(prb, (('W'), (), ('W'), ()))


def countGenesTwoLoci(genotypes, genes):
    geneClst = []
    for (i, genotype) in enumerate(genotypes):
        geneClst.extend([i] * lociCountGenes(genotype, genes))
    geneClst.sort()
    return geneClst


genes = (('G'), ('G'))
geneClst = []
for (i, genotype) in enumerate(genotypes):
    geneClst.extend([i] * lociCountGenes(genotype, genes))
geneClst.sort()
geneClst


genes = [
        (('G'), ('G'))
    ]
countGenesTwoLoci(genotypes, genes)

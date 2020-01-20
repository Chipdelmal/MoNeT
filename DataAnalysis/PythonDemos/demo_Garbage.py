import MoNeT_MGDrivE as monet

type = float
experimentString = "E_095_075_006_015"
pathRoot = "/Volumes/marshallShare/MGDrivE_Datasets/SplitDrive/Datasets/"
pathExt = "SD_BioParams/CRISPR/2018_11_30_GARBAGE/E_03_05_079_076_25_10000/"
pathFull = pathRoot + pathExt

colors = [
    '#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1'
]
style = {
    "width": .05, "alpha": .1, "dpi": 1024, "legend": True,
    "aspect": .075, "colors": colors
}

aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)

paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
    paths, aggregationDictionary,
    male=False, female=True, dataType=float
)
figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
for i in range(0, len(figsArray)):
    figsArray[i].savefig(
            "./images/TracesDemo"+str(i)+".png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None
        )

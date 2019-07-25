import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

colors = [
    "#090446", "#f20060", "#7fff3a",
    "#ff28d4", "#6898ff", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleS = {
    "width": 0, "alpha": .85, "legend": False,
    "aspect": 50.0, "dpi": 2*512,
    "colors": colors, "format": "png",
    "xRange": [0, 5000], "yRange": [0, 440000]  # 2500]
}
genAggDict = monet.autoGenerateGenotypesDictionary(
    ["W", "H", "E", "R", "B"],
    [
        'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
        'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
    ]
)

def plotTimeError(data):
    plt.figure(figsize = (5, 5))
    for i in range(len(data[0])):
        plt.plot(data[:,i], color=aux.colors[i], linewidth=1.5, alpha=.75)
    plt.ylim(0, 1)
    return plt

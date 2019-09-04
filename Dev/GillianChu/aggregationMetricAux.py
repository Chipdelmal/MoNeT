import numpy as np
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

def plotTimeError(data, metric=np.mean, yRange=1):
    plt.figure(figsize=(5, 5))
    plt.grid()
    for i in range(len(data[0])):
        plt.plot(data[:, i], color=colors[i], linewidth=1.5, alpha=.8)
    plt.title(str(np.around(metric(data, axis=0), decimals=3)))
    plt.xlim(0, len(data))
    plt.ylim(0, yRange)
    return plt
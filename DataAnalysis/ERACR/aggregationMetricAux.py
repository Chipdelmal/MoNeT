import MoNeT_MGDrivE as monet

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
aggregationDictionary = monet.autoGenerateGenotypesDictionary(
    ["W", "H", "E", "R", "B"],
    [
        'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
        'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
    ]
)

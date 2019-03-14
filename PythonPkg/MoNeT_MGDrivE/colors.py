from matplotlib.colors import LinearSegmentedColormap

# Define 5 colormaps ranging from transparent to opaque.
cdict1 = {
    'red':   ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'green': ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    'blue':  ((0.0, 0.0, 0.0), (1.0, 0.3, 0.3)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
red1 = LinearSegmentedColormap('Red1', cdict1)

cdict2 = {
    'red':   ((0.0, 0.3, 0.3), (1.0, 0.3, 0.3)),
    'green': ((0.0, 0.5, 0.5), (1.0, 0.5, 0.5)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
light_blue1 = LinearSegmentedColormap('LightBlue1', cdict2)

cdict3 = {
    'red':   ((0.0, 0.5, 0.5), (1.0, 0.5, 0.5)),
    'green': ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
purple1 = LinearSegmentedColormap('Purple1', cdict3)

cdict4 = {
    'red':   ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'green': ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    'blue':  ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
pink1 = LinearSegmentedColormap('Pink1', cdict4)

cdict5 = {
    'red':   ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    'green': ((0.0, 0.25, 0.25), (1.0, 0.25, 0.25)),
    'blue':  ((0.0, 0.75, 0.75), (1.0, 0.75, 0.75)),
    'alpha': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
}
dark_blue1 = LinearSegmentedColormap('DarkBlue1', cdict5)

rgba_colors = [
    (1, 0, 0.3, 0.7), (1, 0, 1, 0.7),
    (0.5, 0, 1, 0.7), (0, 0.325, 0.75, 0.7)
]
cmaps = [light_blue1, red1, purple1, pink1, dark_blue1]


def generateAlphaColorMapFromColor(
    color
):
    """
    Description:
        * Generates the cmap necessary to do the landscape heatmaps.
    In:
        * color: hex color to alpha cmap
    Out:
        * cmap: Color map changing in alpha
    Notes:
        * NA
    """
    alphaMap = LinearSegmentedColormap.from_list(
        'tempMap',
        [(0.0, 0.0, 0.0, 0.0), color],
        gamma=0
    )
    return alphaMap


def generateAlphaColorMapFromColorArray(
    colorArray
):
    """
    Description:
        * Generates a list of cmaps from a colors list.
    In:
        * colorArray: Array containing the colors to cmap.
    Out:
        * cmapsList: List of cmaps
    Notes:
        * NA
    """
    elementsNumb = len(colorArray)
    cmapsList = [None] * elementsNumb
    for i in range(0, elementsNumb):
        cmapsList[i] = generateAlphaColorMapFromColor(colorArray[i])
    return cmapsList

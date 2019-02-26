import matplotlib
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# Define 5 colormaps ranging from transparent to opaque.
cdict1 = {'red':   ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'green': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 0.0, 0.0),
                    (1.0, 0.3, 0.3)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

red1 = LinearSegmentedColormap('Red1', cdict1)

cdict2 = {'red':   ((0.0, 0.3, 0.3),
                    (1.0, 0.3, 0.3)),

          'green': ((0.0, 0.5, 0.5),
                    (1.0, 0.5, 0.5)),

          'blue':  ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

light_blue1 = LinearSegmentedColormap('LightBlue1', cdict2)


cdict3 = {'red':   ((0.0, 0.5, 0.5),
                    (1.0, 0.5, 0.5)),

          'green': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

purple1 = LinearSegmentedColormap('Purple1', cdict3)


cdict4 = {'red':   ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'green': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

pink1 = LinearSegmentedColormap('Pink1', cdict4)

cdict5 = {'red':   ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'green': ((0.0, 0.25, 0.25),
                    (1.0, 0.25, 0.25)),

          'blue':  ((0.0, 0.75, 0.75),
                    (1.0, 0.75, 0.75)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

dark_blue1 = LinearSegmentedColormap('DarkBlue1', cdict5)
rgba_colors = [(1, 0, 0.3, 0.7), (1, 0, 1, 0.7),
               (0.5, 0, 1, 0.7), (0, 0.325, 0.75, 0.7)]
cmaps = [light_blue1, red1, purple1, pink1, dark_blue1]

def alleleCounts(csvFileName, columns, alleleNames, timeSteps, startCol=3):
    """
       In: columns is a list of lists describing the number of times each one
            indexed column should be counted for this allele eg
            [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR, and RR
    	    alleleNames is a list of the allele names for use as column
            titles eg ["W", "R"] startCol is the first column in the csv
            which lists genotypes, one indexed (column 1 in the columns
            argument)
        Out: A pandas dataframe with 1 column for each allele, containing
            the specified sum: eg  col 1 + col 1 + col 2 for "W"
    """
    data = np.genfromtxt(csvFileName, skip_header=1, delimiter=",")
    time = range(1, timeSteps + 1)
    res = pd.DataFrame(time,columns=['Time'])
    for i in range(len(columns)):
        # summed_col contains sum of counts for one allele, such as W
        summed_col = np.zeros_like(data[:,0])
        for index in columns[i]:
            # subtract 2 because index and start col are 1 indexed
            summed_col += data[:,index+startCol - 2]
        allele = alleleNames[i]
        res.insert(i + startCol - 1, alleleNames[i], summed_col)
    return res

# def allCounts(csvPath, columns, alleleNames, female=True):
#     """
#     In: csvPath is a folder of CSV files, such as "CRISPR_SIT/"
#     	columns is a list of lists describing the number of times each one indexed column should be counted for this allele
#     	eg [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR, and RR
#     	alleleNames is a list of the alleleNames. One dataframe is made for each.
#     	female specifies whether to count male or female mosquitoes
#     Out: List of data frames with one allele count column for each run of that gender
#     	 eg  W1W2...WnW1W2...Wn  representing the count of W over n experiments on female mosquitoes
#     """
#     if female:
#         files = glob.glob(csvPath + 'AF1*.csv')
#     else:
#         files = glob.glob(csvPath + 'ADM*.csv')
#     df = pd.read_csv(files[0])
#     res = [df[['Time']] for _ in range(len(alleleNames))]
#     timesteps = len(d["Time"])
#     for i in range(len(files)):
#         count_df = alleleCounts(files[i], columns, alleleNames, timesteps, 2)
#         for j in range(len(alleleNames)):
#             res[j].insert(i + 1, alleleNames[j] + str(i), (count_df[alleleNames[j]]).copy())
#     for j in range(len(alleleNames)):
#         res[j] = res[j].set_index("Time").T
#     return res

# def aggregatedNodesToPandas(aggregatedNodesData):
# 	"""
# 	In: aggregatedNodesData as output by monet_mgdrive.aggregateGenotypesInLandscape()
# 		See example in MoNeT/DataAnalysis/PythonDemos/mainMCR.py
# 		Use this instead of allCounts if data comes from here rather than CSV file
# 	Out: List of data frames with one allele count column for each run of that gender
# 		 eg  W1W2...WnW1W2...Wn  representing the count of W over n experiments on female mosquitoes
# 	"""
# 	genotypes = aggregatedNodesData['genotypes']
# 	landscape = aggregatedNodesData['landscape']
# 	time = [i+1 for i in range(len(landscape[0]))]
# 	res = [pd.DataFrame(time, columns=['Time']) for _ in range(len(genotypes))]
# 	display(res[0].head())
# 	for i in range(len(landscape)):
# 	    for j in range(len(genotypes)):
# 	        res[j].insert(i + 1, genotypes[j] + str(i), landscape[i][:,j])
# 	for j in range(len(genotypes)):
# 	    res[j] = res[j].set_index("Time").T
# 	return res

def makeAlleleCountPlot(alleleCounts, title, linewidth, opacity, color):
	# alleleCounts is table outputted by allCounts or aggregatedNodesToPandas
    alleleCounts.plot(x="Time", figsize=(15, 5), linewidth = linewidth, legend=False, title = title, color = color, alpha = opacity)
    plt.ylabel("Allele Count")
    plt.show()

def plotIndividualAlleles(counts, alleleNames):
    """
    In: counts is the output of allCounts() or aggregatedNodesToPandas()
    	alleleNames is a list of the alleleNames.
    Out: Plot a heatmap of each allele over time. One horizontal line in the heatmap represents one patch's alleles
    	 over time with the opacity of the line defined by the allele count.
    	 The overall map comes from stacked horizontal lines, one from each csv file.
    """
    cmaps = [light_blue1, red1, purple1, pink1]
    for i in range(len(counts)):
        fig, ax = plt.subplots(figsize=(20, 5))
        ax.set_ylabel(alleleNames[i])
        im = ax.imshow(counts[i], cmap=cmaps[i])

def plotAllAlleles(counts, alleleNames):
    """
    In: counts is the output of allCounts() or aggregatedNodesToPandas()
    	alleleNames is a list of the alleleNames.
    Out: Overlay all allele heatmaps such as those produced by plotIndividualAlleles
    """
    cmaps = [light_blue1, red1, purple1, pink1]
    fig = plt.figure(figsize=(20, 5))
    for i in range(len(alleleNames)):
        plt.imshow(counts[i], cmap=cmaps[i])

def stackedAreaPlot(counts, alleleNames):
    """
    In: counts is the output of allCounts() or aggregatedNodesToPandas()
    	alleleNames is a list of the alleleNames.
    Out: A stacked area plot of the total count of each allele over time, summed over all nodes.
    """
    allele_dict = {}
    for i in range(len(alleleNames)):
        allele_dict[alleleNames[i]] = counts[i].sum()
    res = pd.DataFrame(allele_dict)
    return res.plot.area(color=rgba_colors)


# def exportStackedAreaPlots(csvPath, columns, alleleNames, female=True):
#     """
#     In: csvPath is a folder with folders of CSV files and an images folder.
#     Out: For each folder of CSV files, put a stacked area plot in the images folder.
#          Each plot stacks the total count of each allele over time, summed over all nodes in the folder.
#     """
#     folders = glob.glob(csvPath + '*/')
#     for f in folders:
#         counts = allCounts(f, columns, alleleNames, female)
#         plot = stackedAreaPlot(counts, alleleNames)
#         fig = plot.get_figure()
#         fig.savefig(csvPath + '/images/' + f.split(csvPath)[1][:-1])
#         plt.close(fig)

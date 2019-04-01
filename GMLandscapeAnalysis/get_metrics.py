import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
import plotly.plotly as py
import numpy as np
import pandas as pd

###############################################################################
# MCR Construct
###############################################################################
#------------------------------------------------------------------------------
# Analyzing different metrics on drive behavior
#------------------------------------------------------------------------------
experiments = ['base_20m_50n', 'looser_50n', 'tight_50n', 'uneven_test']
iteration = 100
d = {}
for experiment in experiments:
    type = float
    path = "/Users/Biyonka/Desktop/Output/contrived_landscapes_test/" + experiment + "/GARBAGE/0001/"
    time_to_thres, intersection, prop_homing_end = [], [], []
    for i in range(1, iteration+1, 1):
        # Define the experiment's path, aggregation dictionary, and read filenames
        experimentString = '{0:04d}'.format(i)
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "H", "R", "B"],
            [
                [0, 0, 1, 2, 3],
                [1, 4, 4, 5, 6],
                [2, 5, 7, 7, 8],
                [3, 6, 8, 9, 9]
            ]
        )
        filenames = monet.readExperimentFilenames(path + experimentString)

        # To analyze a single node ...................................................
        # Load a single node (auxiliary function just for demonstration)
        nodeIndex = 0
        nodeData = monet.loadNodeData(
            filenames.get("male")[nodeIndex], filenames.get("female")[nodeIndex],
            dataType=float
        )

        # To analyze the sum of the whole landscape ..................................
        # Sum landscape into one array ("in place" memory-wise)
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )

        # Aggregate genotypes (node or landscape) ....................................
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData,
            aggregationDictionary
        )
        wbh = np.sum(aggData['population'], axis =1)
        ratio_homing = aggData['population'][:, 1]/(wbh)
        #get time at which homing ratio exceeds threshold
        if any(ratio_homing >= 0.5):
            #get first time that ratio exceeds 0.5
            time = (list(ratio_homing>= 0.5)).index(True)
        else:
            # if threshold of homing never eceeds 0.5, set time to
            #total length of experiment (i.e. 3 years)
            time = aggData['population'].shape[0]
        time_to_thres.append(time)

        #get proportion of homing at end of 3 years
        prop_homing = aggData['population'][:, 1][-1]/wbh[-1]
        prop_homing_end.append(prop_homing)

        #get the time of intersection between wild and homing
        diff = aggData['population'][:, 1] - aggData['population'][:, 0]
        if i == "TIGHT":
            #no intersection occurs in the tight experiment
            inter = aggData['population'].shape[0]
        else:
            #get index where the wild and homing arrays are the closest
            inter = list(np.abs(diff)).index(min(np.abs(diff)))
        intersection.append(inter)
    d[experiment] = {"thres": time_to_thres, "inter":intersection, "end": prop_homing_end}

#------------------------------------------------------------------------------
# Plotting
#------------------------------------------------------------------------------

def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value

def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Landscape Type (2 Clusters)')
    ax.set_ylim(0, 1)

data = [d['base_20m_50n']['end'],
 d['looser_50n']['end'],
 d['tight_50n']['end'],
  d['uneven_test']['end']]

fig,  ax2 = plt.subplots(nrows=1, ncols=1, figsize=(9, 6), sharey=True)
ax2.set_title('Homing Allele Proportion at End of 3 Years For 50-Node Landscape')
parts = ax2.violinplot(
        data, showmeans=False, showmedians=False,
        showextrema=False)

for pc in parts['bodies']:
    pc.set_facecolor('lightblue')
    pc.set_edgecolor('black')
    pc.set_alpha(1)

quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)
whiskers = np.array([
    adjacent_values(sorted_array, q1, q3)
    for sorted_array, q1, q3 in zip(data, quartile1, quartile3)])
whiskersMin, whiskersMax = whiskers[:, 0], whiskers[:, 1]

inds = np.arange(1, len(medians) + 1)
ax2.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
ax2.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=3)
ax2.vlines(inds, whiskersMin, whiskersMax, color='k', linestyle='-', lw=1)

labels = ['Base', 'Loose', 'Tight', 'Uneven']
set_axis_style(ax2, labels)
plt.show()


fig.savefig("end_violin_1.png", dpi=1024)

import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
import plotly.plotly as py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
###############################################################################
# MCR Construct
###############################################################################
#------------------------------------------------------------------------------
# Analyzing different metrics on drive behavior
#------------------------------------------------------------------------------
#experiments = ['eta1e-05', 'eta5e-04', 'eta1e-04', 'eta5e-03',
#'eta1e-03', 'eta5e-03', 'eta1e-02', 'eta5e-01', 'eta1e-01',
# 'eta1','eta10', 'eta100','eta1000', 'eta10000','eta1e+05']
range(1, 1000000, 10000)
experiments = range(1, 1000000, 10000)
iteration = 1
d = []

for experiment in experiments:
    #type = float
    if experiment < 1:
        e =  "{:.1e}".format(experiment)
    #path = #"/Users/Biyonka/Desktop/Output/1clustering_analysis/drive_output/" + experiment + "/ANALYZED/"
    time_to_thres, avg_rate = [], []
    for i in range(1, iteration+1, 1):
        path = ("/Users/Biyonka/Desktop/Output/1clustering_analysis/drive_output/eta%s_iter%s/ANALYZED/" % (experiment, i))
        # Define the experiment's path, aggregation dictionary, and read filenames
        experimentString = "0001"#'{0:04d}'.format(i)
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
        print(filenames)
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
    #     wbh = np.sum(aggData['population'], axis =1)
        #get first time that exceeds 100
        t1 = filter(lambda x: x[1]>30, enumerate(aggData['population'][:, 1]))[0][0]
        #get first time that is greater than 4000
        t2 = filter(lambda x: x[1]<4000, enumerate(aggData['population'][:, 1]))[-1][0]
        rate = (4000-30)/(t2 - t1)
        #e = float(experiment[3:])
        avg_rate.append((experiment, rate))
    d.extend(avg_rate)


    #     wbh = np.sum(aggData['population'], axis =1)
    #     ratio_homing = aggData['population'][:, 1]/(wbh)
    #     #get time at which homing ratio exceeds threshold
    #     if any(ratio_homing >= 0.90):
    #         #get first time that ratio exceeds 0.5
    #         time = (list(ratio_homing>= 0.90)).index(True)
    #     else:
    #         # if threshold of homing never eceeds 0.5, set time to
    #         #total length of experiment (i.e. 3 years)
    #         time = aggData['population'].shape[0]
    #     e = float(experiment[3:])
    #     time_to_thres.append((e, time))
    # d.extend(time_to_thres)
        # #get proportion of homing at end of 3 years
        # prop_homing = aggData['population'][:, 1][-1]/wbh[-1]
        # prop_homing_end.append(prop_homing)

list1, list2 = zip(*d)
df = pd.DataFrame({"log(eta)":  list1, "thres": list2})
#df.to_csv("regression_data.csv", index = False)

#ax1 = df.plot.scatter(x='eta',
            #          y='thres',
            #         c='DarkBlue')
df
model = LinearRegression()
X= df['log(eta)'].values.reshape(-1,1)
y= df['thres'].values.reshape(-1,1)
model.fit(X,y)
predictions = model.predict(X)
#plt.scatter(X,predictions-y)
df.plot.scatter(x='log(eta)', y = 'thres')
plt.plot(X,predictions)

    #d[experiment] = time_to_thres#{"thres": time_to_thres, "end": prop_homing_end}
model.score(X, y)
model.intercept_
model.coef_
w = df.groupby('log(eta)').var().reset_index()
w.plot.scatter('log(eta)', 'thres')
w
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

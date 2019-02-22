import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plotMeanGenotypeTrace(aggData, style):
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df = pd.DataFrame(time, columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local = pd.DataFrame(pops, columns=groups)
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=style["aspect"])
    # plt.xticks([])
    # plt.yticks([])
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')
    for i in range(len(final)):
        final[i].plot(
            ax=ax, linewidth=style["width"], legend=False,
            color=style["colors"][i], alpha=style["alpha"]
        )
    legends = []
    for i in range(len(groups)):
        legends.append(
            mpatches.Patch(color=style["colors"][i], label=groups[i])
        )
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    ax.xaxis.set_label_text("")
    ax.yaxis.set_label_text("")
    plt.ylabel("Allele Count")
    return fig


def plotMeanGenotypeStack(aggData, style):
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df = pd.DataFrame(time, columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local = pd.DataFrame(pops, columns=groups)
    fig, ax2 = plt.subplots()
    ax2.set_aspect(aspect=style["aspect"])
    allele_dict = {}
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')
    patchList = []
    for i in range(len(groups)):
        patchList.append(mpatches.Patch(
            color=style["colors"][i], label=groups[i]))
    for i in range(len(groups)):
        allele_dict[groups[i]] = final[i].T.sum()
    res = pd.DataFrame(allele_dict)
    res.plot(
        kind='area', ax=ax2, legend=False, color=style["colors"],
        linewidth=style["width"], alpha=style["alpha"]
    )
    plt.ylabel("Allele Count")
    return fig

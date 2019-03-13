import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

groups = ['W', 'H', 'R', 'B', 'E']
weights = [[],[],[],[],[]]
colors = ['#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

legendList = []
for i in range(len(groups)):
    legendList.append(mpatches.Patch(color=colors[i], label=groups[i]))

basepath ='/Volumes/marshallShare/vic/eRACR28/'
releases='_02_'
first = True
headerLen = 0
for efficiency in range(91,100,1):
    folder = str(efficiency).zfill(4)+'_ANALYZED/'
    for hcost in range(0,40,5):
        hstr = str(hcost).zfill(4)
        for ecost in range(0,50,5):
            combination = hstr+'_'+str(ecost).zfill(4)
            for mosquitos in range(1100,1500,50):
                experiment = 'E_'+combination+releases+str(mosquitos).zfill(5)
                fileName = '/ADM_Mean_Patch0000.csv'
                maleFile = open(basepath+folder+experiment+fileName, 'r')
                cleanFile = open('clean2.csv', 'w')

                if first:
                    firstLine = next(maleFile)
                    header = firstLine.split(',')
                    headerLen = len(header)
                    for genotype in header:
                        for i in range(len(groups)):
                            weights[i].append(genotype.count(groups[i]))
                    first=False
                    cleanFile.write(firstLine)

                for line in maleFile:
                    data = line.split(',')
                    if len(data) < headerLen:
                        continue
                    elif len(data) > headerLen:
                        continue
                    else:
                        cleanFile.write(line)
                cleanFile.close()

                maleFile.close()
                try:
                    df = pd.read_csv('clean2.csv')
                except Exception as e:
                    continue

                final = [df[['Time']] for _ in range(len(groups))]
                timesteps = len(df["Time"])

                data = np.genfromtxt('clean2.csv', skip_header=1, delimiter=",", filling_values=0)#, invalid_raise=False)
                time = np.arange(timesteps)
                local = pd.DataFrame(time , columns=['Time'])
                for i in range(len(groups)):
                    # summed_col contains sum of counts for one allele, such as W
                    summed_col = np.zeros_like(data[:,0])
                    for column in range(len(weights[i])):
                        weight = weights[i][column]
                        #ignores columns with weight equal to 0
                        if weight > 0:
                            #adds 2 to the column because column 0 is time and column 1 is usually patch number, and everything else is 0 indexed
                            summed_col += weight * data[:,column]
                    local.insert(i + 1, groups[i], summed_col)

                for j in range(len(groups)):
                    final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
                    final[j] = final[j].set_index('Time')

                fig, ax = plt.subplots()
                for i in range(len(final)):
                    final[i].plot(ax = ax, linewidth = 0.3, legend=False, color = colors[i], alpha = 0.5)

                picfolder = basepath+'/graphs/'+str(efficiency)+'/'
                plt.legend(handles=legendList)
                plt.ylabel("Allele Count")
                plt.savefig(picfolder+experiment+".png",
                            dpi=1024, facecolor='w',
                            edgecolor='w', orientation='portrait', papertype=None,
                            format="png", transparent=False, bbox_inches='tight',
                            pad_inches=0.05, frameon=None)
                plt.close(fig)
                plt.close('all')

                fig, ax2 = plt.subplots()
                allele_dict = {}
                for i in range(len(groups)):
                    allele_dict[groups[i]] = final[i].T.sum()
                res = pd.DataFrame(allele_dict)
                res.plot(kind = 'area', ax =ax2, color=colors)
                plt.savefig(picfolder+experiment+ "stack.png",
                            dpi=1024, facecolor='w',
                            edgecolor='w', orientation='portrait', papertype=None,
                            format="png", transparent=False, bbox_inches='tight',
                            pad_inches=0.05, frameon=None)
                plt.close(fig)
                plt.close('all')

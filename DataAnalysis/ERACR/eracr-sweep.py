import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

basepath ='/Volumes/marshallShare/vic/eRACRfact11/'
for hcost in range(90,99,1) :
    releases='_02_'
    for mosquitos in range(500,3000,50) :
        groups = ['W', 'H', 'R', 'B', 'E']
        weights = [[],[],[],[],[]]
        foldername = 'E_'+str(hcost).zfill(4)+releases+str(mosquitos).zfill(5)
        fileName = '/ADM_Run001.csv'
        try:
            maleFile = open(basepath+foldername+fileName, 'r')
        except Exception as e:
            continue
        first = next(maleFile)
        header = first.split(',')

        for genotype in header:
            for i in range(len(groups)):
                weights[i].append(genotype.count(groups[i]))

        cleanFile = open('clean.csv', 'w')
        cleanFile.write(first)
        for line in maleFile:
            data = line.split(',')
            if len(data) < len(header):
                continue
            elif len(data) > len(header):
                continue
            else:
                cleanFile.write(line)
        cleanFile.close()

        maleFile.close()
        df = pd.read_csv('clean.csv')
        final = [df[['Time']] for _ in range(len(groups))]
        timesteps = len(df["Time"])

        data = np.genfromtxt('clean.csv', skip_header=1, delimiter=",", filling_values=0)
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

        colors = ['#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']
        fig, ax = plt.subplots()
        for i in range(len(final)):
            final[i].plot(ax = ax, linewidth = 0.3, legend=False, color = colors[i], alpha = 0.5)
        W_patch = mpatches.Patch(color='#6e44ff', label='W')
        H_patch = mpatches.Patch(color='#e56399', label='H')
        R_patch = mpatches.Patch(color='#ee6c4d', label='R')
        B_patch = mpatches.Patch(color='#861657', label='B')
        E_patch = mpatches.Patch(color='#5cf64a', label='E')
        plt.legend(handles=[W_patch, H_patch,R_patch,B_patch,E_patch])
        plt.ylabel("Allele Count")
        plt.savefig(basepath+foldername+ ".png",
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
        plt.savefig(basepath+foldername+ "stack.png",
                    dpi=1024, facecolor='w',
                    edgecolor='w', orientation='portrait', papertype=None,
                    format="png", transparent=False, bbox_inches='tight',
                    pad_inches=0.05, frameon=None)
        plt.close(fig)
        plt.close('all')

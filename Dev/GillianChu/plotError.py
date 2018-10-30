"""
Graph difference between noaggregation and some level of aggregation CSV result files . 
Plot the error (delta/noagg) of the homing H allele over time, treating no aggregation as truth.
"""

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from visualizeMultiple import alleleCounts
from pathlib import Path

pathlist = Path("/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/Oct25/noagg/2018_10_15_ANALYZED/E_080_000_000_000/").glob('**/*.csv')
counts1 = 0
count = 0
total = set()
for path in pathlist:
	path_in_str = str(path)
	total.add(path_in_str)
	if count == 0:
		# print('first time')
		count = 1
		counts1 = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
	else:
		# print("iteration ", count)
		h_allele = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
		counts1 = np.add(counts1, h_allele)
plt.plot(counts1, label="No aggregation") #the H allele

count = 0
total = set()
pathlist = Path("/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/Oct25/fullagg/2018_10_15_ANALYZED/E_080_000_000_000/").glob('**/*.csv')
for path in pathlist:
	path_in_str = str(path)
	total.add(path_in_str)
	if count == 0:
		# print('first time')
		count = 1
		counts2 = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
	else:
		# print("iteration ", count)
		h_allele = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
		counts2 = np.add(counts2, h_allele)
plt.plot(counts2, label="Full aggregation") #the H allele

count = 0
pathlist = Path("/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/Oct25/halfagg/2018_10_15_ANALYZED/E_080_000_000_000/").glob('**/*.csv')
for path in pathlist:
	path_in_str = str(path)
	total.add(path_in_str)
	if count == 0:
		# print('first time')
		count = 1
		counts3 = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
	else:
		# print("iteration ", count)
		h_allele = alleleCounts(path_in_str, ['H', 'W', 'B', 'R'])[0]
		counts3 = np.add(counts3, h_allele)
plt.plot(counts3, label="Half aggregation") #the H allele

plt.legend()
plt.show()
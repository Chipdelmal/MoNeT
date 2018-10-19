import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

# Columns is a list of lists describing the number of times each one indexed column should be counted for this allele
# eg [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR, and RR
# alleleNames is a list of the allele names for use as column titles eg ["W", "R"]
# startCol is the first column in the csv which lists genotypes, one indexed. 
# Column 1 in the column argument corresponds to startCol in the table.
# returns 1 summed list for each list in columns, each containing the specified sum: eg  col 1 + col 1 + col 2        
#[WW, WH, WR, WB, HH, HR, HB, RR, RB, BB]

#Let H = 0, W = 1, B = 2, R = 3
# df = np.genfromtxt(csvFileName, dtype=float, skip_header=1, delimiter=",")
def alleleCounts(csvFileName, alleles):
	df = pd.read_csv(csvFileName)
	numEntries = len(df['WW'])
	allele_count = np.zeros(len(alleles))
	result = np.zeros((numEntries, len(allele_count)))
	print(result)

	for i in range(1, len(df['WW'])):
		#adding H's
		allele_count[0] = float(allele_count[0]) + (2 * df['HH'][i]) + df['HB'][i] + df['WH'][i] + df['HR'][i]

		#adding W's
		allele_count[1] += (2 * df['WW'][i]) + df['WH'][i] + df['WR'][i] + df['WB'][i]

		#adding B's
		allele_count[2] += (2 * df['BB'][i]) + df['WB'][i] + df['RB'][i] + df['HB'][i]

		#adding R's
		allele_count[3] += (2 * df['RR'][i]) + df['RB'][i] + df['WR'][i] + df['HR'][i]

		print(allele_count)
		np.copyto(result[i], allele_count)

	return result

csvFileName = "/Users/gillianchu/Desktop/MGDrive-Experiments/Experiments/noagg/2018_10_15_ANALYZED/E_080_000_000_000/ADM_Mean_Patch0004.csv"
df = pd.read_csv(csvFileName)
plt.plot(df)
counts = alleleCounts(csvFileName, ['H', 'W', 'B', 'R'])
plt.plot(counts)
plt.show()
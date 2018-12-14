
import plotly.plotly as py
import pandas as pd
import plotly.figure_factory as FF

# for i in range(25):
	# df = pd.read_csv("/Users/gillianchu/marshall/MoNeT/Dev/GillianChu/Results/DistMatrices/" + str(i) + "AggregationPop.csv")
	# sample_data_table = FF.create_table(df.head())
	# py.iplot(sample_data_table, filename=str(i)+"AggregationPop")



import matplotlib.pyplot as plt

# df = pd.read_csv("/Users/gillianchu/marshall/MoNeT/Dev/GillianChu/Results/DistMatrices/noAggregationCoord.csv")
# df = pd.read_csv("/Users/gillianchu/marshall/MoNeT/Dev/GillianChu/Results/Vectors/24AggregationCoord.csv")

for i in range(0, 105, 15):
	df = pd.read_csv("/Users/gillianchu/marshall/MoNeT/Dev/GillianChu/"+str(i)+"AggregationCoord.csv")
	plt.plot(df)
	plt.title('aggregation coord num '+str(i))
	plt.ylabel('some numbers')
	plt.show()
import numpy as np

#inDegV,outDegV,closeCentrV,betCentrV,eigVecCentrV,pageRankCentrV
data = [[],[],[],[],[],[]]

with open('CentrFeatures.csv', 'r') as infile:
	first = True
	for line in infile:
		if first:
			first = False
			continue
		splitted = line.split(',')
		for i in range(6):
			data[i].append(float(splitted[i+1]))

print "inDegV,outDegV,closeCentrV,betCentrV,eigVecCentrV,pageRankCentrV"
print np.corrcoef(data)
		





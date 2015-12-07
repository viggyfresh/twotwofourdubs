import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

def addToFeatureMap(fn, featureMap):
	print fn
	infile = open(fn,'r')
	first = True
	for line in infile:
		if first:
			first = False
			continue
		splitted = line.split(',')
		user_id = int(splitted[0])
		badges = [float(x) for x in splitted[1:]]
		if user_id not in featureMap:
			featureMap[user_id] = []
		featureMap[user_id] += badges


### Create feature vectors and truth vectors
featureMapCentr = {}
featureMapUser = {}


#addToFeatureMap('UserBadgesFeatures.csv',0)
addToFeatureMap('CentrFeatures.csv',featureMapCentr)
addToFeatureMap('UserFeatures.csv',featureMapUser)


unionMap = {}
for key in featureMapCentr:
	if key in featureMapUser:
		unionMap[key] = featureMapCentr[key] + featureMapUser[key]

reData = [[] for i in range(len(unionMap[76450]))]
for key in unionMap:
	for i,x in enumerate(unionMap[key]):
		reData[i].append(x)

labels = "inDeg,outDeg,closeCentr,betCentr,eigVecCentr,pageRankCentr," + "Views,DownVotes,UpVotes,Reputation,DaysSinceCreation,DaysSinceAccess"

corrOut = np.corrcoef(reData)
print corrOut
sm.graphics.plot_corr(corrOut[::-1])

labels = "inDeg,outDeg,closeCentr,betCentr,eigVecCentr,pageRankCentr," + "Views,DownVotes,UpVotes,Reputation,DaysSinceCreation,DaysSinceAccess"
labels = labels.split(',')
n_groups = len(labels)
index = np.arange(n_groups)
bar_width = 0.35

plt.xticks(index + bar_width, labels)
_, labelsX = plt.xticks()
plt.setp(labelsX, rotation=270)

plt.yticks(index + bar_width, labels)
_, labelsY = plt.yticks()
plt.setp(labelsY, rotation=0)

plt.xlabel("Features")
plt.ylabel("Features")

plt.gcf().subplots_adjust(bottom=0.35)


plt.savefig('images/correlationMatrix.png')
l = [str(x) for x in corrOut[9]]
print ','.join(l) + '\n'
# outfile.write(','.join(l) + '\n')
#outfile.write(str(np.corrcoef(reData)))	





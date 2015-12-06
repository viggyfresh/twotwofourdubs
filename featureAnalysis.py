import numpy as np

def addToFeatureMap(fn, numDefault,featureMap):
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

		if len(featureMap[user_id]) < numDefault:
			featureMap[user_id] = [0 for i in range(numDefault-len(featureMap[user_id]))]
		featureMap[user_id] += badges


### Create feature vectors and truth vectors
featureMapCentr = {}
featureMapUser = {}


#addToFeatureMap('UserBadgesFeatures.csv',0)
addToFeatureMap('CentrFeatures.csv',0, featureMapCentr)
addToFeatureMap('UserFeatures.csv', 0, featureMapUser)


unionMap = {}
for key in featureMapCentr:
	if key in featureMapUser:
		unionMap[key] = featureMapCentr[key] + featureMapUser[key]

reData = [[] for i in range(len(unionMap[76450]))]
for key in unionMap:
	for i,x in enumerate(unionMap[key]):
		reData[i].append(x)




outfile = open('featureAnalysis.out','w')
corrOut = np.corrcoef(reData)
for l in corrOut:
	l = [str(x) for x in l]
	outfile.write(','.join(l) + '\n')
#outfile.write(str(np.corrcoef(reData)))	





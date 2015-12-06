import math
import snap
import matplotlib.pyplot as plt
import cPickle
import collections
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR

def addToFeatureMap(fn, numDefault):
	global featureMap, truthMap
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
		if fn == 'UserFeatures.csv':
			badges = badges[:3] + badges[4:]
			truthMap[user_id] = badges[3]
		if user_id not in featureMap:
			featureMap[user_id] = []
		if len(featureMap[user_id]) < numDefault:
			featureMap[user_id] = [0 for i in range(numDefault-len(featureMap[user_id]))]
		featureMap[user_id] += badges


### Create feature vectors and truth vectors
featureMap = {}
truthMap = {}

addToFeatureMap('UserBadgesFeatures.csv',0)
addToFeatureMap('UserFeatures.csv', 340)
addToFeatureMap('CentrFeatures.csv',346)


for user in featureMap:
	featureMap[user] += [0 for i in range(352 - len(featureMap[user]))]

X = []
Y = []

for user_id in truthMap:
	X.append(featureMap[user_id])
	Y.append(truthMap[user_id])

print len(X)
print len(Y)

X = X[:1000]
Y = Y[:1000]
K = 10
examplesPerFold = len(X) / K
print len(X)

models = [linear_model.LinearRegression()]
models_names = ['linear']
for model_i, model in enumerate(models):
	print "####################Using model " + models_names[model_i] + "######################"
	modelTestResiduals = []
	modelTrainResiduals = []
	for i in range(K):
		print i
		testX = X[i * examplesPerFold: (i+1) * examplesPerFold]
		testY = Y[i * examplesPerFold: (i+1) * examplesPerFold]

		trainX = X[:i * examplesPerFold] + X[(i+1) * examplesPerFold:]
		trainY = Y[:i * examplesPerFold] + Y[(i+1) * examplesPerFold:]


		regr = model
		regr.fit(np.array(trainX), np.array(trainY))

		# The coefficients

		# if model_i == 0:
		#	print('Coefficients: \n', regr.coef_)
			# The mean square error
		residualTest = np.mean((regr.predict(np.array(testX)) - np.array(testY)) ** 2)
		residualTrain = np.mean((regr.predict(np.array(trainX)) - np.array(trainY)) ** 2)
		modelTestResiduals.append(residualTest)
		modelTrainResiduals.append(residualTrain)
		print "Residual sum of squares: {0}, residual sqrt {1}".format(residualTest, residualTest ** .5)
		# Explained variance score: 1 is perfect prediction
		#print('Variance score: %.2f' % regr.score(testX, testY))

	print ('Total RMSD {0}'.format((np.mean(modelTestResiduals)) ** .5))
	print ('Total RMSD {0}'.format((np.mean(modelTrainResiduals)) ** .5))







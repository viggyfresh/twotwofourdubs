import math
import snap
import matplotlib.pyplot as plt
import cPickle
import collections
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR

### Create feature vectors and truth vectors
X = []
Y = []
badgesInfile = open('UserBadgesFeatures.csv','w')


usersInfile = open('UserFeatures.csv','w')


centrInfile = open('CentrFeatures.csv','w')


X = X[:1000]
Y = Y[:1000]
K = 10
examplesPerFold = len(X) / K
print len(X)
models = [linear_model.LinearRegression(),linear_model.Ridge (alpha = .5), 
		  SVR(kernel='rbf', C=1e3, gamma=0.1),  
		  SVR(kernel='linear', C=1e3), SVR(kernel='poly', C=1e3, degree=2)]
models_names = ['linear','ridge','svr_rbf', 'svr_linear', 'svr_poly']
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

		if model_i == 0:
			print('Coefficients: \n', regr.coef_)
			# The mean square error
		residualTest = np.mean((regr.predict(np.array(testX)) - np.array(testY)) ** 2)
		residualTrain = np.mean((regr.predict(np.array(trainX)) - np.array(trainY)) ** 2)
		modelTestResiduals.append(residualTest)
		modelTrainResiduals.append(residualTrain)
		print "Residual sum of squares: {0}, residual sqrt {1}".format(residualTest, residualTest ** .5)
		# Explained variance score: 1 is perfect prediction
		print('Variance score: %.2f' % regr.score(testX, testY))

	print ('Total RMSD {0}'.format((np.mean(modelTestResiduals)) ** .5))
	print ('Total RMSD {0}'.format((np.mean(modelTrainResiduals)) ** .5))







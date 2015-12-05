import math
import snap
import matplotlib.pyplot as plt
import cPickle
import collections
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR

G = snap.LoadEdgeList(snap.PNGraph, "parsed/geometry_qa.csv", 0, 1, ';')

### Get data for all users
users = cPickle.load(open("pickle/users.pickle",'r'))

print "hi"

### Look at the degree distribution for the networks
CntV = snap.TIntPrV()
snap.GetWccSzCnt(G, CntV)
counts = []
for item in CntV:
	counts.append((item.GetVal1(), item.GetVal2()))
x,y = zip(*counts)
plt.plot(map(math.log,x),map(math.log,y))
plt.xlabel('Degree (log)')
plt.ylabel('Frequency (log)')
plt.title('Degree Distribution')
#plt.show()



### Correlate degree distribution with StackOverflow reputation
### TODO need a way to get reputation for a given node

outDeg = collections.defaultdict(int)
inDeg = collections.defaultdict(int)

for NI in G.Nodes():
	inDeg[NI.GetId()] = NI.GetInDeg()
	outDeg[NI.GetId()] = NI.GetOutDeg()

print outDeg


X = []
Y = []
for user_id in users:
	d = users[user_id]
	feature_vec = [int(d['Views']),int(d['DownVotes']),int(d['UpVotes']),outDeg[int(user_id)], 
		inDeg[int(user_id)]]
	y_val = float(d['Reputation'])
	X.append(feature_vec)
	Y.append(y_val)

X = X[:1000]
Y = Y[:1000]
K = 10
examplesPerFold = len(X) / K
print len(X)
models = [linear_model.LinearRegression(),SVR(kernel='rbf', C=1e3, gamma=0.1),  
		  SVR(kernel='linear', C=1e3), SVR(kernel='poly', C=1e3, degree=2),
		  linear_model.Ridge (alpha = .5), ]
models_names = ['linear','svr_rbf', 'svr_linear', 'svr_poly','ridge']
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







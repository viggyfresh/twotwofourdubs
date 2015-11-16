import math
import snap
import matplotlib.pyplot as plt
import cPickle
import collections
import numpy as np
from sklearn import linear_model

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


K = 10
examplesPerFold = len(X) / K
for i in range(K):
	print i
	testX = X[i * examplesPerFold: (i+1) * examplesPerFold]
	testY = Y[i * examplesPerFold: (i+1) * examplesPerFold]

	trainX = X[:i * examplesPerFold] + X[(i+1) * examplesPerFold:]
	trainY = Y[:i * examplesPerFold] + Y[(i+1) * examplesPerFold:]


	regr = linear_model.LinearRegression()
	regr.fit(np.array(trainX), np.array(trainY))

	# The coefficients
	print('Coefficients: \n', regr.coef_)
	# The mean square error
	print("Residual sum of squares: %.2f"
	      % np.mean((regr.predict(np.array(testX)) - np.array(testY)) ** 2))
	# Explained variance score: 1 is perfect prediction
	print('Variance score: %.2f' % regr.score(testX, testY))







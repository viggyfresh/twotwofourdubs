import math
import snap
import matplotlib.pyplot as plt
import cPickle
import collections
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR

G = snap.LoadEdgeList(snap.PNGraph, "parsed/geometry_qa.csv", 0, 1, ';')
print G.GetNodes()
#G = snap.GenRndGnm(snap.PNGraph, 100, 1000)
UNG = snap.ConvertGraph(snap.PUNGraph, G)


### Get data for all users
#users = cPickle.load(open("pickle/users.pickle",'r'))


#G = snap.GenRndGnm(snap.PUNGraph, 100, 1000)
print "Calculate degree centralities"
outDeg = collections.defaultdict(int)
inDeg = collections.defaultdict(int)

for NI in G.Nodes():
	inDeg[NI.GetId()] = NI.GetInDeg()
	outDeg[NI.GetId()] = NI.GetOutDeg()

print "Calculate closeness centrality"
closeCentr = {}
for NI in G.Nodes():
	closeCentr[NI.GetId()] = snap.GetClosenessCentr(UNG, NI.GetId())

print "Calculate betweenness centrality"
Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(UNG, Nodes, Edges, 1.0)

betweenness = {}
for node in Nodes:
	betweenness [node] = Nodes[node]

print "Eigenvector centrality"
eigVecCentr = {}
NIdEigenH = snap.TIntFltH()
snap.GetEigenVectorCentr(UNG, NIdEigenH)
for item in NIdEigenH:
	eigVecCentr [item] = NIdEigenH[item]


print "PageRank centrality"
pageRankCentr = {}
PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)
for item in PRankH:
	pageRankCentr[item] = PRankH[item]


with open('CentrFeatures.csv', 'w') as outfile:
	for NI in G.Nodes():
		features = [NI.GetId(),inDeg[NI.GetId()],outDeg[NI.GetId()],
					closeCentr[NI.GetId()], betweenness[NI.GetId()],
					eigVecCentr[NI.GetId()], pageRankCentr[NI.GetId()]]
		features = [str(x) for x in features]
		outfile.write(",".join(features) + "\n")




### Look at more advanced centrality measures
### Closeness, Betweenness, Eigenvector, Katz, PageRank, Cross-clique, Freeman Centralization

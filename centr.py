import math
import snap
import matplotlib.pyplot as plt


G = snap.LoadEdgeList(snap.PNGraph, "parsed/links.csv", 0, 1, ';')
UG = snap.ConvertGraph(snap.PUNGraph, G)

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

outDeg = {}
inDeg = {}

for NI in G.Nodes():
	inDeg[NI.GetId()] = NI.GetInDeg()
	outDeg[NI.GetId()] = NI.GetOutDeg()

print outDeg

# TODO correlate outDeg, inDeg with reputation


### Correlate betweenness with reputation
###
betweenCentr = {}
Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(UG, Nodes, Edges, 1.0)

for node in Nodes:
	betweenCentr[node] = Nodes[node]

print betweenCentr

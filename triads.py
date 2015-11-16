import math
import snap
import matplotlib.pyplot as plt
import collections

# G = snap.LoadEdgeList(snap.PNGraph, "parsed/userGraph.csv", 0, 1, ';')
# UG = snap.ConvertGraph(snap.PUNGraph, G)

# numTriads = snap.GetTriads(UG)
# print "NumTriads", numTriads
# print "NumNodes", G.GetNodes()




### Returns 
### 0 if no edge between
### 1 if only (i,j) edge
### 2 if only (j,i) edge
### 3 if double edged
def getCode(adj_set, i,j):
	edgeIToJ = i in adj_set and j in adj_set[i]
	edgeJToI = j in adj_set and i in adj_set[j]


	if not edgeIToJ and not edgeJToI: return 0
	if edgeIToJ and not edgeJToI: return 1
	if not edgeIToJ and edgeJToI: return 2
	if edgeIToJ and edgeJToI: return 3
	assert False


adj_lst = collections.defaultdict(list)
undirected_adj_lst = collections.defaultdict(list)

with open('parsed/geometry_qa.csv','r') as infile:
	for line in infile:
		src,dst = line.strip().split(';')
		src = int(src)
		dst = int(dst)
		adj_lst[src].append(dst)
		undirected_adj_lst[min(src,dst)].append(max(src,dst))

adj_set = {key: set(adj_lst[key]) for key in adj_lst}

nodes = sorted(adj_lst.keys())


def calcBaseFour(ij,jk,ik):
	return ik * 8 + jk * 4 + ij

def getTriadMap():
	codes = []
	for ij in range(4):
		for jk in range(4):
			for ik in range(4):
				code = calcBaseFour(ij,jk,ik)
				codes.append(code)

	values = []
	with open('triadMap.txt','r') as infile:
		for line in infile:
			values.append(int(line))

	assert len(codes) == len(values)

	triadMap = {item[0]:item[1] for item in zip(codes,values)}
	return triadMap
triadMap = getTriadMap()

triads = collections.defaultdict(int)
for i in nodes:
	neighbors = sorted(undirected_adj_lst[i])
	for j_id in range(len(neighbors)):
		for k_id in range(j_id+1,len(neighbors)):
			j = neighbors[j_id]
			k = neighbors[k_id]
			### Note that i < j < k
			### Note these triads have ordering, TODO reduce ordering

			ij = getCode(adj_set,i,j)
			jk = getCode(adj_set,j,k)
			ik = getCode(adj_set,i,k)

			code = calcBaseFour(ij,jk,ik)

			triads[triadMap[code]]+= 1

print triads







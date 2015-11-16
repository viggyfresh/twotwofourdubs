import snap
import random
import cPickle
import numpy as np
import operator
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

G = snap.LoadEdgeList(snap.PNGraph, "parsed/geometry_qa.csv", 0, 1, ';')


users = []
experts = {}
askers = {}
for ni in G.Nodes():
	src = ni.GetId()
	out_deg = ni.GetOutDeg()
	in_deg = ni.GetInDeg()
	users.append(src)
	experts[src] = in_deg
	askers[src] = out_deg

s_experts = sorted(experts.items(), key=operator.itemgetter(1), reverse=True)
s_askers = sorted(askers.items(), key=operator.itemgetter(1), reverse=True)

for i in range(0,5):
	print i
	print ('User id: %d In degree: %d' % (s_experts[i][0],s_experts[i][1]))
	print ('User id: %d Out degree: %d' % (s_askers[i][0],s_askers[i][1]))

user_data = cPickle.load(open("pickle/users.pickle",'r'))

X = []
for user_id in users:
	u = user_data[str(user_id)]
	f_vec = [int(u['Views']),int(u['DownVotes']),int(u['UpVotes']),askers[user_id], experts[user_id]]
	X.append(f_vec)

fig = plt.figure(1)
fig.suptitle("K-Means Clustering: Users Contributing to Geometry Posts")

X = np.reshape(X, (len(X),5))
y_pred = KMeans(n_clusters=2).fit_predict(X)
ax1 = fig.add_subplot(221)
ax1.scatter(X[:, 0], X[:, 1], c=y_pred)
ax1.set_title("Number of Clusters = 2")
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)

y_pred = KMeans(n_clusters=3).fit_predict(X)
ax2 = fig.add_subplot(222)
ax2.scatter(X[:, 0], X[:, 1], c=y_pred)
ax2.set_title("Number of Clusters = 3")
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

y_pred = KMeans(n_clusters=4).fit_predict(X)
ax3 = fig.add_subplot(223)
ax3.scatter(X[:, 0], X[:, 1], c=y_pred)
ax3.set_title("Number of Clusters = 4")
ax3.xaxis.set_visible(False)
ax3.yaxis.set_visible(False)

y_pred = KMeans(n_clusters=5).fit_predict(X)
ax4 = fig.add_subplot(224)
ax4.scatter(X[:, 0], X[:, 1], c=y_pred)
ax4.set_title("Number of Clusters = 5")
ax4.xaxis.set_visible(False)
ax4.yaxis.set_visible(False)

plt.show()

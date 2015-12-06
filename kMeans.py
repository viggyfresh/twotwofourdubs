import snap
import random
import cPickle
import numpy as np
import operator
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import KMeans
from scipy.cluster.vq import kmeans2
from sklearn.metrics import silhouette_samples, silhouette_score
import csv


# G = snap.LoadEdgeList(snap.PNGraph, "parsed/geometry_qa.csv", 0, 1, ';')

# users = []
# experts = {}
# askers = {}
# for ni in G.Nodes():
# 	src = ni.GetId()
# 	out_deg = ni.GetOutDeg()
# 	in_deg = ni.GetInDeg()
# 	users.append(src)
# 	experts[src] = in_deg
# 	askers[src] = out_deg

# s_experts = sorted(experts.items(), key=operator.itemgetter(1), reverse=True)
# s_askers = sorted(askers.items(), key=operator.itemgetter(1), reverse=True)

# for i in range(0,5):
# 	print i
# 	print ('User id: %d In degree: %d' % (s_experts[i][0],s_experts[i][1]))
# 	print ('User id: %d Out degree: %d' % (s_askers[i][0],s_askers[i][1]))

# user_data = cPickle.load(open("pickle/users.pickle",'r'))

# X = []
# for user_id in users:
# 	u = user_data[str(user_id)]
# 	f_vec = [int(u['Views']),int(u['DownVotes']),int(u['UpVotes']),askers[user_id], experts[user_id]]
# 	X.append(f_vec)

# id,Views,DownVotes,UpVotes,Reputation,DaysSinceCreation,DaysSinceAccess
users = {}
with open("UserFeatures.csv") as f:
	next(f)
	reader = csv.reader(f)
	for row in reader:
		u_id = row[0]
		f_vec = []
		for x in range(1,4):
			f_vec.append(float(row[x]))
		users[u_id] = f_vec

# id,inDeg,outDeg,closeCentr,betCentr,eigVecCentr,pageRankCentr
X = []
with open("CentrFeatures.csv") as f:
	next(f)
	reader = csv.reader(f)
	for row in reader:
		u_id = row[0]
		f_vec = users[u_id]
		for x in range(1,3):
			f_vec.append(float(row[x]))
		f_vec.append(float(row[3]))
		f_vec.append(float(row[5]))
		f_vec.append(float(row[6]))
		X.append(f_vec)

fig = plt.figure(1)
fig.suptitle("K-Means Clustering: Users Contributing to Geometry Posts")

X = np.reshape(X, (len(X),8))
y_pred = KMeans(n_clusters=2).fit_predict(X)
ax2 = fig.add_subplot(222)
# ax2.scatter(X[:, 0], X[:, 1], c=y_pred)
# ax2.set_title("Number of Clusters = 2")
# ax2.xaxis.set_visible(False)
# ax2.yaxis.set_visible(False)
silhouette_avg = silhouette_score(X, y_pred)
print("For n_clusters = 2 The average silhouette_score is :", silhouette_avg)
sample_silhouette_values = silhouette_samples(X, y_pred)

y_lower = 10
n_clusters = 2
ax1 = fig.add_subplot(221)
for i in range(n_clusters):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = \
        sample_silhouette_values[y_pred == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.spectral(float(i) / n_clusters)
    ax1.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color, edgecolor=color, alpha=0.7)

    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

ax1.set_title("The silhouette plots")

# The vertical line for average silhoutte score of all the values
ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

ax1.set_yticks([])  # Clear the yaxis labels / ticks
ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

# 2nd Plot showing the actual clusters formed
colors = cm.spectral(y_pred.astype(float) / n_clusters)
ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
            c=colors)

ax2.set_title("n = 2 Clusters")
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

y_pred = KMeans(n_clusters=3).fit_predict(X)
ax4 = fig.add_subplot(224)
silhouette_avg = silhouette_score(X, y_pred)
print("For n_clusters = 3 The average silhouette_score is :", silhouette_avg)
sample_silhouette_values = silhouette_samples(X, y_pred)

y_lower = 10
n_clusters = 3
ax3 = fig.add_subplot(223)
for i in range(n_clusters):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = \
        sample_silhouette_values[y_pred == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.spectral(float(i) / n_clusters)
    ax3.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color, edgecolor=color, alpha=0.7)
    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

# The vertical line for average silhoutte score of all the values
ax3.axvline(x=silhouette_avg, color="red", linestyle="--")

ax3.set_yticks([])  # Clear the yaxis labels / ticks
ax3.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

# 2nd Plot showing the actual clusters formed
colors = cm.spectral(y_pred.astype(float) / n_clusters)
ax4.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
            c=colors)

ax4.set_title("n = 3 Clusters")
ax4.xaxis.set_visible(False)
ax4.yaxis.set_visible(False)


# y_pred = KMeans(n_clusters=3).fit_predict(X)
# ax2 = fig.add_subplot(224)
# ax2.scatter(X[:, 0], X[:, 1], c=y_pred)
# ax2.set_title("Number of Clusters = 3")
# ax2.xaxis.set_visible(False)
# ax2.yaxis.set_visible(False)

# fig2 = plt.figure(2)
# fig2.suptitle("K-Means Clustering: Users Contributing to Geometry Posts")

# y_pred = KMeans(n_clusters=4).fit_predict(X)
# ax3 = fig2.add_subplot(222)
# ax3.scatter(X[:, 0], X[:, 1], c=y_pred)
# ax3.set_title("Number of Clusters = 4")
# ax3.xaxis.set_visible(False)
# ax3.yaxis.set_visible(False)

# y_pred = KMeans(n_clusters=5).fit_predict(X)
# ax4 = fig2.add_subplot(224)
# ax4.scatter(X[:, 0], X[:, 1], c=y_pred)
# ax4.set_title("Number of Clusters = 5")
# ax4.xaxis.set_visible(False)
# ax4.yaxis.set_visible(False)

fig2 = plt.figure(2)
fig2.suptitle("K-Means Clustering: Users Contributing to Geometry Posts")
y_pred = KMeans(n_clusters=4).fit_predict(X)
ax6 = fig2.add_subplot(222)
# ax2.scatter(X[:, 0], X[:, 1], c=y_pred)
# ax2.set_title("Number of Clusters = 2")
# ax2.xaxis.set_visible(False)
# ax2.yaxis.set_visible(False)
silhouette_avg = silhouette_score(X, y_pred)
print("For n_clusters = 4 The average silhouette_score is :", silhouette_avg)
sample_silhouette_values = silhouette_samples(X, y_pred)

y_lower = 10
n_clusters = 4
ax5 = fig2.add_subplot(221)
for i in range(n_clusters):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = \
        sample_silhouette_values[y_pred == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.spectral(float(i) / n_clusters)
    ax5.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color, edgecolor=color, alpha=0.7)
    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

ax5.set_title("The silhouette plots")

# The vertical line for average silhoutte score of all the values
ax5.axvline(x=silhouette_avg, color="red", linestyle="--")

ax5.set_yticks([])  # Clear the yaxis labels / ticks
ax5.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

# 2nd Plot showing the actual clusters formed
colors = cm.spectral(y_pred.astype(float) / n_clusters)
ax6.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
            c=colors)

ax6.set_title("n = 4 Clusters")
ax6.xaxis.set_visible(False)
ax6.yaxis.set_visible(False)

y_pred = KMeans(n_clusters=5).fit_predict(X)
ax8 = fig2.add_subplot(224)
silhouette_avg = silhouette_score(X, y_pred)
print("For n_clusters = 5 The average silhouette_score is :", silhouette_avg)
sample_silhouette_values = silhouette_samples(X, y_pred)

y_lower = 10
n_clusters = 5
ax7 = fig2.add_subplot(223)
for i in range(n_clusters):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = \
        sample_silhouette_values[y_pred == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.spectral(float(i) / n_clusters)
    ax7.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color, edgecolor=color, alpha=0.7)

    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

# The vertical line for average silhoutte score of all the values
ax7.axvline(x=silhouette_avg, color="red", linestyle="--")

ax7.set_yticks([])  # Clear the yaxis labels / ticks
ax7.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

# 2nd Plot showing the actual clusters formed
colors = cm.spectral(y_pred.astype(float) / n_clusters)
ax8.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
            c=colors)

ax8.set_title("n = 5 Clusters")
ax8.xaxis.set_visible(False)
ax8.yaxis.set_visible(False)

plt.show()


# ('For n_clusters = 2 The average silhouette_score is :', 0.97279015433590943)
# ('For n_clusters = 3 The average silhouette_score is :', 0.95940627514705934)
# ('For n_clusters = 4 The average silhouette_score is :', 0.91125797659193941)
# ('For n_clusters = 5 The average silhouette_score is :', 0.88663965383489796)


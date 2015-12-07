import math
import snap
import cPickle
import csv
from collections import defaultdict
import operator
from scipy.stats import spearmanr

# Params: reputation, badges, UpVotes, DownVotes
# Computed params:  in/out degree, centrality score
def domain_expertise(reputation, badges, upvotes, downvotes, indegree, outdegree, centrs):
    # return float(reputation)
    # return float(indegree) - float(outdegree)
    # return (float(indegree) - float(outdegree)) * (float(upvotes) - float(downvotes))
    # return float(centrs[1])
    # return float(centrs[2])
    return float(centrs[3]) * float(badges)

g = snap.LoadEdgeList(snap.PNGraph, "parsed/geometry_qa.csv", 0, 1, ';')
ug = snap.ConvertGraph(snap.PUNGraph, g)
users = cPickle.load(open('pickle/users.pickle'))
badges = cPickle.load(open('pickle/badges.pickle'))
user_to_posts = cPickle.load(open('pickle/user_to_posts.pickle'))
# centrality scores
centralities = {}

# centralities[user_id] = [closeCentr,betCentr,eigVecCentr,pageRankCentr]
with open("CentrFeatures.csv") as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        centralities[row[0]] = row[3:]

expertise = defaultdict(float)

for node in g.Nodes():
    id = str(node.GetId())
    user = users[id]
    badge = badges[id]
    posts = user_to_posts[id]

    rep = user["Reputation"]
    b = len(badge)
    upvotes = user["UpVotes"]
    downvotes = user["DownVotes"]
    indegree = node.GetInDeg()
    outdegree = node.GetOutDeg()
    c = centralities[id]
    expertise[id] = domain_expertise(rep, b, upvotes, downvotes, indegree, outdegree, c)

experts = sorted(expertise.items(), key=operator.itemgetter(1), reverse=True)
ids = []
for i in xrange(10):
    id = experts[i][0]
    ids.append(int(id))
    expertise = experts[i][1]
    print "%s - %s - %f" % (id, users[id]["DisplayName"], expertise)
print ids

ranks = []
ranks.append([6312, 12042, 622, 6179, 742, 232, 8508, 13854, 1827, 242])
ranks.append([35416, 1827, 6312, 409, 1303, 39174, 44121, 6622, 42351, 33337])
ranks.append([1827, 6312, 9003, 11667, 589, 13854, 39174, 8269, 498, 1303])
ranks.append([35416, 1827, 409, 6312, 1303, 42351, 39174, 237, 31744, 44121])
ranks.append([35416, 1827, 409, 1303, 6312, 42351, 44121, 39174, 31744, 95860])
ranks.append([14366, 6312, 1827, 39174, 13854, 6622, 409, 44121, 35416, 8508])

for i in xrange(2, 6):
    print "Spearman Rank: %f" % spearmanr(ranks[1], ranks[i])[0]

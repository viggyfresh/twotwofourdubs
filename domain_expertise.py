import math
import snap
import cPickle
from collections import defaultdict
import operator

# Params: reputation, badges, UpVotes, DownVotes
# Computed params:  in/out degree, centrality score
def domain_expertise(reputation, badges, upvotes, downvotes, indegree, outdegree, centrality):
    return float(reputation)
    # return float(indegree) - float(outdegree)
    # return (float(indegree) - float(outdegree)) * (float(upvotes) - float(downvotes))

g = snap.LoadEdgeList(snap.PNGraph, "parsed/geometry_qa.csv", 0, 1, ';')
ug = snap.ConvertGraph(snap.PUNGraph, g)
users = cPickle.load(open('pickle/users.pickle'))
badges = cPickle.load(open('pickle/badges.pickle'))
user_to_posts = cPickle.load(open('pickle/user_to_posts.pickle'))
# centrality scores
centralities = snap.TIntFltH()
temp = snap.TIntPrFltH()
#snap.GetBetweennessCentr(ug, centralities, temp, 0.25)

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
    #centrality = centralities[id]
    centrality = None
    expertise[id] = domain_expertise(rep, b, upvotes, downvotes, indegree, outdegree, centrality)

experts = sorted(expertise.items(), key=operator.itemgetter(1), reverse=True)
for i in xrange(10):
    id = experts[i][0]
    expertise = experts[i][1]
    print "%s - %s - %f" % (id, users[id]["DisplayName"], expertise)

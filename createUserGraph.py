from collections import defaultdict
import pickle

posts = pickle.load(open("pickle/posts.pickle",'r'))
#users = pickle.load("pickle/users.pickle")

edges = defaultdict(list)

for post in posts:
	if "<Geometry>" in post["Tags"]:
		if post["PostTypeId"] == "2":
			edges[post["ParentID"]["OwnerUserId"]].append(post["OwnerUserId"])

with open('parsed/userGraph.csv','w') as outfile:
	for src_id in edges:
		dst_ids = edges[src_id]
		for dst_id in dst_ids:
			outfile.write("{0};{1}\n".format(src_id, dst_id))

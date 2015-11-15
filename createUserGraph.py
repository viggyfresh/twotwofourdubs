from collections import defaultdict
import cPickle

posts = cPickle.load(open("pickle/posts.pickle",'r'))
#users = cPickle.load("pickle/users.pickle")

edges = defaultdict(list)

for p_id in posts:
	post = posts[p_id]
	if post["PostTypeId"] == "2":
		parent_post = posts[post["ParentId"]]
		if "Tags" in parent_post and "<geometry>" in parent_post['Tags']:
			if "OwnerUserId" in parent_post and "OwnerUserId" in post:
				edges[parent_post["OwnerUserId"]].append(post["OwnerUserId"])

with open('parsed/userGraph.csv','w') as outfile:
	for src_id in edges:
		dst_ids = edges[src_id]
		for dst_id in dst_ids:
			outfile.write("{0};{1}\n".format(src_id, dst_id))

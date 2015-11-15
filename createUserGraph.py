from collections import defaultdict
import pickle

posts = pickle.load("pickle/posts.pickle")
users = pickle.load("pickle/users.pickle")

edges = defaultdict(list)

for post in posts:
	if "<Geometry>" in post["Tags"]:
		if post["PostTypeId"] == "2":
			edges[post["ParentID"]["OwnerUserId"]].append(post["OwnerUserId"])


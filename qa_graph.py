from collections import defaultdict
import cPickle

def qa_graph_by_tag(out_filename, tag_name):
    posts = cPickle.load(open("pickle/posts.pickle",'r'))
    edges = defaultdict(set)

    for p_id in posts:
    	post = posts[p_id]
    	if post["PostTypeId"] == "2":
    		parent_post = posts[post["ParentId"]]
    		if "Tags" in parent_post and tag_name in parent_post['Tags']:
    			if "OwnerUserId" in parent_post and "OwnerUserId" in post:
    				edges[parent_post["OwnerUserId"]].add(post["OwnerUserId"])

    with open(out_filename,'wb') as outfile:
    	for src_id in edges:
    		dst_ids = edges[src_id]
    		for dst_id in dst_ids:
    			outfile.write("{0};{1}\n".format(src_id, dst_id))

qa_graph_by_tag("parsed/geometry_qa.csv", "<geometry>")

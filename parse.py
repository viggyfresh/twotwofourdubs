from collections import defaultdict
import numpy as np
import xml.etree.ElementTree as ET
import cPickle

def pickle_posts(post_filename, out_filename):
    tree = ET.parse(post_filename)
    root = tree.getroot()
    posts = {}
    fields = ["Id", "PostTypeId", "ParentId", "AcceptedAnswerId", "Score", "ViewCount", "OwnerUserId", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount"]
    for i, child in enumerate(root):
        attrs = child.attrib
        post = { field: attrs[field] for field in fields if field in attrs }
        posts[post["Id"]] = post
    with open(out_filename, "wb") as outfile:
        cPickle.dump(posts, outfile)

def pickle_users(user_filename, out_filename):
    tree = ET.parse(user_filename)
    root = tree.getroot()
    users = {}
    fields = ["Id", "Reputation", "CreationDate", "DisplayName", "LastAccessDate", "Location", "Age", "Views", "UpVotes", "DownVotes"]
    for i, child in enumerate(root):
        attrs = child.attrib
        user = { field: attrs[field] for field in fields if field in attrs }
        users[user["Id"]] = user
    with open(out_filename, "wb") as outfile:
        cPickle.dump(users, outfile)

def pickle_badges(badge_filename, out_filename):
    tree = ET.parse(badge_filename)
    root = tree.getroot()
    badges = defaultdict(list)
    fields = ["UserId", "Name", "Date"]
    for i, child in enumerate(root):
        attrs = child.attrib
        badge = { field: attrs[field] for field in fields if field in attrs }
        badges[badge["UserId"]].append(badge)
    with open(out_filename, "wb") as outfile:
        cPickle.dump(badges, outfile)

def pickle_user_to_posts(post_filename, out_filename):
    tree = ET.parse(post_filename)
    root = tree.getroot()
    user_to_posts = defaultdict(list)
    fields = ["Id", "PostTypeId", "ParentId", "AcceptedAnswerId", "Score", "ViewCount", "OwnerUserId", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount"]
    for i, child in enumerate(root):
        attrs = child.attrib
        post = { field: attrs[field] for field in fields if field in attrs }
        if "OwnerUserId" in post:
            user_to_posts[post["OwnerUserId"]] = post
    with open(out_filename, "wb") as outfile:
        cPickle.dump(user_to_posts, outfile)

def parse_links(link_filename, out_filename):
    tree = ET.parse(link_filename)
    root = tree.getroot()
    with open(out_filename, "wb") as outfile:
        for child in root:
            attrs = child.attrib
            outfile.write("%s;%s\n" % (attrs["PostId"], attrs["RelatedPostId"]))

#def parse_links_partitioned(link_filename, out_filename, tag_ids):

def parse_tags(tag_filename):
    tag_tree = ET.parse(tag_filename)
    tag_root = tag_tree.getroot()
    tag_ids = {}
    tag_counts = {}
    for i, child in enumerate(tag_root):
        tag_name = child.attrib["TagName"]
        tag_ids[tag_name] = i
        tag_counts[tag_name] = int(child.attrib["Count"])
    return tag_ids, tag_counts

def parse_posts_with_tag(post_filename, tag_name):
    tree = ET.parse(post_filename)
    root = tree.getroot()
    tag_post_ids = set()
    for child in root:
        attrs = child.attrib
        if "Tags" in attrs and tag_name in attrs["Tags"]:
            tag_post_ids.add(int(attrs["Id"]))
    return tag_post_ids

def parse_links_with_tag(link_filename, out_filename, tag_post_ids):
    tree = ET.parse(link_filename)
    root = tree.getroot()
    with open(out_filename, "wb") as outfile:
        for child in root:
            attrs = child.attrib
            if int(attrs["PostId"]) in tag_post_ids or int(attrs["RelatedPostId"]) in tag_post_ids:
                outfile.write("%s;%s\n" % (attrs["PostId"], attrs["RelatedPostId"]))

def pickle_all():
    pickle_posts("data/small/Posts.xml", "pickle/posts.pickle")
    pickle_users("data/small/Users.xml", "pickle/users.pickle")
    pickle_badges("data/small/Badges.xml", "pickle/badges.pickle")
    pickle_user_to_posts("data/small/Posts.xml", "pickle/user_to_posts.pickle")

pickle_all()

#parse_links("data/small/PostLinks.xml", "parsed/links.csv")
#tag_post_ids = parse_posts_with_tag("data/small/Posts.xml", "<geometry>")
#parse_links_with_tag("data/small/PostLinks.xml", "parsed/geometry_links.csv", tag_post_ids)

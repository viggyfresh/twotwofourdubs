import math
import snap
import matplotlib.pyplot as plt
import cPickle
import collections
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR
import datetime

### Get data for all users
users = cPickle.load(open("pickle/users.pickle",'r'))

    # - Id
    # - Reputation
    # - CreationDate
    # - DisplayName
    # - EmailHash
    # - LastAccessDate
    # - WebsiteUrl
    # - Location
    # - Age
    # - AboutMe
    # - Views
    # - UpVotes
    # - DownVotes

with open('UserFeatures.csv', 'w') as outfile:
	outfile.write('Views,DownVotes,UpVotes,Reputation,DaysSinceCreation,DaysSinceAccess\n')
	for user_id in users:
		d = users[user_id]
		createdTime = datetime.datetime.strptime(d['CreationDate'], "%Y-%m-%dT%H:%M:%S.%f")
		lastAccessTime = datetime.datetime.strptime(d['LastAccessDate'], "%Y-%m-%dT%H:%M:%S.%f")

		creationDelta = (datetime.datetime.now() - createdTime).days
		lastAccessDelta = (datetime.datetime.now() - lastAccessTime).days

		feature_vec = [int(d['Views']),int(d['DownVotes']),int(d['UpVotes']), 
					   float(d['Reputation']), creationDelta, lastAccessDelta]
		feature_vec = [str(x) for x in feature_vec]
		outfile.write(','.join(feature_vec) + "\n")




		
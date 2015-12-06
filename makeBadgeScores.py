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
infile = open('data/small/Badges.xml','r')

allBadges = collections.defaultdict(lambda : collections.defaultdict(int))
keySet = set([])

for line in infile:
    line = line.strip()
    if 'row Id="' in line: 
        userId = line.split('UserId="')[1].split('"')[0]
        badgeName = line.split('Name="')[1].split('"')[0]
        keySet.add(badgeName)
        allBadges[userId][badgeName] += 1


outfile = open('UserBadgesFeatures.csv','w')
keyOrdering = list(keySet)
outfile.write(','.join(keyOrdering) + '\n')
for user in allBadges:
    featureList = [str(user)]
    for key in keyOrdering:
        featureList.append(allBadges[user][key])
    featureList = [str(x) for x in featureList]
    outfile.write(','.join(featureList) + '\n')

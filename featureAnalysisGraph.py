import matplotlib.pyplot as plt
import numpy as np

labels = "inDeg,outDeg,closeCentr,betCentr,eigVecCentr,pageRankCentr,Views,DownVotes,UpVotes,Reputation,DaysSinceCreation,DaysSinceAccess"
labels = labels.split(',')

values = [0.573558443941,-0.0096658620718,-1.76693231444e-05,0.433470519625,0.290128734497,0.390468475254,0.882237811207,0.232481082445,0.604550878865,1.0,0.156824069779,-0.107835431033]

zipped = zip(values,labels)
zipped = sorted(zipped, reverse=True)
values, labels = zip(*zipped)

# print labels
# print values

n_groups = len(values)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4

rects1 = plt.bar(index, values, bar_width,
                 alpha=opacity,
                 color='b')
plt.xlabel('Features')
plt.ylabel('CorrCoef with Reputation')
plt.title('Correlation Analysis against Reputation')
plt.xticks(index + bar_width, labels)
locs, labels = plt.xticks()
plt.setp(labels, rotation=-45)
#plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.35)
plt.savefig('images/correlationAnalysis.jpg')
# plt.show()
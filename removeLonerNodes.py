import collections

outNodes = collections.defaultdict(list)
inNodes = collections.defaultdict(list)
with open('parsed/links.csv','r') as infile:
	for line in infile:
		a,b = line.strip().split(';')
		outNodes[a].append(b)
		inNodes[b].append(a)

with open('parsed/removeLonerLinks.csv','w') as outfile:
	for key in outNodes:

		### Do not include if no out and in edges
		if len(outNodes[key]) == 0 and len(inNodes[key]) == 0: continue
		for v in outNodes[key]:
			outfile.write('{0};{1}\n'.format(key,v))



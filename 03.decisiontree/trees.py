from math import log

def calcShannonent(dataset):
	numentries = len(dataset)
	labelcounts = {}
	for featurevec in dataset:
		currentlabel = featurevec[-1]
		labelcounts.setdefault(currentlabel, 0)
		labelcounts[currentlabel] += 1
	shannonent = 0.0
	for key in labelcounts:
		prob = labelcounts[key] / numentries
		shannonent -= prob * log(prob, 2)
	return shannonent

def createdataset():
	dataset = [[1, 1, 'yes'],
			   [1, 1, 'yes'],
			   [1, 0, 'no'],
			   [0, 1, 'no'],
			   [0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	return dataset, labels

def splitdataset(dataset, axis, value):
	returndataset = []
	for featurevec in dataset:
		if featurevec[axis] == value:
			reducefeaturevec = featurevec[:axis]
			reducefeaturevec.extend(featurevec[axis+1:])
			returndataset.append(reducefeaturevec)
	return returndataset

def choosebestfeaturetosplit(dataset):
	numfeatures = len(dataset[0]) - 1
	baseentroy = calcShannonent(dataset)
	bestinfogain = 0.0
	bestfeature = -1
	for i in range(numfeatures):
		featurelist = [example[i] for example in dataset]
		uniqueval = set(featurelist)
		newentroy = 0.0
		for value in uniqueval:
			subdataset = splitdataset(dataset, i, value)
			prob = len(subdataset) / len(dataset)
			newentroy += prob * calcShannonent(subdataset)
		infogain = baseentroy - newentroy
		if infogain > bestinfogain:
			bestinfogain = infogain
			bestfeature = i
	return bestfeature

def majoritycnt(classlist):
	classcount = {}
	for vote in classlist:
		classcount.setdefault(vote, 0)
		classcount[vote] += 1
	sortedclasscount = sorted(classcount.items(), key=lambda x:x[1], reverse=True)
	return sortedclasscount[0][0]

def createtree(dataset, labels):
	classlist = [example[-1] for example in dataset]
	if classlist.count(classlist[0]) == len(classlist):
		return classlist[0]
	if len(dataset[0]) == 1:
		return majoritycnt(classlist)
	bestfeature = choosebestfeaturetosplit(dataset)
	bestfeaturelabel = labels[bestfeature]
	mytree = {bestfeaturelabel: {}}
	featurevalues = [example[bestfeature] for example in dataset]
	uniqueval = set(featurevalues)
	sublabels = labels[:]
	del(sublabels[bestfeature])
	for value in uniqueval:
		mytree[bestfeaturelabel][value] = createtree(splitdataset(dataset, bestfeature, value), sublabels)
	return mytree

def classify(inputtree, featlabels, testvec):
	firststr = list(inputtree.keys())[0]
	seconddict = inputtree[firststr]
	featindex = featlabels.index(firststr)
	for key in seconddict:
		if testvec[featindex] == key:
			if type(seconddict[key]).__name__ == 'dict':
				classlabel = classify(seconddict[key], featlabels, testvec)
			else:	classlabel = seconddict[key]
	return classlabel

def storetree(inputtree, filename):
	import pickle
	fw = open(filename, 'wb')
	pickle.dump(inputtree, fw)
	fw.close()

def grabtree(filename):
	import pickle
	fr = open(filename, 'rb')
	return pickle.load(fr)




























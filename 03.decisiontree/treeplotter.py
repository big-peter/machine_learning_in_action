import matplotlib.pyplot as plt

decisionnode = dict(boxstyle="sawtooth", fc="0.8")
leafnode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotnode(nodetxt, centerpt, parentpt, nodetype):
	createplot.axl.annotate(nodetxt, xy=parentpt, xycoords="axes fraction",xytext=centerpt, \
		textcoords="axes fraction", va="center", ha="center", bbox=nodetype, arrowprops=arrow_args)

'''
def createplot():
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	createplot.axl = plt.subplot(111, frameon=False)
	plotnode("decisionnode", (0.5, 0.1), (0.1, 0.5), decisionnode)
	plotnode("leafnode", (0.8, 0.1), (0.3, 0.8), leafnode)
	plt.show()
'''

def getNumLeafs(mytree):
	numleafs = 0
	firststr = list(mytree.keys())[0]
	seconddict = mytree[firststr]
	for key in seconddict:
		if type(seconddict[key]).__name__ == 'dict':
			numleafs += getNumLeafs(seconddict[key])
		else:	numleafs += 1
	return numleafs

def getTreeDepth(mytree):
	maxDepth = 0
	firstStr = list(mytree.keys())[0]
	secondDict = mytree[firstStr]
	for key in secondDict:
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = 1 + getTreeDepth(secondDict[key])
		else:	thisDepth = 1
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth

def retrieveTree(i):
	listOfTrees = [{ 'no surfacing': { 0: 'no', 1: { 'flippers': { 0: 'no', 1: 'yes'}}}},
				   { 'no surfacing': { 0: 'no', 1: { 'flippers': { 0: { 'head': { 0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
	return listOfTrees[i]

def plotMidText(cntrPt, parentpt, txtString):
	xMid = (parentpt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
	yMid = (parentpt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
	createplot.axl.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
	numleafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)
	firstStr = list(myTree.keys())[0]
	cntrPt = (plotTree.xOff + (1.0 + float(numleafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
	plotMidText(cntrPt, parentPt, nodeTxt)
	plotnode(firstStr, cntrPt, parentPt, decisionnode)
	secondDict = myTree[firstStr]
	plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
	for key in secondDict:
		if type(secondDict[key]).__name__ == 'dict':
			plotTree(secondDict[key], cntrPt, str(key))
		else:
			plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
			plotnode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafnode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
	plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def createplot(inTree):
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	axprops = dict(xticks=[], yticks=[])
	createplot.axl = plt.subplot(111, frameon=False, **axprops)
	plotTree.totalW = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	plotTree.xOff = -0.5 / plotTree.totalW;
	plotTree.yOff = 1.0;
	plotTree(inTree, (0.5, 1.0), '')
	plt.show()


































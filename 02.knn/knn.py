from os import listdir
from numpy import *
import matplotlib
import matplotlib.pyplot as plt

lovedict = {'didntLike':1, 'smallDoses':2, 'largeDoses':3}

def createdataset():
	group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']
	return group, labels

def classify0(inx, dataset, labels, k):
	datasetsize = dataset.shape[0]
	diffmat = tile(inx, (datasetsize, 1)) - dataset
	sqdiffmat = diffmat ** 2
	sqdistances = sqdiffmat.sum(axis=1)
	distances = sqdistances ** 0.5
	sorteddistindicies = distances.argsort()
	classcount = {}
	for i in range(k):
		voteilabel = labels[sorteddistindicies[i]]
		classcount[voteilabel] = classcount.get(voteilabel, 0) + 1
	sortedclasscount = sorted(classcount.items(), key=lambda x:x[1], reverse=True)
	return sortedclasscount[0][0]

def file2matrix(filename):
	f = open(filename)
	arrayoflines = f.readlines()
	numberoflines = len(arrayoflines)
	returnmatrix = zeros((numberoflines, 3))
	classlabelvector = []
	index = 0
	for line in arrayoflines:
		line = line.strip()
		listfromline = line.split('\t')
		returnmatrix[index, :] = listfromline[0:3]
		classlabelvector.append(int(listfromline[-1]))
		index += 1
	return returnmatrix, classlabelvector

def printfigure(matrix, label):
	fig = plt.figure()
	ax = fig.add_subplot(221)
	ax.scatter(matrix[:,0], matrix[:,1], c=array(label), s=array(label))
	
	ax = fig.add_subplot(222)
	ax.scatter(matrix[:,0], matrix[:,2], array(label), array(label))
	
	ax = fig.add_subplot(223)
	ax.scatter(matrix[:,1], matrix[:,2], array(label), array(label))
	
	plt.show()
	plt.savefig('sampledistribution.png')

def autonorm(dataset):
	minvals = dataset.min(0)
	maxvals = dataset.max(0)
	ranges = maxvals - minvals
	normdataset = zeros(shape(dataset))
	m = dataset.shape[0]
	normdataset = dataset - tile(minvals, (m,1))
	normdataset = normdataset / tile(ranges, (m,1))
	return normdataset, ranges, minvals

def datingClassTest():
    hoRatio = 0.50      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autonorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print("the classifier came back with: {}, the real answer is: {}".format(classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print("the total error rate is: %f" % (errorCount/float(numTestVecs)))
    print(errorCount)
    
def img2vector(filename):
	returnvect = zeros((1,1024))
	f = open(filename)
	for i in range(32):
		linestr = f.readline()
		for j in range(32):
			returnvect[0, 32 * i + j] = int(linestr[j])
	return returnvect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount/float(mTest)))










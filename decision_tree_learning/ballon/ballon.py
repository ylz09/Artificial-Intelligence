from math import log
import operator
from random import seed
from random import randrange
from csv import reader
from collections import Counter

# Load a CSV file
def load_csv(filename):
    file = open(filename, "rb")
    lines = reader(file)
    dataset = list(lines)
    return dataset

def createDataSet():
    dataSet=load_csv('4')
    labels = ['color','size','act','age']
    return dataSet, labels

def infoGain(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1      
    entropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        entropy -= prob * log(prob, 2)
    return entropy

def majority(classList):
    cnt = Counter(classList)
    value, count = c.most_common()[0]
    return value

def getBestSplitFeature(dataSet):
    # information gain and information gain ratio are almost same accuracy here!
    # can also choose other methods to split
    numFeatures = len(dataSet[0]) - 1                 
    baseEntropy = infoGain(dataSet)             
    #bestInfoGainRatio = 0.0
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        valList = [row[i] for row in dataSet]  
        uniqueVals = set(valList)                      
        newEntropy = 0.0
        splitInfo = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)  
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * infoGain(subDataSet)
            splitInfo += -prob * log(prob, 2)
        gain = baseEntropy - newEntropy              
        if (splitInfo == 0): # fix the overflow bug
            continue
        #info gain
        if (gain> bestInfoGain):          
            bestInfoGain= gain
            bestFeature = i                              

        #info gain ratio
        #gainRatio = gain / splitInfo             
        #if (gainRatio > bestInfoGainRatio):          
        #    bestInfoGainRatio = gainRatio
        #    bestFeature = i                              

    return bestFeature

# modify here to adapt the continous cases
# this is not split, just a filter
def splitDataSet(dataSet, splitFeature, value):
    # split data set by a feature's value
    retDataSet = []
    for featVec in dataSet:
        if featVec[splitFeature] == value: # equal choose, else ignore
            reduceFeatVec = featVec[:splitFeature]  # delete the used feature     
            reduceFeatVec.extend(featVec[splitFeature+1:])
            retDataSet.append(reduceFeatVec)            
    return retDataSet

def createTree(dataSet, labels):
    classList = [row[-1] for row in dataSet]   
    # all the records belong to same class, no need split just return the class
    if classList.count(classList[0]) == len(classList):
        return classList[0]                                 
    # all the records have different attribute, we just pick the majority one as the final class
    if len(dataSet[0]) == 1:                               
        return majority(classList)
    # find the best feature and get all the possible unique values
    bestFeat = getBestSplitFeature(dataSet)             
    featureName = labels[bestFeat]                         
    tree = {featureName:{}}                   
    del(labels[bestFeat])                                   
    featValues = [row[bestFeat] for row in dataSet]  
    uniqueVals = set(featValues)

    for value in uniqueVals:
        subLabels = labels[:]                              
        tree[featureName][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
        
    return tree

def predict1(inputTree, featLabels, testVec):
    feature = inputTree.keys()[0]
    featureIndex = featLabels.index(feature)
    val = testVec[featureIndex]
    print('value: %d' % val)

    children = inputTree[feature]
    #print(children)

    for first,second in children.iteritems():
        #print(key)
        #print(val)
        #print('val: %d, node: %s' % (val, first))
        if int(first) == val:
            if type(second).__name__ != 'dict':
                return second 
            else:
                predict(second,featLabels,testVec)
        #else
        #    return predict(yi)

def predict(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    #print(firstStr)
    secondDict = inputTree[firstStr]   
    featIndex = featLabels.index(firstStr) 
    for key in secondDict.keys():         
        #print('[%d, %s]' % (testVec[featIndex],key))
        if testVec[featIndex] == int(key):    
            if type(secondDict[key]).__name__ == 'dict':
                #classLabel = predict(secondDict[key], featLabels, testVec)
                return predict(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
                return classLabel
    #return classLabel

    
    

def predicts(inputTree, featLabels, testDataSet):
    classLabelAll = []
    for testVec in testDataSet:
        classLabelAll.append(predict(inputTree, featLabels, testVec))
    return classLabelAll


# Create Test Set
def createTestSet():
    testSet = [ 
[0, 3, 4, 6],
[0, 3, 4, 7],
[0, 3, 5, 6],
[0, 3, 5, 7],
[0, 2, 4, 6],
[1, 3, 4, 7],
[1, 3, 5, 6],
[1, 3, 5, 7],
[1, 2, 4, 6],
[1, 2, 4, 7],
[1, 2, 5, 6],
[1, 2, 5, 7]
               ]
    return testSet

# Print a decision tree
def printTree(node, depth=0):
    for key, value in node.iteritems():
        print('%s%s' % (depth*' ',key))
        if isinstance(value,dict):
            printTree(value,depth+1)
        else:
            print('%s  `->%s' % (depth*' ',value))

dataSet, labels = createDataSet()
labels_tmp = labels[:]
desicionTree = createTree(dataSet, labels_tmp)
printTree(desicionTree)
#print(desicionTree)

inputTree = desicionTree
featLabels = ['color', 'size', 'act', 'age']
#testVec = [1,2,5,7]
#r=predict(inputTree, featLabels, testVec)
#print(r)
testSet = createTestSet()
print('predictResult:\n', predicts(desicionTree, labels, testSet))




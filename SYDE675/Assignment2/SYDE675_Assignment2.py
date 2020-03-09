#SYDE 675 Assignment 2
### Name: Juan Manuel Gomez Gonzalez

# Import the libraries
import pandas as pd
import numpy as np
verbose = True

# Try getting the file locally, if not found try it online
try:
  print("Getting the wine dataset file locally")
  df_wine = pd.read_csv('wine.data',
               header=None) # Load file
except:
  print("Could not find the wine dataset, getting file from the internet")
  df_wine = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data',
               header = None) # Load from WWW
else:
  print("Wine dataset file found locally")

array_wine = df_wine.values

def entropyCalc(data, attribute):
  totalVals = data.shape[0]
  vals, counts = np.unique((data)[:, attribute], return_counts = True)
  valNumber = vals.shape[0]
  entropy = 0.0
  if valNumber > 1:
    for i in range(valNumber):
      p = counts[i]/totalVals
      entropy = entropy - (p * np.log2(p))
  return entropy

def condEntropyCalc(data, classColumn, attribute, threshold):
  condEntropy=[]
  dataset = data[data[:, attribute] < threshold]
  p = dataset.shape[0]/data.shape[0]
  condEntropy.append(entropyCalc(dataset, classColumn) * p)
  dataset = data[data[:, attribute] >= threshold]
  p = dataset.shape[0]/data.shape[0]
  condEntropy.append(entropyCalc(dataset, classColumn) * p)
  return condEntropy

def bestEntropyCalc(data, classColumn, featsLeft):
  entropy = entropyCalc(data, classColumn)
  # sort the array on the specific attribute
  bestInfoGain = 0.0
  for attr in featsLeft:
    dataSort = data[data[:, attr].argsort()]
    lbl = dataSort[0, classColumn] # Get the first label
    for i in range(dataSort.shape[0]):
      if lbl != dataSort[i, classColumn]: # Check if the labels are different
        lbl = dataSort[i, classColumn] # Change the current label
        #calculate the change in entropy
        possibleThreshold = dataSort[i, attr]
        condEntropy = condEntropyCalc(dataSort, classColumn, attr, possibleThreshold)
        condEntropy = np.sum(condEntropy)
        # check if better than what is saved
        if  (entropy - condEntropy) > bestInfoGain:
          bestThreshold = possibleThreshold
          bestValue = i
          bestAttribute = attr
          bestInfoGain = entropy - condEntropy
          if verbose:
            print("System entropy: {1:.2f}, best entropy: {3:.2f}, best attribute: {4:d}, best threshold: {5:.2f} data left: {2:d},  Attributes left: {0:d}".format(len(featsLeft), entropy, data.shape[0], bestInfoGain, bestAttribute, bestThreshold))
  return bestAttribute, bestThreshold

class DT:
  def __init__(self, root = None, featUsed = None, featsLeft = None, threshold = None, leftLeaf = None, rightLeaf = None, prediction = None):
    self.root = root
    self.featUsed = featUsed
    self.featsLeft = featsLeft
    self.threshold = threshold
    self.leftLeaf = leftLeaf
    self.rightLeaf = rightLeaf
    self.prediction = prediction

def dataLeaver(dataSamples, bestAttr, bestTresh):
  leftData = dataSamples[dataSamples[:, bestAttr] < bestTresh]
  # leftData = np.delete(leftData, bestAttr, 1)  # delete attr from list
  rightData = dataSamples[dataSamples[:, bestAttr] >= bestTresh]
  # rightData = np.delete(rightData, bestAttr, 1)  # delete attr from list
  dataLeaves = np.asarray([leftData, rightData])
  return dataLeaves

def decisionTree(dataSamples, classColumn, feats_Left = None):
  dTree = DT()
  if feats_Left is not None:
    featsLeft = list(feats_Left)
  else:
    featsLeft = np.arange(dataSamples.shape[1]).tolist()
    featsLeft.remove(classColumn)
  
  #if all examples are positive, return single node tree root, with label = "positive"
  #if all examples are negative, return single node tree root, with label = "negative"
  if len(np.unique((dataSamples)[:, classColumn])) == 1:
    dTree.prediction = dataSamples[0, classColumn]
    return dTree
  # if number of predicting attributes is empty then return root with the label being the mode of the labels
  if dataSamples.shape[1] <= 1:
    # Get the mode of the dataset
    classList = dataSamples[:, classColumn].tolist()
    dTree.prediction = max(set(classList), key = classList.count)
    return dTree
  else:
    bestAttr, bestTresh = bestEntropyCalc(dataSamples, classColumn, featsLeft)
    dTree.featUsed = bestAttr
    dTree.threshold = bestTresh

    featsLeft.remove(bestAttr)
    dTree.featsLeft = featsLeft
    
    dataLeaves = dataLeaver(dataSamples, bestAttr, bestTresh)
    if verbose:
        print('Left Leaf')
        print('split attribute: ', bestAttr)
        print('Feats left: ', featsLeft)
    dTree.leftLeaf = decisionTree(dataLeaves[0], classColumn, featsLeft)
    if verbose:
        print('Right leaf')
        print('split attribute: ', bestAttr)
        print('Feats left: ', featsLeft)
    dTree.rightLeaf = decisionTree(dataLeaves[1], classColumn, featsLeft)
  return dTree

# Test the tree creation
tree = decisionTree(array_wine, 0)

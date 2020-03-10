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

def catCondEntropyCalc(data, classColumn, attribute):
  condEntropy=[]
  vals = np.unique((data)[:, attribute])
  for val in vals:
    dataset = data[data[:, attribute] == val]
    p = dataset.shape[0]/data.shape[0]
    condEntropy.append(entropyCalc(dataset, classColumn) * p)
  return condEntropy

def is_number(val):
  try:
      float(val) # for int, long, float and complex
  except ValueError:
      return False
  return True

def bestEntropyCalc(data, classColumn, featsLeft):
  entropy = entropyCalc(data, classColumn)
  # Sort the array on the specific attribute
  bestInfoGain = 0.0
  for attr in featsLeft:
    # If the data is catregorical:
    if all([is_number(sample) for sample in data[:, attr]]):
      # If the data is numerical
      dataSort = data[data[:, attr].argsort()]
      lbl = dataSort[0, classColumn] # Get the first label
      for i in range(dataSort.shape[0]):
        if lbl != dataSort[i, classColumn]: # Check if the labels are different
          lbl = dataSort[i, classColumn] # Change the current label
          # Calculate the change in entropy
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
              print("System entropy: {1:.2f}, best entropy: {3:.2f}, best attribute: {4:d}, best threshold: {5:.2f}, data left: {2:d},  Attributes left: {0:d}".format(len(featsLeft), entropy, data.shape[0], bestInfoGain, bestAttribute, bestThreshold))
    else:
      # If the data is not numerical
      condEntropy = catCondEntropyCalc(data, classColumn, attr)
      condEntropy = np.sum(condEntropy)
      if  (entropy - condEntropy) > bestInfoGain:
            bestThreshold = None
            bestAttribute = attr
            bestInfoGain = entropy - condEntropy
            if verbose:
              print("Categorical: System entropy: {1:.2f}, best entropy: {3:.2f}, best attribute: {4:d}, data left: {2:d},  Attributes left: {0:d}".format(len(featsLeft), entropy, data.shape[0], bestInfoGain, bestAttribute))
  return bestAttribute, bestThreshold

class DT:
  def __init__(self, root = None, featUsed = None, featsLeft = None, threshold = None, leftLeaf = None, rightLeaf = None, leaves = None, prediction = None):
    self.root = root
    self.featUsed = featUsed
    self.featsLeft = featsLeft
    self.threshold = threshold
    self.leftLeaf = leftLeaf
    self.rightLeaf = rightLeaf
    self.prediction = prediction
    self.leaves = leaves

def dataLeaver(dataSamples, bestAttr, bestTresh):
  if bestTresh is None:
    dataLeaves = []
    vals = np.unique((dataSamples)[:, bestAttr])
    for val in vals:
      dataLeaves.append(dataSamples[dataSamples[:, bestAttr] == val])
  else:
    leftData = dataSamples[dataSamples[:, bestAttr] < bestTresh]
    rightData = dataSamples[dataSamples[:, bestAttr] >= bestTresh]
    dataLeaves = [leftData, rightData]
  dataLeaves = np.asarray(dataLeaves)
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
    leaves = []
    for leaf, i in zip(dataLeaves, range(dataLeaves.shape[0])):
      if verbose:
        print('Leaf number {0:d}'.format(i))
        print('split attribute: ', bestAttr)
        print('Feats left: ', featsLeft)
      leaves.append(decisionTree(leaf, classColumn, featsLeft))
    dTree.leaves = list(leaves)

    # if verbose:
    #     print('Left Leaf')
    #     print('split attribute: ', bestAttr)
    #     print('Feats left: ', featsLeft)
    # leftLeaf = decisionTree(dataLeaves[0], classColumn, featsLeft)
    # if verbose:
    #     print('Right leaf')
    #     print('split attribute: ', bestAttr)
    #     print('Feats left: ', featsLeft)
    # rightLeaf = decisionTree(dataLeaves[1], classColumn, featsLeft)
    # dTree.leaves = list([leftLeaf, rightLeaf])
  return dTree



try:
  print("Getting the Tic-Tac-Toe dataset file locally")
  df_TTT = pd.read_csv('tic-tac-toe.data',
               header=None) #Load from WWW
except:
  print("Could not find the Tic-Tac-Toe dataset, getting file from the internet")
  df_TTT = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/tic-tac-toe/tic-tac-toe.data',
               header = None) #Load from WWW
else:
  print("Tic-Tac-Toe dataset file found locally")

array_TTT = df_TTT.values

# Test the tree creation
# tree = decisionTree(array_wine, 0)
# print(tree.leaves[0].leaves[1].leaves[1].prediction) # Check if it is creating the tree correctly
tree = decisionTree(array_TTT, 9)
print(tree.leaves[0].leaves[1].leaves[1].prediction) # Check if it is creating the tree correctly

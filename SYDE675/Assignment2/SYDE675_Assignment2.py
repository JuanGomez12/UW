#SYDE 675 Assignment 2
### Name: Juan Manuel Gomez Gonzalez

# Import the libraries
import pandas as pd
import numpy as np
import math
verbose = False

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



# Now for the TTT dataset
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

#-------------------------------------------------------------------------------


def entropyCalc(data, attribute = None):
  totalVals = data.shape[0]
  if attribute is None:
    vals, counts = np.unique(data, return_counts = True)
  else:
    vals, counts = np.unique(data[:, attribute], return_counts = True)
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
  vals = np.unique(data[:, attribute])
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

def is_categorical(data):
  return all([is_number(sample) for sample in data])

def intrinsicVal(data, attribute, threshold = None):
  if threshold is None:
    dataCat = data[:, attribute]
  else:
    dataCat = data[:, attribute] < threshold
  intrinsic = entropyCalc(dataCat)
  return intrinsic

def bestEntropyCalc(data, classColumn, featsLeft, gain_ratio):
  bestAttribute = None
  bestThreshold = None
  entropy = entropyCalc(data, classColumn)
  # Sort the array on the specific attribute
  bestInfoGain = 0.0
  for attr in featsLeft:
    # If the data is categorical:
    if is_categorical(data[:, attr]):
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
          currentEntropy = (entropy - condEntropy)
          if gain_ratio:
            intrinsicValue = intrinsicVal(dataSort, attr, possibleThreshold)
            if intrinsicValue == 0.0:
              currentEntropy = 0
            else:
              currentEntropy = currentEntropy / intrinsicValue
          if  currentEntropy > bestInfoGain:
            bestThreshold = possibleThreshold
            bestValue = i
            bestAttribute = attr
            bestInfoGain = currentEntropy
            if verbose:
              print("System entropy: {1:.2f}, best entropy: {3:.2f}, best attribute: {4:d}, best threshold: {5:.2f}, data left: {2:d},  Attributes left: {0:d}".format(len(featsLeft), entropy, data.shape[0], bestInfoGain, bestAttribute, bestThreshold))
    else:
      # If the data is not numerical
      condEntropy = catCondEntropyCalc(data, classColumn, attr)
      condEntropy = np.sum(condEntropy)
      currentEntropy = (entropy - condEntropy)
      if gain_ratio:
        intrinsicValue = intrinsicVal(data, attr)
        if intrinsicValue == 0.0:
          currentEntropy = 0
        else:
          currentEntropy = currentEntropy / intrinsicValue
      if  currentEntropy > bestInfoGain:
            bestThreshold = np.unique(data[:, attr])
            bestAttribute = attr
            bestInfoGain = currentEntropy
            if verbose:
              print("Categorical: System entropy: {1:.2f}, best entropy: {3:.2f}, best attribute: {4:d}, data left: {2:d},  Attributes left: {0:d}".format(len(featsLeft), entropy, data.shape[0], bestInfoGain, bestAttribute))
  return bestAttribute, bestThreshold 

def dataLeaver(dataSamples, bestAttr, bestThresh):
  if isinstance(bestThresh, np.ndarray):
    dataLeaves = []
    for thresh in bestThresh:
      dataLeaves.append(dataSamples[dataSamples[:, bestAttr] == thresh])
  else:
    leftData = dataSamples[dataSamples[:, bestAttr] < bestThresh]
    rightData = dataSamples[dataSamples[:, bestAttr] >= bestThresh]
    dataLeaves = [leftData, rightData]
  dataLeaves = np.asarray(dataLeaves)
  return dataLeaves

class DT:
  def __init__(self, featUsed = None, featsLeft = None, threshold = None, leaves = None, prediction = None):
    self.featUsed = featUsed
    self.featsLeft = featsLeft
    self.threshold = threshold
    self.prediction = prediction
    self.leaves = leaves
  def __repr__(self):
    return "Tree object"
  def __str__(self):
    return "Member of tree"
  def predict(self, value):
    subTree = self
    prediction = subTree.prediction
    leaves = subTree.leaves

    while leaves is not None:
      if verbose:
        print('-----------------------')
      feat = subTree.featUsed
      thresh = subTree.threshold
      
      if not isinstance(thresh, np.ndarray):
        # Attribute is numerical
        if verbose:
          print('Numerical feat used: {0:d}, thresh used: {1:.2f} and value of samples is {2}'.format(feat, thresh, value[feat]))
        if value[feat] < thresh:
          if verbose:
            print('Feat smaller than tresh')
          leaf = 0
        else:
          if verbose:
            print('Feat larger than tresh')
          leaf = 1
      else:
        # Attribute is categorical
        if verbose:
            print('Categorical feat used: {0:d}, values has {1}'.format(feat, value[feat]))
        indices = np.where(thresh == value[feat])[0]
        try:
          leaf = indices[0]
        except:
          leaf = None
      if leaf is not None:
        subTree = subTree.leaves[leaf]
        leaves = subTree.leaves
        prediction = subTree.prediction
      else:
        leaves = None
    return prediction

def decisionTree(dataSamplesX, dataSamplesY, feats_Left = None, gain_ratio = False):
  dataSamplesY = np.reshape(dataSamplesY,(-1,1))
  dataSamples = np.concatenate([dataSamplesX, dataSamplesY], axis=1)
  classColumn = dataSamples.shape[1] - 1
  dTree = DT()
  if feats_Left is not None:
    featsLeft = list(feats_Left)
  else:
    featsLeft = np.arange(dataSamplesX.shape[1]).tolist()
  
  #if all examples are of one specific class, set the class as the prediction of the tree
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
    bestAttr, bestThresh = bestEntropyCalc(dataSamples, classColumn, featsLeft, gain_ratio)
    dTree.featUsed = bestAttr
    dTree.threshold = bestThresh

    classList = dataSamples[:, classColumn].tolist()
    dTree.prediction = max(set(classList), key = classList.count)
    if bestAttr is not None and bestThresh is not None:
      featsLeft.remove(bestAttr)
      dTree.featsLeft = featsLeft
      
      dataLeaves = dataLeaver(dataSamples, bestAttr, bestThresh)
      leaves = []
      for leaf, i in zip(dataLeaves, range(dataLeaves.shape[0])):
        if verbose:
          print('Leaf number {0:d}'.format(i))
          print('split attribute: ', bestAttr)
          print('Feats left: ', featsLeft)
        leaves.append(decisionTree(leaf[:, :classColumn], leaf[:, classColumn], featsLeft, gain_ratio))
      dTree.leaves = list(leaves)
  return dTree

def k_folder(data, folds = 10):
  """ Get the input data, with rows being the samples, and create the amount of folds selected.
  Attributes:
    data (numpy array): Numpy array with the dataset. The function assumes that
    the samples are the rows, while the columns are the attributes.
    num_folds (int):  Number of folds to perform on the dataset.
  Args:
        data (numpy array): Numpy array with the dataset. The function
          assumes that the samples are the rows, while the columns are the attributes.
        folds (int, optional): Number of folds to perform on the dataset.
          Defaults to 10.
  Returns:
      datasplit: List with each of the number of folds selected in the input.
  """
  data_size = data.shape[0] # Get the size of the data
  remainder = data_size % folds # Get the remainder of the data
  low_bound = math.floor(data_size/ folds) # Find the upper bound/ceiling
  up_bound = math.ceil(data_size/ folds) # Find the upper bound/ceiling
  datasplit = [] # Create and empty list
  for i in range(remainder): #iterate over the folds with more values
    datasplit.append(data[i * up_bound : (i + 1) * up_bound]) # append the fold to the list
  for i in range(folds - remainder): # iterate over the folds with less values
    datasplit.append(data[remainder * up_bound + i * low_bound : remainder * up_bound + (i + 1) * low_bound])
  return datasplit

def trainTestTree(trainData, testData, classColumn, gain_ratio = False):
  tree = decisionTree(trainData[:, :classColumn], trainData[:, classColumn], gain_ratio = gain_ratio)
  correctPredictions = 0
  totalValues = testData.shape[0]
  for i in range(totalValues):
    prediction = tree.predict(testData[i, :])
    if testData[i, classColumn] == prediction:
      correctPredictions += 1
  accuracy = correctPredictions/totalValues
  #use unique to filter the possible classes, loop thru them after filtering and get the relevant info to create the confusion matrix
  return accuracy, tree

def k_fold_crossval(dataX, dataY, folds = 10, gain_ratio = False):
  dataY = np.reshape(dataY,(-1,1))
  data = np.concatenate([dataX, dataY], axis = 1)
  classColumn = data.shape[1] - 1

  datasplit = k_folder(data, folds)
  accuracy = []
  forest = []
  for i in range(folds):
    data = list(datasplit)
    test_data = data.pop(i)
    train_data = np.concatenate((data), axis = 0)
    acc, tree = trainTestTree(train_data, test_data, classColumn, gain_ratio)
    forest.append(tree)
    accuracy.append(acc)
  return list(accuracy), list(forest)

if verbose:
  # Test the tree creation
  tree = decisionTree(array_wine[:,1:], array_wine[:,0], gain_ratio = True)
  tree_TTT = decisionTree(array_TTT[:,:9], array_TTT[:,9], gain_ratio = True)
  #print(tree.leaves[0].leaves[1].leaves[1].prediction) # Check if it is creating the tree correctly
  print('wine prediction of val 20: ', tree.predict(array_wine[20, 1:]))
  print('wine prediction of val 120: ', tree.predict(array_wine[120, 1:]))
  print('TTT prediction of val 100: ', tree_TTT.predict(array_TTT[100, :9]))
  print('TTT prediction of val 700: ', tree_TTT.predict(array_TTT[700, :9]))

# Question 2 a)
# First, using the wine dataset
array = array_wine
accuracies_wine = []
forests_wine = []
for i in range(10):
  np.random.shuffle(array)
  accuracy_wine, forest_wine = k_fold_crossval(array[:,1:], array[:,0], gain_ratio = False)
  accuracies_wine.append(accuracy_wine)
  forests_wine.append(forest_wine)

# Now using the Tic-tac-toe dataset
array = array_TTT
accuracies_TTT = []
forests_TTT = []
for i in range(10):
  np.random.shuffle(array)
  accuracy_TTT, forest_TTT = k_fold_crossval(array[:,:9], array[:,9], gain_ratio = False)
  accuracies_TTT.append(accuracy_TTT)
  forests_TTT.append(forest_TTT)

# Question 2 b)
# Using the wine dataset
array = array_wine
accuracies_wine = []
forests_wine = []
for i in range(10):
  np.random.shuffle(array)
  accuracy_wine, forest_wine = k_fold_crossval(array[:,1:], array[:,0], gain_ratio = True)
  accuracies_wine.append(accuracy_wine)
  forests_wine.append(forest_wine)

# Now using the Tic-tac-toe dataset
array = array_TTT
accuracies_TTT = []
forests_TTT = []
for i in range(10):
  np.random.shuffle(array)
  accuracy_TTT, forest_TTT = k_fold_crossval(array[:,:9], array[:,9], gain_ratio = True)
  accuracies_TTT.append(accuracy_TTT)
  forests_TTT.append(forest_TTT)


def addAttrNoise(data, percentage):
  # Set the sample size
  sample_size = data.shape[0]
  # Set the divider using a uniform distr., for selecting the attributes to add noise
  divider = np.random.uniform(size = sample_size).T
  totalSamples = np.concatenate([data, divider], axis = 1)
  noisyData = data[data[:,-1] <= percentage]
  cleanData = data[data[:,-1] > percentage]

  # Add noise to each attr
  for attr in data.shape[1]:
    addNoise = np.random.randint(2) # Decide if the attribute will have noise added
    if addNoise:
      # Check if the data is numerical or categorical
      if is_categorical(data[:, attr]): #If the data is categorical
        vals = np.unique((data)[:, attr]) # Find the possible labels for the attribute
        noisyVal = vals[np.random.randint(vals.shape[0])] # Select randomly one of the labels
        # Assign it to the value in the data
      else:
        pass
  # Rebuild the dataset
  noisedUpData = np.concatenate([noisyData, cleanData], axis = 0)
  noisedUpData = numpy.delete(noisedUpData, noisedUpData.shape[1], axis = 1)
  np.random.shuffle(noisedUpData)
  return noisedUpData


def addClassNosie():
  pass
#SYDE 675 Assignment 2
### Name: Juan Manuel Gomez Gonzalez

# Import the libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplab
import matplotlib.mlab as mlab
import seaborn as sns
import pandas as pd
import math

# Set parameters
sns.set_style("darkgrid") # Set seaborn's dark grid style
sns.set_context("talk") # Make the font of the plots bigger
verbose = False
test = True
saveResults = False
Q2 = False
Q3 = True

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


# Convert to numpy arrays
array_wine = df_wine.values
array_TTT = df_TTT.values

#---------------------------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------------------------

def condEntropyCalc(data, classColumn, attribute, threshold):
  condEntropy=[]
  dataset = data[data[:, attribute] < threshold]
  p = dataset.shape[0]/data.shape[0]
  condEntropy.append(entropyCalc(dataset, classColumn) * p)
  dataset = data[data[:, attribute] >= threshold]
  p = dataset.shape[0]/data.shape[0]
  condEntropy.append(entropyCalc(dataset, classColumn) * p)
  return condEntropy

#---------------------------------------------------------------------------------------------------------------------------

def catCondEntropyCalc(data, classColumn, attribute):
  condEntropy=[]
  vals = np.unique(data[:, attribute])
  for val in vals:
    dataset = data[data[:, attribute] == val]
    p = dataset.shape[0]/data.shape[0]
    condEntropy.append(entropyCalc(dataset, classColumn) * p)
  return condEntropy

#---------------------------------------------------------------------------------------------------------------------------

def is_number(val):
  try:
    float(val) # for int, long, float and complex
  except ValueError:
    return False
  return True

#---------------------------------------------------------------------------------------------------------------------------

def is_numerical(data):
  return all([is_number(sample) for sample in data])

#---------------------------------------------------------------------------------------------------------------------------

def intrinsicVal(data, attribute, threshold = None):
  if threshold is None:
    dataCat = data[:, attribute]
  else:
    dataCat = data[:, attribute] < threshold
  intrinsic = entropyCalc(dataCat)
  return intrinsic

#---------------------------------------------------------------------------------------------------------------------------

def bestEntropyCalc(data, classColumn, featsLeft, gain_ratio):
  bestAttribute = None
  bestThreshold = None
  entropy = entropyCalc(data, classColumn)
  # Sort the array on the specific attribute
  bestInfoGain = 0.0
  for attr in featsLeft:
    # If the data is categorical:
    if is_numerical(data[:, attr]):
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

#---------------------------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------------------------

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
  def confusionMat(self, testData):
    """Note: there is going to be an error state if the test data does not have all the possible classes. This can be
      fixed by adding a possibleClasses to the tree object and using it as the complete list for possible classes"""
    expectedLabels = np.unique(testData[:, -1]) # Get the classes/labels of the dataset
    confusionMatrix = np.full((expectedLabels.shape[0], expectedLabels.shape[0]), 0) # Create an empty conf mat
    for i in range(expectedLabels.shape[0]): # Iterate over the possible labels
      expectedLabel = expectedLabels[i]
      labelData = testData[testData[:,-1] == expectedLabel]
      predict = []
      # Check predictions
      for j in range(labelData.shape[0]):
        predict.append(self.predict(labelData[j, :]))
      # Count the number of each prediction
      unique, counts = np.unique(predict, return_counts = True)
      # Build the confusion matrix for the label 
      for element, count in zip(unique, counts):
        for j in range(expectedLabels.shape[0]):
          if expectedLabels[j] == element:
            confusionMatrix[i, j] = count
    return confusionMatrix

#---------------------------------------------------------------------------------------------------------------------------  

def decisionTree(dataSamplesX, dataSamplesY, feats_Left = None, gain_ratio = False):
  dataSamplesY = np.reshape(dataSamplesY,(-1,1))
  dataSamples = np.concatenate([dataSamplesX, dataSamplesY], axis = 1)
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

#---------------------------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------------------------
  
def trainTestTree(trainData, testData, gain_ratio = False):
  tree = decisionTree(trainData[:, :-1], trainData[:, -1], gain_ratio = gain_ratio)
  correctPredictions = 0
  totalValues = testData.shape[0]
  #use unique to filter the possible classes, loop thru them after filtering and get the relevant info to create the confusion matrix
  confusionMat = tree.confusionMat(testData)
  accuracy = np.trace(confusionMat) / np.sum(confusionMat)
  return tree, accuracy, confusionMat

#---------------------------------------------------------------------------------------------------------------------------

from sklearn.preprocessing import StandardScaler
def addAttrNoise(dataX, dataY, percentage):
  """ Get the input data, in the form of [n_samples, n_attrributes], and return the dataset
    with the desired percentage of it modified with noise.
  Args:
        dataX (numpy array): Numpy array with the dataset's attributes. The function
          assumes that the samples are the rows, while the columns are the attributes.
        dataY (numpy array): Numpy array with the dataset's labels or classes.
        percentage (float): Percentage of the dataset to modify with noise
  Returns:
      noisedUpData: One joined dataset with the respective noise and the class column 
        as the last column of the dataset
  """
  dataY = np.reshape(dataY, (-1,1))
  
  # Find which values are categories (and what are they), and which aren't categories
  numericalVals = []
  categories = []
  for attr in range(dataX.shape[1]):
    numericalVal = is_numerical(dataX[:, attr])
    if not numericalVal:
      cats = np.unique(dataX[:, attr]) # Find the possible labels for the attribute
    else:
      cats = None
    numericalVals.append(numericalVal)
    categories.append(cats)

  if all(numericalVals): # If all values are numerical
   # standardize the dataset
    dataScaler = StandardScaler()
    data_scaled = dataScaler.fit_transform(dataX)
  else:
    data_scaled = dataX

  # Set the sample size
  sample_size = dataX.shape[0]

  # Create an index for the data
  index = np.arange(sample_size)
  index = index[np.newaxis].T

  # Set the divider using a uniform distr., for selecting the attributes to add noise
  divider = np.random.uniform(size = sample_size)
  divider = divider[np.newaxis].T

  # Add the divider and the index to the dataset
  totalSamples = np.concatenate([index, data_scaled, divider], axis = 1)

  # Separate the data into clean and soon to be noisy
  noisyData = totalSamples[totalSamples[:,-1] <= percentage]
  cleanData = totalSamples[totalSamples[:,-1] > percentage]

  # Remove the divider
  noisyData = noisyData[:, :-1]
  cleanData = cleanData[:, :-1]

  count = 0 # To see how many values were modified

  # Add noise to each value
  for val in range(noisyData.shape[0]):
    # Add noise to each attr
    for attr in range(1, noisyData.shape[1]): # Starts in 1 so as to not add noise to the index
      # addNoise = np.random.randint(2) # Decide if the attribute will have noise added
      addNoise = True # For now 'leave it always on'
      if addNoise:
        count += 1
        if verbose:
          print('Adding noise to attr:', attr, 'in val:', val, 'with a value of:', noisyData[val, attr])
        # Check if the data is numerical or categorical
        if numericalVals[attr - 1]: # If the data is numerical
          noise = np.random.normal()
          noisyData[val, attr] = noisyData[val, attr] + noise
        else:
         # It is a categorical value
          cats = categories[attr - 1] # Retrieve the labels for the attribute
          noisyVal = cats[np.random.randint(cats.shape[0])] # Select randomly one of the labels
          # Assign it to the value in the data
          noisyData[val, attr] = noisyVal
        if verbose:
          print('val now is:', noisyData[val, attr])

  # Rebuild the dataset
  noisedUpData = np.concatenate([noisyData, cleanData], axis = 0)
  # noisedUpData = np.delete(noisedUpData, noisedUpData.shape[1] - 1, axis = 1) # Delete the divider
  noisedUpData = noisedUpData[noisedUpData[:,0].argsort()]
  noisedUpData = np.delete(noisedUpData, 0, axis = 1) # Delete the index column
  if all(numericalVals):
    noisedUpData = dataScaler.inverse_transform(noisedUpData) # Unscale the data
  if verbose:
    print('Total vals changed:', count)
  # noisedUpData = noisedUpData[noisedUpData[:,0].argsort()]
  noisedUpData = np.concatenate([noisedUpData, dataY], axis = 1)
  return noisedUpData

#---------------------------------------------------------------------------------------------------------------------------

def addClassNoise(dataX, dataY, percentage, contradictory = False):
  #Contradictory examples. The same examples appear more than once and are labeled with different classifications  
  #Misclassifications. Instances are labeled with wrong classes. This type of errors is common in situations that different classes have similar sympto
  dataY = np.reshape(dataY, (-1,1))

  categories = np.unique(dataY) # Find the possible labels for the class

  # Set the sample size
  sample_size = dataX.shape[0]

  # Create an index for the data
  index = np.arange(sample_size)
  index = index[np.newaxis].T

  # Set the divider using a uniform distr., for selecting the attributes to add noise
  divider = np.random.uniform(size = sample_size)
  divider = divider[np.newaxis].T

  # Add the divider and the index to the dataset
  totalSamples = np.concatenate([index, dataX, dataY, divider], axis = 1)

  # Separate the data into clean and soon to be noisy
  noisyData = totalSamples[totalSamples[:,-1] <= percentage]
  cleanData = totalSamples[totalSamples[:,-1] > percentage]

  # Remove the divider
  noisyData = noisyData[:, :-1]
  cleanData = cleanData[:, :-1]

  if contradictory: # If creating contradictory samples
    duplicateData = np.copy(noisyData)

  # Add noise to each value
  for val in range(noisyData.shape[0]):
    if contradictory: # If creating contradictory samples
      noisyVal =  categories[np.random.randint(categories.shape[0])] # Select randomly one of the labels
      while noisyVal == noisyData[val, -1]:
        noisyVal =  categories[np.random.randint(categories.shape[0])]
      # Assign it to the value in the data
      noisyData[val, -1] = noisyVal
    else: # If adding missclassifications
      if verbose:
        print('Adding noise to class in val:', val, 'with a value of:', noisyData[val, -1])
      noisyVal = categories[np.random.randint(categories.shape[0])] # Select randomly one of the labels
      # Assign it to the value in the data
      noisyData[val, -1] = noisyVal
    if verbose:
      print('val now is:', noisyData[val, -1])


  # Rebuild the dataset
  if contradictory: # If creating contradictory samples
    noisyData = np.concatenate([noisyData, duplicateData], axis = 0)
  noisedUpData = np.concatenate([noisyData, cleanData], axis = 0)
  # noisedUpData = np.delete(noisedUpData, noisedUpData.shape[1] - 1, axis = 1) # Delete the divider
  noisedUpData = noisedUpData[noisedUpData[:,0].argsort()]
  noisedUpData = np.delete(noisedUpData, 0, axis = 1) # Delete the index column
  return noisedUpData

#---------------------------------------------------------------------------------------------------------------------------

def k_fold_crossval(dataX, dataY, folds = 10, gain_ratio = False, dirtyTrain = False, 
dirtyTest = False, attrNoisePerc = 0.05, dirtyClass = False, classNoisePerc = 0.05, contraClassNoise = False):
  
  if dirtyClass:
    data = addClassNoise(dataX, dataY, classNoisePerc, contraClassNoise)
  else:
    dataY = np.reshape(dataY,(-1,1))
    data = np.concatenate([dataX, dataY], axis = 1)

  datasplit = k_folder(data, folds)
  forest = []
  accuracy = []
  confMats = []
  for i in range(folds):
    data = list(datasplit) # Get the list of folds
    test_data = data.pop(i) # Get and remove the respective test fold for the iteration
    train_data = np.concatenate((data), axis = 0) # Concatenate the rest of the data
    if dirtyTrain: # If you need to add atribute noise to the train data
      train_data = addAttrNoise(train_data[:,:-1], train_data[:,-1], attrNoisePerc)
    if dirtyTest: # If you need to add atribute noise to the test data
      test_data = addAttrNoise(test_data[:,:-1], test_data[:,-1], attrNoisePerc)
    tree, acc, confMat = trainTestTree(train_data, test_data, gain_ratio) # Train and get results
    forest.append(tree)
    accuracy.append(acc)
    confMats.append(confMat)
  return list(forest), list(accuracy), list(confMats)

#---------------------------------------------------------------------------------------------------------------------------

def repeated_k_fold(dataX, dataY, reps = 10, folds = 10, gain_ratio = False, dirtyTrain = False, 
dirtyTest = False, attrNoisePerc = 0.05, dirtyClass = False, classNoisePerc = 0.05, contraClassNoise = False):
  dataY = np.reshape(dataY,(-1,1))
  data = np.concatenate([dataX, dataY], axis = 1)

  forests = []
  accuracies = []
  confMats = []

  for i in range(reps):
    np.random.shuffle(data)
    forest, accuracy, confMat = k_fold_crossval(data[:,:-1], data[:,-1], folds, gain_ratio,
     dirtyTrain, dirtyTest, attrNoisePerc, dirtyClass,classNoisePerc, contraClassNoise)
    forests.append(forest) # Calculating this in case it is needed in the future
    accuracies += accuracy 
    confMats += confMat
  bestConfMat = confMats[np.argmax(accuracies)]
  return list(accuracies), bestConfMat

#---------------------------------------------------------------------------------------------------------------------------

def plotConfMat(mat1, mat2, mat1Labels = None, mat2Labels = None, saveFig = False):
  # Use pandas to create the column names and idx 
  if mat1Labels is None:
    mat1Labels = []
    for i in range(mat1.shape[0]):
      mat1Labels.append('C' + str(i + 1))
  else:
    pass

  if mat2Labels is None:
    mat2Labels = []
    for i in range(mat2.shape[0]):
      mat2Labels.append('C' + str(i + 1))
  else:
    pass
  df_mat1 = pd.DataFrame(mat1, index = mat1Labels,
                    columns = mat1Labels)
  df_mat2 = pd.DataFrame(mat2, index = mat2Labels,
                    columns = mat2Labels)

  # Get the min and max values
  vmin = min(df_mat1.values.min(), df_mat2.values.min())
  vmax = max(df_mat1.values.max(), df_mat2.values.max())


  fig, axs = plt.subplots(nrows = 1, ncols = 3,
                        figsize = [20.0, 10.0],
                        gridspec_kw = dict(width_ratios = [3, 2.8, 0.2]))

  # Plot both heat maps
  axs[0] = sns.heatmap(df_mat1, vmin = vmin, vmax = vmax, annot = True, fmt = 'g', cbar = False, cmap = "summer", ax = axs[0])
  axs[1] = sns.heatmap(df_mat2, vmin = vmin, vmax = vmax, annot = True, fmt = 'g', cbar = False, cmap = "summer", ax = axs[1])

  # Configure aesthetics for ax 0
  axs[0].xaxis.set_ticks_position('top')
  axs[0].xaxis.set_tick_params(length = 0)
  axs[0].set_title("Actual Values")
  axs[0].set_xlabel("(a) Wine")
  axs[0].set_ylabel("Predicted Values")

  # Configure aesthetics for ax 1
  axs[1].xaxis.set_ticks_position('top')
  axs[1].xaxis.set_tick_params(length=0)
  axs[1].set_title("Actual Values")
  axs[1].set_xlabel("(b) Tic-Tac-Toe")

  # Configure colorbar in ax 2
  axs[2] = fig.colorbar(axs[0].collections[0], cax = axs[2])
  fig.tight_layout()
  if saveFig:
    plt.savefig('ConfusionMatrix.png', bbox_inches = 'tight')
  plt.show()

#---------------------------------------------------------------------------------------------------------------------------

if verbose and test:
  # Test the tree creation
  tree = decisionTree(array_wine[:,1:], array_wine[:,0], gain_ratio = True)
  tree_TTT = decisionTree(array_TTT[:,:9], array_TTT[:,9], gain_ratio = True)
  print('wine prediction of val 20: ', tree.predict(array_wine[20, 1:]))
  print('wine prediction of val 120: ', tree.predict(array_wine[120, 1:]))
  print('TTT prediction of val 100: ', tree_TTT.predict(array_TTT[100, :9]))
  print('TTT prediction of val 700: ', tree_TTT.predict(array_TTT[700, :9]))


# Question 2 a)
if Q2:
  labels_wine = np.unique(array_wine[:, 0])
  labels_TTT = np.unique(array_TTT[:, 9])

  # First, using the wine dataset

  accuracies_wine_IG, bestConfMat_wine_IG = repeated_k_fold(array_wine[:,1:], array_wine[:,0])

  # Now using the Tic-tac-toe dataset

  accuracies_TTT_IG, bestConfMat_TTT_IG = repeated_k_fold(array_TTT[:,:9], array_TTT[:,9])

  # ----------------------------------------------------------------------------------------------------------
  # Question 2 b)
  # Using the wine dataset

  accuracies_wine_GR, bestConfMat_wine_GR = repeated_k_fold(array_wine[:,1:], array_wine[:,0], gain_ratio = True)

  # Now using the Tic-tac-toe dataset

  accuracies_TTT_GR, bestConfMat_TTT_GR = repeated_k_fold(array_TTT[:,:9], array_TTT[:,9], gain_ratio = True)

  # Printing the results
  print('--------------------------------------------------------------------------------------')
  print('Question 2. a)')
  print('The mean accuracy for the wine decision tree was {0:.2f}% and its variance was {1:.4f}'.format(100 * np.mean(accuracies_wine_IG), np.var(accuracies_wine_IG)))
  print('The mean accuracy for the Tic-tac-toe decision tree was {0:.2f}% and its variance was {1:.4f}'.format(100 * np.mean(accuracies_TTT_IG), np.var(accuracies_TTT_IG)))

  plotConfMat(bestConfMat_wine_IG, bestConfMat_TTT_IG, labels_wine, labels_TTT, saveFig = saveResults)

  print('--------------------------------------------------------------------------------------')
  print('Question 2. b)')
  print('The mean accuracy for the wine decision tree was {0:.2f}% and its variance was {1:.4f}'.format(100 * np.mean(accuracies_wine_GR), np.var(accuracies_wine_GR)))
  print('The mean accuracy for the Tic-tac-toe decision tree was {0:.2f}% and its variance was {1:.4f}'.format(100 * np.mean(accuracies_TTT_GR), np.var(accuracies_TTT_GR)))

  plotConfMat(bestConfMat_wine_GR, bestConfMat_TTT_GR, labels_wine, labels_TTT, saveFig = saveResults)

# Question 3 A)

# First the plotting functions
import matplotlib.ticker as mtick
def plotConfMat(data, percentages, saveFig = False):
  fig, axs = plt.subplots(nrows = 1, ncols = 2, sharey = True, figsize = [20.0, 10.0], gridspec_kw = {'wspace':0.04, 'hspace':0})

  colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] # colors to use for the plot
  categories = ['CxC', 'DxC', 'CxD', 'DxD'] # labels to use for the plot

  for i in range(len(data)): # iterate over the CxC, DxC, CxD, DxD categories
    cat = data[i]
    for j in range(len(cat)): # iterate over dataset
      axs[j].plot(percentages, cat[j], color = colors[i], label = categories[i])


  # Configure aesthetics for ax 0
  axs[0].set_xlabel("Noise Percentage" "\n" "\n" "(a) Wine dataset")
  axs[0].set_ylabel("Accuracy")
  axs[0].xaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1))
  axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1))

  # Configure aesthetics for ax 1
  axs[1].set_xlabel("Noise Percentage" "\n" "\n" "(b) Tic-Tac-Toe dataset")
  axs[1].xaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1))
  axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1))

  # Set the legend
  axs[0].legend(ncol = 4, loc = 'center', fontsize = 'small',columnspacing = 0.8, handlelength=1.5, bbox_to_anchor = (1.02, -0.1))

  # fig.tight_layout()
  if saveFig:
      plt.savefig('AccuracyVSNoise.png', bbox_inches = 'tight')
  plt.show()
  

# fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = [20.0, 10.0])
# fig.tight_layout()
# if saveFig:
#     plt.savefig('ConfusionMatrix.png', bbox_inches = 'tight')
# plt.show()

if Q3:
  # To make the data more easy to manage, let's move the class column to the end of both datasets
  wine = np.concatenate([array_wine[:, 1:], np.reshape(array_wine[:,0],(-1,1))], axis = 1)
  TTT = array_TTT

  CxC = []
  DxC = []
  CxD = []
  DxD = []

  datasets = [wine, TTT]
  percentages = [0.05, 0.1, 0.15]

  for i in range(len(datasets)):
    CxC_temp = []
    DxC_temp = []
    CxD_temp = []
    DxD_temp = []
    for perc in percentages:
      dataset = datasets[i]
      accuraciesCxC = repeated_k_fold(dataset[:,:-1], dataset[:,-1], reps = 10, folds = 10, gain_ratio = False, dirtyTrain = False, 
      dirtyTest = False, attrNoisePerc = perc)[0]
      CxC_temp.append(np.mean(accuraciesCxC))

      accuraciesDxC = repeated_k_fold(dataset[:,:-1], dataset[:,-1], reps = 10, folds = 10, gain_ratio = False, dirtyTrain = True, 
      dirtyTest = False, attrNoisePerc = perc)[0]
      DxC_temp.append(np.mean(accuraciesDxC))

      accuraciesCxD = repeated_k_fold(dataset[:,:-1], dataset[:,-1], reps = 10, folds = 10, gain_ratio = False, dirtyTrain = False, 
      dirtyTest = True, attrNoisePerc = perc)[0]
      CxD_temp.append(np.mean(accuraciesCxD))

      accuraciesDxD = repeated_k_fold(dataset[:,:-1], dataset[:,-1], reps = 10, folds = 10, gain_ratio = False, dirtyTrain = True, 
      dirtyTest = True, attrNoisePerc = perc)[0]
      DxD_temp.append(np.mean(accuraciesDxD))
    CxC.append(CxC_temp)
    DxC.append(DxC_temp)
    CxD.append(CxD_temp)
    DxD.append(DxD_temp)

data = [CxC, DxC, CxD, DxD]

# For the wine dataset

# Question 3 B)


if test:
  a = addClassNoise(array_wine[:, 1:], array_wine[:,0], 0.05)
  b = addClassNoise(array_TTT[:, :-1], array_TTT[:,-1], 0.05)
  c = addClassNoise(array_wine[:, 1:], array_wine[:,0], 0.05, True)
  d = addClassNoise(array_TTT[:, :-1], array_TTT[:,-1], 0.05, True)
  print('done')
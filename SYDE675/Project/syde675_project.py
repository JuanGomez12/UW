#SYDE 675 Project
### Name: Juan Manuel Gomez Gonzalez

# Import the libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplab
import matplotlib.mlab as mlab
import seaborn as sns
import pandas as pd
import math
from sklearn.preprocessing import StandardScaler # For standardizing numerical datasets
import matplotlib.ticker as mtick

# Import some elements needed for the plotting
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
import string

sns.set_style("darkgrid") # Set seaborn's dark grid style
sns.set_context("poster") # Make the font of the plots bigger
figure_size = [20.0, 10.0]
verbose = True
moreThan1Hour = False # Change this flag to compute the 10-times 10-fold cross-validation parameters that take more than 1 hour
test = True # For testing all the algorithms with small parameters so it doesn't take long to compute

# Try getting the file locally
# df_features = pd.read_csv('features.txt', delim_whitespace=True,  header = None) # Load file
# features = df_features.values[:, 1] # The names cant be added to the X_train as there are repeated feature names

X_train = pd.read_csv('X_train.txt', delim_whitespace=True,  header = None).values
y_train = pd.read_csv('y_train.txt', delim_whitespace=True,  header = None).values
trainData = np.concatenate([X_train, np.reshape(y_train,(-1, 1))], axis = 1)

X_test = pd.read_csv('X_test.txt', delim_whitespace=True,  header = None).values
y_test = pd.read_csv('y_test.txt', delim_whitespace=True,  header = None).values
testData = np.concatenate([X_test, np.reshape(y_test,(-1, 1))], axis = 1)

# create the adaboost multiclass class
from sklearn import tree

class adaBoostMC:
  def __init__(self, classifierNumber = 500, trainSamples = 500, maxDepth = 1):
    self.classifierNumber = classifierNumber # target number of classifiers to use
    self.trainSamples = trainSamples # number of samples to use for training
    self.maxDepth = maxDepth
    self.classifierList = []
    self.classifierWeights = []
    self.classes = []

  def __repr__(self):
    return 'adaBoost SAMME with stumps as classifier'

  def __str__(self):
    return 'adaBoost SAMME with stumps as classifier'

  def get_params(self, deep = True):
    return {"classifierNumber": self.classifierNumber, "trainSamples": self.trainSamples,
    "maxDepth": self.maxDepth}

  def set_params(self, **parameters):
    for parameter, value in parameters.items():
        setattr(self, parameter, value)
    return self

  def fit(self, xTrain, yTrain, classifierNumber = None, maxDepth = None):
    """ Train the classifiers according to the predefined private attributes and the dataset that was input """
    self.classifierList = []
    self.classifierWeights = []
    if classifierNumber is not None:
      self.classifierNumber = classifierNumber
    if maxDepth is not None:
      self.maxDepth = maxDepth
    yTrainReshaped = np.reshape(yTrain,(-1, 1)) # reshape the yTrain array
    sampleData = np.concatenate([xTrain, yTrainReshaped], axis = 1) # concatenate all of the data
    self.classes = np.unique(yTrain) # get the possible values for the classes
    # Initialize sample weights
    dataSamples = xTrain.shape[0]
    sampleWeights = np.full(dataSamples, 1.0/dataSamples)

    # iteratively create the classifiers
    for i in range(self.classifierNumber):
      # estimatorErr = 1
      # while estimatorErr >= 0.5:
      trainData = sampleData[np.random.choice(dataSamples, self.trainSamples, p = sampleWeights)]# sample the training set
      classifier = tree.DecisionTreeClassifier(max_depth = self.maxDepth) # create tree
      classifier.fit(trainData[:, :-1], trainData[:, -1]) # fit the classifier
      yPredict = classifier.predict(xTrain) # predict with the newly created classifier
      incorrectPreds = (yPredict != yTrain) # Find the incorrect predictions
      estimatorErr = np.mean(np.average(incorrectPreds, weights = sampleWeights, axis = 0)) # calculate the classifier error
      estimatorWeight = np.log((1 - estimatorErr + 0.0001) / (estimatorErr + 0.0001)) + np.log(self.classes.shape[0] - 1)# calculate the estimator weight
      # 1 for correct vals, -1 for incorrect vals
      yTrain_x_yPred = np.zeros(incorrectPreds.shape)
      yTrain_x_yPred[incorrectPreds == False] = 1
      yTrain_x_yPred[incorrectPreds == True] = -1
      exp = np.exp(-estimatorWeight * yTrain_x_yPred)
      sampleWeights = np.multiply(sampleWeights, exp)
      sampleWeights = sampleWeights/np.sum(sampleWeights) # normalize the sample weights
      self.classifierList.append(classifier)
      self.classifierWeights.append(estimatorWeight) #append sample weights to list
    return self

  def predict(self, value):
    """ Function that predicts a class label based on the value or array of values given as input """
    if value.ndim > 1: # multiple samples for prediction?
      totalSamples = value.shape[0]
    else:
      value = np.reshape(value, (1, -1)) # reshape the data sample
      totalSamples = 1
    predictionWeights = np.full([totalSamples, self.classes.shape[0]], 0.0)
    # predictionWeight = np.full([totalSamples, self.classifierNumber], np.nan)
    for i in range(self.classifierNumber):
      prediction = self.classifierList[i].predict(value)
      for j in range(totalSamples):
        predictionWeights[j, int(prediction[j] - 1)] += self.classifierWeights[i]
    predictions = np.argmax(predictionWeights, axis = 1) + 1
    return predictions

  def score(self, xTest, yTest):
    """ Function that calculates the accuracy of the classifier according to some test data """
    sampleNumber = xTest.shape[0]
    prediction = self.predict(xTest)
    correctPredictions = prediction == yTest
    return(sum(correctPredictions)/sampleNumber)
    
  def confusionMat(self, xTest, yTest):
    """ Function that calculates the confusion matrix for the test data"""
    expectedLabels = self.classes # Get the classes/labels of the dataset
    confusionMatrix = np.full((expectedLabels.shape[0], expectedLabels.shape[0]), 0) # Create an empty conf mat
    for i in range(expectedLabels.shape[0]): # Iterate over the possible labels
      expectedLabel = expectedLabels[i]
      labelData = xTest[yTest == expectedLabel]
      predict = []
      # Check predictions
      predict = self.predict(labelData)
      # Count the number of each prediction
      unique, counts = np.unique(predict, return_counts = True)
      # Build the confusion matrix for the label 
      for element, count in zip(unique, counts):
        for j in range(expectedLabels.shape[0]):
          if expectedLabels[j] == element:
            confusionMatrix[i, j] = count
    return confusionMatrix
  def plotConfMat(self, xTest, yTest, figSize = [20.0, 10.0]):
    """ Function that pltos the confusion matrix for the test data """
    # Calculate the conf matrix:
    confMat = self.confusionMat(xTest, yTest)
    # Get the min and max values
    vmin = np.min(confMat)
    vmax = np.max(confMat)
    classes = self.classes
    classes = classes.astype(str)
    df_CM = pd.DataFrame(confMat, index = classes,
                  columns = classes)
    
    fig, axs = plt.subplots(nrows = 1, ncols = 2,
                       figsize = figSize,
                       gridspec_kw = dict(width_ratios = [3, 0.2]))
    # Plot both heat maps
    axs[0] = sns.heatmap(df_CM, vmin = vmin, vmax = vmax, annot = True, fmt = 'g', cbar = False, cmap = "summer", ax = axs[0])

    # Configure aesthetics for ax 0
    # axs[0].xaxis.set_ticks_position('top')
    axs[0].xaxis.set_tick_params(length = 0)
    axs[0].set_xlabel("Actual Values")
    axs[0].set_ylabel("Predicted Values")

    # Configure colorbar in ax 1
    axs[1] = fig.colorbar(axs[0].collections[0], cax = axs[1])
    fig.tight_layout()
    return fig, axs




# Now the adaboost using SVC
from sklearn.svm import SVC
class adaBoostMC_SVC:
  def __init__(self, classifierNumber = 500, trainSamples = 500, C = 1):
    self.classifierNumber = classifierNumber # target number of classifiers to use
    self.trainSamples = trainSamples # number of samples to use for training
    self.C = C
    self.classifierList = []
    self.classifierWeights = []
    self.classes = []

  def __repr__(self):
    return 'adaBoost SAMME with SVM as classifier'

  def __str__(self):
    return 'adaBoost SAMME with SVM as classifier'

  def get_params(self, deep = True):
    return {"classifierNumber": self.classifierNumber, "learningRate": self.learningRate,
     "trainSamples": self.trainSamples, "C": self.C}

  def set_params(self, **parameters):
    for parameter, value in parameters.items():
        setattr(self, parameter, value)
    return self

  def fit(self, xTrain, yTrain, classifierNumber = None, C = None):
    """ Train the classifiers according to the predefined private attributes and the dataset that was input """
    self.classifierList = []
    self.classifierWeights = []
    if classifierNumber is not None:
      self.classifierNumber = classifierNumber
    if C is not None:
      self.C = C
    yTrainReshaped = np.reshape(yTrain,(-1, 1)) # reshape the yTrain array
    sampleData = np.concatenate([xTrain, yTrainReshaped], axis = 1) # concatenate all of the data
    self.classes = np.unique(yTrain) # get the possible values for the classes
    # Initialize sample weights
    dataSamples = xTrain.shape[0]
    sampleWeights = np.full(dataSamples, 1.0/dataSamples)

    # iteratively create the classifiers
    for i in range(self.classifierNumber):
      # estimatorErr = 1
      # while estimatorErr >= 0.5:
      trainData = sampleData[np.random.choice(dataSamples, self.trainSamples, p = sampleWeights)]# sample the training set
      classifier = SVC(C = self.C) # create tree
      classifier.fit(trainData[:, :-1], trainData[:, -1]) # fit the classifier
      yPredict = classifier.predict(xTrain) # predict with the newly created classifier
      incorrectPreds = (yPredict != yTrain) # Find the incorrect predictions
      estimatorErr = np.mean(np.average(incorrectPreds, weights = sampleWeights, axis = 0)) # calculate the classifier error
      estimatorWeight = np.log((1 - estimatorErr + 0.0001) / (estimatorErr + 0.0001)) + np.log(self.classes.shape[0] - 1)# calculate the estimator weight
      # 1 for correct vals, -1 for incorrect vals
      yTrain_x_yPred = np.zeros(incorrectPreds.shape)
      yTrain_x_yPred[incorrectPreds == False] = 1
      yTrain_x_yPred[incorrectPreds == True] = -1
      exp = np.exp(-estimatorWeight * yTrain_x_yPred)
      sampleWeights = np.multiply(sampleWeights, exp)
      sampleWeights = sampleWeights/np.sum(sampleWeights) # normalize the sample weights
      self.classifierList.append(classifier)
      self.classifierWeights.append(estimatorWeight) #append sample weights to list
    return self

  def predict(self, value):
    """ Function that predicts a class label based on the value or array of values given as input """
    if value.ndim > 1: # multiple samples for prediction?
      totalSamples = value.shape[0]
    else:
      value = np.reshape(value, (1, -1)) # reshape the data sample
      totalSamples = 1
    predictionWeights = np.full([totalSamples, self.classes.shape[0]], 0.0)
    # predictionWeight = np.full([totalSamples, self.classifierNumber], np.nan)
    for i in range(self.classifierNumber):
      prediction = self.classifierList[i].predict(value)
      for j in range(totalSamples):
        predictionWeights[j, int(prediction[j] - 1)] += self.classifierWeights[i]
    predictions = np.argmax(predictionWeights, axis = 1) + 1
    return predictions

  def score(self, xTest, yTest):
    """ Function that calculates the accuracy of the classifier according to some test data """
    sampleNumber = xTest.shape[0]
    prediction = self.predict(xTest)
    correctPredictions = prediction == yTest
    return(sum(correctPredictions)/sampleNumber)

  def confusionMat(self, xTest, yTest):
    """ Function that calculates the confusion matrix for the test data"""
    expectedLabels = self.classes # Get the classes/labels of the dataset
    confusionMatrix = np.full((expectedLabels.shape[0], expectedLabels.shape[0]), 0) # Create an empty conf mat
    for i in range(expectedLabels.shape[0]): # Iterate over the possible labels
      expectedLabel = expectedLabels[i]
      labelData = xTest[yTest == expectedLabel]
      predict = []
      # Check predictions
      predict = self.predict(labelData)
      # Count the number of each prediction
      unique, counts = np.unique(predict, return_counts = True)
      # Build the confusion matrix for the label 
      for element, count in zip(unique, counts):
        for j in range(expectedLabels.shape[0]):
          if expectedLabels[j] == element:
            confusionMatrix[i, j] = count
    return confusionMatrix
  def plotConfMat(self, xTest, yTest, figSize = [20.0, 10.0]):
    """ Function that pltos the confusion matrix for the test data """
    # Calculate the conf matrix:
    confMat = self.confusionMat(xTest, yTest)
    # Get the min and max values
    vmin = np.min(confMat)
    vmax = np.max(confMat)
    classes = self.classes
    classes = classes.astype(str)
    df_CM = pd.DataFrame(confMat, index = classes,
                  columns = classes)
    
    fig, axs = plt.subplots(nrows = 1, ncols = 2,
                       figsize = figSize,
                       gridspec_kw = dict(width_ratios = [3, 0.2]))
    # Plot both heat maps
    axs[0] = sns.heatmap(df_CM, vmin = vmin, vmax = vmax, annot = True, fmt = 'g', cbar = False, cmap = "summer", ax = axs[0])

    # Configure aesthetics for ax 0
    # axs[0].xaxis.set_ticks_position('top')
    axs[0].xaxis.set_tick_params(length = 0)
    axs[0].set_xlabel("Actual Values")
    axs[0].set_ylabel("Predicted Values")

    # Configure colorbar in ax 1
    axs[1] = fig.colorbar(axs[0].collections[0], cax = axs[1])
    fig.tight_layout()
    return fig, axs


# Now we need to define the repeated k-folder cross validation technique
# First, define the k-folder function:
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


# Then, the k fold cross validation function
def k_fold_crossval(estimator, dataX, dataY, folds = 10, parameters = None):
  clf = estimator
  dataY = np.reshape(dataY,(-1,1))
  data = np.concatenate([dataX, dataY], axis = 1)

  datasplit = k_folder(data, folds)
  classifier = []
  accuracy = []
  for i in range(folds):
    data = list(datasplit) # Get the list of folds
    test_data = data.pop(i) # Get and remove the respective test fold for the iteration
    train_data = np.concatenate((data), axis = 0) # Concatenate the rest of the data

    # create the classifier
    individual_classifier = estimator
    # set the classifier parameters
    if parameters is not None:
      individual_classifier.set_params(**parameters)
    individual_classifier.fit(trainData[:,:-1], trainData[:,-1]) # train the classifier

    # get the accuracy
    acc = individual_classifier.score(testData[:,:-1], testData[:,-1])
    
    classifier.append(individual_classifier)
    accuracy.append(acc)
  bestClassifier = classifier[np.argmax(accuracy)]
  avg_accuracy = np.mean(accuracy)
  return bestClassifier, avg_accuracy

# Finally, the repeated k-fold function:
def repeated_k_fold(estimator, dataX, dataY, reps = 10, folds = 10, parameters = None):
  reshapedDataY = np.reshape(dataY,(-1,1))
  data = np.concatenate([dataX, reshapedDataY], axis = 1)

  classifier_list = []
  accuracies = []

  for i in range(reps):
    np.random.shuffle(data) # shuffle the data
    classifier, accuracy = k_fold_crossval(estimator, data[:,:-1], data[:,-1], folds = folds, parameters = parameters)
    classifier_list.append(classifier)
    accuracies.append(accuracy) 
  return list(classifier_list), list(accuracies)

from timeit import default_timer as timer
classifierNumbersStump = [1, 10, 50, 100, 200, 500, 1000]
if test:
  classifierNumbersStump = [1, 10, 50]
if moreThan1Hour:
  classifierNumbersStump.append([2000])
totalClassifiersStump = len(classifierNumbersStump)
gridSearchStump = np.full([totalClassifiersStump, 2], np.nan)


estimator = adaBoostMC()
if verbose:
  print('Trying adaBoostMC with stumps')
for i in range(totalClassifiersStump):
  classNum = classifierNumbersStump[i]
  if verbose:
    print('Number of Classifiers: {0:d}'.format(classNum))
  parameters = {'classifierNumber':classNum}
  timerStart = timer()
  classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
  timerEnd = timer()
  totalTime = timerEnd - timerStart
  gridSearchStump[i, 0] = np.mean(accuracies) # save the mean of the accuracies
  gridSearchStump[i, 1] = totalTime # save the time it took to compute
  if verbose:
    print('10 times 10 fold adaboost: Average accuracy = {0:.2f}%, variance = {1:.4f}, time to compute: {2:.2f} seconds'.format(np.mean(accuracies) * 100, np.var(accuracies), totalTime))


classifierNumbersSVM = [1, 10, 50]
if test:
  classifierNumbersSVM = [1, 5]
if moreThan1Hour:
  classifierNumbersSVM.append([100])

totalClassifiersSVM = len(classifierNumbersSVM)
gridSearchSVM = np.full([totalClassifiersSVM, 2], np.nan)

estimator = adaBoostMC_SVC()
if verbose:
  print('Trying adaBoostMC with SVM')
for i in range(totalClassifiersSVM):
  classNum = classifierNumbersSVM[i]
  if verbose:
    print('Number of Classifiers: {0:d}'.format(classNum))
  parameters = {'classifierNumber':classNum}
  timerStart = timer()
  classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
  timerEnd = timer()
  totalTime = timerEnd - timerStart
  gridSearchSVM[i, 0] = np.mean(accuracies) # save the mean of the accuracies
  gridSearchSVM[i, 1] = totalTime # save the time it took to compute
  if verbose:
    print('10 times 10 fold adaboost: Average accuracy = {0:.2f}%, variance = {1:.4f}, time to compute: {2:.2f} seconds'.format(np.mean(accuracies) * 100, np.var(accuracies), totalTime))

# Select the best performing classifier
maxStumpPos = np.argmax(gridSearchStump[:,0])
maxSVMPos = np.argmax(gridSearchSVM[:,0])


classifiers = []
columns = ['accuracy', 'time_to_compute']
classifierComparisonAcc = []
classifierComparisonTime = []

#Check which had the highest accuracy:
if gridSearchStump[maxStumpPos, 0] >= gridSearchSVM[maxSVMPos, 0]:
  comparisonEstimator = adaBoostMC()
  classifiers.append('SAMME_stumps')
  chosenParams = {'classifierNumber':classifierNumbersStump[maxStumpPos]}
  chosenEstimator = 'stumps'
else:
  comparisonEstimator = adaBoostMC_SVC()
  classifiers.append('SAMME_SVM')
  chosenParams = {'classifierNumber':classifierNumbersSVM[maxSVMPos]}
  chosenEstimator = 'SVM'

#calculate SAMME accuracy and time
if verbose:
  print('Calculating SAMME using', chosenEstimator)
estimator = comparisonEstimator
estimator.set_params(**chosenParams)
timerStart = timer()
estimator.fit(trainData[:,:-1], trainData[:,-1])
accuracies = estimator.score(testData[:,:-1], testData[:,-1])
timerEnd = timer()
confMat = estimator.confusionMat(testData[:,:-1], testData[:,-1]) # Calculate the confusion matrix
fig, ax = estimator.plotConfMat(testData[:,:-1], testData[:,-1]) # Plot the confusion matrix
plt.show()
if test:
  plt.savefig('confusionMatrix.png', bbox_inches = 'tight')
totalTime = timerEnd - timerStart
classifierComparisonAcc.append(np.mean(accuracies))
classifierComparisonTime.append(totalTime)
if verbose:
  print('Time to compute:', totalTime) # show time it took to compute
  print('Mean accuracy:', np.mean(accuracies))

# Multiclass SVC as 1-vs-1
from sklearn.svm import SVC
classifiers.append('1v1_SVM')
if verbose:
  print('Calculating 1vs1 SVM using C=1')
estimator = SVC()
timerStart = timer()
estimator.fit(trainData[:,:-1], trainData[:,-1])
accuracies = estimator.score(testData[:,:-1], testData[:,-1])
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierComparisonAcc.append(np.mean(accuracies))
classifierComparisonTime.append(totalTime)
if verbose:
  print('Time to compute:', totalTime) # show time it took to compute
  print('Mean accuracy:', np.mean(accuracies))

# Random forest
from sklearn.ensemble import RandomForestClassifier
classifiers.append('Random_Forest')
if verbose:
  print('Calculating Random Forest using stumps')
estimator = RandomForestClassifier(max_depth=1, random_state=0)
timerStart = timer()
estimator.fit(trainData[:,:-1], trainData[:,-1])
accuracies = estimator.score(testData[:,:-1], testData[:,-1])
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierComparisonAcc.append(np.mean(accuracies))
classifierComparisonTime.append(totalTime)
if verbose:
  print('Time to compute:', totalTime) # show time it took to compute
  print('Mean accuracy:', np.mean(accuracies))

from sklearn.neighbors import KNeighborsClassifier
classifiers.append('KNN')
if verbose:
  print('Calculating KNN with K=1')
estimator = KNeighborsClassifier(n_neighbors=1)
timerStart = timer()
estimator.fit(trainData[:,:-1], trainData[:,-1])
accuracies = estimator.score(testData[:,:-1], testData[:,-1])
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierComparisonAcc.append(np.mean(accuracies))
classifierComparisonTime.append(totalTime)
if verbose:
  print('Time to compute:', totalTime) # show time it took to compute
  print('Mean accuracy:', np.mean(accuracies))

classifierAcc = np.asarray(classifierComparisonAcc)
classifierTime = np.asarray(classifierComparisonTime)
classifierComparison = np.concatenate([np.reshape(classifierAcc,(-1, 1)), np.reshape(classifierTime,(-1, 1))], axis = 1)

df_classifierComparison = pd.DataFrame(classifierComparison, index = classifiers, columns = columns)
print(df_classifierComparison)
if test:
  df_classifierComparison.to_excel("classifierComparison.xlsx")

def autolabel(ax, bars):
    """Attach a text label above each bar in *bars*, displaying its height."""
    for rect in bars:
        height = rect.get_height()
        ax.annotate('{0:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        
fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = figure_size, gridspec_kw = {'wspace':0.25})
x = np.arange(len(classifiers))  # the label locations
width = 0.35  # the width of the bars
colors = ["tab:blue", "tab:green"]
for ax, info, color, letter, lbl in zip(axs, [100 * classifierAcc, classifierTime], colors, ['(a)', '(b)'], ['Accuracy (%)', 'Time (s)']):
  bars = ax.bar(x - width/2, info, width, color=color, label = lbl)
  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel(lbl)
  ax.set_xticks(x)
  ax.set_xticklabels(classifiers, fontsize=14, rotation=45)
  ax.set_xlabel(letter)
  autolabel(ax, bars)
plt.show()
if test:
  plt.savefig('classifier.png', bbox_inches = 'tight')
  print('done!')
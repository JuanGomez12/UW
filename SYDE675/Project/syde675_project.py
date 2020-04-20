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
verbose = False

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
classifierNumbers = [1, 10, 50, 100, 200, 500, 1000]
totalClassifiers = len(classifierNumbers)
estimators = [adaBoostMC_SVC(), adaBoostMC()]
totalEstimators = len(estimators)
gridSearchStump = np.full([totalClassifiers, 2], np.nan)
gridSearchSVM = np.full([totalClassifiers, 2], np.nan)

estimator = adaBoostMC_SVC()
for i in range(totalClassifiers):
  classNum = classifierNumbers[i]
  print('Number of Classifiers: {0:d}'.format(classNum))
  parameters = {'classifierNumber':classNum}
  timerStart = timer()
  classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
  timerEnd = timer()
  totalTime = timerEnd - timerStart
  gridSearchSVM[i, 0] = np.mean(accuracies) # save the mean of the accuracies
  gridSearchSVM[i, 1] = totalTime # save the time it took to compute
  print('10 times 10 fold adaboost: Average accuracy = {0:.2f}%, variance = {1:.4f}, time to compute: {2:.2f} seconds'.format(np.mean(accuracies) * 100, np.var(accuracies), totalTime))

estimator = adaBoostMC()
for i in range(totalClassifiers):
  classNum = classifierNumbers[i]
  print('Number of Classifiers: {0:d}'.format(classNum))
  parameters = {'classifierNumber':classNum}
  timerStart = timer()
  classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
  timerEnd = timer()
  totalTime = timerEnd - timerStart
  gridSearchStump[i, 0] = np.mean(accuracies) # save the mean of the accuracies
  gridSearchStump[i, 1] = totalTime # save the time it took to compute
  print('10 times 10 fold adaboost: Average accuracy = {0:.2f}%, variance = {1:.4f}, time to compute: {2:.2f} seconds'.format(np.mean(accuracies) * 100, np.var(accuracies), totalTime))

classifiers = []
columns = ['accuracy', 'time_to_compute']

# adaboostMC using SAMME, 200 classifiers
parameters = {'classifierNumber':200, 'maxDepth':1}
classifiers.append('SAMME_AdaBoost_200')
estimator = adaBoostMC()
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = classifierInfo
# classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

# adaboostMC using SAMME, 500 classifiers
parameters = {'classifierNumber':500, 'maxDepth':1}
classifiers.append('SAMME_AdaBoost_500')
estimator = adaBoostMC()
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

# adaboostMC using SAMME, 800 classifiers
parameters = {'classifierNumber':800, 'maxDepth':1}
classifiers.append('SAMME_AdaBoost_800')
estimator = adaBoostMC()
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

# adaboostMC_SVC using C = 1, 100 classifiers
parameters = {'classifierNumber':100, 'C':1}
classifiers.append('SVC_AdaBoost_100')
estimator = adaBoostMC_SVC()
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1], parameters = parameters)
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

# Multiclass SVC as 1-vs-1
from sklearn.svm import SVC
classifiers.append('1v1_SVM')
estimator = SVC()
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1])
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

# Random forest
from sklearn.ensemble import RandomForestClassifier
classifiers.append('Random_Forest')
estimator = RandomForestClassifier(max_depth=1, random_state=0)
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1])
timerEnd = timer()
totalTime = timerEnd - timerStart
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

from sklearn.neighbors import KNeighborsClassifier
classifiers.append('KNN')
estimator = KNeighborsClassifier(n_neighbors=1)
timerStart = timer()
classifier, accuracies = repeated_k_fold(estimator, trainData[:,:-1], trainData[:,-1])
timerEnd = timer()
classifierInfo = np.zeros((1,2))
classifierInfo[0,0] = np.mean(accuracies)
classifierInfo[0,1] = totalTime
classifierComparison = np.concatenate([classifierComparison, classifierInfo], axis = 0)
print('Time to compute:', totalTime) # show time it took to compute
print('Mean accuracy:', np.mean(accuracies))

df_classifierComparison = pd.DataFrame(classifierComparison, index = classifiers, columns = columns)
# df_classifierComparison.to_excel("classifierComparison.xlsx")
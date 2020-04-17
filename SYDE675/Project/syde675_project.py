# -*- coding: utf-8 -*-
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
from sklearn.svm import SVC

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

# try:
#   df_X_train = pd.read_csv('X_train.txt', delim_whitespace=True,  header = None, names = features) # Load file
# except:
#   print("Could not find the hw3_dataset1 dataset, is it in the same folder as the .py?")
# else:
#   print("hw3_dataset1 dataset loaded correctly")

# create the adaboost multiclass class
from sklearn import tree

class adaBoostMC:
  def __init__(self, classifierNumber = 50, learningRate = 0.5, trainSamples = 1000, maxDepth = 1):
    self.classifierNumber = classifierNumber # target number of classifiers to use
    self.learningRate = learningRate # learning rate
    self.trainSamples = trainSamples # number of samples to use for training
    self.maxDepth = maxDepth
    self.classifierList = []
    self.classifierWeights = []
    self.classes = []
  def __repr__(self):
    return 'adaBoost classifier'
  def __str__(self):
    return 'adaBoost classifier'
  def fit(self, xTrain, yTrain):
    """ Train the classifiers according to the predefined private attributes and the dataset that was input """
    yTrainReshaped = np.reshape(yTrain,(-1, 1)) # reshape the yTrain array
    sampleData = np.concatenate([xTrain, yTrainReshaped], axis = 1) # concatenate all of the data
    self.classes = np.unique(yTrain) # get the possible values for the classes
    # Initialize sample weights
    dataSamples = xTrain.shape[0]
    sampleWeights = np.full(dataSamples, 1/dataSamples)

    # iteratively create the classifiers
    for i in range(self.classifierNumber):
      estimatorErr = 1
      while estimatorErr >= 0.5:
        trainData = sampleData[np.random.choice(dataSamples, self.trainSamples, p = sampleWeights)]# sample the training set
        classifier = tree.DecisionTreeClassifier(max_depth = self.maxDepth) # create tree
        classifier.fit(trainData[:, :-1], trainData[:, -1]) # fit the classifier
        yPredict = classifier.predict(xTrain) # predict with the newly created classifier
        incorrectPreds = (yPredict != yTrain) # Find the incorrect predictions
        estimatorErr = np.mean(np.average(incorrectPreds, weights = sampleWeights, axis = 0)) # calculate the classifier error
      estimatorWeight = np.log((1 - estimatorErr) / estimatorErr) # calculate the estimator weight
      yTrain_x_yPred = np.multiply(yPredict, yTrain)
      exp = np.exp(-estimatorWeight * yTrain_x_yPred)
      sampleWeights = np.multiply(sampleWeights, exp)
      sampleWeights = sampleWeights/np.sum(sampleWeights) # normalize the sample weights
      self.classifierList.append(classifier)
      self.classifierWeights.append(estimatorWeight) #append sample weights to list
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
      for j in totalSamples:
        predictionWeights[j, prediction[j]] += self.classifierWeights[i]
    predictions = np.argmax(predictionWeights, axis = 1)
    return predictions
  def OGpredict(self, value):
    """ Function that predicts a class label based on the value or array of values given as input """
    if value.ndim > 1: # multiple samples for prediction?
      totalSamples = value.shape[0]
    else:
      value = np.reshape(value, (1, -1)) # reshape the data sample
      totalSamples = 1
    predictionWeight = np.full([totalSamples, self.classifierNumber], np.nan)
    for i in range(self.classifierNumber):
      prediction = self.classifierList[i].predict(value)
      predictionWeight [:, i]= prediction * self.classifierWeights[i]
    predictions = np.sum(predictionWeight, axis = 1)
    predictions[predictions >= 0] = 1.0 # samples predicted as 1
    predictions[predictions < 0] = -1.0 # samples predicted as -1
    return predictions
  def score(self, xTest, yTest):
    """ Function that calculates the accuracy of the classifier according to some test data """
    sampleNumber = xTest.shape[0]
    prediction = self.predict(xTest)
    correctPredictions = prediction == yTest
    return(sum(correctPredictions)/sampleNumber)
  def plot(self, datasetX, datasetY, figureSize = [20, 10], h = 0.1):
    """ Function that plots the decision boundary and scatterplots of the dataset given as input """
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = figureSize)
    alph = 0.35

    datasetClasses = np.unique(datasetY)

    datasetYReshaped = np.reshape(datasetY,(-1, 1))
    dataset = np.concatenate([datasetX, datasetYReshaped], axis = 1)

    # Create and set the color map
    heatmap_colors = ["tab:blue", "tab:green"]
    cmap_jm = ListedColormap(heatmap_colors)

    # for dataset, i in zip(datasets, range(len(datasets))):
    xVals = datasetX
    classLabels = datasetY

    # create a mesh
    x_min, x_max = xVals[:, 0].min() - 0.3 * abs(xVals[:, 0].min()), xVals[:, 0].max() + 0.3 * abs(xVals[:, 0].max())
    y_min, y_max = xVals[:, 1].min() - 0.3 * abs(xVals[:, 1].min()), xVals[:, 1].max() + 0.3 * abs(xVals[:, 1].max())
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Put the result into a color plot
    Z = self.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap = cmap_jm, alpha = alph) #plot the mesh in color


    #plot the dataset
    dsetC1 = datasetX[datasetY == datasetClasses[0]]
    dsetC2 = datasetX[datasetY == datasetClasses[1]]
    ax.scatter(dsetC1[:, 0], dsetC1[:, 1], color = heatmap_colors[0], s = 40, label = 'Class ' + str(int(datasetClasses[0])))
    ax.scatter(dsetC2[:, 0], dsetC2[:, 1], color = heatmap_colors[1], s = 40, label = 'Class ' + str(int(datasetClasses[1])))

    ax.set_xlabel('feat1')
    ax.set_ylabel('feat2')
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())

    legendHandles, labels = ax.get_legend_handles_labels()
    legendHandles.insert(0, Patch(facecolor = heatmap_colors[1], alpha = alph,  edgecolor = 'None',
                        label = 'Class ' + str(int(datasetClasses[1]))))
    legendHandles.insert(0, Patch(facecolor = heatmap_colors[0], alpha = alph, edgecolor = 'None',
                        label = 'Class ' + str(int(datasetClasses[0]))))
    ax.legend(ncol = 2, handles = legendHandles, columnspacing = 0.8, handlelength = 1.5)
    # plt.show()
    return fig, ax

class adaBoost:
  def __init__(self, classifierNumber = 50, learningRate = 0.5, trainSamples = 100):
    self.classifierNumber = classifierNumber # target number of classifiers to use
    self.learningRate = learningRate # learning rate
    self.trainSamples = trainSamples # number of samples to use for training
    self.classifierList = []
    self.classifierWeights = []
  def __repr__(self):
    return 'adaBoost classifier'
  def __str__(self):
    return 'adaBoost classifier'
  def fit(self, xTrain, yTrain):
    """ Train the classifiers according to the predefined private attributes and the dataset that was input """
    yTrainReshaped = np.reshape(yTrain,(-1, 1)) # reshape the yTrain array
    sampleData = np.concatenate([xTrain, yTrainReshaped], axis = 1) # concatenate all of the data

    # Initialize sample weights
    dataSamples = xTrain.shape[0]
    sampleWeights = np.full(dataSamples, 1/dataSamples)

    # iteratively create the classifiers
    for i in range(self.classifierNumber):
      estimatorErr = 1
      while estimatorErr >= 0.5:
        trainData = sampleData[np.random.choice(dataSamples, self.trainSamples, p = sampleWeights)]# sample the training set
        classifier = tree.DecisionTreeClassifier(max_depth = 1) # create the stump
        classifier.fit(trainData[:, :-1], trainData[:, -1]) # fit the classifier
        yPredict = classifier.predict(xTrain) # predict with the newly created classifier
        incorrectPreds = (yPredict != yTrain) # Find the incorrect predictions
        estimatorErr = np.mean(np.average(incorrectPreds, weights = sampleWeights, axis = 0)) # calculate the classifier error
      estimatorWeight = self.learningRate * np.log((1 - estimatorErr) / estimatorErr) # calculate the estimator weight
      yTrain_x_yPred = np.multiply(yPredict, yTrain)
      exp = np.exp(-estimatorWeight * yTrain_x_yPred)
      sampleWeights = np.multiply(sampleWeights, exp)
      sampleWeights = sampleWeights/np.sum(sampleWeights) # normalize the sample weights
      self.classifierList.append(classifier)
      self.classifierWeights.append(estimatorWeight) #append sample weights to list
  def predict(self, value):
    """ Function that predicts a class label based on the value or array of values given as input """
    if value.ndim > 1: # multiple samples for prediction?
      totalSamples = value.shape[0]
    else:
      value = np.reshape(value, (1, -1)) # reshape the data sample
      totalSamples = 1
    predictionWeight = np.full([totalSamples, self.classifierNumber], np.nan)
    for i in range(self.classifierNumber):
      prediction = self.classifierList[i].predict(value)
      predictionWeight [:, i]= prediction * self.classifierWeights[i]
    predictions = np.sum(predictionWeight, axis = 1)
    predictions[predictions >= 0] = 1.0 # samples predicted as 1
    predictions[predictions < 0] = -1.0 # samples predicted as -1
    return predictions
  def score(self, xTest, yTest):
    """ Function that calculates the accuracy of the classifier according to some test data """
    sampleNumber = xTest.shape[0]
    prediction = self.predict(xTest)
    correctPredictions = prediction == yTest
    return(sum(correctPredictions)/sampleNumber)
  def plot(self, datasetX, datasetY, figureSize = [20, 10], h = 0.1):
    """ Function that plots the decision boundary and scatterplots of the dataset given as input """
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = figureSize)
    alph = 0.35

    datasetClasses = np.unique(datasetY)

    datasetYReshaped = np.reshape(datasetY,(-1, 1))
    dataset = np.concatenate([datasetX, datasetYReshaped], axis = 1)

    # Create and set the color map
    heatmap_colors = ["tab:blue", "tab:green"]
    cmap_jm = ListedColormap(heatmap_colors)

    # for dataset, i in zip(datasets, range(len(datasets))):
    xVals = datasetX
    classLabels = datasetY

    # create a mesh
    x_min, x_max = xVals[:, 0].min() - 0.3 * abs(xVals[:, 0].min()), xVals[:, 0].max() + 0.3 * abs(xVals[:, 0].max())
    y_min, y_max = xVals[:, 1].min() - 0.3 * abs(xVals[:, 1].min()), xVals[:, 1].max() + 0.3 * abs(xVals[:, 1].max())
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Put the result into a color plot
    Z = self.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap = cmap_jm, alpha = alph) #plot the mesh in color


    #plot the dataset
    dsetC1 = datasetX[datasetY == datasetClasses[0]]
    dsetC2 = datasetX[datasetY == datasetClasses[1]]
    ax.scatter(dsetC1[:, 0], dsetC1[:, 1], color = heatmap_colors[0], s = 40, label = 'Class ' + str(int(datasetClasses[0])))
    ax.scatter(dsetC2[:, 0], dsetC2[:, 1], color = heatmap_colors[1], s = 40, label = 'Class ' + str(int(datasetClasses[1])))

    ax.set_xlabel('feat1')
    ax.set_ylabel('feat2')
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())

    legendHandles, labels = ax.get_legend_handles_labels()
    legendHandles.insert(0, Patch(facecolor = heatmap_colors[1], alpha = alph,  edgecolor = 'None',
                        label = 'Class ' + str(int(datasetClasses[1]))))
    legendHandles.insert(0, Patch(facecolor = heatmap_colors[0], alpha = alph, edgecolor = 'None',
                        label = 'Class ' + str(int(datasetClasses[0]))))
    ax.legend(ncol = 2, handles = legendHandles, columnspacing = 0.8, handlelength = 1.5)
    # plt.show()
    return fig, ax


# ada = adaBoostMC(maxDepth = 2)
ada = adaBoostMC()
ada.fit(trainData[:,:-1], trainData[:,-1])
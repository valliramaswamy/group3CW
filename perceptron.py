#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:17:29 2022

@author: adil
"""
import os
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from math import sqrt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import math
import matplotlib.pyplot as plt
import seaborn as sns


datapath = "/Users/adil/Documents/INTRO TO AI COURSEWORK/dataset modified/Clean_Dataset_group3(classifier).csv"
# this will read the dataset as a dataframe i.e. flight is the dataframe 
flight = pd.read_csv(datapath)

# FAIZA:
flight = flight.sort_values(by='airline', ascending=True)
flight.isnull().values.all().sum()

# VALLI:
# Feature Engineering: removing outliers & adding new logged price column
# error with boxplot code
plt.boxplot(flight['price'])
plt.show()

# Creates a new column in the dataframe named 'price outlier'
flight['price_outlier'] = 0

#to find the mean and standard deviation of the price values to work out the outlier
price_mean = np.mean(flight['price'])
print(price_mean)
price_std = np.std(flight['price'])
print(price_std)

#calculation to assign 0 or 1 to the price values (0 if the datapoint is not an outlier & 1 if it is)
flight.loc[abs(flight['price'] - price_mean) > 2 * price_std,'price_outlier'] = 1

#This counts the number of unique outlier values
print(Counter(flight['price_outlier']))

flight = flight[flight.price_outlier != 1]
print (flight.shape) 

# Dropping 'price outlier' column
flight.drop('price_outlier', 1, inplace=True)


# AAKASH:
le = LabelEncoder()

flight['airline'] = le.fit_transform(flight['airline'])
flight['source_city'] = le.fit_transform(flight['source_city'])
flight['departure_time'] = le.fit_transform(flight['departure_time'])
flight['arrival_time'] = le.fit_transform(flight['arrival_time'])
flight['destination_city'] = le.fit_transform(flight['destination_city'])
flight['class'] = le.fit_transform(flight['class'])

flight['price_classifier'] = le.fit_transform(flight['price_classifier'])


# Find unique values within the stops column
#print(list(set(flight['stops'])))

# Match and replace the numerical values in text with integers
flight['stops'] = flight['stops'].replace(["zero", "one", "two_or_more"], [0, 1, 2])

# ABOVE WAS PRE PROCESSING

# flight.price_classifier was created using a seperate table with extra column under adil branch 
# and its value is either "high" or "low" relative to the median of the log price column = 4.358886.
# Median of log price was retrieved using python code: print(flight.log_price.describe())

print(flight)
print(flight.price_classifier)


# target variable
Y = flight.price_classifier
print(Y)

# splitting the data. difering random states widly affects the accuracy of the model. can also be None
flight_train, flight_test, Y_train, Y_test = train_test_split(flight, Y, test_size=0.2, random_state=55)

# row numbers showing a split of 80 to 20 when printed compared to just printing flight.shape
print (flight_train.shape)
print (flight_test.shape)
print (Y_train.shape)
print (Y_test.shape)

# will adjust training parameters s
percep = Perceptron(max_iter = 500, tol=0.001, eta0=1)

# training perceptron.  
percep.fit(flight_train,Y_train)

# make predication
Y_pred = percep.predict(flight_test)
# evaluate accuracy
print('Accuracy: %.2f' % accuracy_score(Y_test, Y_pred))
print(Y_pred)

# It started working from here
result = []

# Should i use price classifier or price for if statement? 
for x in flight.columns:
    if x != 'price_classifier':
        result.append(x)

# Taking 
X = flight[result].values
y = flight['price_classifier'].values


kf = KFold(5,shuffle=True)
fold = 1
# The data is split five ways, for each fold, the 
# Perceptron is trained, tested and evaluated for accuracy
for train_index, validate_index in kf.split(X,y):
    # ERROR BECAUSE OF LINE 128 (fixed because of the new X instead of just the dataframe  )
    percep.fit(X[train_index],y[train_index])
    y_test = y[validate_index]
    y_pred = percep.predict(X[validate_index])

    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print(f"Fold #{fold}, Training Size: {len(X[train_index])}, Validation Size: {len(X[validate_index])}")
    fold += 1

# we want to comapre the prediction data with the testing data since testing data is what the 
# prediction is based on and is the actual data. so convert the column to an array then calculate 
# rmse. 
#What is this code should i keep? 
priceclassifier_testarray = flight_test.price_classifier.to_numpy()
# printing test data price classifier's array

plt.scatter(y_pred[:100], y_test[:100])

sns.regplot(x = y_test, y = y_pred, scatter = False)

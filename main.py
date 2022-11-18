# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kGJFmcjR9azJKCLxHVDtR5JldHrQyCRS
"""

from google.colab import drive
drive.mount('/content/drive')

"""First we import libraries that we are going to use"""

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""Here we define a class that can calculate polynomial regression with getting train data, target column, dimensions, epoch & learning rate.
In this class we define some function for this job.

#normalize:#
In here, first we calculate train data's power that are determined in the dimension list and put the resluts in a np.array object.
Then we calculate mean and var for all columns in we calculated in the prevoius part and store them in a np.array object.(In case that we can use them on the test data)
And we also find the normalized (standardized) data by this var and mean arrays.

#gradian_function:#
This gradian function is exactly the same as linear gradian_function.

#cost_function_simplified:#
This cost function is exactly the same as linear cost_function.

#PR_GD:#
Here we fist normalize data using the function normalize().
then we make random weights vector by using random.random() function. But we multiplies numbers by 1000000000 because when we normalize data, data range (specialy for powers more than 1 or 2) is very low, so we do this just to make the this weights acceptable. (If we don't do this, our PR_GD function, can only find the bias parameter (w of the 0 power of the traing data) correctly, and it won't fluctuate in an appropriate order, it almost fluctuate in 0.00001)
Then we run the algorithm epoch times.

#test:#
Here we use the weight vector that we figured in the previous part and the test data (after we calculated power of test data by the dimensions list and normalizing them using mean & var narrays) and we draw plots of the result.
"""

class Polynomial_Regression:
  def __init__(self, train, target, dimensions, learning_rate, epoch):
    self.train = train.to_numpy()
    self.target = target.to_numpy()
    self.dimensions = dimensions
    self.learning_rate = learning_rate
    self.epoch = epoch
  
  # def normalize(self):
  #   self.mean = np.mean(self.train)
  #   self.var = np.var(self.train)
  #   self.x = (self.train - self.mean) / self.var
  #   self.x = np.array([(np.array(self.x) ** x) for x in self.dimensions])
  #   self.x = np.transpose(self.x)

  def normalize(self):
    self.x = np.array([self.train ** dim for dim in dimensions])
    self.mean = np.array([np.mean(i) for i in self.x])
    self.var = np.array([np.var(i) for i in self.x])
    self.x = np.array([(self.x[i] - self.mean[i]) / self.var[i] if self.var[i] != 0 else self.x[i] for i in range(len(self.x))])
    self.x = np.transpose(self.x)

  def gradian_function(self, predict, w):
    return np.dot(predict - self.target, self.x) / len(self.x)

  def cost_function_simplified(self, predicts):
    return np.sum((predicts - self.target) ** 2) / (2 * len(self.target))

  def PR_GD(self):
    self.normalize()
    w = np.array([random.random() * (10 ** (9)) if x != 0 else random.random() for x in self.dimensions])
    print('Random Weights: ', w)
    predict = np.dot(self.x, w)
    costs = []
    cost = self.cost_function_simplified(predict)
    costs.append(cost)
    for i in range(self.epoch):
      gradian = self.gradian_function(predict, w)
      # print('gradian')
      # print(gradian)
      w = w - (self.learning_rate * gradian)
      predict = np.dot(self.x, w)
      cost = self.cost_function_simplified(predict)
      costs.append(cost)
    print('Final Cost: ', cost)
    plt.plot([i for i in range(len(costs))], costs)
    plt.xlabel('Test Number')
    plt.ylabel('Cost Function')
    plt.title('Cost-Function-Result')
    plt.savefig("Cost-Function-Image.png")
    plt.show()
    return w
  
  def test(self, w, test, correct):
    # test = np.array((test - self.mean) / self.var)
    test = np.array([(test ** x) for x in self.dimensions])
    test = np.array([np.array((test[i] - self.mean[i]) / self.var[i]) if self.var[i] != 0 else test[i] for i in range(len(test))])
    test = np.transpose(test)
    print('test[0]: ', test[0])
    predict = np.dot(test, weights)
    print('Predict:')
    print(predict)
    # plt.scatter([x for x in test_copy], np.array(correct), color='b')
    # plt.scatter([x for x in test_copy], np.array(predict), color='r')
    plt.plot([x for x in range(len(correct))], np.array(correct), color='b')
    plt.plot([x for x in range(len(predict))], np.array(predict), color='r')
    plt.xlabel('Number')
    # plt.xlabel('Mileage')
    plt.ylabel('Price/Predict')
    # dff = pd.read_csv('/content/drive/MyDrive/ML_HW2_Q2/data.csv')
    # lable = dff.iloc[len(dff) - 100:, :]
    # lable = np.array(lable['Mileage'])
    # plt.scatter(lable, np.array(correct), color='b')
    # plt.scatter(lable, np.array(predict), color='r')
    # plt.savefig('Predict-Terget*Mileage.png')
    plt.show()
    mins = [min(correct), min(predict)]
    maxs = [max(correct), max(predict)]
    plt.plot([min(mins), max(maxs)], [min(mins), max(maxs)])
    plt.scatter(predict, correct)
    plt.xlabel('Predict')
    plt.ylabel('Price')
    # plt.savefig('Terget*Predict.png')
    plt.show()

df = pd.read_csv('/content/drive/MyDrive/ML_HW2_Q2/data.csv')
train_limit_number = len(df) - 100
test = df.iloc[train_limit_number:, :]
df = df.iloc[:train_limit_number, :]
dimensions = list(range(5))
train = df['Mileage']
target = df['Price']
# learning_rate = 0.000017
learning_rate = 0.0000170007
epoch = 10000000
pr = Polynomial_Regression(train, target, dimensions, learning_rate, epoch)
weights = pr.PR_GD()
print('weights: ', weights)
pr.test(weights, test['Mileage'].to_numpy(), test['Price'].to_numpy())
from sklearn import svm, preprocessing, decomposition
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import pandas as pd
import sys
from keras.utils import to_categorical
from keras.layers import Conv1D, Convolution1D, GlobalAveragePooling1D, MaxPooling1D

# Feature Importance
from sklearn import datasets
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier


a = np.loadtxt('weather109.txt')
a_rows = a.shape[0]
y1 = np.zeros(a_rows)

b = np.loadtxt('time_here109.txt')
b_rows = b.shape[0]
y2 = np.ones(b_rows)

# create a combined matrix
X = np.concatenate((a, b), axis=0)

# create vector of labels
y = np.append(y1, y2)



# SVM = support vector machine
X = preprocessing.StandardScaler().fit_transform(X) # 0.88 - more accurate than .normalize
#X = preprocessing.normalize(X) # 0.72 accuracy

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33) #can change to 0.20 #train_test_split(X[:,:10], y, test_size=0.33)

clf = svm.SVC()
print clf.fit(X_train, y_train)
svm_score = clf.score(X_test, y_test)*100
print "accuracy: ", svm_score




pca = decomposition.PCA(2) #because we want 2D to visualize
x_pca = pca.fit_transform(X)

#print x_pca.shape

fig = plt.figure()
# Make room for legend at bottom
fig.subplots_adjust(bottom=0.2)
# The axes for your lists 1-3
ax1 = fig.add_subplot(111)

# Plot line
color = ['b' if i == 0 else 'g' if i == 1 else 'r' for i in y]
line = ax1.scatter(x_pca[:,0], x_pca[:,1], c=color, marker='.') #(x_pca,'.',label='pca')

#plt.show() # this 2 D plot is low key a bad representation. seems super clustered and seems hard to differentiate

# LSTM Recurrent Neural Networks with Keras (long short-term memory)
X = np.expand_dims(X, axis=2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
y_train = to_categorical(y_train, 2) #Converts a class vector (integers) to binary class matrix.
y_test = to_categorical(y_test, 2) #E.g. for use with categorical_crossentropy. SECOND ARGUMENT IS NUMBER OF CLASSES

#print "X train shape: ", X_train.shape
embedding_vector_length = 1
model = Sequential()
model.add(LSTM(50, input_shape=(70, 1))) # 50 is the number of "rows" (number of nodes that are vertical). (350, 1) or (70, 1) is the input shape
model.add(Dense(2, activation='softmax')) # activation='softmax'???? 2 or 3 for number of classes we have (classes 0, 1, 2 means Dense(3) while classes 0, 1 means Dense(2))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) # categorical_crossentropy!!!
print(model.summary())
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=7, batch_size=64) # epochs=170 gives ~92-95%

scores = model.evaluate(X_test, y_test, verbose=0)
acc = scores[1]*100
print("Accuracy of LSTM: %.2f%%" % (scores[1]*100))
########################

print "X before: ", X.shape
seq_length = 1
#X = np.expand_dims(X, axis=2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
print "X after: ", X.shape
model2 = Sequential()
model2.add(Conv1D(64, 3, activation='relu', input_shape=(70, 1))) # input shape the same shape as training data?
model2.add(Conv1D(64, 3, activation='relu'))
model2.add(MaxPooling1D(3))
model2.add(Conv1D(128, 3, activation='relu'))
model2.add(Conv1D(128, 3, activation='relu'))
model2.add(GlobalAveragePooling1D())
model2.add(Dropout(0.5))
model2.add(Dense(1, activation='sigmoid')) # use 2 if using sparse_categorical_crossentropy

print "x train: ", X_train.shape
print "y train: ", y_train.shape
print "x test: ", X_test.shape
print "y test: ", y_test.shape
#loss='binary_crossentropy'
#sparse_categorical_crossentropy
model2.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model2.fit(X_train, y_train, batch_size=16, epochs=17)
model2.fitX = np.expand_dims(X, axis=2)

score = model2.evaluate(X_test, y_test, batch_size=16)
print("Accuracy of 1D Convolutions: %.2f%%" % (score[1]*100))



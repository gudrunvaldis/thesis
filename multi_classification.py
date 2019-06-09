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
from keras.utils import to_categorical
import pandas as pd
import sys
from keras.layers import Conv1D, Convolution1D, GlobalAveragePooling1D, MaxPooling1D

# previously two_group_classification.py
# time interval on these vectors was 1 second
svmm = open("svm_5class_largebuckets.txt", "w")
lstmm = open("lstm_5class_largebuckets.txt", "w")
one = open("oned_5class_largebuckets.txt", "w")
# load in vectors and find the number of rows of each

total_svm = 0
total_lstm = 0
total_oned = 0
for x in range(0, 100):

	# read in the vectors - comment out as needed
	a = np.loadtxt('20x4.txt')
	a_rows = a.shape[0]
	y1 = np.zeros(a_rows)

	b = np.loadtxt('forecast_today.txt')
	b_rows = b.shape[0]
	y2 = np.ones(b_rows)

	c = np.loadtxt('google_home.txt')
	c_rows = c.shape[0]
	y3 = np.full((1, c_rows), 2)

	d = np.loadtxt('turing_largebuckets.txt')
	d_rows = d.shape[0]
	y4 = np.full((1, d_rows), 3)

	e = np.loadtxt('mars_largebuckets.txt')
	e_rows = e.shape[0]
	y5 = np.full((1, e_rows), 4)

	# create a combined matrix
	X = np.concatenate((a, b), axis=0)
	X = np.concatenate((X, c), axis=0)
	X = np.concatenate((X, d), axis=0)
	X = np.concatenate((X, e), axis=0)

	# create vector of labels
	y = np.append(y1, y2)
	y = np.append(y, y3)
	y = np.append(y, y4)
	y = np.append(y, y5)

	# SVM = support vector machine
	X = preprocessing.StandardScaler().fit_transform(X) # 0.88 - more accurate than .normalize in the line below
	#X = preprocessing.normalize(X) # 0.72 accuracy

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

	clf = svm.SVC()
	print clf.fit(X_train, y_train)
	svm_score = clf.score(X_test, y_test)*100
	print "accuracy: ", svm_score
	svmm.write('%s' % svm_score)
	svmm.write(" ")
	total_svm += svm_score

	# LSTM Recurrent Neural Networks with Keras (long short-term memory)
	X = np.expand_dims(X, axis=2)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
	y_train = to_categorical(y_train, 5) #Converts a class vector (integers) to binary class matrix.
	y_test = to_categorical(y_test, 5) #E.g. for use with categorical_crossentropy. SECOND ARGUMENT IS NUMBER OF CLASSES

	embedding_vector_length = 1
	model = Sequential()
	model.add(LSTM(50, input_shape=(70, 1))) # 50 is the number of "rows" (number of nodes that are vertical). (350, 1) or (140, 1) or (70, 1) is the input shape
	model.add(Dense(5, activation='softmax')) # activation='softmax' works best. 2 or 3 for number of classes we have (classes 0, 1, 2 means Dense(3) while classes 0, 1 means Dense(2))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	print(model.summary())
	model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=170, batch_size=64) # epochs=170 gives most accurate results

	scores = model.evaluate(X_test, y_test, verbose=0)
	acc = scores[1]*100
	print("Accuracy of LSTM: %.2f%%" % (scores[1]*100))
	lstmm.write('%s' % acc)
	lstmm.write(" ")
	total_lstm += acc

	
	# 1D Convolutions
	seq_length = 1

	model2 = Sequential()
	model2.add(Conv1D(64, 3, activation='relu', input_shape=(70, 1)))
	model2.add(Conv1D(64, 3, activation='relu'))
	model2.add(MaxPooling1D(3))
	model2.add(Conv1D(128, 3, activation='relu'))
	model2.add(Conv1D(128, 3, activation='relu'))
	model2.add(GlobalAveragePooling1D())
	model2.add(Dropout(0.5))
	model2.add(Dense(5, activation='sigmoid')) # use 2 if using sparse_categorical_crossentropy - first argument is number of classes

	model2.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	model2.fit(X_train, y_train, batch_size=16, epochs=170)
	model2.fitX = np.expand_dims(X, axis=2)

	score = model2.evaluate(X_test, y_test, batch_size=16)
	acc = score[1]*100
	one.write('%s' % acc)
	one.write(" ")
	total_oned += acc
	print("Accuracy of 1D Convolutions: %.2f%%" % (score[1]*100))

svmm.close()
lstmm.close()
one.close()
print "total SVM: ", total_svm
print "total LSTM: ", total_lstm
print "total 1D: ", total_oned


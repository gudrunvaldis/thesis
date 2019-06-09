import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys



# # load numpy arrays
a = np.loadtxt('lstm_smallbuckets_forecToday_20x4.txt')

print "min: ", np.amin(a)
print "max: ", np.amax(a)
print "std dev: ", np.std(a)
print "mean: ", np.mean(a)




sys.exit()



time = [1, 0.2]
two_qs = [88.37, 94.07]
three_qs = [66.72, 77.05]

plt.plot(time, two_qs, color='g', label='Binary Classification')
plt.plot(time, three_qs, color='orange', label='Three-Class Classification')
plt.xlabel('Time interval (sec)')
plt.ylabel('Average Accuracy of Classification Models')
plt.xticks(time)
plt.ylim(50, 100)
plt.legend(loc='upper right')
plt.show()


sys.exit()
# a_rows = a.shape[0]
# y1 = np.zeros(a_rows)

# b = np.loadtxt('time_here.txt')
# b_rows = b.shape[0]
# y2 = np.ones(b_rows)

# #	c = np.loadtxt('bebe12.txt')
# #	c_rows = c.shape[0]
# #	y3 = np.full((1, c_rows), 2)
# #print "current y3:", y3 
# #print "c rows: ", c_rows

# #############################################################

# # create a combined matrix
# X = np.concatenate((a, b), axis=0)
# #	X = np.concatenate((X, c), axis=0)
# #print X

# # create vector of labels
# y = np.append(y1, y2)
# #	y = np.append(y, y3)
# #print y

# #sys.exit()

# #############################################################

# #print "X shape: ", X.shape
# #print "Y shape: ", y.shape

# # summary statistics to see if need more data
# df = pd.DataFrame(data=X)
# #df = df.mean(axis=1)
# df['y'] = pd.Series(y, index=df.index)
# #print "DF: ", df
# df_grouped = df.groupby('y')

# df_mean = df_grouped.mean()
# df_mean = df_mean.transpose()
# df_mean.plot()
# plt.xlim((0, 30))
# #plt.show() # shows average traffic size 

# df_std = df_grouped.std()
# df_std = df_std.transpose()
# df_std.plot()
# plt.xlim((0, 30))
# #plt.show()

#############################################################

# get the numpy vectors of accuracy for each ML aglorithm
q = np.loadtxt('oned_20x4_forecToday_smallbuckets.txt') #svm_smallbuckets_bebe12_dada12
num_bins = 12
#use 'blue' for LSTM - 'red' for SVM - 'green' for 1D
n, bins, patches = plt.hist(q, num_bins, facecolor='green', edgecolor='black', alpha=0.5)
#plt.title('Distribution of Accuracy')
plt.ylabel('Quantity')
plt.xlabel('Accuracy (%)')
plt.ylim(0, 40)
plt.axvline(q.mean(), color='k', linestyle='dashed', linewidth=1)
plt.xlim(70, 100)
plt.subplots_adjust(left=0.15)
plt.show()


# plot the distribution









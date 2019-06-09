import numpy as np


q = np.loadtxt('oned_bebe12_dada6_received_largebuckets.txt')

total_sum = 0

for element in q:
	total_sum = total_sum + element

print "accuracy (%): ", total_sum/100




# lstm_smallbuckets_bebe12_dada12: 52.24%
# svm_smallbuckets_bebe12_dada12: 53.97%
# svm_stocks_smallbuckets: 53.10%
# lstm_stocks_smallbuckets: 51.00%
# svm_smallbuckets_forecToday_20x4: 98.09%
# lstm_smallbuckets_forecToday_20x4: 86.85%


# lstm_sentTraffic_forecToday_20x4_smallbuckets: 66.71%
# svm_sentTraffic_forecToday_20x4_smallbuckets: 88.06%

# lstm_receivedTraffic_forecToday_20x4_smallbuckets: 91.69%
# svm_receivedTraffic_forecToday_20x4_smallbuckets: 98.15%



import numpy as np
from scapy.all import *
import pcapy
import matplotlib.pyplot as plt
import os
import dpkt
import examples
from dpkt.compat import compat_ord

# ------------------------------------------------ #

# This program takes an already created pcap file
# and creates vectors of specific time frames with
# the packet sizes sent/received by the device.
# It can also plot the values found.

# ------------------------------------------------ #

# Initializations
dot_data = [] # initialize list
packets = []
vector_value = 0 # initialize value of vector
start_time = 0 # start counting time from t = 0
mac_address = '6c:56:97:f0:93:e4' # MAC address of Echo. This is case sensitive
time_interval = 1.0 # size of time windows in vector (in seconds)



f = open("mars_largebuckets.txt", "w")

try: 

	# Make a figure
#	fig = plt.figure()
	# Make room for legend at bottom
#	fig.subplots_adjust(bottom=0.2)
	# The axes for your lists 1-3
#	ax = fig.add_subplot(111)

	# gets the packets from the pcap file that have the source address from the dot, and are tcp packets
	for filename in os.listdir("mars"):
		if filename.endswith(".pcap"):
			#f = open("weather/" + filename, 'rb')
			#print filename
			dot_data = []
			packets = []

			for packet in PcapReader("mars/" + filename): #for packet in PcapReader("weather/" + filename):

				if (packet[Ether].src == mac_address or packet[Ether].dst == mac_address): # USE THIS WHEN DOING BOTH SENT AND RECEIVED TRAFFIC 
#				if (packet[Ether].dst == mac_address): # use this for received traffic
#				if (packet[Ether].src == mac_address): # use this for sent traffic
					if (IP in packet): # ath - if IP doesn't exist, could it then be a tcp layer or not?
						if (packet[IP].proto == 6): # 6 is TCP layer
							packets.append(packet)
							
		# testing the incrementation of time
		#	start_time = packets[0].time # time when packet was received
		#	print "start time: ", start_time
		#	local_time = time.localtime(start_time)
		#	human_time = time.asctime(local_time)
		#	print "human time: ", human_time
		#	test_time = start_time + 10
		#	print "plus 10 sec: ", time.asctime(time.localtime(test_time))

			if (len(packets) > 0):
				start_time = packets[0].time + time_interval # get time of first packet + "time_interval" seconds to be the window of the first interval
				#print start_time
				byte_size = 0
				for packet in packets:
					if packet.time <= start_time:
						byte_size = byte_size + packet[IP].len
					else:
						start_time = start_time + time_interval # increment start time by length of time window
						dot_data.append(byte_size)
						byte_size = packet[IP].len 

			#change dot_data from a list to numpy array
			dot_data_numpy = np.asarray(dot_data[0:70]) # up to 70 because 70 seconds pass between readings

			#CREATE VECTORS
			#write vectors to the text file created in the beginning
			for element in dot_data[0:70]: # [0:70] for 1 sec windows, [0:140] for 0.5 sec, [0:350] for 0.2 sec
				f.write(str(element))
				f.write(" ")
			f.write('\n')
			
			print "len: ", len(dot_data)

			# Plot line
#			line = ax.plot(dot_data_numpy,'b-',label='data sent', linewidth=0.5)

	f.close()


except pcapy.PcapError:
	pass


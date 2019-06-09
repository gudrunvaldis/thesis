import numpy as np
from scapy.all import *
import pcapy
import matplotlib.pyplot as plt
import os
import dpkt
import examples
from dpkt.compat import compat_ord

# ------------------------------------------------ #

# previously audio_detection.py and pcap_to_vectors.py
# THIS VERSION DOESN'T WRITE TO A FILE, BUT GRAPHS SENT AND RECEIVED TRAFFIC SEPARATELY
# This program takes an ~already created pcap file~
# and creates vectors of specific time frames with
# the packet sizes sent/received by the device.
# It then plots these values.

# ------------------------------------------------ #

# INITIALIZATIONS
dot_data = [] # initialize list
packets = []
vector_value = 0 # initialize value of vector
start_time = 0 # start counting time from t=0
mac_address = '6c:56:97:f0:93:e4' #this is case sensitive!!
# 44:65:0d:c0:9e:ce is the MAC address of Noah's Echo
# 6c:56:97:f0:93:e4 is the MAC address of my dot
# b8:e8:56:08:0f:94 is the MAC address of my computer
time_interval = 1 # size of timeslots in vector (in seconds)



#f = open("stocks_female_flite_vectors.txt", "w")

try: 
	# gets the packets from the pcap file that have the source address from the dot, and are tcp packets
	#for packet in PcapReader('alexa10_B.pcap'): #('alexa_7_7_16.pcap'): # use PcapReader rather than rdpcap bc rdpcap creates a list in memory
	#while rcapreader doesn't so it makes it possible to process huge pcap files

	# Make a figure
	fig = plt.figure()
	# Make room for legend at bottom
	fig.subplots_adjust(bottom=0.2)
	# The axes for your lists 1-3
	ax = fig.add_subplot(111)

	# Make a figure
#	fig1 = plt.figure()
	# Make room for legend at bottom
#	fig1.subplots_adjust(bottom=0.2)
	# The axes for your lists 1-3
#	ax1 = fig1.add_subplot(111)


	for filename in os.listdir("stocks_male_flite"):
		fig = plt.figure()
		# Make room for legend at bottom
		fig.subplots_adjust(bottom=0.2)
		# The axes for your lists 1-3
		ax = fig.add_subplot(111)
		if filename.endswith(".pcap"):
			#f = open("weather/" + filename, 'rb')
			print filename
			#dot_data = []
			dot_data_sent = []
			dot_data_received = []
			#packets = []
			packets_sent = []
			packets_received = []

			for packet in PcapReader("stocks_male_flite/" + filename): #for packet in PcapReader("weather/" + filename):
				#if (packet[Ether].src == mac_address or packet[Ether].dst == mac_address):
				if (packet[Ether].src == mac_address):
					if (IP in packet): # ath - if IP doesn't exist, could it then be a tcp layer or not?
						if (packet[IP].proto == 6): # 6 means it's the TCP layer
							#packets.append(packet)
							packets_sent.append(packet)
				elif (packet[Ether].dst == mac_address):
					if (IP in packet): # ath - if IP doesn't exist, could it then be a tcp layer or not?
						if (packet[IP].proto == 6): # 6 means it's the TCP layer
							#packets.append(packet)
							packets_received.append(packet)

		# testing the incrementation of time
		#	start_time = packets[0].time # time when packet was received
		#	print "start time: ", start_time
		#	local_time = time.localtime(start_time)
		#	human_time = time.asctime(local_time)
		#	print "human time: ", human_time
		#	test_time = start_time + 10
		#	print "plus 10 sec: ", time.asctime(time.localtime(test_time))
			


			if (len(packets) > 0):
				start_time = packets[0].time + time_interval # get time of first packet +"time_interval" seconds to be the window of the first interval
				#print start_time
				byte_size = 0
				for packet in packets:
					if packet.time <= start_time:
						byte_size = byte_size + packet[IP].len # is this the length I want????????????????????????????????????
					else:
						start_time = start_time + time_interval # increment start time by 10 seconds
						dot_data.append(byte_size)
						#print "byte size: ", byte_size
						byte_size = packet[IP].len 

			if (len(packets_sent) > 0):
				start_time = packets_sent[0].time + time_interval # get time of first packet +"time_interval" seconds to be the window of the first interval
				#print start_time
				byte_size = 0
				for packet in packets_sent:
					if packet.time <= start_time:
						byte_size = byte_size + packet[IP].len # is this the length I want????????????????????????????????????
					else:
						start_time = start_time + time_interval # increment start time by 10 seconds
						dot_data_sent.append(byte_size)
						#print "byte size: ", byte_size
						byte_size = packet[IP].len 

			if (len(packets_received) > 0):
				start_time = packets_received[0].time + time_interval # get time of first packet +"time_interval" seconds to be the window of the first interval
				#print start_time
				byte_size = 0
				for packet in packets_received:
					if packet.time <= start_time:
						byte_size = byte_size + packet[IP].len # is this the length I want????????????????????????????????????
					else:
						start_time = start_time + time_interval # increment start time by 10 seconds
						dot_data_received.append(byte_size)
						#print "byte size: ", byte_size
						byte_size = packet[IP].len 




			#change dot_data from a list to numpy array
			#dot_data_numpy = np.asarray(dot_data[0:70]) #[0:70]) # makes sense bc there's 70 seconds between readings
#			dot_data_numpy_sent = np.asarray(dot_data_sent[0:70]) #[0:70]) # makes sense bc there's 70 seconds between readings
			dot_data_numpy_received = np.asarray(dot_data_received[0:70]) #[0:70]) # makes sense bc there's 70 seconds between readings



			#NEED THIS TO CREATE VECTORS
			#write vectors to file (vigrar.txt)
#			for element in dot_data[0:70]:
#				f.write(str(element))
#				f.write(" ")
#			f.write('\n')
			
#			print "len: ", len(dot_data)

			
			

			# Plot line
#			line = ax.plot(dot_data_numpy_sent,'b-',label='data sent', linewidth=0.5)
			#plt.ylim(0, )
			#plt.xlim(0, 70)
			#plt.ylabel('Size (bytes)')
			#plt.xlabel('Time (sec)')
			#plt.show()
			#plt.ylabel('Size (bytes)')
			#plt.xlabel('Time (sec)')
			#plt.xlim(0, 40)
			line1 = ax.plot(dot_data_numpy_received,'r-',label='data received', linewidth=0.5)
	plt.xlim(0, 40)
	plt.ylim(0, 120000)
	#ax.xlim(0, 40)
	#ax1.xlim(0, 40)
	#plt.title('Size of packets sent over time........')
	plt.ylabel('Size (bytes)')
	plt.xlabel('Time (sec)')
	#ax.ylabel('Size (bytes)')
	#ax.xlabel('Time (sec)')
	#ax1.ylabel('Size (bytes)')
	#ax1.xlabel('Time (sec)')
	plt.show()
	#f.close()


except pcapy.PcapError:
	pass


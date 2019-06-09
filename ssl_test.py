import numpy as np
from scapy.all import *
import pcapy
import matplotlib.pyplot as plt
import os
import dpkt
import examples
from dpkt.compat import compat_ord

# ------------------------------------------------ #

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



# PUT IN CODE THAT ITERATES THROUGH FILES AND SAVES VECTORS TO A TEXT FILE???
f = open("vigrar.txt", "w")

try: 
	# gets the packets from the pcap file that have the source address from the dot, and are tcp packets
	#for packet in PcapReader('alexa10_B.pcap'): #('alexa_7_7_16.pcap'): # use PcapReader rather than rdpcap bc rdpcap creates a list in memory
	#while rcapreader doesn't so it makes it possible to process huge pcap files

	for filename in os.listdir("weather"):
		if filename.endswith(".pcap"):
			f = open("weather/" + filename, 'rb')
			for packet in PcapReader("weather/" + filename):
			#for packet in dpkt.pcap.Reader(f):
				pcap = dpkt.pcap.Reader(f)
				for ts, buf in pcap:
					if (pcap is not None): #check for SSL here
						eth = dpkt.ethernet.Ethernet(buf)
						#print examples.print_packets.mac_addr(eth.src)
						mac_source = ':'.join('%02x' % compat_ord(b) for b in eth.src) # MAC address!!!!
						mac_dest = ':'.join('%02x' % compat_ord(b) for b in eth.dst)

						if (mac_source == mac_address or mac_dest == mac_address):
							if isinstance(eth.data, dpkt.ip.IP): #checks if the Ethernet data contains an IP packet
								ip = eth.data
								print ip.p

								if isinstance(ip.data, dpkt.tcp.TCP): # check if there's a tcp layer
									packets.append(buf)


					#if (packet[Ether].src == mac_address or packet[Ether].dst == mac_address):
					#	if (IP in packet): # ath - if IP doesn't exist, could it then be a tcp layer or not?
					#		if (packet[IP].proto == 6): # 6 means it's the TCP layer
					#			packets.append(packet)

			# testing the incrementation of time
		#	start_time = packets[0].time # time when packet was received
		#	print "start time: ", start_time
		#	local_time = time.localtime(start_time)
		#	human_time = time.asctime(local_time)
		#	print "human time: ", human_time
		#	test_time = start_time + 10
		#	print "plus 10 sec: ", time.asctime(time.localtime(test_time))

			start_time = packets[0].time + time_interval # get time of first packet +10 seconds to be the start time
			byte_size = 0
			for packet in packets:
				if packet.time <= start_time:
					byte_size = byte_size + packet[IP].len # is this the length I want????????????????????????????????????
				else:
					start_time = start_time + time_interval # increment start time by 10 seconds
					dot_data.append(byte_size)
					#print "byte size: ", byte_size
					byte_size = packet[IP].len 

			#print len(dot_data)
			for element in dot_data:
				print "data size: ", element

			#change dot_data from a list to numpy array
			dot_data_numpy = np.asarray(dot_data)
			#print "this: ", type(dot_data_numpy)
			#print type(packets)

			#write vector to file (vigrar.txt)
			for element in dot_data:
				f.write(str(element))
				f.write(", ")
			f.write('\n\n')
			
			#print dot_data_numpy[0]
			#print dot_data_numpy[29]
			#print dot_data_numpy
			print "len: ", len(dot_data)

			# Make a figure
			fig = plt.figure()
			# Make room for legend at bottom
			fig.subplots_adjust(bottom=0.2)
			# The axes for your lists 1-3
			ax1 = fig.add_subplot(111)

			# Plot line
			line = ax1.plot(dot_data_numpy,'bo-',label='dot data')

		#	plt.show()
	f.close()


except pcapy.PcapError:
	pass


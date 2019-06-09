#!/bin/bash

import os
import subprocess
import time
import signal
import pyttsx


# This file collects PCAP file of network traffic until the program is terminated
# Each file collects 4000 packets

# starting index of pcap file
i = 0


while (True):
	# construct filename
	number = str(i)
	extension = ".pcap"
	filename = "mars" + number + extension

	# start tcpdump
	proc = subprocess.Popen(["sudo", "tcpdump", "-c", "4000", "-w", filename, "-i", "wlan0"])

	# wait for 10 seconds before ask question
	time.sleep(10)

	# ask question
	p = subprocess.Popen(["espeak", "-ven-us+m3", "-s140", "Alexa, is there life on Mars?"]) # use +m3 for male voice, +f1 for female voice
	#p = subprocess.Popen(["flite", "-voice", "slt", "Alexa, how is the stock market?"]) # use kal16 for male voice, slt for female voice

	# wait for 60 seconds to make sure longest question gets completed
	time.sleep(60)

	# end tcpdump
	p.kill()
	
	# increment index for next pcap file
	i = i + 1


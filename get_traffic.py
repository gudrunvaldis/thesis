import pyshark

# PyShark documentation: https://github.com/KimiNewt/pyshark

# dumpcap and tcpdump

# Reading from a live interface - LIVE CAPTURE DOESN'T STORE THE PACKAGES?

cap = pyshark.LiveCapture(interface='en0')
cap.set_debug()
#cap.sniff(timeout=50)
cap.sniff(packet_count=50)
time.sleep(4)
cap.close()
print(cap)
print(cap[3])



# reads from an existing file??
#cap = pyshark.FileCapture('/testcapture.cap')
#print cap[0]



#wlan0
#ssh into pi, run dumpcap command on rapsberry pi

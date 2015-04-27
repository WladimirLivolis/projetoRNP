import os, socket, struct

# Based on the "Pure Python version of ICMP ping" from https://github.com/samuel/python-ping
#
# Author: Wladimir Cabral
# 	  wladimircabral@gmail.com

class ICMPLib:

	def __init__(self):
		self.ICMP_ECHO_REQUEST = 8

	def checksum(self, source_string):
		    sum = 0
		    countTo = (len(source_string)/2)*2
		    count = 0
		    while count<countTo:
			thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
			sum = sum + thisVal
			sum = sum & 0xffffffff
			count = count + 2

		    if countTo<len(source_string):
			sum = sum + ord(source_string[len(source_string) - 1])
			sum = sum & 0xffffffff

		    sum = (sum >> 16)  +  (sum & 0xffff)
		    sum = sum + (sum >> 16)
		    answer = ~sum
		    answer = answer & 0xffff

		    answer = answer >> 8 | (answer << 8 & 0xff00)

		    return answer

	def send_icmp_packet(self, my_socket, dest_addr, port, MESSAGE):

		    dest_addr  =  socket.gethostbyname(dest_addr)

		    ID = os.getpid() & 0xFFFF

		    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
		    my_checksum = 0

		    # Make a dummy header with a 0 checksum.
		    header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
		    data = MESSAGE

		    # Calculate the checksum on the data and the dummy header.
		    my_checksum = self.checksum(header + data)

		    # Now that we have the right checksum, we put that in. It's just easier
		    # to make up a new header than to stuff it into the dummy.
		    header = struct.pack(
			"bbHHh", self.ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
		    )
		    packet = header + data
		    my_socket.sendto(packet, (dest_addr, port))
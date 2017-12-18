#!/usr/bin/python3.6.1
#Written by Stephen Wang for COMP9331 Assessment1
#This is receivier part

import sys
from segment import *
import socket
import random
import time
import struct

#step 0:create the socket on receiver side;

receiverPort = int(sys.argv[1])
file = sys.argv[2]


receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))

serverISN = random.randint(128,255)
headerSegment = struct.calcsize("iii????")
maxSegmentSize = 0


f = open(file, 'w')
receiverLog = open('Receiver_log.txt', 'w')
f = open(file, 'a')
receiverLog = open('Receiver_log.txt', 'a')

def getKey(packet):
     return packet.seq_num

################ 3 hand shakeing to establish connection ###############

message, address = receiverSocket.recvfrom(headerSegment)
decodedMessage = segments.decodePacket(message)

if(decodedMessage.syn_flag == True):
     maxSegementSize = decodedMessage.MSS
     response = segment.segments(max_MSS = maxSegmentSize)
     response.syn_flag = True
     response.ack_flag = True
     response.seq_num = serverISN
     response.ack_num = decodedMessage.seq_num + 1
     encodedResponse = segments.encodePacket(response)
     receiverSocket.sendto(encodedResponse, address)


message, address =receiverSocket.recvfrom(headerSegment)
decodedMessage = segments.decodePacket(message)


if (decodedMessage.ack_flag == True):
     consatantSeq = decodedMessage.ack_num
     print("connection established...")

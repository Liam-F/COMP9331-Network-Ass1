#!/usr/bin/python3.6.1
#Written by Stephen Wang for COMP9331 Assessment1
#This is sender part


import sys
from segment import *
import socket
import random
import time
import struct
import threading


#step 0 :initializing the arguments from terminal;


start_timer = time
receiverIP = str(sys.argv[1])
receiverPort = int(sys.argv[2])
file = str(sys.argv[3])
MWS = int(sys.argv[4])
MSS = int(sys.argv[5])
#timeout = float(sys.argv[6])
#pdrop = float(sys.argv[7])
#seed = int(sys.argv[8])

senderLog = open('Sender_log.txt', 'w')
senderLog = open('Sender_log.txt', 'a')
#random.seed(seed)
#headerSegment = struct.calcsize("iii????")  #which = 16
#clientISN = random.randint(0,255)  #


def PLDModule(pdrop):
     number = random.random()
     if(number > pdrop):
          return True
     else:
          return False
     
def timeoutFunction(time):
     time[0] = True
     return


#step 2:establish the connection using 3-way handshake.(done)

def three_way_handshake():
     logTime = time.time()
     logTime = logTime * 1000
     ran_seq_num = random.randint(0,127)   #produce the first-shake random int for the sequence number
     senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #create UDP socket
     senderSocket.setblocking(0)
     
     first_handshake = segments(max_MSS = MSS)
     first_handshake.seq_num = ran_seq_num
     first_handshake.syn_flag = True
     encodedPacket = segments.encodePacket(first_handshake)
     senderSocket.sendto(encodedPacket, (receiverIP,receiverPort))  #first send
     
     print("snd %f S %d 0 %d" % (timer,first_handshake.seq_num,first_handshake.ack_num))  #first send info
     senderLog.write("SND 0 S %d 0 0\n" % packet.seq_num)

     packetReceived, addr = senderSocket.recvfrom(headerSegment)            #listening...
     decodedPacket = segments.decodePacket(packetReceived) 
     
     if(decodedPacket.ack_flag == True and decodedPacket.flag.syn_flag == True):
          print("rcv %.3f SA %d 0 %d" % (timer,second_handshake_response.seq_num,second_handshake_response.ack_num)) #second
          senderLog.write("rcv %.3f SA %d 0 %d\n" % (time.time()*1000-logTime,decodedPacket.seq_num,decodedPacket.ACKNumber))
          constantACK = decodedPacket.seq_num + 1

          packet = segments(max_MSS = MSS)
          packet.ack_flag = 1
          packet.seq_num = ran_seq_num + 1
          packet.ack_num = decodedPacket.seq_num + 1

          encodedPacket = segments.encodePacket(packet)
          senderSocket.sendto(encodedPacket, (receiverIP, receiverPort))

          senderLog.write("snd %.3f A 0 %d\n" % (time.time()*1000 -logTime, packet.seq_num, packet.ack_num))
     
     return
        
three_way_handshake()












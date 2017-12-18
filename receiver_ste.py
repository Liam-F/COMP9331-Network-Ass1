#!/usr/bin/python3.6.1
#Written by Stephen Wang for COMP9331 Assessment1
#This is receivier part

import sys
from segment import *
import socket
import random
import time
import pickle

#step 0:create the socket on receiver side;

receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_port = int(sys.argv[1])
receiverSocket.bind(('', receiver_port))
#file = str(sys.argv[2])


print("has binded the UDP on %d" % receiver_port)

#step 1: 3 ways handshake:

first_data, addr = receiverSocket.recvfrom(1024)        #listening...
print('Received from %s:%s' % addr)
first_handshake_response = pickle.loads(first_data)  #first receive
#print("rcv %f SA %d 0 %d" % (second_handsh))


if(first_handshake_response.syn_flag == 1):
     ran_ack_num = random.randint(first_handshake_response.seq_num,255)
     second_handshake_response = segments()
     second_handshake_response.seq_num = ran_ack_num
     second_handshake_response.ack_num = first_handshake_response.seq_num + 1
     second_handshake_response.ack_flag = 1
     second_handshake_response.syn_flag = 1

     receiverSocket.sendto(pickle.dumps(second_handshake_response),addr) #second send

     third_data, addr = receiverSocket.recvfrom(1024)  #listening...
     third_handshake_response = pickle.loads(third_data)
     if(third_handshake_response.ack_flag == 1 and third_handshake_response.syn_flag == 0):
          print(third_handshake_response.seq_num,third_handshake_response.ack_num,third_handshake_response.ack_flag,third_handshake_response.fin_flag,third_handshake_response.syn_flag)
          print("connection established.")
     

     

     
#receiverSocket.close()

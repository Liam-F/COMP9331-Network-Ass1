#!/usr/bin/python3.6.1
#Written by Stephen Wang for COMP9331 Assessment1
#This is sender part


import sys
from segment import *
import socket
import random
import time
import pickle

#step 0 :initializing the arguments from terminal;

receiverIP = str(sys.argv[1])
receiverPort = int(sys.argv[2])
file = str(sys.argv[3])
#MWS = int(sys.argv[4])
MSS = int(sys.argv[5])
#timeout = float(sys.argv[6])
#pdrop = float(sys.argv[7])
#seed = int(sys.argv[8])

#step 1：open and read files；
content = "Today is a goooooooooooooooood day!!!"
#opened_file = open(file, 'r')
#for line in opened_file:
#     content = content + line


message = str(content)

#opened_file.close()

#print(message)


#step 2:establish the connection using 3-way handshake.(done)

def three_way_handshake():
     timer = time.clock()
     timer = timer * 1000
     ran_seq_num = random.randint(0,255)   #produce the first-shake random int for the sequence number
#     ran_ack_num = random.randint(ran_seq_num,255) 
     senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #create UDP socket
     
     first_handshake = segments()
     first_handshake.seq_num = ran_seq_num
#     first_handshake.ack_num = ran_ack_num
     first_handshake.syn_flag = 1
     #print(first_handshake.seq_num,first_handshake.ack_num)

     senderSocket.sendto(pickle.dumps(first_handshake),(receiverIP,receiverPort))   
     print("snd %f S %d 0 %d" % (timer,first_handshake.seq_num,first_handshake.ack_num))  #first
 
     second_data, addr = senderSocket.recvfrom(1024)             #listening...
     second_handshake_response = pickle.loads(second_data)  
     
     if(second_handshake_response.ack_flag == 1 and second_handshake_response.syn_flag == 1):
          print("rcv %f SA %d 0 %d" % (timer,second_handshake_response.seq_num,second_handshake_response.ack_num)) #second
          third_handshake = segments()
          third_handshake.seq_num = second_handshake_response.ack_num
          third_handshake.ack_num = second_handshake_response.seq_num + 1
          third_handshake.ack_flag = 1
          third_handshake.syn_flag = 0
          senderSocket.sendto(pickle.dumps(third_handshake),addr)  #third send...
          print("snd %f A %d 0 %d" % (timer,third_handshake.seq_num,third_handshake.ack_num))

     if(third_handshake.seq_num == first_handshake.seq_num + 1 and third_handshake.ack_num == second_handshake_response.seq_num + 1):
          print("connection established.")
     return third_handshake   #acknowlegde the success of 3-way handshake.


def data_transmission(three_handshake):
     print(three_handshake.seq_num,three_handshake.ack_num)
     f = open(file,'rb')
     f.seek(0,2)    #set the offset
     size = f.tell() #get the size of file
#     print(size)

     eofCheck = False
     data_trans_start = 0;
     while True:
          #check if the file has been loaded at the end.
          bytes = f.read(MSS)
          while(eofCheck == False):
               if(bytes == ""):
                    eofCheck = True
                    break
               if time.
          
               
               
          
     
     

     
     
     
     
     



#while True:
#     senderSocket.sendto(pickle.dumps(message),(receiverIP,receiverPort))  #using pickle package to trans data type
     
#print("has sent the message")

three_handshake = segments()
three_handshake = three_way_handshake()

data_transmission(three_handshake)
     
     
#     print(senderSocket.recv(1024))












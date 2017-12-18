#!/usr/bin/env python3

import time
import socket
import sys,os
import random
import pickle
import re
import select
import time

#if not len(sys.argv) == 3:
#    print("Usage: python sender.py <receiver_host_ip> <receiver_port> ")
#    sys.exit(-1)

receiver_host_ip = sys.argv[1]
receiver_port = int(sys.argv[2])
file = str(sys.argv[3])
MWS = int(sys.argv[4])
MSS = int(sys.argv[5])
delay_time = sys.argv[6]
pdrop = sys.argv[7]
seed = sys.argv[8]





address = (receiver_host_ip ,receiver_port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = ""

f = open(file,'r')
for line in f:
    message = message + line

#print(message)

#print(len(message))
#MWS = 20
#MSS = 4
seq_no = 0
LBA = 0
LBS = 0
next_seq_no = 0
init_seq_no = 0
ack_no = 0
random.seed(300)
delay_time = 1
pdrop = 0.3

senderLog = open('Sender_log.txt', 'w')
senderLog = open('Sender_log.txt', 'a')


#timer_start = time.clock()



def int_to_string(n, nbytes):
    return str(n).zfill(nbytes)

def string_to_int(s):
    return int(s)


# header = (seq_no, ack_no, ACK, SYN, FIN)
# data is string
def make_datagram(header, data):
    datagram = int_to_string(header[0], 8)
    datagram += int_to_string(header[1], 8)
    datagram += int_to_string(header[2], 1)
    datagram += int_to_string(header[3], 1)
    datagram += int_to_string(header[4], 1)
    datagram += data
    return datagram

def extr_datagram(datagram):
    seq_no = int(datagram[0:8])
    ack_no = int(datagram[8:16])
    ACK = int(datagram[16])
    SYN = int(datagram[17])
    FIN = int(datagram[18])
    data = ""
    if len(datagram) > 19:
        data = datagram[19:]
    return (seq_no, ack_no, ACK, SYN, FIN), data

def PLD():
    global pdrop
    number = random.random()
    if(number > pdrop):
        return True
    else:
        return False


def TWHS():
    global seq_no
    global next_seq_no
    global init_seq_no
    global ack_no
    global LBS
    global LBA
#first handshake
    org_time = time.time()
    address = (receiver_host_ip ,receiver_port)
    seq_no = random.randint(1,255)
    SYN = 1
    header = (seq_no, 0, 0, SYN, 0)
    print(header)
    
    

    client_socket.sendto(make_datagram(header, "").encode("utf-8"), address)
    senderLog.write("snd %.3f S %d 0 0\n" % (org_time, header[0]))


#second handshake
    datagram, address = client_socket.recvfrom(4096)

    header, data = extr_datagram(datagram.decode("utf-8"))
    if header[2] == 1:
        print(header, data)
        senderLog.write("rcv %.3f SA %d 0 %d\n" % (time.time()*1000-org_time, header[0],header[1]))

#third handshake
        init_seq_no = seq_no = next_seq_no = header[1]
        ack_no = header[0] + 1
        header = (seq_no, ack_no, 0, 0, 0)
        LBS = LBA = seq_no - 1

        client_socket.sendto(make_datagram(header, "").encode("utf-8"), address)
        senderLog.write("snd %.3f A %d 0 %d\n" % (time.time()*1000-org_time, header[0],header[1]))
        print(header)



TWHS()
print(seq_no, ack_no, LBA, LBS, init_seq_no, next_seq_no)
#message = "something"
window = {}

# fin
def fin(seq, ack):
    #first fin
    global address
    global file
    seq_no = ack
    ack_no = seq
    header = (seq_no, ack_no, 0, 0, 1)
    
    client_socket.sendto(make_datagram(header, "").encode("utf-8"), address)
    print("4- s ")
    #second fin
    if header[2] == 1 :

        datagram, address = client_socket.recvfrom(4096)
        header, data = extr_datagram(datagram.decode("utf-8"))
    
    
    
    #third fin
    if header[-1] == 1:
        datagram, address = client_socket.recvfrom(4096)
        header, data = extr_datagram(datagram.decode("utf-8"))
        
        
    #forth fin
        seq_no = header[1]
        ack_no = header[0] + 1
        header = (seq_no, ack_no , 1, 0, 1)
        print(header)
        datagram = make_datagram(header, "")
        client_socket.sendto(datagram.encode("utf-8"), address)
        print("4 - rs")
            #         file.close()
        client_socket.close()
#  sys.exit()







# after 3-way handshake
def send(socket, addr):
    global next_seq_no
    global MSS
    global seq_no
    global LBS
    global LBA
    global ack_no
    global init_seq_no
    global MWS
    global window
    global nbytes
    global start_idx
    
    
    seq_no = next_seq_no
    start_idx = seq_no - init_seq_no
    nbytes = min(MSS, len(message[start_idx:]), MWS - (LBS - LBA))
    window[seq_no] = message[start_idx:start_idx + nbytes]
    #    print(message[start_idx:start_idx + nbytes])
    header = (seq_no, ack_no, 0, 0, 0)
    datagram = make_datagram(header, \
                             message[start_idx:start_idx + nbytes])
#    print(header)
    if datagram[19:] == "" and not window:
        final_seq_no = header[0]
        final_ack_no = header[1]
        fin(final_seq_no, final_ack_no)
        


#        print(header)
        #        print(header[1])

    

    if PLD() and not datagram[19:]:
        client_socket.sendto(datagram.encode("utf-8"), addr)
    else:
        print('drrrrrrop',header[0])
        pass


                             
    next_seq_no = seq_no + nbytes
    LBS = next_seq_no - 1

def receive(socket):
    global LBA
    global seq_no
    global window
    global ack_no
    
    
    datagram, address = socket.recvfrom(4096)
    header, data = extr_datagram(datagram.decode("utf-8"))
    if header[2:] == (1, 0, 0):
        print('#',header)
        if header[1] > LBA:
            ack_no = header[1]
            #print(header)
            LBA = header[1] - 1
            to_remove = []
            for seq_no in window:
                if seq_no < header[1]:
                    to_remove.append(seq_no)
            for seq_no in to_remove:
                window.pop(seq_no)



while LBA - init_seq_no < len(message) - 1:
    print(window)
    try:
        read_ready = select.select([client_socket], [], [], delay_time)
    except ValueError:
        sys.exit()
    #    read_ready, write_ready, except_ready = select.select([client_socket], [], [], delay_time)

    duplicate = 0
    if read_ready[0]:
        receive(client_socket)
#        time_end = time.clock()

        if LBA != ack_no:
            duplicate = duplicate + 1
            if duplicate == 4:
                header = (LBA, ack_no, 0, 0, 0)
                datagram = make_datagram(header, \
                                                 message[start_idx:start_idx + nbytes])
                
                client_socket.sendto(datagram.encode("utf-8"), address)
                duplicate = 0
    
    
    if not read_ready[0]:
        print('pppppppppptime')
        if window == {}:
            pass
        else:
            header = (LBA+1, ack_no, 0, 0, 0)
            datagram = make_datagram(header, window[LBA+1])
            print('-----dddd',datagram,message[LBA:LBA + nbytes]
                  ,message)
            client_socket.sendto(datagram.encode("utf-8"), address)
            duplicate = 0

    if LBS - LBA < MWS:
        send(client_socket, address)










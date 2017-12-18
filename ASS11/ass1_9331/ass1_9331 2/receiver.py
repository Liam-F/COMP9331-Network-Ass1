#!/usr/bin/env python3
from random import *
import socket
import sys,os
import select
import time

#if not len(sys.argv) == 2:
#    print("Usage: python receiver.py <receiver_port> ")
#    sys.exit(-1)

receiver_port = int(sys.argv[1])
#f = str(sys.argv[2])


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("", receiver_port)
server_socket.bind(address)
ack_no = 0
seq_no = 0
message = ""
buffer = {}
ip_address = ""
mss = 0
file = open('file1.txt','w')
#receiverLog = open('Receiver_log.txt', 'w')
#file = open(file,'a')
#receiverLog = open('Receiver_log.txt', 'a')




# header = (seq_no, ack_no, ACK, SYN, FIN)
# data is string
def int_to_string(n, nbytes):
    return str(n).zfill(nbytes)

def string_to_int(s):
    return int(s)


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



def TWHS():
    global ack_no
    global seq_no
    global mss
    address = ("" ,receiver_port)
#first handshake
    datagram, address = server_socket.recvfrom(4096)
    header, data = extr_datagram(datagram.decode("utf-8"))
    print(header)
    ip_address = data
    print(ip_address)
    if header[3] == 1:
    
#second handshake
        ack_no = header[0] + 1
        seq_no = randint(1, 255)
        SYN = 1
        ACK = 1
        header = (seq_no, ack_no, ACK, SYN, 0)
        print(header)
        
        server_socket.sendto(make_datagram(header, "").encode("utf-8"), address)


#third handshake
        datagram, address = server_socket.recvfrom(4096)
        header, data = extr_datagram(datagram.decode("utf-8"))
        mss = int(data)
        
        print(mss)
        seq_no = header[1]
        print(header)
#        if ACK == 1:
#            pass

TWHS()

print(seq_no, ack_no)
def receive(socket):
    global mss
    global ack_no
    global seq_no
    global message
    global buffer
    global file
    tof=True
    datagram, address = socket.recvfrom(4096)
    header, data = extr_datagram(datagram.decode("utf-8"))
    print('a',header,ack_no)
    if header[2:] == (0, 0, 0):
        if header[0] > ack_no and header[0] not in buffer:
            buffer[header[0]] = data
            print(buffer)
        if header[0] == ack_no:
            print(ack_no)
            print('dataaaaaaaaa',data)
            file.write(data)
            ack_no+=mss
            if buffer and list(buffer.keys())[0]-ack_no>0:
                print('----listbufferkey--',list(buffer.keys())[0],ack_no)
                pass
            else:
                
                while buffer and tof:
                    length=len(list(buffer.keys()))
                    print('-----$$$',length)
                    print('acknoinbuffer',ack_no)
                    count=0
                    for i in range(length):
                        print(list(buffer.keys()))
                        print('-----',i)
                        
                        if i==0:
                            pass
                        
                        elif list(buffer.keys())[i] - list(buffer.keys())[i-1] > mss:
                            print('ggggggap',list(buffer.keys())[i] - list(buffer.keys())[i-1])
                            tof= False
                            break
                
                        part_of_message = buffer[list(buffer.keys())[i]]
                        print('---buffer data---',part_of_message)
                        #message = part_of_message+message
                        ack_no += mss
                        print('___________',ack_no)
                    #                print(part_of_message)
                        file.write(part_of_message)
                        datagram = make_datagram((seq_no, list(buffer.keys())[i]+mss, 1, 0, 0), "")
                        server_socket.sendto(datagram.encode("utf-8"), address)
                        #ack_no+=mss
                        count+=1
                    while 1:
                        if count==0:
                            break
                        if not buffer:
                            break
                        temp = buffer.pop(list(buffer.keys())[0])
                        count-=1
                    print('ttttof:',tof)
                    if not tof:
                        break
                print('while loop break!!')
                
        print('aacknow sssend!!!')
        datagram = make_datagram((seq_no, ack_no, 1, 0, 0), "")
        server_socket.sendto(datagram.encode("utf-8"), address)
        

        return True
            
#first fin receive
        # second fin
    elif header[2:] == (0, 0, 1):
        seq_no = header[1]
        ack_no = header[0] + 1
        header = (seq_no, ack_no , 1, 0, 0)
#        print(header)

        datagram = make_datagram(header, "")
        server_socket.sendto(datagram.encode("utf-8"), address)

#third fin
        seq_no = header[1]
        ack_no = header[0] + 1
        header = (seq_no, ack_no , 1, 0, 1)
        print(header)
        
        datagram = make_datagram(header, "")
        server_socket.sendto(datagram.encode("utf-8"), address)
#forth fin
        datagram, address = server_socket.recvfrom(4096)
        header, data = extr_datagram(datagram.decode("utf-8"))
        file.close()
        server_socket.close()
        
        
        



        return False

while 1:
    read_ready, write_ready, except_ready = select.select([server_socket], [], [], 0)
    if read_ready:
        status = receive(server_socket)
        if not status:
            break

#def fin():
#print(message)













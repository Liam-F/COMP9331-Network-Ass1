#define the segements;

import struct
import time

class segments:
     def __init__(self, max_MSS = 0, seq_num = 0 , ack_num = 0, ack_flag = False, rst_flag = False, fin_flag = False, syn_flag = False, data="",):
          self.MSS = max_MSS
          self.seq_num = seq_num
          self.ack_num = ack_num
          self.ack_flag = ack_flag
          self.rst_flag = rst_flag
          self.fin_flag = fin_flag
          self.syn_flag = syn_flag
          self.data = data
          


     def encodePacket(packet):
          string = struct.pack("iii????", packet.MSS, packet.seq_num, packet.ack_num, packet.ack_flag ,packet.rst_flag, packet.syn_flag,packet.fin_flag)
          print(string)
          print(type(packet.data))
          return string + packet.data
     def decodePacket(encodedPacket):
          decodedTuple = list(struct.unpack("iii????", encodedPacket[0:struct.calcsize("iii????")]))
          decodedTuple.append(encodedPacket[struct.calcisze("iii????"):])
          flag_change = ""
          if (decodedTuple[3] == True):
               self.ack_flag = True
          if (decodedTuple[4] == True):
               self.rst_flag = True
          if (decodedTuple[5] == True):
               self.syn_flag = True
          if (decodedTuple[6] == True):
               self.fin_flag = True
          if (decodedTuple[3] == True and decodedTuple[5] == True):
               self.syn_flag = True
               self.ack_flag = True
          if (decodedTuple[3] == True and decodedTuple[6] == True):
               self.fin_flag = True
               self.ack_flag = True
          decodedPacket = segments(decodedTuple[0], self.ack_flag, self.rst_flag, self.syn_flag, self.fin_flag, decodedTuple[1],decodedTuple[2],decodedTuple[7])
          return decodedPacket               
               

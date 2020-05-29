# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:17:34 2020

@author: ryanp
"""

import join_phase as jp
import threading
from socket import *

def establish_data_connection(data_port): #Call this fcn w threading
    baseSocket = socket(AF_INET, SOCK_STREAM)
    baseSocket.bind(('',data_port))
    baseSocket.listen(1)
    
    dataSocket, addr = baseSocket.accept()
    print("Data socket on port " + str(data_port) + " successfully connected")
    dataSocket.send("Welcome to your data connection".encode())
    
    dataSocket.close()
    

if __name__ == "__main__":
    data_ports = jp.join_phase()
    #establish_data_connection(data_ports)

#x = threading.Thread(target=thread_function, args=(1,))
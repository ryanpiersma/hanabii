# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:17:34 2020

@author: ryanp
"""

import join_phase as jp
import threading
from socket import *

def establish_data_connection(client_ip, data_port): #Call this fcn w threading

    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((client_ip, data_port))
    
    print("Data socket on port " + str(data_port) + " successfully connected")
    dataSocket.send("Welcome to your data connection".encode())
    dataSocket.close()
    
  
if __name__ == "__main__":
    (client_ips, data_ports) = jp.join_phase()
    for i in range(len(client_ips)):
        establish_data_connection(client_ips[i], data_ports[i])

#x = threading.Thread(target=thread_function, args=(1,))
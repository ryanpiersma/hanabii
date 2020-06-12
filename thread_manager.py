# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:17:34 2020

@author: ryanp
"""

import join_phase as jp
import threading
import queue
from socket import *

threadActivationList = [] #Populate this w condition variables

def create_condition_variables(num_players):
    return 0


def game_manager():
    return 0
    
def game_player():
    return 0
    
def establish_data_connection(client_ip, data_port): #Call this fcn thru game_manager??

    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((client_ip, data_port))
    
    print("Data socket on port " + str(data_port) + " successfully connected")
    dataSocket.send("Welcome to your data connection".encode())
    dataSocket.close()
    
  
if __name__ == "__main__":
    (client_ips, data_ports) = jp.join_phase()
    

#x = threading.Thread(target=thread_function, args=(1,))
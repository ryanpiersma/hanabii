# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:17:34 2020

@author: ryanp
"""

import join_phase as jp
import threading

def establish_data_connections(data_ports):
    for port in data_ports:
        print("Creating data connection to port " + str(port))

if __name__ == "__main__":
    data_ports = jp.join_phase()
    establish_data_connections(data_ports)

#x = threading.Thread(target=thread_function, args=(1,))
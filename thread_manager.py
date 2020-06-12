# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:17:34 2020

@author: ryanp
"""

import join_phase as jp
import threading
import queue
from socket import *


threadActivatorList = [] #Populate this w condition variables

sendMessageQueue = queue.Queue(0) #TODO: Decide reasonable size for these queues
receiveMessageQueue = queue.Queue(0)

globalLock = threading.Lock() #Any thread can release primitive lock. This means manager can release the lock when needed??

gameFinished = False

playerOrder = []

def game_manager(): #Goal + TODO = Use game manager to both spawn and control game players
    return 0
    
def game_player(player_id, player_ip, player_data_port):
    
    #For each player, open up their data socket and give it to the thread
    playerDataSocket = establish_data_connection(player_ip, player_data_port)
    
    #Wait until a message is received, then put it on the receive message queue
    while gameFinished != True:
        threadActivatorList[player_id].acquire() #Acquire the lock
        
        #Making receiving a message from a game player an atomic task
        print("Server waiting on a message from player " + player_id)
        playerMessage = playerDataSocket.recv(32)
        messageTuple = (player_id, playerMessage)
        receiveMessageQueue.put(messageTuple)
        
        threadActivatorList[player_id].release() #Release the lock
    return 0
    
def establish_data_connection(client_ip, data_port): #Call this fcn thru game_manager??

    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((client_ip, data_port))
    
    print("Data socket on port " + str(data_port) + " successfully connected")
    dataSocket.send("Welcome to your data connection".encode())
    #dataSocket.close()
    
    return dataSocket
    
def create_condition_variables(num_players):
    for i in range(num_players + 1):
        #Create condition variables for each player in the game + 1
        threadActivatorList.append(threading.Condition(globalLock))
  
if __name__ == "__main__":
    (client_ips, data_ports) = jp.join_phase()
    create_condition_variables(len(client_ips))
    managerThread = threading.Thread(target=game_manager)    
    managerThread.run()
    
#x = threading.Thread(target=thread_function, args=(1,))
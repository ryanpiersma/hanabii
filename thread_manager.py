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

sendMessageQueue = queue.Queue(0) #TODO: Decide reasonable size for these queues? Will infinite work??
receiveMessageQueue = queue.Queue(0)

globalLock = threading.Lock() #Any thread can release primitive lock. This means manager can release the lock when needed??

gameFinished = False

playerOrder = []

numPlayers = 0

def game_manager(num_players, ip_list, port_list):
    
    print("***Game manager beginning operation***\n")
    playerOrder = list(range(numPlayers)) # right now could have hard coded. but will support more advanced functionality later!
    
    for i in range(num_players):
        newPlayerThread = threading.Thread(target=game_player, args=(i, ip_list[i], port_list[i],))
        print("Spawned player thread " + str(i + 1) + "\n")
        newPlayerThread.start()
    
    print("***Game manager has spawned all player threads***\n")
    
    
    print("***Game players will now establish data connections***\n")
    
    threadActivatorList[numPlayers].acquire()
    for i in range(num_players):
        threadActivatorList[i].notify()
        threadActivatorList[numPlayers].wait()
    
    print("***Game players have successfully established data connections***\n")
    
    
    print("***Game will now begin! LETS RUMBLE***\n")
    
    totalTurnLimit = 20 * numPlayers #This will not exist in final version (?) . Just for demo of basic functionality
    turnCounter = 0
    currentPlayer = 0
    roundCounter = 0
    
    while turnCounter < totalTurnLimit: #gameFinished != True:
        if currentPlayer == 0:
            roundCounter = roundCounter + 1
            print("^^^BEGIN ROUND " + str(roundCounter) + " ^^^")
        threadActivatorList[playerOrder[currentPlayer]].notify()
        currentPlayer = (currentPlayer + 1) % num_players
        turnCounter = turnCounter + 1
        threadActivatorList[numPlayers].wait()

    print("*** GAME COMPLETE ***")
        
def game_player(player_id, player_ip, player_data_port):
    
    #Immediately make the player wait on its cond var
    threadActivatorList[player_id].acquire()
    threadActivatorList[player_id].wait()
    
    #For each player, open up their data socket and give it to the thread
    print("Thread for player " + str(player_id+1) + " has begun execution")
    playerDataSocket = establish_data_connection(player_ip, player_data_port)
    
    if playerDataSocket is None:
        print("Thread for player " + str(player_id+1) + " has unsuccessfully reached client data port :(")
        
    threadActivatorList[numPlayers].notify()
    print("Thread for player " + str(player_id+1) + " has successfully set up data connection!")
    threadActivatorList[player_id].wait()
    
    #Wait until a message is received, then put it on the receive message queue
    while gameFinished != True:
        
        #Making receiving a message from a game player an atomic task
        print("Server waiting on a message from player " + str(player_id+1) + "...")
        playerMessage = playerDataSocket.recv(32)
        messageTuple = (player_id, playerMessage)
        receiveMessageQueue.put(messageTuple)
        print("Message received from player " + str(player_id+1) +  ", placed on queue! TURN COMPLETE\n")
        
        threadActivatorList[numPlayers].notify() #Using n+1 condition variable to reactivate manager
        threadActivatorList[player_id].wait() #Release the lock, wait on assigned condition variable
    
def establish_data_connection(client_ip, data_port): #Call this fcn thru game_manager??

    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((client_ip, data_port))
    
    dataSocket.send("Welcome to your data connection".encode())

    return dataSocket
    
def create_condition_variables(num_players):
    for i in range(num_players + 1):
        #Create condition variables for each player in the game + 1
        threadActivatorList.append(threading.Condition(globalLock))
  
if __name__ == "__main__":
    (client_ips, data_ports) = jp.join_phase()
    numPlayers = len(client_ips)
    create_condition_variables(numPlayers)
    managerThread = threading.Thread(target=game_manager, args=(numPlayers, client_ips, data_ports))
    managerThread.run()


"""
Created on Mon May 11 15:44:34 2020

@author: ryanp
"""

from socket import *
import random
import logging
import threading
import time
import echo_server
import sys


""" What does the thread manager need to do?
    -- Listen on some defined port(s) to add a connection
    --

"""
#define join port globally
joinPort = 60598
dataPorts = []

# Open a connection on the Hanabi port to add players + an associated thread
def join_phase():
    connectedPlayers = 0
    numPlayers = 99 #initialize to number much greater than actual ||players||
    
    while (connectedPlayers != numPlayers):
        #Socket setup
        joinSocket = socket(AF_INET, SOCK_STREAM)
        joinSocket.bind(('', joinPort))
        joinSocket.listen(1)
        
        print("Entered join phase successfully on join port " + str(joinPort))
        
        if numPlayers == 99:
            print("Waiting to determine number of players in game")  
            numPlayers = get_num_players(joinSocket)
        else:
            print("Waiting for " + str(numPlayers - connectedPlayers) + " player(s) to connect")
    
        connectionSocket, addr = joinSocket.accept()
            
        dataPort = get_available_port()
        sendString = "Please connect to your game on port " + str(dataPort)
        connectionSocket.send(sendString.encode())
        connectedPlayers = connectedPlayers + 1
        connectionSocket.close()
    
    print("All players have connected!")

#Return port on which the client can then connect    
def get_available_port():
    portAvailable = 0
    portProspect = 0
    while (portAvailable == 0):
        portProspect = random.randint(1024,65536)
        portLocation = ("127.0.0.1", portProspect)
        testSocket = socket(AF_INET, SOCK_STREAM)
        portAvailable = testSocket.connect_ex(portLocation)
    dataPorts.append(portProspect)
    return portProspect

# Return tuple (numPlayers, firstPlayerSocket)
def get_num_players(joinSocket):
    numSocket, addr = joinSocket.accept()
    
    numPlayers = 0
    while (not (numPlayers > 1 and numPlayers < 6)):
        askString = "Welcome to Hana(N)bi! How many players for your game?"
        numSocket.send(askString.encode())
        numPlayerString = numSocket.recv(4).decode()
        numPlayers = int(numPlayerString)
        
    return numPlayers

if __name__ == "__main__":
    join_phase()
    
    #x = threading.Thread(target=thread_function, args=(1,), daemon=True)


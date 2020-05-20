
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
from send_codes import SendCode


""" What does the thread manager need to do?
    -- Listen on some defined port(s) to add a connection
    --

"""
#define join port globally
joinPort = 60595
dataPorts = []
sendString = ''

# Open a connection on the Hanabi port to add players + an associated thread
def join_phase():
    connectedPlayers = 0
    numPlayers = 99 #initialize to number much greater than actual ||players||
    firstPlayer = True
    
    while (connectedPlayers != numPlayers):
        #Socket setup
        joinSocket = socket(AF_INET, SOCK_STREAM)
        joinSocket.bind(('', joinPort))
        joinSocket.listen(1)
        
        print("Entered join phase successfully on join port " + str(joinPort))
        
        connectionSocket, addr = joinSocket.accept()
        
        if firstPlayer:
            print("Waiting to determine number of players in game")  
            numPlayers = get_num_players(connectionSocket)
            print("There will be " + str(numPlayers) + " players")
            firstPlayer = False
        else:
            connectionSocket.send(str(SendCode.INDICATE_JOINING_GAME.value).encode())
            print("Waiting for " + str(numPlayers - connectedPlayers) + " player(s) to connect")
    
        
        dataPort = get_available_port()
        sendString = str(dataPort)
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

# Return numPlayers
def get_num_players(numSocket):

    numPlayers = 0
    numIterations = 0
    
    numSocket.send(str(SendCode.INDICATE_PLAYER_ONE.value).encode())
    
    while (not (numPlayers > 1 and numPlayers < 6)):
        if numIterations > 0:
            numSocket.send("Please enter valid number between 1 and 5 (inclusive)".encode())
        print("Waiting to receive number of players")
        numPlayerString = numSocket.recv(4).decode()
        numPlayers = int(numPlayerString)
        numIterations = numIterations + 1
        
    return numPlayers

if __name__ == "__main__":
    join_phase()
    
    #x = threading.Thread(target=thread_function, args=(1,), daemon=True)


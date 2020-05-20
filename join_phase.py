
"""
Created on Mon May 11 15:44:34 2020

@author: ryanp
"""

from socket import *
import random
from send_codes import SendCode


""" What does the thread manager need to do?
    -- Listen on some defined port(s) to add a connection
    --

"""
#define join port globally
joinPort = 0
dataPorts = []
sendString = ''

# Open a connection on the Hanabi port to add players + an associated thread
def join_phase():
    connectedPlayers = 0
    numPlayers = 99 #initialize to number much greater than actual ||players||
    firstPlayer = True
    joinPort = get_available_port(False)
    
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
            connectionSocket.send(SendCode.INDICATE_JOINING_GAME.value.encode())
            print("Waiting for " + str(numPlayers - connectedPlayers) + " player(s) to connect")
    
        
        dataPort = get_available_port(True)
        sendString = str(dataPort)
        connectionSocket.send(sendString.encode())
        connectedPlayers = connectedPlayers + 1
        connectionSocket.close()
    
    print("All players have connected!\n")
    
    print("Will create data connections on following ports: ")
    print(dataPorts)
    return dataPorts
    

#Return port on which the client can then connect    
#Input param = do you want to add port to returned port list or not
def get_available_port(addThisPort):
    
    portAvailable = 0
    portProspect = 0
    
    while (portAvailable == 0):
        portProspect = random.randint(1024,65536)
        portLocation = ("127.0.0.1", portProspect)
        testSocket = socket(AF_INET, SOCK_STREAM)
        portAvailable = testSocket.connect_ex(portLocation)
    
    if addThisPort:
        dataPorts.append(portProspect)
        
    return portProspect

# Return numPlayers
def get_num_players(numSocket):

    numPlayers = 0
    numIterations = 0
    
    numSocket.send(SendCode.INDICATE_PLAYER_ONE.value.encode())
    print("Waiting to receive number of players")
    
    while (not (numPlayers > 1 and numPlayers < 6)):
        if numIterations > 0:
            numSocket.send(SendCode.INDICATE_INVALID_PLAYERNUM.value.encode())
            print("Received invalid number of players")
        numPlayerString = numSocket.recv(4).decode()
        numPlayers = int(numPlayerString)
        numIterations = numIterations + 1
        
    numSocket.send(SendCode.INDICATE_VALID_PLAYERNUM.value.encode())
    
    return numPlayers

if __name__ == "__main__":
    join_phase()
    
    #x = threading.Thread(target=thread_function, args=(1,), daemon=True)


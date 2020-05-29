
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
client_ips = []
dataPorts = []
sendString = ''

# Open a connection on the Hanabi port to add players + an associated thread
def join_phase():
    connectedPlayers = 0
    numPlayers = 99 #initialize to number much greater than actual ||players||
    firstPlayer = True
    joinPort = get_available_port(False)
    
    numIterations = 0
    while (connectedPlayers != numPlayers):
        #Socket setup
        joinSocket = socket(AF_INET, SOCK_STREAM)
        joinSocket.bind(('', joinPort))
        joinSocket.listen(1)
        
        if numIterations == 0:
            print("Entered join phase successfully on join port " + str(joinPort))
        else:
            print("Waiting for " + str(numPlayers - connectedPlayers) + " player(s) to obtain data port...")
        
        connectionSocket, addr = joinSocket.accept()
        print("Connection made from address: " + str(addr[0]))
        client_ips.append(str(addr[0]))
        
        if firstPlayer:
            print("Waiting to determine number of players in game...")  
            numPlayers = get_num_players(connectionSocket)
            print("There will be " + str(numPlayers) + " players")
            firstPlayer = False
        else:
            connectionSocket.send(SendCode.INDICATE_JOINING_GAME.value.encode())
        
        ''' Code from when the server sent the data port rather than the client '''
        #dataPort = get_available_port(True)
        #sendString = str(dataPort)
        #connectionSocket.send(sendString.encode())
        
        connectedPlayers = connectedPlayers + 1
        numIterations = numIterations + 1
        
        connectionSocket.send(SendCode.SERVER_REQUEST_DATA_PORT.value.encode())
        print("Waiting for data port from PLAYER " + str(connectedPlayers))
        
        dataPort = int(connectionSocket.recv(8).decode())
        if (dataPort >= 1024 and dataPort < 65536):
            print("\nPLAYER " + str(connectedPlayers) + " HAS SENT DATA PORT \n")
            dataPorts.append(dataPort)
            connectionSocket.send(SendCode.SERVER_RECEIVED_DATA_PORT.value.encode())
            
        closeSignal = connectionSocket.recv(4).decode()
        if closeSignal == SendCode.CLIENT_CLOSE_SOCKET.value:
            connectionSocket.close()
        
    print("All players have been sent a port for data connection!\n")
        
    print("Clients have the following IPs: ")
    print(client_ips)
    
    print("Will create data connections on following ports for those respective clients: ")
    print(dataPorts)
    return (client_ips, dataPorts)
    

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
    print("Waiting to receive number of players from first player...")
    
    while (not (numPlayers > 1 and numPlayers < 6)):
        if numIterations > 0:
            numSocket.send(SendCode.INDICATE_INVALID_PLAYERNUM.value.encode())
            print("Received invalid number of players!")
        numPlayerString = numSocket.recv(4).decode()
        numPlayers = int(numPlayerString)
        numIterations = numIterations + 1
        
    numSocket.send(SendCode.INDICATE_VALID_PLAYERNUM.value.encode())
    
    return numPlayers

if __name__ == "__main__":
    join_phase()
    


# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:33:05 2020

@author: ryanp
"""

# Import socket module
from socket import *
from send_codes import SendCode
import sys  # In order to terminate the program
import random
import time
   

def send_data_port(server_ip, server_port):

    # Create server socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server_ip, server_port))
    print("Successful connection to server made")

    try:
        print("Waiting to receive server code...")
        serverMessage = clientSocket.recv(4).decode()
    
        if serverMessage == SendCode.INDICATE_PLAYER_ONE.value:
            to_server = input('Welcome to Hanabii! How many players for your game?\n')
        
            numIterations = 0
            while (serverMessage != SendCode.INDICATE_VALID_PLAYERNUM.value):
                if numIterations != 0:
                    to_server = input("Sorry, enter a number of players between 2 and 5!\n")
                clientSocket.send(to_server.encode())
                print('Thank you!')
                serverMessage = clientSocket.recv(4).decode()
                numIterations = numIterations + 1
        else:
            print('Welcome to your game of Hanabii!\n')
             
        serverMessage = clientSocket.recv(4).decode()
        while (serverMessage != SendCode.SERVER_REQUEST_DATA_PORT.value):
                serverMessage = clientSocket.recv(4).decode()
                
        serverMessage = ''
        numIterations = 0
        while (serverMessage != SendCode.SERVER_RECEIVED_DATA_PORT.value):
            if (numIterations != 0):
                print("Server failed to receive data port! Retrying...")
            dataPort = get_available_port()
            clientSocket.send(str(dataPort).encode())  
            print("Data port sent to server!")
            serverMessage = clientSocket.recv(4).decode()
                
        clientSocket.send(SendCode.CLIENT_CLOSE_SOCKET.value.encode())
        clientSocket.close()
        return dataPort

    except EOFError:
        clientSocket.close()
          
def open_data_socket(dataPort):
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.bind(('', dataPort))
    dataSocket.listen(1)
    
    serverDataSocket, addr = dataSocket.accept()
    print("Successful data connection created with server")
    
    return serverDataSocket

def play_game(socket):
    
    while True:
        serverMessage = socket.recv(4).decode()
        
        socket.send(SendCode.CLIENT_ACK_MESSAGE.value.encode())
        
        if serverMessage == SendCode.CLIENT_PROMPT_MESSAGE.value:
            sendServer = input('Input your game action: ')
            socket.send(sendServer.encode())
            
        elif serverMessage == SendCode.CLIENT_RECV_MESSAGE.value:
            clientAction = socket.recv(256).decode()
            print(clientAction)


def get_available_port():
    
    portAvailable = 0
    portProspect = 0
    
    while (portAvailable == 0):
        portProspect = random.randint(1024,65536)
        portLocation = ("127.0.0.1", portProspect)
        testSocket = socket(AF_INET, SOCK_STREAM)
        portAvailable = testSocket.connect_ex(portLocation)
            
    return portProspect

if __name__ == '__main__':
    server_ip = input("Enter server IP (default localhost): ")
    
    if server_ip == '':
        server_ip = "127.0.0.1"
        
    if sys.argv[1] == '':
        server_port = input("Enter server port: ")
    else:
        server_port = sys.argv[1]
        
    print("Client will connect to server and tell it its data port\n\n")
    dataPort = send_data_port(server_ip, int(server_port))
    
    print("Client will open socket for its data port and alert when connected to server")
    serverSocket = open_data_socket(dataPort)
    
    print("A socket has been successfully created. Let's play HANABII")
    play_game(serverSocket)

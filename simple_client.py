# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:33:05 2020

@author: ryanp
"""

# Import socket module
from socket import *
from send_codes import SendCode
import sys  # In order to terminate the program


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):

        # Create server socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.server_ip, self.server_port))
        print("Successful connection to server made")

        try:
            print("Waiting to receive server code")
            serverMessage = clientSocket.recv(4).decode()
            
            print(serverMessage)
            if serverMessage == SendCode.INDICATE_PLAYER_ONE.value:
                to_server = input('Welcome to Hana(N)bi! How many players for your game?\n')
                
                numIterations = 0
                while (serverMessage != SendCode.INDICATE_VALID_PLAYERNUM.value):
                    if numIterations != 0:
                        to_server = input("Sorry, enter a number of players between 2 and 5!\n")
                    clientSocket.send(to_server.encode())
                    print('Thank you! Please wait for your data port number')
                    serverMessage = clientSocket.recv(4).decode()
                    numIterations = numIterations + 1
            else:
                print('Welcome to your game of Hana(N)bi! Please wait for your port\n')
                
            dataPort = clientSocket.recv(4).decode()
            print("Going to connect on port " + dataPort)    

        except EOFError:
            clientSocket.close()

if __name__ == '__main__':
    server_ip = input("Enter server IP (default localhost): ")
    
    if server_ip == '':
        server_ip = "127.0.0.1"
        
    if sys.argv[1] == '':
        server_port = input("Enter server port: ")
    else:
        server_port = sys.argv[1]
        
    client = Client(server_ip, int(server_port))
    client.run()
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):

        # Create server socket

        # Add your code here
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.server_ip, self.server_port))

        # Get input with python raw_input() or input()

        # Add your code here
        # Hint:
        # try:
        #     from_client = raw_input("Enter message: \n")
        # ...
        # ...
        try:
            while to_server.lower().strip() != 'bye':
                # send and receive message

                # Add your code here
                clientSocket.send(to_server.encode())
                from_server = clientSocket.recv(512).decode()
                print(from_server)   # show in terminal

                # Get input again

                # Add your code here
                try:
                    to_server = input('Enter message: \n')
                except EOFError:
                    clientSocket.close()  # close the connection
                    break
        except EOFError:
            clientSocket.close()
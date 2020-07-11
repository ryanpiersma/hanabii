# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:17:34 2020

@author: ryanp
"""

import join_phase as jp
import threading
import queue
from socket import *
from send_codes import SendCode
from main import *


threadActivatorList = [] #Populate this w condition variables

sendClientQueue = queue.Queue(0) #TODO: Decide reasonable size for these queues? Will infinite work?? I think...
sendMessageQueue = queue.Queue(0) 
receiveMessageQueue = queue.Queue(0)

globalLock = threading.Lock() #Any thread can release primitive lock. This means manager can release the lock when needed??

playerOrder = []
gamePlayers = []
hanabiGame = None

sendReceiveToggle = False #control whether you want to send or receive a message to one of the clients
#True = send, False = receive

def game_manager(num_players, ip_list, port_list):
    global sendReceiveToggle, gamePlayers, hanabiGame
    
    print("***Game manager beginning operation***\n")
    playerOrder = list(range(numPlayers)) # right now could have hard coded. but will support more advanced functionality later!
    
    for i in range(num_players):
        newPlayerThread = threading.Thread(target=game_player, args=(i, ip_list[i], port_list[i],))
        print("Spawned player thread " + str(i + 1) + "\n")
        newPlayerThread.start()

    print("***Game manager has spawned all player threads***\n")
    
    print("***Game manager will create the game! ***")
    for i in range(num_players):
        gamePlayers.append(Player(str(port_list[i]))) #for prototype just using data port numbers

    hanabiGame = Hanabi(gamePlayers, seed=1) #hard coded as 1 for now
    print("***Game object successfully instantiated***")
    
    print("***Game players will now establish data connections***\n")
    
    threadActivatorList[numPlayers].acquire()
    for i in range(num_players):
        threadActivatorList[i].notify()
        threadActivatorList[numPlayers].wait()
    
    print("***Game players have successfully established data connections***\n")
    
    
    print("***Game will now begin! LETS RUMBLE***\n")
    
    turnCounter = 0
    currentPlayer = 0
    roundCounter = 0
    
    iterations = 0
    while not hanabiGame.isGameOver: 
        broadcastCommand = False
        try:
            if iterations != 0:
                (gamePlayer, gameCommand) = receiveMessageQueue.get()
                broadcastCommand = hanabiGame.update(gameCommand)
            iterations = iterations + 1
            
            if broadcastCommand:
                for i in range(num_players):
                    sendClientQueue.put(i)
                    sendMessageQueue.put(gameCommand)
                    
            elif iterations > 1:
                errorMessage = 'ERROR! Your command was incorrect...'
                sendClientQueue.put(currentPlayer)
                sendMessageQueue.put(errorMessage)
                
            else:
                pass
            
        except queue.Empty:
            print("Receive queue was empty")

        hanabiGame.displayGameState()
        

        # SEND PHASE
        sendReceiveToggle = True
        while not sendClientQueue.empty():
            client = sendClientQueue.get_nowait()
            threadActivatorList[client].notify()
            threadActivatorList[numPlayers].wait()
            
        if hanabiGame.isGameOver: #Game could end after send phase
            break
        
        # RECEIVE PHASE
        sendReceiveToggle = False

        
        if broadcastCommand:
            if currentPlayer == 0:
                roundCounter = roundCounter + 1
                print("^^^BEGIN ROUND " + str(roundCounter) + " ^^^")
            
            currentPlayer = (currentPlayer + 1) % num_players
            turnCounter = turnCounter + 1
        
        threadActivatorList[playerOrder[currentPlayer]].notify()
        threadActivatorList[numPlayers].wait()

    print("*** GAME COMPLETE ***")
    
    print("Terminating game for the clients")
    for i in range(num_players):
        threadActivatorList[i].notify()
        sendMessageQueue.put(SendCode.TERMINATE_GAME.value) 
        
def game_player(player_id, player_ip, player_data_port):
    global sendReceiveToggle, hanabiGame
    
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
    while not hanabiGame.isGameOver:
    
        if sendReceiveToggle:
            
            print("~~~ SEND PHASE, PLAYER " + str(player_id + 1) + " ~~~")
            print("Sending message to player " + str(player_id + 1))
            if not sendMessageQueue.empty():
                playerDataSocket.send(SendCode.CLIENT_RECV_MESSAGE.value.encode())
                response = playerDataSocket.recv(1).decode()
                
                while response != SendCode.CLIENT_ACK_MESSAGE.value:
                    playerDataSocket.send(SendCode.CLIENT_RECV_MESSAGE.encode())
                    response = playerDataSocket.recv(1).decode()
                    
                sendData = sendMessageQueue.get()  
                playerDataSocket.send(sendData.encode())
                    
                ack = playerDataSocket.recv(1).decode()
                while ack != SendCode.CLIENT_ACK_MESSAGE.value:
                    playerDataSocket.send(sendData.encode())
                    ack = playerDataSocket.recv(1).decode() #Using for time sync between client and server
                    
            else:
                playerDataSocket.send(SendCode.DO_NOTHING.value.encode())
            
        else:
            print("~~~ RECEIVE PHASE, PLAYER " + str(player_id + 1) + " ~~~")
            print("Server waiting on a message from player " + str(player_id+1) + "...")
            
            playerDataSocket.send(SendCode.CLIENT_PROMPT_MESSAGE.value.encode())
            response = playerDataSocket.recv(1).decode()
            
            while response != SendCode.CLIENT_ACK_MESSAGE.value:
                playerDataSocket.send(SendCode.CLIENT_PROMPT_MESSAGE.value.encode())
                response = playerDataSocket.recv(1).decode()
                
            playerMessage = playerDataSocket.recv(5).decode()
            while playerMessage[0] == '0':
                playerMessage = playerDataSocket.recv(5).decode()
                
            playerDataSocket.send(SendCode.SERVER_ACK_MESSAGE.value.encode())
                
            messageTuple = (player_id+1, playerMessage)
            receiveMessageQueue.put(messageTuple)
            
            print(messageTuple)
                
            print("Message received from player " + str(player_id+1) +  ", placed on queue! TURN COMPLETE\n")
            
        threadActivatorList[numPlayers].notify() #Using n+1 condition variable to reactivate manager
        threadActivatorList[player_id].wait() #Release the lock, wait on assigned condition variable
        
    playerDataSocket.send(SendCode.TERMINATE_GAME.value.encode())
    threadActivatorList[numPlayers].notify()
    playerDataSocket.close()
    threadActivatorList[player_id].release()
   
def establish_data_connection(client_ip, data_port): #Call this fcn thru game_manager??

    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((client_ip, data_port))
    
    dataSocket.send(SendCode.ACTIVATE_DATA_CONNECTION.value.encode())
    
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

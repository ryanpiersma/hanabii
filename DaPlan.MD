In which the noblest of coders, Sir Tahj M. Starr, Order of the Golden Spider, and Sir Ryan R. Piersma, Order of the Emerald Elephant construct one "Hana(N)bi" labeled sort of game endeavor thing.

So what's the plan you may ask? (but you can't actually read it because it's invisible to idiots)

TOP SECRET PLAN:

5/2/20
- Set up a Visual Studio Liveshare for the first time
- Used ECE356 echo server lab (completed by Ryan lol) in order to establish connection between 2 separate hosts as example
- Tahj had to port said script to work for Python 3 on Windows (was made in Python 2 on Linux)
- 

Tahj:
- Try moving (existing) functions of Tahj's Hanabi code into the echo server and compile list of stuff that needs to be changed

Ryan:
- Enhance networking capabilities of the script to account for multiple players

5/6/20
. Make Hanabi game object (Tahj) [Purpose: Accommodate the server running multiple games, good OOP, encapsulate state of game 
  and separate this logically from server immediately running a game]
	- __init__ function intializes game state
	- current functions in Tahj's Hanabi code become methods of Hanabi game object
	- change printing functions to return a string that can be sent to client

- Multithreading realization
    - In order to accommodate multiple clients, one thread/process per client must be created
    - Then, the server must manage these clients, so we plan to write a thread-managing program in order to control client 
      threads with regard to game flow

Tahj:
    - Make Hanabi game object

Ryan:
    - Work on thread manager for clients to be run from server

5/13/20
- Ryan: Wrote beginning code for "joining phase", where the server handles the number of people playing a particular game
of Hana(N)bi and then gives each player a port to connect to in order to send data that will eventually be affecting game state
- Tahj: Made "Game" object using Python classes

- Ryan's "joining phase" code needs to be debugged, which can more efficiently done when using a specially designed testing
script for a client, rather than "echo_server" unmodified. This must be done before attempting any kind of multithreaded code! (Ryan, duh)
- Add code to each Hanabi game object method to construct a string that will be sent to the client(s). This will update the appropriate clients
on what the method changed in the game state (Tahj)

5/21/20
- Ryan: Completed "join_phase.py" (renamed original "thread_manager.py") and "simple_client.py" --> The two scripts are able to interact in order to establish the number of players in a game as well as distribute and agree on data ports on a per-player basis with no bugs (AFAIK, and I did test lol). 

-Tahj: Made Hanabi object methods return strings to update the client on whats going on; added player naming feature (right now naming players is required to make the Hanabi object); squashed some stupid bugs

TODO:
Think about/work on the interface between the thread manager and Hanabi object

- Ryan: Continue work on "thread_manager.py" and "simple_client.py" so that threads are created for each player and each player can connect on their data port, hopefully with the ability to easily integrate a flexible interface (the one referenced immediately above)

-Tahj: Write a run method (maybe more like an update function) that can just be called in a loop. This method updates the game state based off of some input that it receives and then returns a message that can be sent to the clients.

5/29/20
Notes on integrating Ryan and Tahj's code...
- Ryan will add functionality for players entering their name. Once the join phase (with this addition) is complete, these will be passed to Tahj's code in order to instantiate the Hanabi game object (from an interface???)
- Tahj's update() method in main.py will need to be integrated with the thread manager for various reasons, including
      1) Translating calls in the Hanabi game object to 'notify()' and 'broadcast()' to functions in the thread manager that activate select (or all) threads for data transfer
      2) Creating some sort of simple information transfer protocol for relaying hints, playing, discarding
         (This hopefully wouldn't be much more than packaging the messages that you already generate)
      3) Making sure that individual players are able to receive their individual view of the game

Ryan: Refactored "join_phase.py" and "hanabi_client.py" (renamed from "simple_client.py") in order to accommodate the creation of data connections between the client and the servers, which has been shown to
work correctly!

Tahj: Implemented messaging scheme for updating players about how the state of the game just changed (see update() function) and tested this out using fake Scooby-Doo characters.

TODO

Ryan: - Will look into allowing the game to start with an arbitrary number of players (less than 5), making use of Player 1 being able to trigger a start signal for the game (LEAST PRIORITY, MAYBE WAIT FOR NOW)
      - Allow players to enter their name
      - Create thread manager (i.e. use threads so that the server can send data to specific players) 
        MAIN PRIORITY

Tahj:
- Debug the timing issue of the update function. Currently, the updated state of the game is displayed one turn too late.
- Debug hinting mechanism. Currently, the hints do not stack on top of one another. When a player receives a hint, all previous hints are erased.

Testing note from 5/29: Current server code throws an error when run on Linux (written on Windows) due to a port already being in use during the join phase.

6/5/20
Tahj: Performed debugging tasks that he said he would. Yay?

Ryan: Conceptualized thread manager but did not code one single line of code. At least for this project.

THE THREAD MANAGER:
- Method for controlling thread activation: condition variable

Condition variable: notify() - lock associated with condition variable is released, first thread on queue waiting for this condition variable gets the lock, wait() - put a thread on a queue associated with that condition variable, broadcast() - wake all threads associated with condition variable

- One condition variable per client

- Global list of condition variables. The "thread managing" part is basically notifying the right clients by calling notify() on the right condition variable.

- Globally defined order for thread activation through list of integers.
For Hanabi, something like for a four player game [1, 2, 3, 4]
For a complex game [1, 2, 3, 4, 2, 3, 4] (skip player 1 on every other cycle)

- How do we process the data from the threads? A global queue of messages. In the threaded function, once the message is received from the client, it is pushed onto the global "receive message" queue.

- Two types of threads (i.e. I write two threaded functions). One will be a game_manager(), the rest will be game_player() (or some other similar name). The game_players are associated with the data connections to each of the clients. Their function is to push data on to the global message queue when they are activated and the clients send data. The game_manager I guess is like the interface with the Hanabi game. It is what is activating condition variables based on the order, pulling messages off the global "receive message queue", and pushing messages onto a second "send message" queue. 

Tahj recommends: "Use what comes from the update function!" Will def look into this :)

Use a client ID as the name (keys to the update dictionary)

- Receive one thing from the "receive message" queue at a time. Implement by triggering an Event every time the "receive message" queue is pushed to

- Seems like the thread manager will comprise two threaded functions called in "thread_manager.py". There will be n + 1 threads, where n is the number of players in the Hanabi game. "n" of the threads will be "game_players" that will be using the "game_player()" threaded function. The remaining thread is a "game_manager" that uses the "game_manager()" threaded function. Additionally, the following global data structures will be implemented: a queue for receiving messages, a queue for sending messages, a list describing the order in which game_player threads will be updated, and a list of condition variable objects that correspond to each client.

- In order to handle a universal update to the game state (or something that is essentially universal...?) we will send something to all the clients. We can use an "n+1"th condition variable that all the game_players are associated with. By broadcasting on this condition variable, we can send all threads the correct game state update as a result of the individual player's action.
----------------------------------------------------------------------------------------------------------
Adding a Hand class?

"Hand" --> has "isVisible" state variable
update_hand(position, card) --> replaces card at position "position" with card "card"

"Bob played whatever and drew a white 1" = message to server from Bob --> in Hanabi game bob.update_hand(position, white 1)
-----------------------------------------------------------------------------------------------------------
TODO:

Ryan - Actually code the thread manager! Oh god... Rough specification has been typed above!

Tahj - Refactoring the Game object to account for client/server architecture
  1. Make two Hanabi game objects: a server one and a client one (where the client one is a dumber version of the server one)
  2. Make player & hand objects
  3. Get rid of hintHands
  4. Pass only smaller messages (not the complete game state)

After this has been successfully completed: Collaborate to make message passing successfully go between thread management and the different copies of the game
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Testing note, 6/12: May want to look into handling "ConnectionResetErrors", I envision this will be necessary to handle bad 
network connections in the future. (Ryan)

Testing note, 6/12: Another situation currently not handled super well - A second player is trying to join while the first player
is inputting the number of players. Might go away when restructuring join phase to account for flexible number of players.

Refactoring note, 6/12: Handle that thread manager has a global numPlayers, but it is also separately passed into game_manager(). Will become annoying??

TODO:

Ryan - Complete thread manager (implement flexible way of sending messages to clients) 

Tahj - Finish stuff from last week
  1. Make two Hanabi game objects: a server one and a client one (where the client one is a dumber version of the server one
  2. Pass only smaller messages (not the complete game state)

  ... and fix hinting because it broke now
  
-----------------------------------------------------------------------------------------------------------------------------
Ryan - Finished thread manager, but is buggy (main issue seems to be a correct interpretation of when messages are sent from the client)

Tahj - Implemented Client/Server versions of the Hanabi class

TODO:
Both Ryan and Tahj will try to debug their code as much as possible before having two peer coding sessions next week

Ryan: Fix messaging bug, maybe try generating garbage messages to send to client to verify this functionality,
      Refactor join_phase to allow players to join on a rolling basis, gather player names that will be needed for the Game object

Tahj: Update shuffling so that random seed is passed to hanabi client games. Sending which cards are drawn will now not be necessary anymore.
----------------------------------------------------------------------------------------------------------------------------
6/25/20: PEER CODING SESSION 1

Ryan and Tahj did some debugging and convened very intellectually in order to establish messaging conventions using a series of Enums that will
help to transfer information between the game objects and the networking code. This resulted in "hanabi_constants.py"

Result: Tahj will ensure that these messages become valid game input, Ryan will ensure that user inputs becomes these messages, then we're off to the races...

----------------------------------------------------------------------------------------------------------------------------
6/26/20: PEER CODING SESSION 2

- Ryan wrote code to translate user input into a standardized message format
- Tahj integrated hanabi_constants into the Game object

"gatekeeper.py" was conceived of and written as a utility for the Game object to use (only server?) with functionalities of formatting a message to a format
that the Game object can use and the first iteration of a validation function was written to check if the command works with the current game.

Next steps: Adapt Game object (or other utility??) to make use of the queues for messages provided by the thread_manager (server)
            Include copies of Game object in hanabi_client and thread_manager which will perform above interactions... [HanabiMaster, HanabiClone]
            
Mostly peer coding from now on, but:
    Tahj - Adapt Game to use all enums, fix hinting
    Ryan - Rewrite join phase to accommodate a non-predefined number of players
---------------------------------------------------------------------------------------------------------------------------
6/30/20: PEER CODING SESSION 3 - INTEGRATION W/ SERVER CODE

- Tahj integrated 'hanabi_constants' Enum more into the code, and re-fixed hinting
- Ryan began work on the not-yet-functional flexible join-phase (join_phase_flex())

In 'main.py', 'gatekeeper' was integrated in order to be able to receive commands from the receiving messageQueue of the
thread manager.

In 'thread_manager.py', the Hanabi Game was integrated in order to be able to take received messages and input them as
commands into the Hanabi game, as well as placing these commands back on the send queues in order to broadcast to eventual
client copies of the game.

Unfortunately, testing was inconclusive as to whether any of this actually worked due to bugs in the thread manager sending code.
Ryan's bad, lol

Ryan: Fix bugs such that the integration with the thread manager is successful!
Tahj: Think about ASCII/any other ideas
---------------------------------------------------------------------------------------------------------------------------

TO REMEMBER from debugging:
Hints broken while clients use the name that was never given to the server
Fixed 7/3/20, preliminary server/client integration with game performed, but many bugs uncovered

---------------------------------------------------------------------------------------------------------------------------

7/10/20 - Debugging session, fixed a couple minor bugs and uncovered major bug
7/11/20 - Debugging session 2, Ryan managed to fix major bug beforehand, Tahj and Ryan then were able to successfully
play the game with a few bugs via localhost...

For next week:
Tahj - Bug with hint hands - When removing a card from a hand, also remove from "hint hand"!
Ryan - Add more info to join phase so ugly hard coding can be deleted, try making sure inter-machine join phase works consistently
by making join phase robust




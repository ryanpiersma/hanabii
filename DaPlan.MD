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

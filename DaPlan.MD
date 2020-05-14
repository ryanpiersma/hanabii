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
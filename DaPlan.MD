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
. Make Hanabi game object
	- __init__ function intializes game state
	- current functions in Tahj's Hanabi code become methods of Hanabi game object
	- change printing functions to return a string that can be sent to client
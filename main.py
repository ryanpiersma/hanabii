import random


class Hanabi():

    # Takes in a list of Player objects
    def __init__(self, players):
        
        self.players = players
        self.numPlayers = len(self.players)
        self.currPlayer = -1
        self.currPlayerIndex = -1
        self.messages = {player: [] for player in self.players}

        self.hints = 8
        self.mistakesRem = 3
        self.turnsRem = -1
        self.isGameOver = False

        self.display = {'R': 0, 'G': 0, 'B': 0, 'Y': 0, 'W': 0}
        self.discardPile = []
        self.colors = self.display.keys()

        self.deck = self.makeDeck()
        self.dealHands()

        self.broadcast("Welcome to Hanabi!")
        self.nextPlayer()

    # Deck functions
    def addToDeck(self, deck, card, number):
        for _ in range(number):
            deck.append(card)

    def makeDeck(self):
        deck = []
        for color in self.colors:
            for i in range(1, 6):
                if i == 1:
                    number = 3
                elif i == 5:
                    number = 1
                else:
                    number = 2
                self.addToDeck(deck, color[0] + str(i), number)
        random.shuffle(deck)
        return deck

    def dealHands(self):
        if self.numPlayers == 2 or self.numPlayers == 3:
            handSize = 5
        elif self.numPlayers == 4 or self.numPlayers == 5:
            handSize = 4

        for player in self.players:
            for _ in range(handSize):
                player.hand.append(self.deck.pop())

    

    # Messaging functions
    def notify(self, message, player):
        self.messages[player].append(message)
    
    def broadcast(self, message):
        for player in self.players:
            self.notify(message, player)

    def displayHands(self):
        for player in self.players:
            handStr = "What you see:\n"
            for otherPlayer in self.players:
                handStr += otherPlayer.name + ": "

                for card in otherPlayer.hand:
                    if otherPlayer == player:
                        handStr += "** "
                    else:
                        handStr += card + " "

                handStr += "\n"

            self.notify(handStr, player)

    def displayGameState(self):
        self.broadcast("Here is the current state of the display:\n" + str(self.display))
        self.broadcast("Here is the discard pile:\n" + str(self.discardPile))
        self.broadcast("Hints: " + str(self.hints) + "\tMistakes remaining: " + str(self.mistakesRem))
        self.displayHands()

    def clearMessages(self):
        for messageList in self.messages.values():
            messageList.clear()

    # Game state update functions
    def addHint(self):
        if self.hints < 8:
            self.hints += 1

    def draw(self):
        if self.deck:
            card = self.deck.pop()
            self.currPlayer.hand.append(card) # Replace this with function allowing player to choose where in hand they place the 

            # Last card was drawn and deck is now empty
            if not self.deck:
                self.turnsRem = 5
                self.broadcast("Last card drawn. Everyone gets one last action!")
            

    def play(self, cardPos):
        pick = self.currPlayer.hand.pop(cardPos)
        if int(pick[1]) - 1 == self.display[pick[0]]:
            self.display[pick[0]] = int(pick[1])
            if self.display[pick[0]] == 5:
                self.addHint()
        else:
            self.discardPile.append(pick)
            self.mistakesRem -= 1
        self.draw()

        self.broadcast(self.currPlayer.name + " played " + pick + ".")
        

    def discard(self, cardPos):
        pick = self.currPlayer.hand.pop(cardPos)
        self.discardPile.append(pick)
        self.addHint()
        self.draw()
        
        self.broadcast(self.currPlayer.name + " discarded " + pick + ".")

    def giveHint(self, recipient, hint):
        ### No longer needed w/o hintHands
        # hand = recipient.hand
        # for i in range(len(hand)):
        #     card = ""
        #     for j in range(len(hand[i])):
        #         if hand[i][j] == hint:
        #             card += hand[i][j]
        #         else:
        #             card += hintHand[i][j]
        #     hintHand[i] = card

        self.hints -= 1
        
        self.broadcast(self.currPlayer.name + " gave hint to " + recipient.name + " about " + hint + "'s.")

    def nextPlayer(self):
        self.currPlayerIndex += 1
        if self.currPlayerIndex == self.numPlayers:
            self.currPlayerIndex = 0
        self.currPlayer = self.players[self.currPlayerIndex]
        
        if self.turnsRem > 0:
            self.turnsRem -= 1
        
        self.broadcast("It's " + self.currPlayer.name + "'s turn!")

    def parseCommand(self, command):
        if command:
            action = command[0]
            if action == "P":
                self.play(int(command[1]) - 1)
                self.nextPlayer()
            elif action == "D":
                self.discard(int(command[1]) - 1)
                self.nextPlayer()
            elif action == "H":
                self.giveHint(self.players[int(command[1]) - 1], command[2])
                self.nextPlayer()
            else:
                self.notify("Not a valid choice. Please type H, P, or D.", self.currPlayer)

    '''
    This method takes in a command, updates the state of the Hanabi object, then returns messages to the appropriate players.

    Recognized Commands:
        - P<card_number>
        - D<card_number>
        - H<player><hint>
    '''
    def update(self, command):
        self.clearMessages()
        if not self.isGameOver:
            self.parseCommand(command)
            self.displayGameState()
            self.isGameOver = self.mistakesRem == 0 or self.turnsRem == 0

        if not self.isGameOver:
            self.notify("Pick an action:\n\tH: HINT\n\tP: PLAY\n\tD: DISCARD\n\nAction (H/P/D): ", self.currPlayer)
        else:
            self.broadcast("Game over!\nYou scored " + str(sum(self.display.values())) + " points!")
        
        return self.messages


class Player():

    def __init__(self, name):
        self.name = name
        self.hand = []


# Testing. Testing. 1, 2, 3.

fred = Player("Fred")
daphne = Player("Daphne")
velma = Player("Velma")
shaggy = Player("Shaggy")
scooby = Player("Scooby")

hanabi = Hanabi([fred, daphne, velma, shaggy, scooby])
while not hanabi.isGameOver:
    messages = hanabi.update(input())
    for player in messages:
        for message in messages[player]:
            print(message)

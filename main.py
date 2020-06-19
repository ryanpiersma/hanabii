import random


class Hanabi():


    # Takes in a list of Player objects
    def __init__(self, players, og=True, owner=None):
        
        self.players = players
        self.numPlayers = len(self.players)
        self.currPlayer = None
        self.currPlayerIndex = -1
        self.owner = owner

        self.hints = 8
        self.mistakesRem = 3
        self.turnsRem = -1
        self.isGameOver = False

        self.display = {'R': 0, 'G': 0, 'B': 0, 'Y': 0, 'W': 0}
        self.discardPile = []
        self.colors = self.display.keys()

        self.og = og
        self.commands = {
            'P': lambda args : self.play(int(args[0])),
            'D': lambda args : self.discard(int(args[0])),
            'H': lambda args : self.giveHint(int(args[0]), args[1])
        }
        
        if self.og:
            self.messages = {player: [] for player in self.players}
            self.deck = self.makeDeck()
            self.dealHands()
        else:
            self.commands['+'] = lambda args : self.currPlayer.hand.append(args[0])
            self.commands['>'] = lambda : self.nextPlayer()

        print("Welcome to Hanabi!")
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
        handStr = "What you see:\n"
        for otherPlayer in self.players:
            handStr += otherPlayer.name + ": "

            for card in otherPlayer.hand:
                if otherPlayer == self.owner:
                    handStr += "** "
                else:
                    handStr += card + " "

            handStr += "\n"

        print(handStr)


    def displayGameState(self):
        print("Here is the current state of the display:\n" + str(self.display))
        print("Here is the discard pile:\n" + str(self.discardPile))
        print("Hints: " + str(self.hints) + "\tMistakes remaining: " + str(self.mistakesRem))
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
            self.currPlayer.hand.append(card) # Replace this with function allowing player to choose where in hand they place the card

            # Last card was drawn and deck is now empty
            if not self.deck:
                self.turnsRem = 5
                print("Last card drawn. Everyone gets one last action!")

        return card
            

    def play(self, cardPos):
        pick = self.currPlayer.hand.pop(cardPos - 1)
        if int(pick[1]) - 1 == self.display[pick[0]]:
            self.display[pick[0]] = int(pick[1])
            if self.display[pick[0]] == 5:
                self.addHint()
        else:
            self.discardPile.append(pick)
            self.mistakesRem -= 1
        
        print(self.currPlayer.name + " played " + pick + ".")
        

    def discard(self, cardPos):
        pick = self.currPlayer.hand.pop(cardPos - 1)
        self.discardPile.append(pick)
        self.addHint()
        
        print(self.currPlayer.name + " discarded " + pick + ".")


    def giveHint(self, recipient_id, hint):
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
        
        print(self.currPlayer.name + " gave hint to " + self.players[recipient_id - 1].name + " about " + hint + "'s.")


    def nextPlayer(self):
        self.currPlayerIndex += 1
        if self.currPlayerIndex == self.numPlayers:
            self.currPlayerIndex = 0
        self.currPlayer = self.players[self.currPlayerIndex]
        
        if self.turnsRem > 0:
            self.turnsRem -= 1
        
        print("It's " + self.currPlayer.name + "'s turn!")


    def parseCommand(self, command):
        if command:
            action = command[0]
            if action in self.commands:
                if command[1:]:
                    self.commands[action](command[1:])
                else:
                    self.commands[action]()
                if self.og:
                    self.broadcast(command)
                    if action in ['P', 'D']:
                        self.broadcast(('+', self.draw()))
                    self.nextPlayer()
                    self.broadcast(('>'))
            elif self.og:
                self.notify("Not a valid choice. Please type H, P, or D.", self.currPlayer)


    '''
    This method takes in a command, updates the state of the Hanabi object, then returns messages to the appropriate players.

    Recognized Commands:
        - ('P', <card_num>): play card at index <card_num> in hand
        - ('D', <card_num>): discard card at index <card_num> in hand
        - ('H', <player_id>, <hint>): give hint about <hint>'s to player <player_id>
        - ('+' <card>): draw <card> (for Hanabi clones only)
        - ('>'): move to next player (for Hanabi clones only)
    '''
    def update(self, command):
        if self.og:
            self.clearMessages()

        if not self.isGameOver:
            self.parseCommand(command)
            self.isGameOver = self.mistakesRem == 0 or self.turnsRem == 0
        else:
            print("Game over!\nYou scored " + str(sum(self.display.values())) + " points!")
        
        if self.og:
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

ogGame = Hanabi([fred, daphne, velma, shaggy, scooby])

games = {
    fred: Hanabi([fred, daphne, velma, shaggy, scooby], og=False, owner=fred),
    daphne: Hanabi([fred, daphne, velma, shaggy, scooby], og=False, owner=daphne),
    velma: Hanabi([fred, daphne, velma, shaggy, scooby], og=False, owner=velma),
    shaggy: Hanabi([fred, daphne, velma, shaggy, scooby], og=False, owner=shaggy),
    scooby: Hanabi([fred, daphne, velma, shaggy, scooby], og=False, owner=scooby)
}

while not ogGame.isGameOver:
    messages = ogGame.update([ch for ch in input()])
    for player in messages:
        for message in messages[player]:
            games[player].update(message)
    games[scooby].displayGameState()

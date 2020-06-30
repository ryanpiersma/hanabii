import random
import sys
from hanabi_constants import *

class Hanabi():


    # Takes in a list of Player objects
    def __init__(self, players, og=True, owner=None, seed=None):
        
        self.players = players
        self.numPlayers = len(self.players)
        self.currPlayer = None
        self.currPlayerIndex = -1
        self.owner = owner

        self.hints = 8
        self.mistakesRem = 3
        self.turnsRem = -1
        self.isGameOver = False

        self.display = {color: 0 for color in HanabiColor}
        self.discardPile = []

        if seed:
            self.seed = seed
        else:
            self.seed = random.randrange(sys.maxsize)

        self.deck = self.makeDeck()
        self.dealHands()
        
        self.og = og
        self.commands = {
            HanabiCommand.PLAY_CARD: lambda args : self.play(args[0]),
            HanabiCommand.DISCARD_CARD: lambda args : self.discard(args[0]),
            HanabiCommand.GIVE_HINT: lambda args : self.giveHint(args[0], args[1])
        }
        
        if self.og:
            self.messages = {player: [] for player in self.players}

        print("Welcome to Hanabi!")
        self.nextPlayer()


    # Deck functions
    def addToDeck(self, deck, card, copies):
        for _ in range(copies):
            deck.append(card)


    def makeDeck(self):
        deck = []
        for color in HanabiColor:
            for num in HanabiNumber:
                if num == HanabiNumber.ONE:
                    copies = 3
                elif num == HanabiNumber.FIVE:
                    copies = 1
                else:
                    copies = 2
                self.addToDeck(deck, (color, num), copies)
        random.seed(self.seed)
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


    # Display functions
    def displayCard(self, card):
        return card[0].value + card[1].value


    def displayHands(self):
        handStr = "What you see:\n"
        for otherPlayer in self.players:
            handStr += otherPlayer.name + ": "

            for card in otherPlayer.hand:
                if otherPlayer == self.owner:
                    handStr += "** "
                else:
                    handStr += self.displayCard(card) + " "

            handStr += "\n"

        print(handStr)


    def displayGameState(self):
        print("Here is the current state of the display:\n" + str({color.value: self.display[color] for color in self.display}))
        print("Here is the discard pile:\n" +str([self.displayCard(discarded) for discarded in self.discardPile]))
        print("Hints: " + str(self.hints) + "\tMistakes remaining: " + str(self.mistakesRem))
        self.displayHands()

    
    # Messaging functions
    def notify(self, message, player):
        self.messages[player].append(message)
    

    def broadcast(self, message):
        for player in self.players:
            self.notify(message, player)


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
        pick = self.currPlayer.hand.pop(int(cardPos.value) - 1)
        if int(pick[1].value) - 1 == self.display[pick[0]]:
            self.display[pick[0]] = int(pick[1])
            if self.display[pick[0]] == 5:
                self.addHint()
        else:
            self.discardPile.append(pick)
            self.mistakesRem -= 1
        self.draw()
        
        print(self.currPlayer.name + " played " + self.displayCard(pick) + ".")
        

    def discard(self, cardPos):
        pick = self.currPlayer.hand.pop(int(cardPos.value) - 1)
        self.discardPile.append(pick)
        self.addHint()
        self.draw()
        
        print(self.currPlayer.name + " discarded " + self.displayCard(pick) + ".")


    def giveHint(self, hint, recipient_id):
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
        
        print(self.currPlayer.name + " gave hint to " + self.players[recipient_id - 1].name + " about " + hint.value + "'s.")


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
                self.nextPlayer()
            elif self.og:
                self.notify("Not a valid choice. Please type H, P, or D.", self.currPlayer)


    '''
    This method takes in a command, updates the state of the Hanabi object, then returns messages to the appropriate players.

    Recognized Commands:
        - (HanabiCommand.PLAY_CARD, <card_num>): play card at index <card_num> in hand
        - (HanabiCommand.DISCARD_CARD, <card_num>): discard card at index <card_num> in hand
        - (HanabiCommand.GIVE_HINT, <hint>, <player_id>): give hint about <hint>'s to player <player_id>
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
games = {owner: Hanabi([Player(player.name) for player in ogGame.players], og=False, owner=owner, seed=ogGame.seed) for owner in ogGame.players}

# print(ogGame.deck)
# print()
# for game in games.values():
#     print(game.deck)

testCommands = [
    (HanabiCommand.PLAY_CARD, HanabiPosition.ONE), 
    (HanabiCommand.DISCARD_CARD, HanabiPosition.TWO), 
    (HanabiCommand.GIVE_HINT, HanabiColor.BLUE, 1),
    (HanabiCommand.GIVE_HINT, HanabiNumber.THREE, 2)
]

# while not ogGame.isGameOver:
ogGame.displayGameState()
for tc in testCommands:
    messages = ogGame.update(tc)
    for player in messages:
        for message in messages[player]:
            games[player].update(message)
        games[player].displayGameState()
    

import random
from hanabi_constants import *
from gatekeeper import *
import sys

class Card():

    def __init__(self, color, number):
        self.color = color
        self.number = number
        self.colorHinted = False
        self.numberHinted = False

class Player():

    def __init__(self, name):
        self.name = name
        self.hand = []


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

        if not seed:
            self.seed = random.randint(0, sys.maxsize)
        else:
            self.seed = seed
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

        self.history = []

        self.nextPlayer()


    # Deck functions
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
                    
                for _ in range(copies):
                    deck.append(Card(color, num))
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
                self.turnsRem = self.numPlayers

            return card
            

    def play(self, cardPos):
        pick = self.currPlayer.hand.pop(int(cardPos.value) - 1)
        if int(pick.number.value) - 1 == self.display[pick.color]:
            self.display[pick.color] = int(pick.number.value)
            if self.display[pick.color] == 5:
                self.addHint()
        else:
            self.discardPile.append(pick)
            self.mistakesRem -= 1
        self.draw()
        self.history.append((self.currPlayer, HanabiCommand.PLAY_CARD, pick))
        

    def discard(self, cardPos):
        pick = self.currPlayer.hand.pop(int(cardPos.value) - 1)
        self.discardPile.append(pick)
        self.addHint()
        self.draw()
        self.history.append((self.currPlayer, HanabiCommand.DISCARD_CARD, pick))


    def giveHint(self, hint, recipient_id):
        ### No longer needed w/o hintHands
        recipient = self.players[recipient_id - 1]
        for card in recipient.hand:
            if card.color == hint:
                card.colorHinted = True
            if card.number == hint:
                card.numberHinted = True
        self.hints -= 1
        self.history.append((self.currPlayer, HanabiCommand.GIVE_HINT, recipient, hint))


    def nextPlayer(self):
        self.currPlayerIndex += 1
        if self.currPlayerIndex == self.numPlayers:
            self.currPlayerIndex = 0
        self.currPlayer = self.players[self.currPlayerIndex]
        
        if self.turnsRem > 0:
            self.turnsRem -= 1


    def parseCommand(self, command):
        if validate_command(self, command):
            action = command[0]
            if action in self.commands:
                if command[1:]:
                    self.commands[action](command[1:])
                else:
                    self.commands[action]()
                # if self.og:
                #     self.broadcast(command)
                self.nextPlayer()
            return True
        return False


    '''
    This method takes in a command, updates the state of the Hanabi object, then returns messages to the appropriate players.

    Recognized Commands:
        - (HanabiCommand.PLAY_CARD, <card_num>): play card at index <card_num> in hand
        - (HanabiCommand.DISCARD_CARD, <card_num>): discard card at index <card_num> in hand
        - (HanabiCommand.GIVE_HINT, <hint>, <player_id>): give hint about <hint>'s to player <player_id>
    '''
    def update(self, command):
        formattedCommand = format_message(command)
        # if self.og:
        #     self.clearMessages()

        is_valid = False
        
        if not self.isGameOver:
            is_valid = self.parseCommand(formattedCommand)
            self.isGameOver = self.mistakesRem == 0 or self.turnsRem == 0
        return is_valid
        
        # if self.og:
        #     return self.messages




# Testing. Testing. 1, 2, 3.

# fred = Player("Fred")
# daphne = Player("Daphne")
# velma = Player("Velma")
# shaggy = Player("Shaggy")
# scooby = Player("Scooby")

# ogGame = Hanabi([fred, daphne, velma, shaggy, scooby])
# games = {owner: Hanabi([Player(player.name) for player in ogGame.players], og=False, owner=owner, seed=ogGame.seed) for owner in ogGame.players}

# testCommands = ["P$1", "D$2", "H$B$1", "H$3$2"]

# # while not ogGame.isGameOver:
# ogGame.displayGameState()
# for tc in testCommands:
#     ogGame.update(tc)
#     for player in ogGame.players:
#         games[player].update(tc)
#     ogGame.displayGameState()

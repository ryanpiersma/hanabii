import random


class Hanabi():

    def __init__(self, playerNames):
        
        self.playerNames = playerNames
        self.numPlayers = len(playerNames)
        self.currPlayer = 0

        self.hints = 8
        self.mistakesRem = 3
        self.turnsRem = -1

        self.display = {'R': 0, 'G': 0, 'B': 0, 'Y': 0, 'W': 0}
        self.discardPile = []
        self.colors = self.display.keys()

        self.deck = self.makeDeck()
        self.hands, self.hintHands = self.dealHands(self.deck)

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

    def dealHands(self, deck):
        if self.numPlayers == 2 or self.numPlayers == 3:
            handSize = 5
        elif self.numPlayers == 4 or self.numPlayers == 5:
            handSize = 4

        hands, hintHands = [], []
        for _ in range(len(self.numPlayers)): 
            hand = []
            for _ in range(handSize):
                hand.append(deck.pop())
            hands.append(hand)
            hintHands.append(["**"]*handSize)

        return hands, hintHands

    def displayHands(self):
        handStr = ""
        for player in self.playerNames:
            handStr += player + ": "

            for card in self.hands[player]:
                if player == self.currPlayer:
                    handStr += "** "
                else:
                    handStr += card + " "

            handStr += "\t" * 2

            for card in self.hintHands[player]:
                handStr += card + " "
            handStr += "\n"
        return handStr

    def addHint(self):
        if self.hints < 8:
            self.hints += 1

    def draw(self):
        if self.deck:
            card = self.deck.pop()
            self.hands[self.currPlayer].append(card) # Replace this with function allowing player to choose where in hand they place the 
            self.hintHands[self.currPlayer].append("**")

            # Last card was drawn and deck is now empty
            if not self.deck:
                self.turnsRem = 5
                return "Last card drawn. Everyone gets one last action!"
            

    def play(self, cardPos):
        pick = self.hands[self.currPlayer].pop(cardPos)
        self.hintHands[self.currPlayer].pop(cardPos)
        if int(pick[1]) - 1 == self.display[pick[0]]:
            self.display[pick[0]] = int(pick[1])
            if self.display[pick[0]] == 5:
                self.addHint()
        else:
            self.discardPile.append(pick)
            self.mistakesRem -= 1
        self.draw()
        return self.playerNames[self.currPlayer] + " played " + pick + "."
        

    def discard(self, cardPos):
        pick = self.hands[self.currPlayer].pop(cardPos)
        self.discardPile.append(pick)
        self.hintHands[self.currPlayer].pop(cardPos)
        self.addHint()
        self.draw()
        return self.playerNames[self.currPlayer] + " discarded " + pick + "."

    def giveHint(self, recipient, hint):
        hand = self.hands[recipient]
        for i in range(len(hand)):
            card = ""
            for letter in hand[i]:
                if letter == hint:
                    card += letter
                else:
                    card += "*"
            self.hintHands[recipient][i] = card
        self.hints -= 1
        return self.playerNames[self.currPlayer] + " gave hint to " + self.playerNames[recipient] + " about " + hint + "'s."

    def nextPlayer(self):
        self.currPlayer += 1
        if self.currPlayer == self.numPlayers:
            self.currPlayer = 0
        return "It's " + self.playerNames[self.currPlayer] + "'s turn!"

    # This will have to use the thread manager
    # def run(self):
    #     print("Welcome to Hanabi!")

    #     while True:
    #         for player in range(numPlayers):
    #             print("\nHere is the current state of the display:")
    #             print(display)

    #             print("\nHere is the discard pile:")
    #             print(discardPile)

    #             print("\nHints: " + str(hints) + "\tMistakes remaining: " + str(mistakesRem))

    #             print("\nWhat you see:" + "\t" * 2 + "Hints given:")
    #             printHands(player)

    #             while True:
    #                 action = input("\nPlayer " + str(player + 1) + ", pick an action:\nH: HINT\nP: PLAY\nD: DISCARD\n\nAction (H/P/D): ")

    #                 if action == "H":
    #                     if hints > 0:
    #                         recipient = int(input("Who will receive the hint: ")) - 1
    #                         hint = input("Hint: ")
    #                         giveHint(recipient, hint)
    #                         break
    #                     else:
    #                         print("No more hints. Choose a different action.")
    #                 elif action == "P":
    #                     pick = int(input("Pick a card (1-" + str(handSize) + "): ")) - 1
    #                     play(player, pick)
    #                     break
    #                 elif action == "D":
    #                     pick = int(input("Pick a card (1-" + str(handSize) + "): ")) - 1
    #                     discard(player, pick)
    #                     break
    #                 else:
    #                     print("Not a valid choice. Please type H, P, or D.")

    #             if turnsRem > 0:
    #                 turnsRem -= 1
                
    #             if mistakesRem == 0 or turnsRem == 0:
    #                 break
            
    #         if mistakesRem == 0 or turnsRem == 0:
    #             break

    #     print("\nGame over!")
    #     print("You scored " + str(sum(display.values())) + " points!")

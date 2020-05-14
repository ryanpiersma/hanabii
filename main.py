import random


class Hanabi():

    def __init__(self, numPlayers):
        self.numPlayers = numPlayers

        self.hints = 8
        self.mistakesRem = 3
        self.turnsRem = -1

        self.display = {'R': 0, 'G': 0, 'B': 0, 'Y': 0, 'W': 0}
        self.discardPile = []
        self.colors = self.display.keys()

        self.deck = makeDeck()
        self.hands, self.hintHands = dealHands(self.deck)

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
                addToDeck(deck, color[0] + str(i), number)
        random.shuffle(deck)
        return deck

    def dealHands(self, deck):
        for _ in range(self.numPlayers): 
            if self.numPlayers == 2 or self.numPlayers == 3:
                handSize = 5
            elif self.numPlayers == 4 or self.numPlayers == 5:
                handSize = 4

            hand = [] 
            for _ in range(handSize):
                hand.append(deck.pop())
            hands.append(hand)
            hintHands.append(["**"]*handSize)

        return hands, hintHands

    def displayHands(self, currPlayer):
        handStr = ""
        for player in range(self.numPlayers):
            handStr += str(player + 1) + ": "

            for card in self.hands[player]:
                if player == currPlayer:
                    handStr += "** "
                else:
                    handStr += card + " "

            handStr += "\t" * 2

            for card in self.hintHands[player]:
                handStr += card + " "
            handStr += "\n"

    def addHint(self):
        if self.hints < 8:
            self.hints += 1

    def draw(self, playerNum):
        if self.deck:
            card = self.deck.pop()
            self.hands[playerNum].append(card) # Replace this with function allowing player to choose where in hand they place the 
            self.hintHands[playerNum].append("**")

            # Last card was drawn and deck is now empty
            if not self.deck:
                self.turnsRem = 5
                print("Last card drawn. Everyone gets one last action!")
            

    def play(self, playerNum, cardPos):
        pick = self.hands[playerNum].pop(cardPos)
        self.hintHands[playerNum].pop(cardPos)
        if int(pick[1]) - 1 == self.display[pick[0]]:
            self.display[pick[0]] = int(pick[1])
            if self.display[pick[0]] == 5:
                addHint()
        else:
            self.discardPile.append(pick)
            self.mistakesRem -= 1
        draw(playerNum)
        

    def discard(self, playerNum, cardPos):
        self.discardPile.append(self.hands[playerNum].pop(cardPos))
        self.hintHands[playerNum].pop(cardPos)
        addHint()
        draw(playerNum)

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


    # This will have to use the thread manager
    def run(self):
        print("Welcome to Hanabi!")

        while True:
            for player in range(numPlayers):
                print("\nHere is the current state of the display:")
                print(display)

                print("\nHere is the discard pile:")
                print(discardPile)

                print("\nHints: " + str(hints) + "\tMistakes remaining: " + str(mistakesRem))

                print("\nWhat you see:" + "\t" * 2 + "Hints given:")
                printHands(player)

                while True:
                    action = input("\nPlayer " + str(player + 1) + ", pick an action:\nH: HINT\nP: PLAY\nD: DISCARD\n\nAction (H/P/D): ")

                    if action == "H":
                        if hints > 0:
                            recipient = int(input("Who will receive the hint: ")) - 1
                            hint = input("Hint: ")
                            giveHint(recipient, hint)
                            break
                        else:
                            print("No more hints. Choose a different action.")
                    elif action == "P":
                        pick = int(input("Pick a card (1-" + str(handSize) + "): ")) - 1
                        play(player, pick)
                        break
                    elif action == "D":
                        pick = int(input("Pick a card (1-" + str(handSize) + "): ")) - 1
                        discard(player, pick)
                        break
                    else:
                        print("Not a valid choice. Please type H, P, or D.")

                if turnsRem > 0:
                    turnsRem -= 1
                
                if mistakesRem == 0 or turnsRem == 0:
                    break
            
            if mistakesRem == 0 or turnsRem == 0:
                break

        print("\nGame over!")
        print("You scored " + str(sum(display.values())) + " points!")

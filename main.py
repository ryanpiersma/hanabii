import random

colors = ["RED", "GREEN", "BLUE", "YELLOW", "WHITE"]

# class Card():
#     def __init__(self, color, number):
#         self.color = color
#         self.number = number

# Deck functions
def addToDeck(deck, card, number):
    for _ in range(number):
        deck.append(card)

def makeDeck():
    deck = []
    for color in colors:
        for i in range(1, 6):
            if i == 1:
                number = 3
            elif i == 5:
                number = 1
            else:
                number = 2
            addToDeck(deck, color[0] + str(i), number)
    return deck

# def printCard(card):
#     print(str(card.color) + str(card.number))

deck = makeDeck()
random.shuffle(deck)

# For debugging
# for card in deck:
#     printCard(card)

numPlayers = 5

hints = 8
mistakesRem = 3
turnsRem = -1

hands = []
hintHands = []
display = {'R': 0, 'G': 0, 'B': 0, 'Y': 0, 'W': 0}
discardPile = []

# Deal hands
for _ in range(numPlayers): 
    if numPlayers == 2 or numPlayers == 3:
        handSize = 5
    elif numPlayers == 4 or numPlayers == 5:
        handSize = 4

    hand = [] 
    for _ in range(handSize):
        hand.append(deck.pop())
    hands.append(hand)
    hintHands.append(["**"]*handSize)

def printHands(currPlayer):
    for player in range(numPlayers):
        print(str(player + 1) + ": ", end="")

        for card in hands[player]:
            if player == currPlayer:
                print("** ", end="")
            else:
                print(card + " ", end="")

        print("\t" * 2, end="")

        for card in hintHands[player]:
            print(card + " ", end="")
        print()

def addHint():
    global hints
    if hints < 8:
        hints += 1

def draw(playerNum):
    global turnsRem
    if deck:
        card = deck.pop()
        hands[playerNum].append(card) # Replace this with function allowing player to choose where in hand they place the 
        hintHands[playerNum].append("**")

        # Last card was drawn and deck is now empty
        if not deck:
            turnsRem = 5
            print("Last card drawn. Everyone gets one last action!")
        

def play(playerNum, cardPos):
    global mistakesRem
    pick = hands[playerNum].pop(cardPos)
    hintHands[playerNum].pop(cardPos)
    if int(pick[1]) - 1 == display[pick[0]]:
        display[pick[0]] = int(pick[1])
        if display[pick[0]] == 5:
            addHint()
    else:
        discardPile.append(pick)
        mistakesRem -= 1
    draw(playerNum)
    

def discard(playerNum, cardPos):
    global hints
    discardPile.append(hands[playerNum].pop(cardPos))
    hintHands[playerNum].pop(cardPos)
    addHint()
    draw(playerNum)

def giveHint(recipient, hint):
    global hints
    hand = hands[recipient]
    for i in range(len(hand)):
        card = ""
        for letter in hand[i]:
            if letter == hint:
                card += letter
            else:
                card += "*"
        hintHands[recipient][i] = card
    hints -= 1



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

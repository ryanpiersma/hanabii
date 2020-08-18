from display_constants import DEFAULT_CARD_SIZE, DEFAULT_PADDING


def displayASCIICards(cards, size=DEFAULT_CARD_SIZE):
    cardLinesList = []
    for card in cards:
        cardLinesList.append(createCard(card, size))
    return concatenateCards(cardLinesList)

def createCard(card, size):
    cardLines = [" " * (size + 2) for _ in range(size + 1)]
    addUnderscores(cardLines, size)
    addPipes(cardLines)
    addNumber(cardLines, card.number.value)
    addColor(cardLines, card.color.value)
    return cardLines

def concatenateCards(cardLinesList, padding=DEFAULT_PADDING):
    handLines = ["" for _ in cardLinesList[0]]
    for cardLines in cardLinesList:
        for i in range(len(cardLines)):
            handLines[i] += cardLines[i] + " " * padding
    return "\n".join(handLines)

def addUnderscores(cardLines, size):
    cardLines[0][1:-1] = "_" * size
    cardLines[-1][1:-1] = "_" * size

def addPipes(cardLines):
    for line in cardLines[1:]:
        line[0] = "|"
        line[-1] = "|"

def addNumber(cardLines, number):
    cardLines[1][1] = number
    cardLines[-1][-2] = number

def addColor(cardLines, color):
    center = (len(cardLines) - 1) // 2 + 1
    cardLines[center][center] = color
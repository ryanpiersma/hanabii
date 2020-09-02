from display_constants import *
from hanabi_constants import HanabiColor
import colorama

backgroundMap = {
    HanabiColor.RED: BackgroundColor.RED,
    HanabiColor.GREEN: BackgroundColor.GREEN,
    HanabiColor.BLUE: BackgroundColor.BLUE,
    HanabiColor.YELLOW: BackgroundColor.YELLOW,
    HanabiColor.MAGENTA: BackgroundColor.MAGENTA,
    "black": BackgroundColor.BLACK,
    "white": BackgroundColor.DEFAULT,
    "reset": BackgroundColor.RESET
    }

def displayASCIICards(cards, size=DEFAULT_CARD_SIZE, fullDisplay=False):
    cardLinesList = []
    for card in cards:
        if card.number == 0:
            cardLinesList.append(createCard(card, size, fullDisplay, True))
        else:
            cardLinesList.append(createCard(card, size, fullDisplay))
    return concatenateCards(cardLinesList)

def createCard(card, size, fullDisplay, blank=False):
    cardLines = [[] for _ in range(size + 1)]
    for cardLine in cardLines:
        for i in range(size + 2):
            cardLine.append(" ")

    addPipes(cardLines, card, fullDisplay)        
    addUnderscores(cardLines, card, fullDisplay)
    if not blank:
        addNumber(cardLines, card, fullDisplay)
        addTextColor(cardLines, card, fullDisplay)
    
    for cardLine in cardLines:
        cardLine.insert(0, DISPLAY_MAP["card"])
        cardLine.append(colorama.Fore.RESET)
    
    return ["".join(line) + backgroundMap["reset"].value for line in cardLines]

def concatenateCards(cardLinesList, padding=DEFAULT_PADDING):
    
    handLines = ["" for _ in cardLinesList[0]]
    for cardLines in cardLinesList:
        for i in range(len(cardLines)):
            handLines[i] += cardLines[i] + " " * padding
    
    return "\n".join(handLines) 

def addUnderscores(cardLines, card, fullDisplay):
     if card.colorHinted or fullDisplay:
         return
         
     for i in range(1, len(cardLines[0]) - 1):
        cardLines[0][i] =  "_"
        cardLines[-1][i] = "_" 
    

def addPipes(cardLines, card, fullDisplay):
    if (not card.colorHinted) and (not fullDisplay):    
        for line in cardLines[1:]:
            line[0] = "|"
            line[-1] = "|"
    else:
        for line in cardLines[1:]:
            line[0] = backgroundMap[card.color].value + " "
            line[-1] = " " + backgroundMap["reset"].value

def addNumber(cardLines, card, fullDisplay):
    if (not card.numberHinted) and (not fullDisplay) :
        cardLines[1][1] = colorama.Fore.WHITE + "#"
        cardLines[-1][-2] = colorama.Fore.WHITE + "#"
    elif not card.colorHinted:
        cardLines[1][1] = colorama.Fore.WHITE + card.number.value
        cardLines[-1][-2] = colorama.Fore.WHITE + card.number.value
    else:
        cardLines[1][1] = colorama.Fore.BLACK +  card.number.value + colorama.Fore.RESET
        cardLines[-1][-2] = colorama.Fore.BLACK +  card.number.value + colorama.Fore.RESET

def addTextColor(cardLines, card, fullDisplay):
    center = (len(cardLines) - 1) // 2 + 1
    if (not card.colorHinted) and (not fullDisplay) :
        cardLines[center][center] = "X"
    else:
        cardLines[center][center] = colorama.Fore.BLACK + card.color.value  + colorama.Fore.RESET 
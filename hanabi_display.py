# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:33:16 2020

@author: ryanp
"""

import colorama
import os
from display_constants import *
from hanabi_constants import *
from visual_mode import *
import re
from main import Card

class HanabiDisplay():
    def __init__(self, game):
        colorama.init()
        self.hanabiGame = game

    def displayGameState(self, finalDisplay=False):
        print(self.__center(BOX_SIZE, colorama.Style.BRIGHT + DISPLAY_MAP["box"] + " " + "_" * BOX_SIZE + DISPLAY_MAP["background"]), end='')
        gameState = "\nHere is the current state of the display:\n"
        
        # for color in self.hanabiGame.display:
            # gameState += COLOR_MAP[color].value + color.value  + ": " + str(self.hanabiGame.display[color]) + DISPLAY_MAP["background"] + "\t"
        gameState += displayASCIICards(self.displayScoreDisplay())

        gameState += "\n\nHere is the discard pile:\n"
        # for discarded in self.hanabiGame.discardPile:
        #     gameState += self.displayCard(discarded) + "  "
        if self.hanabiGame.discardPile:
            gameState += displayASCIICards(self.hanabiGame.discardPile[-5:], fullDisplay=True)

        gameState += colorama.Style.BRIGHT + DISPLAY_MAP["background"] + "\n"   
        gameState += "\nHints: " + str(self.hanabiGame.hints) + "\tMistakes remaining: " + str(self.hanabiGame.mistakesRem) + "\n\nCards remaining: " + str(len(self.hanabiGame.deck))
        gameState += "\n" + self.displayHands(finalDisplay)
        print(self.__center(BOX_SIZE, self.__enpipesulate(BOX_SIZE, gameState + DISPLAY_MAP["box"] + "_" * BOX_SIZE)), end='')
        print(DISPLAY_MAP["client"])

    def displayScoreDisplay(self):
        cards = []
        for color in self.hanabiGame.display:
            number = self.hanabiGame.display[color]
            if number == 0:
                cards.append(Card(color, number))
            else:
                card = Card(color, list(HanabiNumber)[number-1])
                card.colorHinted = True
                card.numberHinted = True
                cards.append(card)
        return cards
        
    def displayHands(self, finalDisplay=False):
        handStr = "\nWhat you see:\n"
        for player in self.hanabiGame.players:
            handStr += "\n" + DISPLAY_MAP["name"] + player.name.upper() + DISPLAY_MAP["background"] + "\n"
            if player == self.hanabiGame.owner:
                #handStr += self.displayHand(player, CardVisibility.HINTS)
                handStr += displayASCIICards(player.hand, fullDisplay=finalDisplay)
            else:
                #handStr += self.displayHand(player)
                handStr += displayASCIICards(player.hand, fullDisplay=True)
            handStr += "\n"
            if not player == self.hanabiGame.players[-1]:
                handStr += ("-" * int(BOX_SIZE * 0.9))

        return handStr
    
    def displayHand(self, hanabiPlayer, mode=CardVisibility.FULL):
        handStr = ""
        for card in hanabiPlayer.hand:
            handStr += self.displayCard(card, mode) + " "
            
        return handStr
    
    def displayCard(self,card,mode=CardVisibility.FULL):
        if mode == CardVisibility.HIDDEN:
            return DISPLAY_MAP["asterisk"] + "**" + colorama.Fore.RESET
        elif mode == CardVisibility.HINTS:
            cardStr = ""
            if card.colorHinted:
                cardStr += COLOR_MAP[card.color].value
                cardStr += card.color.value
            else:
                cardStr += DISPLAY_MAP["asterisk"] + "*"
    
            if card.numberHinted:
                cardStr += card.number.value
            else:
                cardStr += DISPLAY_MAP["asterisk"] + "*"
            return cardStr + colorama.Fore.RESET
        else:
            return COLOR_MAP[card.color].value + card.color.value + card.number.value + colorama.Fore.RESET

    def displayEvent(self):
        self.displayAction()
        print(DISPLAY_MAP["event"])
        
        if self.hanabiGame.isGameOver:
            print("Game over!\nYou scored " + str(sum(self.hanabiGame.display.values())) + " points!")
        elif not self.hanabiGame.deck:
            print("It's " + self.hanabiGame.currPlayer.name + "'s LAST turn!")
        else:
            print("It's " + self.hanabiGame.currPlayer.name + "'s turn!")

    def displayAction(self):
        if self.hanabiGame.history:
            print(DISPLAY_MAP["action"])
            action = self.hanabiGame.history[-1]
            if action[1] == HanabiCommand.PLAY_CARD:
                print(action[0].name + " played " + self.displayCard(action[2]) + ".")
            elif action[1] == HanabiCommand.DISCARD_CARD:
                print(action[0].name + " discarded " + self.displayCard(action[2]) + ".")
            elif action[1] == HanabiCommand.GIVE_HINT:
                print(action[0].name + " gave hint to " + action[2].name + " about " + action[3].value + "'s.")

    def __enpipesulate(self, boxLength, string):
        stringPieces = string.split("\n")
        redPipe = colorama.Fore.RED + "|" + DISPLAY_MAP["background"]
        finalString = ""
        for lineString in stringPieces:
            string = lineString.replace("\t", "    ")
            remainderSpace = boxLength - (len(string) - self.__coloramaLengthCount(string))
            if remainderSpace <= 0:
                finalString = finalString + redPipe + string + redPipe
            else:
                halfSpace = " " * (remainderSpace//2)
                if remainderSpace % 2 == 0:
                    finalString = finalString + redPipe + halfSpace + string + halfSpace + redPipe
                else:
                    oddSpace = halfSpace + " "
                    finalString = finalString +  redPipe + halfSpace + string + oddSpace + redPipe
            finalString = finalString + "\n"
        return finalString
    
    def __center(self, boxLength, string):
        try:
            currTerminalDimensions = os.get_terminal_size()
        except OSError:
            return string
        
        terminalLength = currTerminalDimensions[0]
        
        stringPieces = string.split("\n")
        finalString = ""
        for string in stringPieces:
            remainderSpace = terminalLength - boxLength - 2
            if remainderSpace <= 0:
                pass
            else:
                halfSpace = " " * (remainderSpace//2)
                if remainderSpace % 2 == 0:
                    finalString = finalString + halfSpace + string + halfSpace 
                else:
                    oddSpace = halfSpace + " "
                    finalString = finalString +  halfSpace + string + oddSpace
        finalString += "\n"
        return finalString
    
    def __coloramaLengthCount(self, string):
        coloramas = "".join(re.findall(r'\x1b\[[0-9]{1,2}m', string))
        return len(coloramas)
        
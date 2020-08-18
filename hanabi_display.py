# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:33:16 2020

@author: ryanp
"""

import colorama
import os
from display_constants import *
from hanabi_constants import HanabiColor
from hanabi_constants import HanabiCommand
import visual_mode

class HanabiDisplay():
    def __init__(self, game):
        colorama.init()
        self.hanabiGame = game

        self.colorMap = {
            HanabiColor.RED: CardColor.RED,
            HanabiColor.GREEN: CardColor.GREEN,
            HanabiColor.BLUE: CardColor.BLUE,
            HanabiColor.YELLOW: CardColor.YELLOW,
            HanabiColor.MAGENTA: CardColor.MAGENTA,
            "black": CardColor.BLACK,
            "white": CardColor.DEFAULT,
            "reset": CardColor.RESET
            }
        
        self.displayMap ={
            "background": colorama.Fore.GREEN,
            "asterisk": colorama.Fore.WHITE,
            "name": colorama.Fore.CYAN,
            "client": colorama.Fore.WHITE,
            "event": colorama.Fore.YELLOW,
            "action": colorama.Fore.MAGENTA,
            "box": colorama.Fore.RED
        }

    def displayGameState(self):
        print(self.__center(BOX_SIZE, colorama.Style.BRIGHT + self.displayMap["box"] + " " + "_" * BOX_SIZE + self.displayMap["background"]), end='')
        gameState = "\nHere is the current state of the display:\n"
        
        for color in self.hanabiGame.display:
            gameState += self.colorMap[color].value + color.value  + ": " + str(self.hanabiGame.display[color]) + self.displayMap["background"] + "\t"
            
        gameState += "\n\nHere is the discard pile:\n  "
        # for discarded in self.hanabiGame.discardPile:
        #     gameState += self.displayCard(discarded) + "  "
        if self.hanabiGame.discardPile:
            gameState += visual_mode.displayASCIICards(self.hanabiGame.discardPile)

        gameState += colorama.Style.BRIGHT + self.displayMap["background"] + "\n"   
        gameState += "\nHints: " + str(self.hanabiGame.hints) + "\tMistakes remaining: " + str(self.hanabiGame.mistakesRem)
        gameState += "\n" + self.displayHands()
        print(self.__center(BOX_SIZE, self.__enpipesulate(BOX_SIZE, gameState + self.displayMap["box"] + "_" * BOX_SIZE)), end='')
        print(self.displayMap["client"])
        
        
    
    def displayHands(self):
        handStr = "\nWhat you see:\n"
        for player in self.hanabiGame.players:
            handStr += self.displayMap["name"] + player.name + self.displayMap["background"] + ": "
            if player == self.hanabiGame.owner:
                handStr += self.displayHand(player, CardVisibility.HINTS)
            else:
                handStr += self.displayHand(player)
            handStr += "\n"

        return handStr
    
    def displayHand(self, hanabiPlayer, mode=CardVisibility.FULL):
        handStr = ""
        for card in hanabiPlayer.hand:
            handStr += self.displayCard(card, mode) + " "
        return handStr
    
    def displayCard(self,card,mode=CardVisibility.FULL):
        if mode == CardVisibility.HIDDEN:
            return self.displayMap["asterisk"] + "**" + colorama.Fore.RESET
        elif mode == CardVisibility.HINTS:
            cardStr = ""
            if card.colorHinted:
                cardStr += self.colorMap[card.color].value
                cardStr += card.color.value
            else:
                cardStr += self.displayMap["asterisk"] + "*"
    
            if card.numberHinted:
                cardStr += card.number.value
            else:
                cardStr += self.displayMap["asterisk"] + "*"
            return cardStr + colorama.Fore.RESET
        else:
            return self.colorMap[card.color].value + card.color.value + card.number.value + colorama.Fore.RESET

    def displayEvent(self):
        self.displayAction()
        print(self.displayMap["event"])
        if self.hanabiGame.turnsRem == self.hanabiGame.numPlayers:
            print("Last card drawn. Everyone gets one last action!")
        if self.hanabiGame.isGameOver:
            print("Game over!\nYou scored " + str(sum(self.hanabiGame.display.values())) + " points!")
        else:
            print("It's " + self.hanabiGame.currPlayer.name + "'s turn!")

    def displayAction(self):
        print(self.displayMap["action"])
        action = self.hanabiGame.history[-1]
        if action[1] == HanabiCommand.PLAY_CARD:
            print(action[0].name + " played " + self.displayCard(action[2]) + ".")
        elif action[1] == HanabiCommand.DISCARD_CARD:
            print(action[0].name + " discarded " + self.displayCard(action[2]) + ".")
        elif action[1] == HanabiCommand.GIVE_HINT:
            print(action[0].name + " gave hint to " + action[2].name + " about " + action[3].value + "'s.")

    def __enpipesulate(self, boxLength, string):
        stringPieces = string.split("\n")
        redPipe = colorama.Fore.RED + "|" + self.displayMap["background"]
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
        lengthCounter = 0
        for color in self.colorMap.values():
            lengthCounter = lengthCounter + (string.count(color.value) * len(color.value))
           
        lengthCounter = lengthCounter + (string.count(colorama.Style.BRIGHT) * len(colorama.Style.BRIGHT))
        
        return lengthCounter
        
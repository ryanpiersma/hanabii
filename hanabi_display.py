# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:33:16 2020

@author: ryanp
"""

import colorama
from display_constants import *
from hanabi_constants import HanabiColor
from hanabi_constants import HanabiCommand

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
            "background": colorama.Fore.GREEN,
            "asterisk": colorama.Fore.WHITE,
            "name": colorama.Fore.CYAN,
            "client": colorama.Fore.WHITE,
            "event": colorama.Fore.YELLOW,
            "action": colorama.Fore.MAGENTA,
            "box": colorama.Fore.RED
        }

    def displayGameState(self):
        print(self.colorMap["box"] + "_" * BOX_SIZE)
        print(colorama.Style.BRIGHT + self.colorMap["background"])
        gameState = "\nHere is the current state of the display:\n"
        
        for color in self.hanabiGame.display:
            gameState += self.colorMap[color].value + color.value  + ": " + str(self.hanabiGame.display[color]) + self.colorMap["background"] + "\t"
            
        gameState += "\n\nHere is the discard pile:\n  "
        for discarded in self.hanabiGame.discardPile:
            gameState += self.displayCard(discarded) + "  "

        gameState += colorama.Style.BRIGHT + self.colorMap["background"]   
        gameState += "\nHints: " + str(self.hanabiGame.hints) + "\tMistakes remaining: " + str(self.hanabiGame.mistakesRem)
        gameState += "\n" + self.displayHands()
        print(self.__enpipesulate(BOX_SIZE, gameState))
        print(self.colorMap["box"] + "_" * BOX_SIZE)
        print(self.colorMap["client"])
        
        
    
    def displayHands(self):
        handStr = "What you see:\n"
        for player in self.hanabiGame.players:
            handStr += self.colorMap["name"] + player.name + self.colorMap["background"] + ": "
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
    
    def displayCard(self,card, mode=CardVisibility.FULL):
        if mode == CardVisibility.HIDDEN:
            return self.colorMap["asterisk"] + "**" + colorama.Fore.RESET
        elif mode == CardVisibility.HINTS:
            cardStr = ""
            if card.colorHinted:
                cardStr += self.colorMap[card.color].value
                cardStr += card.color.value
            else:
                cardStr += self.colorMap["asterisk"] + "*"
    
            if card.numberHinted:
                cardStr += card.number.value
            else:
                cardStr += self.colorMap["asterisk"] + "*"
            return cardStr + colorama.Fore.RESET
        else:
            return self.colorMap[card.color].value + card.color.value + card.number.value + colorama.Fore.RESET

    def displayEvent(self):
        self.displayAction()
        print(self.colorMap["event"])
        if self.hanabiGame.turnsRem == self.hanabiGame.numPlayers:
            print("Last card drawn. Everyone gets one last action!")
        if self.hanabiGame.isGameOver:
            print("Game over!\nYou scored " + str(sum(self.hanabiGame.display.values())) + " points!")
        else:
            print("It's " + self.hanabiGame.currPlayer.name + "'s turn!")

    def displayAction(self):
        print(self.colorMap["action"])
        action = self.hanabiGame.history[-1]
        if action[1] == HanabiCommand.PLAY_CARD:
            print(action[0].name + " played " + self.displayCard(action[2]) + ".")
        elif action[1] == HanabiCommand.DISCARD_CARD:
            print(action[0].name + " discarded " + self.displayCard(action[2]) + ".")
        elif action[1] == HanabiCommand.GIVE_HINT:
            print(action[0].name + " gave hint to " + action[2].name + " about " + action[3].value + "'s.")

    def __enpipesulate(self, boxLength, string):
        stringPieces = string.split("\n")
        finalString = ""
        for lineString in stringPieces:
            string = lineString.replace("\t", "    ")
            remainderSpace = boxLength - len(string) 
            if remainderSpace <= 0:
                finalString = finalString + "|" + string + "|"
            else:
                halfSpace = " " * (remainderSpace//2)
                if remainderSpace % 2 == 0:
                    finalString = finalString + "|" + halfSpace + string + halfSpace + "|"
                else:
                    oddSpace = halfSpace + " "
                    finalString = finalString +  "|" + halfSpace + string + oddSpace + "|"
            finalString = finalString + "\n"
        return finalString
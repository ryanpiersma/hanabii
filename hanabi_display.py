# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:33:16 2020

@author: ryanp
"""

import colorama
from display_constants import *
from hanabi_constants import HanabiColor

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
            "name": colorama.Fore.CYAN
        }

    def displayGameState(self):
        print(colorama.Style.BRIGHT + self.colorMap["background"])
        print("\nHere is the current state of the display:")
        for color in self.hanabiGame.display:
            print(self.colorMap[color].value + color.value  + ": " + str(self.hanabiGame.display[color]) + self.colorMap["background"], end="\t")
        print("\n\nHere is the discard pile:\n" +str([self.displayCard(discarded) for discarded in self.hanabiGame.discardPile]))
        print("\nHints: " + str(self.hanabiGame.hints) + "\tMistakes remaining: " + str(self.hanabiGame.mistakesRem))
        print("\n" + self.displayHands())
    
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
            return self.colorMap["asterisk"] + "**" + self.colorMap["background"]
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
            return cardStr + self.colorMap["background"]
        else:
            return self.colorMap[card.color].value + card.color.value + card.number.value + self.colorMap["background"]
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:33:16 2020

@author: ryanp
"""

import colorama
from display_constants import CardVisibility

class HanabiDisplay():
    def __init__(self, game):
        colorama.init()
        self.hanabiGame = game

    def displayGameState(self):
        print(colorama.Fore.GREEN)
        print("\nHere is the current state of the self.display:\n" + str({color.value: self.hanabiGame.display[color] for color in self.hanabiGame.display}))
        print("\nHere is the discard pile:\n" +str([self.displayCard(discarded) for discarded in self.hanabiGame.discardPile]))
        print("\nHints: " + str(self.hanabiGame.hints) + "\tMistakes remaining: " + str(self.hanabiGame.mistakesRem))
        print("\n" + self.displayHands())
        print(colorama.Fore.WHITE)
    
    def displayHands(self):
        handStr = "What you see:\n"
        for player in self.hanabiGame.players:
            handStr += player.name + ": "
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
            return "**"
        elif mode == CardVisibility.HINTS:
            cardStr = ""
            if card.colorHinted:
                cardStr += card.color.value
            else:
                cardStr += "*"
    
            if card.numberHinted:
                cardStr += card.number.value
            else:
                cardStr += "*"
            return cardStr
        else:
            return card.color.value + card.number.value
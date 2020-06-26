# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 14:48:28 2020

@author: ryanp
"""
from hanabi_constants import *

def format_message(inMessage):
    commands = [item.value for item in HanabiCommand]
    
    commandComponents = inMessage.split('$')
    
    if len(commandComponents) != 2 and len(commandComponents) != 3:
        return "ERROR"
    
    prospectiveCommand = commandComponents[0]
    prospectiveObject = commandComponents[1]
    
    commandEnum = ''
    objectEnum = ''
    
    if prospectiveCommand in commands:
        if prospectiveCommand == HanabiCommand.GIVE_HINT.value:
            if len(commandComponents) != 3:
                return "ERROR"
            
            commandEnum = HanabiCommand.GIVE_HINT
            
            for color in HanabiColor:
                if prospectiveObject == color.value:
                    objectEnum = color
                    break
                
            for num in HanabiNumber:
                if prospectiveObject == num.value:
                    objectEnum = num
                    break
                
            return (commandEnum, objectEnum, int(commandComponents[2]))
        
        else:
            if prospectiveCommand == HanabiCommand.DISCARD_CARD.value:
                commandEnum = HanabiCommand.DISCARD_CARD
            else:
                commandEnum = HanabiCommand.PLAY_CARD
            
            for pos in HanabiPosition:
                if prospectiveObject == pos.value:
                    objectEnum = pos
                    break
                
            return (commandEnum, objectEnum)
  
    else:
        return "ERROR"
    
def validate_command(command, game):
    action = command[0]
    if action == HanabiCommand.GIVE_HINT:
        
        # Check if hints remaining
        if game.hints <= 0:
            return False
        
        # Check valid recipient
        if command[2] == game.currPlayerIndex or command[2] < 0 or command[2] >= game.numPlayers:
            return False
        
    return True
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:39:45 2020

@author: ryanp
"""
from enum import Enum
from hanabi_constants import HanabiColor
import colorama

BOX_SIZE = 50
DEFAULT_CARD_SIZE = 5
DEFAULT_PADDING = 2

class CardVisibility(Enum):
    FULL = 0
    HINTS = 1
    HIDDEN = 2

class CardColor(Enum):
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    BLUE = colorama.Fore.CYAN
    YELLOW = colorama.Fore.YELLOW
    MAGENTA = colorama.Fore.MAGENTA
    DEFAULT = colorama.Fore.WHITE
    BLACK = colorama.Fore.BLACK
    RESET = colorama.Fore.RESET
    
class BackgroundColor(Enum):
    RED = colorama.Back.RED
    GREEN = colorama.Back.GREEN
    BLUE = colorama.Back.CYAN
    YELLOW = colorama.Back.YELLOW
    MAGENTA = colorama.Back.MAGENTA
    DEFAULT = colorama.Back.WHITE
    BLACK = colorama.Back.BLACK
    RESET = colorama.Back.RESET
    
COLOR_MAP = {
    HanabiColor.RED: CardColor.RED,
    HanabiColor.GREEN: CardColor.GREEN,
    HanabiColor.BLUE: CardColor.BLUE,
    HanabiColor.YELLOW: CardColor.YELLOW,
    HanabiColor.MAGENTA: CardColor.MAGENTA,
    "black": CardColor.BLACK,
    "white": CardColor.DEFAULT,
    "reset": CardColor.RESET
            }
        
DISPLAY_MAP = {
    "background": colorama.Fore.GREEN,
    "asterisk": colorama.Fore.WHITE,
    "name": colorama.Fore.CYAN,
    "client": colorama.Fore.WHITE,
    "event": colorama.Fore.YELLOW,
    "action": colorama.Fore.MAGENTA,
    "box": colorama.Fore.RED,
    "card": colorama.Fore.WHITE
        }
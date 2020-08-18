# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:39:45 2020

@author: ryanp
"""
from enum import Enum
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
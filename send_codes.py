# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:26:23 2020

@author: ryanp
"""

from enum import Enum
class SendCode(Enum):
    INDICATE_PLAYER_ONE = "1"
    INDICATE_JOINING_GAME = "2"
    INDICATE_INVALID_PLAYERNUM = "3"
    INDICATE_VALID_PLAYERNUM = "4"
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
    SERVER_RECEIVED_DATA_PORT = "5"
    SERVER_REQUEST_DATA_PORT = "6"
    DATA_SOCKET_READY = "7"
    CLIENT_CLOSE_SOCKET = "8"
    CLIENT_RECV_MESSAGE = "9"
    CLIENT_ACK_MESSAGE = "0"
    CLIENT_PROMPT_MESSAGE = "A"
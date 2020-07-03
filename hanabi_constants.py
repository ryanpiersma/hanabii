from enum import Enum

class HanabiCommand(Enum):
    PLAY_CARD = "P"
    DISCARD_CARD = "D"
    GIVE_HINT = "H" 
    
class HanabiColor(Enum):
    RED = "R"
    GREEN = "G"
    BLUE = "B"
    YELLOW = "Y"
    WHITE = "W"

class HanabiNumber(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"

class HanabiPosition(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"

MAX_HINTS = 8

#Let's delimit with dollar signs lol
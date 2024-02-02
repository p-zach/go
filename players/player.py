# player.py
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Base class for a Go player.
# Author: Porter Zach

from enum import IntFlag, auto

class PlayerType(IntFlag):
    HUMAN  = auto()
    AI     = auto() # after submit, prompt for ai source file
    UNK    = auto() # server or client player type is unknown
    LOCAL  = auto()
    SERVER = auto() # after submit, indicate IP to share with opponent
    CLIENT = auto() # after submit, prompt for IP
    
class Player:
    def __init__(self):
        pass
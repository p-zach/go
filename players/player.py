# player.py
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Base class for a Go player.
# Author: Porter Zach

from enum import IntFlag, auto
from abc import ABC, abstractmethod

class PlayerType(IntFlag):
    HUMAN  = auto()
    AI     = auto() # after submit, prompt for ai source file
    UNK    = auto() # server or client player type is unknown
    LOCAL  = auto()
    SERVER = auto() # after submit, indicate IP to share with opponent
    CLIENT = auto() # after submit, prompt for IP
    
class Player(ABC):
    # Gets the move from a player agent.
    # Returns the move (x, y) or a string describing the non-move action.
    # ---
    # Does not provide unfettered access to the Game object to avoid unwanted
    # modifications. Instead, provides an encoding of the game state that may
    # be converted to a Board object and manipulated.
    @abstractmethod
    def get_move(self, board_state: str) -> tuple | str:
        raise NotImplementedError("get_move not implemented in subclass")
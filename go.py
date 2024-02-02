# go.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Program entry point for Go game.
# Author: Porter Zach

import graphics
import game
from player import PlayerType
from dataclasses import dataclass
from popups import *

class Go:
    def __init__(self):
        params = get_game_params()
        
        self.model = game.Game(params.width, params.height)
        self.view = graphics.Graphics(board_width=params.width, board_height=params.height)

@dataclass
class GameParams:
    width: int
    height: int
    player1: PlayerType
    player2: PlayerType

if __name__ == "__main__":
    Go()
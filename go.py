# go.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Program entry point for Go game.
# Author: Porter Zach

import game
import interface.graphics as graphics
from interface.popups import *

class Go:
    def __init__(self):
        params = get_game_params()
        
        self.model = game.Game(self, params.size)
        self.view = graphics.Graphics(self, params.size)

    def try_place(self, x: int, y: int) -> bool:
        return self.model.try_place(x, y)
    def get_turn(self) -> int:
        return self.model.get_turn()
    def get_board(self) -> str:
        return self.model.get_board()

if __name__ == "__main__":
    Go()
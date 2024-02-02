# graphics.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Classes and functions for graphical interfacing in Go game.
# Author: Porter Zach

from graphics_utils import *
from graphics_constants import *
from tkinter import Event

class Graphics(Clickable):
    def __init__(self, board_width=9, board_height=9):
        window_width = (board_width - 1) * GRID_UNIT_SIZE + 2 * GRID_OFFSET_X
        window_height = (board_height - 1) * GRID_UNIT_SIZE + 2 * GRID_OFFSET_Y

        begin_graphics(self, window_width, window_height, BACKGROUND_COLOR, "Go")
        self.board_width = board_width
        self.board_height = board_height

        self.draw_board()

        self.stones = {
            StoneColor.BLACK: dict(),
            StoneColor.WHITE: dict()
        }

        enter_graphics()

    def draw_board(self):
        board_width_pixels = GRID_UNIT_SIZE * (self.board_width - 2) + GRID_BOX_SIZE
        board_height_pixels = GRID_UNIT_SIZE * (self.board_height - 2) + GRID_BOX_SIZE

        # Draw board square
        draw_rectangle(GRID_OFFSET_X, GRID_OFFSET_Y, board_width_pixels, board_height_pixels, color=BOARD_COLOR, outline=LINE_COLOR, outline_thickness=3)

        # Draw grid lines
        for i in range(self.board_width - 2):
            x = GRID_OFFSET_X + GRID_UNIT_SIZE * (i + 1)
            draw_line(x, GRID_OFFSET_Y, x, GRID_OFFSET_Y + board_height_pixels, GRID_LINE_THICKNESS, LINE_COLOR)

        for i in range(self.board_height - 2):
            y = GRID_OFFSET_Y + GRID_UNIT_SIZE * (i + 1)
            draw_line(GRID_OFFSET_X, y, GRID_OFFSET_X + board_width_pixels, y, GRID_LINE_THICKNESS, LINE_COLOR)

        # Draw hint circles
        def draw_hint(x, y):
            draw_circle(GRID_OFFSET_X + x * GRID_UNIT_SIZE, GRID_OFFSET_Y + y * GRID_UNIT_SIZE, HINT_RADIUS, LINE_COLOR)
        if (self.board_width, self.board_height) == (9, 9):
            for x, y in [(2, 2), (2, 6), (6, 2), (4, 4), (6, 6)]:
                draw_hint(x, y)
        if (self.board_width, self.board_height) == (13, 13):
            for x, y in [(3, 3), (3, 9), (9, 3), (6, 6), (9, 9)]:
                draw_hint(x, y)
        if (self.board_width, self.board_height) == (19, 19):
            for x, y in [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]:
                draw_hint(x, y)

    # Add a stone to the board.
    def add_stone(self, x: int, y: int, stone_color: StoneColor):
        pix_x = GRID_OFFSET_X + x * GRID_UNIT_SIZE
        pix_y = GRID_OFFSET_Y + y * GRID_UNIT_SIZE
        id = draw_circle(pix_x, pix_y, STONE_RADIUS, self.color(stone_color))
        self.stones[stone_color][(x, y)] = id
    
    # Remove a stone from the board.
    def remove_stone(self, x: int, y: int, stone_color: StoneColor):
        id = self.stones[stone_color][(x, y)]
        delete(id)

    def color(self, stone_color: StoneColor):
        if stone_color == StoneColor.WHITE: 
            return WHITE_COLOR
        if stone_color == StoneColor.BLACK:
            return BLACK_COLOR
        raise TypeError("Invalid stone color")

    def left_click(self, event: Event):
        self.add_stone(1, 1, StoneColor.BLACK)

    def right_click(self, event: Event):
        self.remove_stone(1, 1, StoneColor.BLACK)
    
    def middle_click(self, event: Event):
        pass
    
    def double_click(self, event: Event):
        pass
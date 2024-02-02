# graphics_constants.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Constants for graphics in Go game.
# Author: Porter Zach

from graphics_utils import format_color

GRID_OFFSET_X = 20
GRID_OFFSET_Y = 20

GRID_BOX_SIZE = 40
GRID_LINE_THICKNESS = 2
GRID_UNIT_SIZE = GRID_BOX_SIZE + GRID_LINE_THICKNESS

STONE_RADIUS = 21
HINT_RADIUS = 5

BACKGROUND_COLOR = format_color(0, 128, 0)
BOARD_COLOR = format_color(148, 94, 28)
LINE_COLOR = format_color(46, 27, 4)
WHITE_COLOR = format_color(255, 255, 255)
BLACK_COLOR = format_color(0, 0, 0)
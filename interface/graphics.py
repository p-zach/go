# graphics.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Classes and functions for graphical interfacing in Go game.
# Author: Porter Zach

from .graphics_utils import *
from .graphics_constants import *
from tkinter import Event
from game import string_to_board

class Graphics(Clickable):
    def __init__(self, controller, board_size: int):
        self.controller = controller
        self.window_width = (board_size - 1) * GRID_UNIT_SIZE + 2 * GRID_OFFSET_X + SIDEBAR_WIDTH
        self.window_height = (board_size - 1) * GRID_UNIT_SIZE + 2 * GRID_OFFSET_Y

        begin_graphics(self, self.window_width, self.window_height, "Go")
        self.board_size = board_size

        self.turn_text = tk.StringVar(value="Black's turn.")

        self.draw_board()
        self.make_buttons()

        self.drawn_stones = []

        self.turn = self.controller.get_turn()

        # Guide outlines on hover
        self.motion_ids = []

        self.frozen = False

    def draw_board(self):
        board_width_pixels = GRID_UNIT_SIZE * (self.board_size - 2) + GRID_BOX_SIZE
        board_height_pixels = GRID_UNIT_SIZE * (self.board_size - 2) + GRID_BOX_SIZE
        
        # Draw background
        draw_rectangle(0, 0, self.window_width, self.window_height, SIDEBAR_COLOR)

        # Draw board background
        draw_rectangle(0, 0, self.window_width - SIDEBAR_WIDTH, self.window_height, BOARD_COLOR, LINE_COLOR, SIDEBAR_BORDER_THICKNESS)

        # Draw board square
        draw_rectangle(GRID_OFFSET_X, GRID_OFFSET_Y, board_width_pixels, board_height_pixels, BOARD_COLOR, LINE_COLOR, BOARD_OUTLINE_THICKNESS)

        # Draw grid lines
        for i in range(self.board_size - 2):
            x = GRID_OFFSET_X + GRID_UNIT_SIZE * (i + 1)
            draw_line(x, GRID_OFFSET_Y, x, GRID_OFFSET_Y + board_height_pixels, GRID_LINE_THICKNESS, LINE_COLOR)

        for i in range(self.board_size - 2):
            y = GRID_OFFSET_Y + GRID_UNIT_SIZE * (i + 1)
            draw_line(GRID_OFFSET_X, y, GRID_OFFSET_X + board_width_pixels, y, GRID_LINE_THICKNESS, LINE_COLOR)

        # Draw hint circles
        def draw_hint(x, y):
            draw_circle(GRID_OFFSET_X + x * GRID_UNIT_SIZE, GRID_OFFSET_Y + y * GRID_UNIT_SIZE, HINT_RADIUS, LINE_COLOR)
        if self.board_size == 9:
            for x, y in [(2, 2), (2, 6), (6, 2), (4, 4), (6, 6)]:
                draw_hint(x, y)
        if self.board_size == 13:
            for x, y in [(3, 3), (3, 9), (9, 3), (6, 6), (9, 9)]:
                draw_hint(x, y)
        if self.board_size == 19:
            for x, y in [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]:
                draw_hint(x, y)

    def make_buttons(self):
        frame = get_frame()

        turn_label = ttk.Label(frame, textvariable=self.turn_text, font=("Arial", 12), background=SIDEBAR_COLOR)
        turn_label.place(x=self.window_width+TURN_LABEL_X, y=TURN_LABEL_Y)

        passb = ttk.Button(frame, text="Pass", command=self.pass_turn)
        passb.place(x=self.window_width+PASS_BUTTON_X, y=PASS_BUTTON_Y)
        resign = ttk.Button(frame, text="Resign", command=self.request_resign)
        resign.place(x=self.window_width+RESIGN_BUTTON_X, y=self.window_height+RESIGN_BUTTON_Y)

        forward = ttk.Button(frame, text=">", command=lambda: self.state_change(1, False))
        forward.place(x=self.window_width+FORWARD_BUTTON_X, y=self.window_height+FORWARD_BUTTON_Y)
        ff = ttk.Button(frame, text=">>", command=lambda: self.state_change(1, True))
        ff.place(x=self.window_width+FF_BUTTON_X, y=self.window_height+FF_BUTTON_Y)
        backward = ttk.Button(frame, text="<", command=lambda: self.state_change(-1, False))
        backward.place(x=self.window_width+BACKWARD_BUTTON_X, y=self.window_height+BACKWARD_BUTTON_Y)
        fb = ttk.Button(frame, text="<<", command=lambda: self.state_change(-1, True))
        fb.place(x=self.window_width+FB_BUTTON_X, y=self.window_height+FB_BUTTON_Y)

    def pass_turn(self):
        self.controller.pass_turn()
        self.redraw_board(self.controller.get_board())

    def request_resign(self):
        # TODO: Ask go.py to present user with "Are you sure you want to resign?"
        destroy_window()

    def state_change(self, delta, skip=False):
        print(delta, skip)

    # Attempt to add a stone to the board.
    def add_stone(self, x: int, y: int):
        if self.controller.try_place(x, y):
            self.redraw_board(self.controller.get_board())
    
    # Redraw the board as the new state
    def redraw_board(self, board_enc: str):
        for stone in self.drawn_stones:
            delete(stone)
        self.drawn_stones.clear()

        size, self.turn, board = string_to_board(board_enc)
        color_text = "Black" if self.turn == 0 else "White"
        color_text += "'s turn."
        if self.controller.just_passed():
            color_text += "\nOpponent passed."
        self.turn_text.set(color_text)

        for x in range(size):
            for y in range(size):
                color = board[x][y]
                if color is not None:
                    pix_x = GRID_OFFSET_X + x * GRID_UNIT_SIZE
                    pix_y = GRID_OFFSET_Y + y * GRID_UNIT_SIZE
                    id = draw_circle(pix_x, pix_y, STONE_RADIUS, STONE_COLORS[color])
                    self.drawn_stones.append(id)

    def left_click(self, event: Event):
        if self.frozen:
            return
        
        # Only consider clicks on the canvas
        if type(event.widget) is tk.Canvas:
            # Get board position of mouse if it is hovering over the canvas
            pos = self.board_position(event.x, event.y)
            if pos is None:
                return
            # Try to add a stone
            self.add_stone(*pos)

    def motion(self, event: Event):
        if self.frozen:
            # Remove previous guide outlines if any exists
            while len(self.motion_ids) > 0:
                delete(self.motion_ids.pop())
            return
        
        # Only consider motion on the canvas
        if type(event.widget) is tk.Canvas:
            # Remove previous guide outlines if any exists
            while len(self.motion_ids) > 0:
                delete(self.motion_ids.pop())
            # Get board position of mouse if it is hovering over the canvas
            pos = self.board_position(event.x, event.y)
            if pos is None:
                return
            # Draw new guide outline
            pix_x = GRID_OFFSET_X + pos[0] * GRID_UNIT_SIZE
            pix_y = GRID_OFFSET_Y + pos[1] * GRID_UNIT_SIZE
            self.motion_ids.append(draw_circle_outline(pix_x, pix_y, STONE_RADIUS, STONE_HOVER_THICKNESS, STONE_COLORS[self.turn]))

    # Transform pixel coordinates into board coordinates
    def board_position(self, pix_x: int, pix_y: int) -> tuple | None:
        for x in range(self.board_size):
            c_x = x * GRID_UNIT_SIZE + GRID_OFFSET_X
            for y in range(self.board_size):
                c_y = y * GRID_UNIT_SIZE + GRID_OFFSET_Y
                if (pix_x - c_x)**2 + (pix_y - c_y)**2 <= STONE_RADIUS**2:
                    return x, y
        return None

    def right_click(self, event: Event):
        pass

    def middle_click(self, event: Event):
        pass
    
    def double_click(self, event: Event):
        pass

    def start(self):
        enter_graphics()

    def freeze(self):
        self.frozen = True
        for child in get_frame().winfo_children():
            child.config(state='disable')

    def destroy(self):
        destroy_window()
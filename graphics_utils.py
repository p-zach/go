# graphics_utils.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Tkinter graphics utilities for event-based graphics.
# Author: Porter Zach

import sys
import tkinter
from abc import ABC, abstractmethod
from enum import Enum

_window = None
_canvas = None
_canvas_w = None
_canvas_h = None
_color = None

# Interface for a clickable display.
class Clickable(ABC):
    @abstractmethod
    def left_click(event: tkinter.Event):
        raise NotImplementedError("left_click not implemented in subclass")
    
    @abstractmethod
    def right_click(event: tkinter.Event):
        raise NotImplementedError("right_click not implemented in subclass")
    
    @abstractmethod
    def middle_click(event: tkinter.Event):
        raise NotImplementedError("middle_click not implemented in subclass")
    
    @abstractmethod
    def double_click(event: tkinter.Event):
        raise NotImplementedError("double_click not implemented in subclass")

class StoneColor(Enum):
    BLACK = 0
    WHITE = 1

def format_color(r, g, b):
    return '#%02x%02x%02x' % (int(r), int(g), int(b))

def begin_graphics(clickable: Clickable, width=640, height=480, color=format_color(0, 0, 0), title=None):
    global _window, _canvas, _canvas_w, _canvas_h, _color

    # Destroy root graphics window if it already exists
    if _window is not None:
        _window.destroy()

    # Create graphics window
    _window = tkinter.Tk()
    _window.protocol('WM_DELETE_WINDOW', destroy_window)
    _window.title(title or 'tkinter')
    _window.resizable(False, False)

    # Create canvas
    _canvas = tkinter.Canvas(_window, width=width, height=height)
    _canvas.pack()
    _canvas_w = width
    _canvas_h = height
    _color = color
    draw_background()
    _canvas.update()

    # Bind mouse events
    _window.bind("<Button-1>", clickable.left_click)
    _window.bind("<Button-2>", clickable.middle_click)
    _window.bind("<Button-3>", clickable.right_click)
    _window.bind("<Double-1>", clickable.double_click)

def enter_graphics():
    # Begin tkinter mainloop. This is the last sequential logical line of code
    # in an event-based program.
    _window.mainloop()

def draw_background():
    _canvas.create_rectangle(0, 0, _canvas_w, _canvas_h, fill=_color, outline=_color)

def draw_rectangle(x: int, y: int, w: int, h: int, color, outline:str="", outline_thickness:int=0) -> int:
    return _canvas.create_rectangle(x, y, x + w, y + h, fill=color, outline=outline, width=outline_thickness)

def draw_line(x0: int, y0: int, x1: int, y1: int, thickness: int, color) -> int:
    return _canvas.create_line(x0, y0, x1, y1, fill=color, width=thickness)

def draw_circle(x: int, y: int, r: int, color) -> int:
    return _canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

def delete(id: int):
    _canvas.delete(id)

def destroy_window(event=None):
    sys.exit(0)
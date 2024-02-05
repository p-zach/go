# graphics_utils.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Tkinter graphics utilities for event-based graphics.
# Author: Porter Zach

import sys
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from enum import IntEnum

_root = None
_frame = None
_canvas = None
_canvas_w = None
_canvas_h = None

# Interface for a clickable display.
class Clickable(ABC):
    @abstractmethod
    def left_click(event: tk.Event):
        raise NotImplementedError("left_click not implemented in subclass")
    
    @abstractmethod
    def right_click(event: tk.Event):
        raise NotImplementedError("right_click not implemented in subclass")
    
    @abstractmethod
    def middle_click(event: tk.Event):
        raise NotImplementedError("middle_click not implemented in subclass")
    
    @abstractmethod
    def double_click(event: tk.Event):
        raise NotImplementedError("double_click not implemented in subclass")
    
    @abstractmethod
    def motion(event: tk.Event):
        raise NotImplementedError("motion not implemented in subclass")

class StoneColor(IntEnum):
    BLACK = 0
    WHITE = 1

def format_color(r, g, b):
    return '#%02x%02x%02x' % (int(r), int(g), int(b))

def begin_graphics(clickable: Clickable, width=640, height=480, title="tk"):
    global _root, _frame, _canvas, _canvas_w, _canvas_h

    # Destroy root graphics window if it already exists
    if _root is not None:
        _root.destroy()

    # Create graphics window
    _root, _frame = create_themed_window(title, width, height)
    _root.protocol('WM_DELETE_WINDOW', destroy_window)
    _root.resizable(False, False)

    # Create canvas
    _canvas = tk.Canvas(_frame, width=width, height=height)
    _canvas.pack()
    _canvas_w = width
    _canvas_h = height
    _canvas.update()

    # Bind mouse events
    _root.bind("<Button-1>", clickable.left_click)
    _root.bind("<Button-2>", clickable.middle_click)
    _root.bind("<Button-3>", clickable.right_click)
    _root.bind("<Double-1>", clickable.double_click)
    _root.bind("<Motion>", clickable.motion)

def enter_graphics():
    # Begin tkinter mainloop. This is the last sequential logical line of code
    # in a purely event-based program.
    _root.mainloop()

def draw_rectangle(x: int, y: int, w: int, h: int, color, outline:str="", outline_thickness:int=0) -> int:
    return _canvas.create_rectangle(x, y, x + w, y + h, fill=color, outline=outline, width=outline_thickness)

def draw_line(x0: int, y0: int, x1: int, y1: int, thickness: int, color) -> int:
    return _canvas.create_line(x0, y0, x1, y1, fill=color, width=thickness)

def draw_circle(x: int, y: int, r: int, color) -> int:
    return _canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

def draw_circle_outline(x: int, y: int, r: int, outline_thickness: int, color) -> int:
    return _canvas.create_oval(x - r, y - r, x + r, y + r, fill="", outline=color, width=outline_thickness)

def delete(id: int):
    _canvas.delete(id)

def get_frame():
    return _frame

def destroy_window(event=None):
    _root.destroy()
    sys.exit(0)

def create_themed_window(title, width=None, height=None):
    root = tk.Tk()
    root.title(title) 
    
    frame = ttk.Frame(root, width=width, height=height)
    frame.pack(fill="both", expand=False)

    root.tk.call("source", "interface/azure.tcl")
    root.tk.call("set_theme", "light")
    root.iconbitmap("icon.ico")

    return root, frame
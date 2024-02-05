# popups.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Tkinter dialogs for Go game.
# Author: Porter Zach

import sys
import tkinter as tk
from tkinter import ttk
from players.player import PlayerType
from game import GameParams
from .graphics_utils import create_themed_window

def get_game_params():
    root, frame = create_themed_window("Go Settings", width=300, height=200)
    root.resizable(False, False)
    
    # Define quit button and close window behavior
    def quit():
        root.destroy()
        sys.exit(0)
   
    # Quit application if window is closed
    root.protocol('WM_DELETE_WINDOW', quit)

    # Define dropdown options
    size_options = {"9x9": 9, 
                    "13x13": 13, 
                    "19x19": 19}
    p1_options = {"Play locally": PlayerType.HUMAN | PlayerType.LOCAL,
                  "Play locally as AI": PlayerType.AI | PlayerType.LOCAL,
                  "Host an online game": PlayerType.HUMAN | PlayerType.SERVER,
                  "Host an online game as AI": PlayerType.AI | PlayerType.SERVER,
                  "Join an online game": PlayerType.HUMAN | PlayerType.CLIENT,
                  "Join an online game as AI": PlayerType.AI | PlayerType.CLIENT}
    p2_options = {"Play locally": PlayerType.HUMAN | PlayerType.LOCAL,
                  "Play locally as AI": PlayerType.AI | PlayerType.LOCAL}

    # Create title and instructions
    ttk.Label(frame, text="Welcome to the game of Go!", font=("Arial", 18)).pack(side="top", pady=5)
    ttk.Label(frame, text="Select your game settings.", font=("Arial", 12)).pack(side="top", pady=5)

    # Create 3 dropdown frames
    options_frame_p1 = ttk.Frame(frame)
    options_frame_p1.pack(fill="y", expand=True, pady=5)
    options_frame_p2 = ttk.Frame(frame)
    options_frame_p2.pack(fill="y", expand=True, pady=5)
    options_frame_size = ttk.Frame(frame)
    options_frame_size.pack(fill="y", expand=True, pady=5)

    # Functions for greying out illogical options
    def update_options(p1_option: str):
        player_type = p1_options[p1_option]
        if player_type & PlayerType.CLIENT:
            disable(options_frame_p2)
            disable(options_frame_size)
        elif player_type & PlayerType.SERVER:
            disable(options_frame_p2)
            enable(options_frame_size)
        else:
            enable(options_frame_p2)
            enable(options_frame_size)
    def disable(f: ttk.Frame):
        for child in f.winfo_children():
            child.configure(state="disable")
    def enable(f: ttk.Frame):
        for child in f.winfo_children():
            child.configure(state="normal")

    # Create player 1 dropdown
    p1_string = tk.StringVar(options_frame_p1)     
    options_list_p1 = list(p1_options.keys())
    ttk.OptionMenu(options_frame_p1, p1_string, options_list_p1[0], *options_list_p1, command=update_options).pack(side="right")
    ttk.Label(options_frame_p1, text="Player 1:  ").pack(side="left")

    # Create player 2 dropdown
    p2_string = tk.StringVar(options_frame_p2)     
    options_list_p2 = list(p2_options.keys())
    ttk.OptionMenu(options_frame_p2, p2_string, options_list_p2[0], *options_list_p2).pack(side="right")
    ttk.Label(options_frame_p2, text="Player 2:  ").pack(side="left")

    # Create size dropdown
    size_string = tk.StringVar(options_frame_size)     
    options_list_size = list(size_options.keys())
    ttk.OptionMenu(options_frame_size, size_string, options_list_size[0], *options_list_size).pack(side="right")
    ttk.Label(options_frame_size, text="Board size:  ").pack(side="left")

    # Create start, quit buttons
    ttk.Button(frame, text="Start game", command=root.destroy).pack(side="right", padx=50, pady=10) 
    ttk.Button(frame, text="Quit", command=quit).pack(side="left", padx=50, pady=10)
    
    # Wait for user choices
    root.mainloop() 

    size = size_options[size_string.get()]
    p1 = p1_options[p1_string.get()]
    p2 = None
    if p1 & PlayerType.LOCAL:
        p2 = p2_options[p2_string.get()]
    elif p1 & PlayerType.SERVER:
        p2 = PlayerType.UNK | PlayerType.CLIENT
    elif p1 & PlayerType.CLIENT:
        p2 = PlayerType.UNK | PlayerType.SERVER

    return GameParams(size, p1, p2)
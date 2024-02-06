# go
Go board game implementation in Python.

## Setup
The program requires no setup or extra packages. Run `python go.py`.

## Scoring
Chinese area-type scoring is used. Per Wikipedia: A player's score is the number of stones that the 
player has on the board, plus the number of empty intersections surrounded by that player's stones. 

Note: Chinese and Japanese rules usually return the same score. 
If the results are different, it almost never changes the game's outcome.

A constant komi (White compensation) value of 6.5 is used.

## To do:
- Add player types so you can plug in AI / play online (currently the player selection feature does nothing)
- Add forward/backward buttons so you can see previous game states
- Add counters in the sidebar to know how many stones each player has captured
- Add marking as dead on game end (contingent on both players' agreement)
# game.py͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# ----------------͏󠄂͏️͏󠄌͏󠄎͏󠄑͏︇͏󠄇
# Game logic for Go game.
# Author: Porter Zach

from enum import IntEnum
from dataclasses import dataclass
from players.player import PlayerType

@dataclass
class GameParams:
    size: int
    player1: PlayerType
    player2: PlayerType

class Stone(IntEnum):
    BLACK = 0
    WHITE = 1

NEIGHBORHOOD = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# TODO: Optimize redundant searches and extract various BFS implementations into single function

class Game:
    def __init__(self, controller, size: int):
        self._controller = controller
        self._size = size

        self._board = [[None for _ in range(size)] for _ in range(size)]
        self._prior_state = deepcopy(self._board)
        self._turn = Stone.BLACK

        self._states = [board_to_string(self._size, self._turn, self._board)]
        self._passed_last = False

        # This implementation chooses to use a constant komi (White compensation)
        # following the argument that as board size decreases, komi should
        # decrease (fewer tiles to gain points from) and also increase (going 
        # first provides a larger lead).
        self._komi = 6.5

    # Gets an encoding of the board state
    def get_board(self) -> str:
        return board_to_string(self._size, self._turn, self._board)

    # Gets the current turn: 0 for Black, 1 for White
    def get_turn(self) -> int:
        return int(self._turn)

    # Whether a stone can be placed at the given coordinates
    def can_place(self, x: int, y: int) -> bool:
        return _can_place(self._board, self._prior_state, x, y, self._turn)

    # Place a stone at the given coordinates if possible 
    # Returns True if successful, False otherwise
    def try_place(self, x: int, y: int) -> bool:
        if self.can_place(x, y,):
            self._place(x, y)
            return True
        return False
    
    # Get the winner of the board and each player's score.
    # Under Chinese rules of area scoring:
    # A player's score is the number of stones that the player has on the
    # board, plus the number of empty intersections surrounded by that player's
    # stones. 
    # Note: Chinese and Japanese rules usually return the same score. 
    # If the results are different, it almost never changes the game's outcome.
    # Returns the player that won (Black (0) or White (1)) and each player's score.
    def score(self) -> (int, int, int):
        scores = [0, self._komi]
        considered = set()

        def consider(pos):
            if pos in considered:
                return
            considered.add(pos)
            color = self._board[pos[0]][pos[1]]
            if color is not None:
                scores[color] += 1
                return
            # Perform BFS to see if the group of empty tiles is 
            # bounded entirely by 1 color
            queue = [pos]
            count = 1
            hopeful_color = None
            failed = False
            while len(queue) != 0:
                p = queue.pop(0)
                for neighbor in _neighbors(self._board, *p):
                    nabe_color = self._board[neighbor[0]][neighbor[1]]
                    if nabe_color is None:
                        if neighbor not in considered:
                            # Found another empty tile. Continue BFS
                            considered.add(neighbor)
                            queue.append(neighbor)
                            count += 1
                    elif hopeful_color is None:
                        # Found the first non-empty tile. Consider it as the hopeful
                        # color surrounding the entire territory.
                        hopeful_color = nabe_color
                    elif nabe_color != hopeful_color:
                        # Found a neighbor different to original hopeful color.
                        # No singly-bounded territory here; ignore tiles of this group.
                        failed = True
            if hopeful_color is not None and not failed:
                scores[hopeful_color] += count

        for x in range(self._size):
            for y in range(self._size):
                consider((x, y))

        return scores.index(max(scores)), *scores
    
    def pass_turn(self):
        if self._passed_last:
            return True
        self._turn = 1 - self._turn
        self._passed_last = True
        return False
    
    def just_passed(self):
        return self._passed_last

    # Place a stone at the given coordinates
    def _place(self, x: int, y: int):
        # Save prior state for ko checking
        self._prior_state = deepcopy(self._board)
        # Place stone, update board
        self._board[x][y] = self._turn
        self._update_board(x, y)
        self._turn = 1 - self._turn
        # Keep track of past board states for later examination
        self._states.append(board_to_string(self._size, self._turn, self._board))
        # Reset pass count for game end checking
        self._passed_last = False

    # Update the board in the neighborhood of the stone placed at x, y.
    def _update_board(self, x: int, y: int):
        color = self._board[x][y]
        # For all 4 neighbors,
        for neighbor in _neighbors(self._board, x, y):
            neighbor_color = self._board[neighbor[0]][neighbor[1]]
            # If the neighbor is a different color,
            if neighbor_color is not None and color != neighbor_color:
                # And its group has no more liberties,
                if not self._has_liberties(*neighbor):
                    # Remove the group.
                    self._remove_group(*neighbor)

    # Returns whether the group containing the stone at x, y has any liberties.
    def _has_liberties(self, x: int, y: int) -> bool:
        return _has_liberties(self._board, x, y)
    
    # Removes the stone at x, y.
    def _remove_stone(self, x: int, y: int):
        self._board[x][y] = None

    # Removes the group containing the stone at x, y and returns the number
    # of stones that were in the group.
    def _remove_group(self, x: int, y: int) -> int:
        group = {(x, y)}
        queue = [(x, y)]

        # Perform BFS to look for neighboring same-color stones to add to group
        while len(queue) != 0:
            stone = queue.pop(0)
            stone_color = self._board[stone[0]][stone[1]]
            for neighbor in _neighbors(self._board, *stone):
                color = self._board[neighbor[0]][neighbor[1]]
                if neighbor not in group and color == stone_color:
                    queue.append(neighbor)
                    group.add(neighbor)

        num_removed = len(group)
        for stone in group:
            self._remove_stone(*stone)
            
        return num_removed

    # Returns whether x, y are within the bounds of the board.
    def _in_bounds(self, x: int, y: int) -> bool:
        return _in_bounds(self._board, x, y)

# Whether a stone can be placed at the given coordinates
def _can_place(board: list, prior_state: list, x: int, y: int, color: int) -> bool:
    # Can't place on top of another stone
    if board[x][y] is not None:
        return False
    
    mutable_board = deepcopy(board)
    mutable_board[x][y] = color
    has_liberties = _has_liberties(mutable_board, x, y)
    # Check if the group being added to still has liberties after placement
    if has_liberties:
        # If it does, can place.
        return True
    # If it doesn't, check if the placement will cause a removal of any 
    # manhattan neighbors
    else:
        for neighbor in _neighbors(board, x, y):
            # Ignore if same color
            if mutable_board[x][y] == mutable_board[neighbor[0]][neighbor[1]]:
                continue
            if not _has_liberties(mutable_board, *neighbor):
                # If it does, and the move doesn't violate ko, can place. 
                mutable_board[neighbor[0]][neighbor[1]] = None
                if eq(mutable_board, prior_state):
                    # Violates ko
                    return False
                return True
    # Otherwise, cannot place.
    return False

# Returns whether x, y are within the bounds of the board.
def _in_bounds(board: list, x: int, y: int) -> bool:
    return x >= 0 and x < len(board) and y >= 0 and y < len(board)

# Returns whether the group containing the stone at x, y has any liberties.
def _has_liberties(board: list, x: int, y: int) -> bool:
    if not _in_bounds(board, x, y):
        return None

    group = set()
    queue = [(x, y)]

    # Perform BFS to look for liberties
    while len(queue) != 0:
        stone = queue.pop(0)
        stone_color = board[stone[0]][stone[1]]
        for neighbor in _neighbors(board, *stone):
            color = board[neighbor[0]][neighbor[1]]
            # Found a liberty
            if color is None:
                return True
            elif neighbor not in group and color == stone_color:
                queue.append(neighbor)
                group.add(neighbor)

    # Found no liberties
    return False

def _neighbors(board: list, x: int, y: int) -> list:
    nabes = []
    for dir in NEIGHBORHOOD:
        new_stone = (x + dir[0], y + dir[1])
        if _in_bounds(board, *new_stone):
            nabes.append(new_stone)
    return nabes

# Returns a deep copy of a board.
def deepcopy(board: list) -> list:
    new_board = [[None for _ in range(len(board))] for _ in range(len(board))]
    for x in range(len(board)):
        for y in range(len(board)):
            new_board[x][y] = board[x][y]
    return new_board

# Returns whether two boards are equivalent.
def eq(board1: list, board2: list) -> bool:
    for x in range(len(board1)):
        for y in range(len(board1)):
            if board1[x][y] != board2[x][y]:
                return False
    return True

# Encodes a board state into a board state encoding
def board_to_string(size: int, to_play: Stone, board: list):
    if size != len(board) or size != len(board[0]):
        raise ValueError("size does not match board shape")
    
    encoding = str(size)
    encoding += "b" if to_play == Stone.BLACK else "w"

    board_enc = 0
    for x in range(size):
        for y in range(size):
            board_enc *= 3
            board_enc += 0 if board[x][y] is None else (1 if board[x][y] == Stone.BLACK else 2)
    encoding += format(board_enc, 'x')

    return encoding

# Decodes a board state encoding into a board state
def string_to_board(encoding: str):
    to_play_index = encoding.find("w")
    if to_play_index == -1:
        to_play_index = encoding.find("b")

    size = int(encoding[:to_play_index])
    to_play = int(Stone.BLACK) if encoding[to_play_index] == "b" else int(Stone.WHITE)

    board = [[None for _ in range(size)] for _ in range(size)]
    board_enc = int(encoding[to_play_index+1:], base=16)

    for x in range(size - 1, -1, -1):
        for y in range(size - 1, -1, -1):
            board[x][y] = None if board_enc % 3 == 0 else (int(Stone.BLACK) if board_enc % 3 == 1 else int(Stone.WHITE))
            board_enc //= 3

    return size, to_play, board